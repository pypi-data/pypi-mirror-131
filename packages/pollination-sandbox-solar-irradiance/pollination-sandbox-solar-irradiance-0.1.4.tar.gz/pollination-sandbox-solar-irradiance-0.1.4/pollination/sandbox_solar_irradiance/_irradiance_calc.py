from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass

from pollination.honeybee_radiance.translate import CreateRadianceFolderGrid
from pollination.honeybee_radiance.octree import CreateOctree, CreateOctreeWithSky

from ._raytracing import IncidentIrradianceRayTracing


@dataclass
class IncidentIrradianceEntryPoint(DAG):
    """Incident irradiance entry point."""

    # inputs
    model_name = Inputs.str(
        description='Model file name. This is useful for naming the final results.'
    )

    sunpath = Inputs.file(
        description='Sun matrix.',
        extensions=['mtx']
    )

    sun_modifiers = Inputs.file(
        description='Sun matrix.',
        extensions=['mod']
    )

    sky_dome = Inputs.file(
        description='Sun matrix.',
        extensions=['dome']
    )

    sky_matrix = Inputs.file(
        description='Sun matrix.',
        extensions=['mtx']
    )

    radiance_parameters = Inputs.str(
        description='Radiance parameters for ray tracing.',
        default='-ad 5000 -lw 2e-05'
    )

    model = Inputs.file(
        description='Path to a HBJSON model to be simulated.'
    )

    @task(template=CreateRadianceFolderGrid)
    def create_rad_folder(self, input_model=model, name=model_name):
        """Translate the input model to a radiance folder."""
        return [
            {
                'from': CreateRadianceFolderGrid()._outputs.model_folder,
                'to': 'model'
            },
            {
                'from': CreateRadianceFolderGrid()._outputs.sensor_grids_file,
                'to': '../../results/states/{{self.name}}/grids_info.json'
            },
            {
                'from': CreateRadianceFolderGrid()._outputs.sensor_grids,
                'description': 'Sensor grids information.'
            }
        ]

    @task(template=CreateOctree, needs=[create_rad_folder])
    def create_octree(self, model=create_rad_folder._outputs.model_folder):
        """Create octree from radiance folder."""
        return [
            {
                'from': CreateOctreeWithSky()._outputs.scene_file,
                'to': 'resources/scene.oct'
            }
        ]

    @task(
        template=CreateOctreeWithSky, needs=[create_rad_folder]
    )
    def create_octree_with_suns(
        self, model=create_rad_folder._outputs.model_folder,
        sky=sunpath
    ):
        """Create octree from radiance folder and sunpath for direct studies."""
        return [
            {
                'from': CreateOctreeWithSky()._outputs.scene_file,
                'to': 'resources/scene_with_suns.oct'
            }
        ]

    @task(
        template=IncidentIrradianceRayTracing,
        needs=[create_octree_with_suns, create_octree, create_rad_folder],
        loop=create_rad_folder._outputs.sensor_grids,
        sub_folder='initial_results/{{item.name}}',  # create a subfolder for each grid
        sub_paths={'sensor_grid': 'grid/{{item.full_id}}.pts'}  # sub_path for sensor_grid arg
    )
    def incident_irradiance_raytracing(
        self,
        radiance_parameters=radiance_parameters,
        octree_file_with_suns=create_octree_with_suns._outputs.scene_file,
        octree_file=create_octree._outputs.scene_file,
        model_name=model_name,
        grid_name='{{item.full_id}}',
        sensor_count='{{item.count}}',
        sensor_grid=create_rad_folder._outputs.model_folder,
        sky_dome=sky_dome,
        sky_matrix_indirect=sky_matrix,
        sunpath=sunpath,
        sun_modifiers=sun_modifiers
    ):
        pass
