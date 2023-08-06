"""Raytracing DAG for incident irradiance."""

from pollination_dsl.dag import Inputs, DAG, task
from dataclasses import dataclass

from pollination.honeybee_radiance.contrib import DaylightContribution
from pollination.honeybee_radiance.coefficient import DaylightCoefficient
from pollination.honeybee_radiance.sky import AddSkyMatrix


@dataclass
class IncidentIrradianceRayTracing(DAG):

    # inputs
    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing',
        default='-ab 1'
    )

    octree_file_with_suns = Inputs.file(
        description='A Radiance octree file with suns.',
        extensions=['oct']
    )

    octree_file = Inputs.file(
        description='A Radiance octree file.',
        extensions=['oct']
    )

    model_name = Inputs.str(
        description='Model file name. This is useful for naming the final results.'
    )

    grid_name = Inputs.str(
        description='Sensor grid file name. This is useful to rename the final result '
        'file to {grid_name}.res'
    )

    sensor_count = Inputs.int(
        description='The maximum number of grid points.',
        spec={'type': 'integer', 'minimum': 1}
    )


    sensor_grid = Inputs.file(
        description='Sensor grid file.',
        extensions=['pts']
    )

    sun_modifiers = Inputs.file(
        description='A file with sun modifiers.'
    )

    sky_matrix_indirect = Inputs.file(
        description='Path to indirect skymtx file (i.e. gendaymtx -s).'
    )

    sky_dome = Inputs.file(
        description='Path to sky dome file.'
    )

    @task(
        template=DaylightContribution
    )
    def direct_sunlight(
        self,
        radiance_parameters=radiance_parameters,
        fixed_radiance_parameters='-aa 0.0 -I -ab 0 -dc 1.0 -dt 0.0 -dj 0.0 -dr 0',
        sensor_count=sensor_count, modifiers=sun_modifiers,
        sensor_grid=sensor_grid,
        conversion='0.265 0.670 0.065',
        output_format='a',  # make it ascii so we can expose the file as a separate output
        scene_file=octree_file_with_suns,
        name=grid_name
    ):
        return [
            {
                'from': DaylightContribution()._outputs.result_file,
                'to': '{{self.name}}_direct.ill'
            }
        ]

    @task(
        template=DaylightCoefficient
    )
    def indirect_sky(
        self,
        radiance_parameters=radiance_parameters,
        fixed_radiance_parameters='-aa 0.0 -I -c 1',
        sensor_count=sensor_count,
        sky_matrix=sky_matrix_indirect, sky_dome=sky_dome,
        sensor_grid=sensor_grid,
        conversion='0.265 0.670 0.065',  # divide by 179
        scene_file=octree_file,
        name=grid_name
    ):
        return [
            {
                'from': DaylightContribution()._outputs.result_file,
                'to': '{{self.name}}_indirect.ill'
            }
        ]

    @task(
        template=AddSkyMatrix,
        needs=[direct_sunlight, indirect_sky]
    )
    def output_matrix_math(
        self,
        indirect_sky_matrix=indirect_sky._outputs.result_file,
        sunlight_matrix=direct_sunlight._outputs.result_file,
        model_name=model_name, name=grid_name
    ):
        return [
            {
                'from': AddSkyMatrix()._outputs.results_file,
                'to': '../../../../results/states/{{self.model_name}}/{{self.name}}.ill'
            }
        ]
