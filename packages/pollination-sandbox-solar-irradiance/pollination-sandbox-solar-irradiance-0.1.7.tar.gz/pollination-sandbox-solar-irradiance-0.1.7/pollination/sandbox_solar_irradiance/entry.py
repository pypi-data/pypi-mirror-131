from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from pollination.honeybee_radiance.sun import CreateSunMatrix, ParseSunUpHours
from pollination.honeybee_radiance.sky import CreateSkyDome, CreateSkyMatrix
from pollination.honeybee_radiance.post_process import AnnualIrradianceMetrics, \
    SolarTrackingSynthesis
from pollination.path.read import ReadJSONList

# input/output alias
from pollination.alias.inputs.model import hbjson_model_input
from pollination.alias.inputs.wea import wea_input
from pollination.alias.inputs.north import north_input
from pollination.alias.inputs.radiancepar import rad_par_annual_input
from pollination.alias.outputs.daylight import average_irradiance_results, \
    cumulative_radiation_results

from ._irradiance_calc import IncidentIrradianceEntryPoint


@dataclass
class SandboxSolarIrradianceEntryPoint(DAG):
    """Sandbox Solar irradiance entry point."""

    # inputs
    tracking_increment = Inputs.int(
        description='An integer for the increment angle of each state in degrees.',
        default=5, spec={'type': 'integer', 'maximum': 90, 'minimum': 1}
    )

    north = Inputs.float(
        default=0,
        description='A number for rotation from north.',
        spec={'type': 'number', 'minimum': -360, 'maximum': 360},
        alias=north_input
    )

    radiance_parameters = Inputs.str(
        description='Radiance parameters for ray tracing.',
        default='-ad 5000 -lw 2e-05',
        alias=rad_par_annual_input
    )

    models = Inputs.file(
        description='A JSON array of the names for the HBJSON models to be simulated.'
    )

    model_folder = Inputs.folder(
        description='A folder containing the HBJSON models to be simulated.'
    )

    wea = Inputs.file(
        description='Wea file.',
        extensions=['wea'],
        alias=wea_input
    )

    @task(template=CreateSunMatrix)
    def generate_sunpath(self, north=north, wea=wea, output_type=1):
        """Create sunpath for sun-up-hours."""
        return [
            {'from': CreateSunMatrix()._outputs.sunpath, 'to': 'resources/sunpath.mtx'},
            {
                'from': CreateSunMatrix()._outputs.sun_modifiers,
                'to': 'resources/suns.mod'
            }
        ]

    @task(template=CreateSkyDome)
    def create_sky_dome(self):
        """Create sky dome for daylight coefficient studies."""
        return [
            {'from': CreateSkyDome()._outputs.sky_dome, 'to': 'resources/sky.dome'}
        ]

    @task(template=CreateSkyMatrix)
    def create_indirect_sky(
        self, north=north, wea=wea, sky_type='no-sun', output_type='solar',
        output_format='ASCII', sun_up_hours='sun-up-hours'
    ):
        return [
            {
                'from': CreateSkyMatrix()._outputs.sky_matrix,
                'to': 'resources/sky_direct.mtx'
            }
        ]

    @task(template=ParseSunUpHours, needs=[generate_sunpath])
    def parse_sun_up_hours(self, sun_modifiers=generate_sunpath._outputs.sun_modifiers):
        return [
            {
                'from': ParseSunUpHours()._outputs.sun_up_hours,
                'to': 'results/sun-up-hours.txt'
            }
        ]

    @task(template=ReadJSONList)
    def read_model_list(self, src=models):
        return [
            {
                'from': ReadJSONList()._outputs.data,
                'description': 'List of model information.'
            }
        ]

    @task(
        template=IncidentIrradianceEntryPoint,
        needs=[
            create_sky_dome, generate_sunpath, create_indirect_sky, read_model_list
        ],
        loop=read_model_list._outputs.data,
        sub_folder='initial_results/{{item.name}}',  # create a subfolder for each grid
        sub_paths={'model': '{{item.name}}.hbjson'}  # sub_path for sensor_grid arg
    )
    def incident_irradiance_calc(
        self,
        model=model_folder,
        radiance_parameters=radiance_parameters,
        sunpath=generate_sunpath._outputs.sunpath,
        sun_modifiers=generate_sunpath._outputs.sun_modifiers,
        sky_dome=create_sky_dome._outputs.sky_dome,
        sky_matrix=create_indirect_sky._outputs.sky_matrix,
        model_name='{{item.name}}'
    ):
        pass

    @task(
        template=SolarTrackingSynthesis,
        needs=[parse_sun_up_hours, incident_irradiance_calc]
    )
    def synthesize_solar_tracking(
        self, folder='results/states',
        sun_up_hours=parse_sun_up_hours._outputs.sun_up_hours,
        wea=wea, north=north, tracking_increment=tracking_increment
    ):
        return [
            {
                'from': SolarTrackingSynthesis()._outputs.results,
                'to': 'results'
            }
        ]

    @task(
        template=AnnualIrradianceMetrics,
        needs=[synthesize_solar_tracking]
    )
    def calculate_metrics(
        self, folder='results', wea=wea
    ):
        return [
            {
                'from': AnnualIrradianceMetrics()._outputs.metrics,
                'to': 'metrics'
            },
            {
                'from': AnnualIrradianceMetrics()._outputs.timestep_file,
                'to': 'results/timestep.txt'
            }
        ]

    results = Outputs.folder(
        source='results', description='Folder with raw result files (.ill) that '
        'contain matrices of total irradiance.'
    )

    average_irradiance = Outputs.folder(
        source='metrics/average_irradiance', description='The average irradiance in '
        'W/m2 for each sensor over the Wea time period.',
        alias=average_irradiance_results
    )

    cumulative_radiation = Outputs.folder(
        source='metrics/cumulative_radiation', description='The cumulative radiation '
        'in kWh/m2 over the Wea time period.', alias=cumulative_radiation_results
    )
