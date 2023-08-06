"""
This file is auto-generated from a Queenbee recipe. It is unlikely that
you should be editing this file directly. Instead try to edit the recipe
itself and regenerate the code.

Contact the recipe maintainers with additional questions.
    mostapha: mostapha@ladybug.tools
    ladybug-tools: info@ladybug.tools

This file is licensed under "PolyForm Shield License 1.0.0".
See https://polyformproject.org/wp-content/uploads/2020/06/PolyForm-Shield-1.0.0.txt for more information.
"""


import luigi
import os
import pathlib
from queenbee_local import QueenbeeTask
from .dependencies.incident_irradiance_entry_point import _IncidentIrradianceEntryPoint_15a1447bOrchestrator as IncidentIrradianceEntryPoint_15a1447bWorkerbee


_default_inputs = {   'model_folder': None,
    'models': None,
    'north': 0.0,
    'params_folder': '__params',
    'radiance_parameters': '-ad 5000 -lw 2e-05',
    'simulation_folder': '.',
    'tracking_increment': 5,
    'wea': None}


class CalculateMetrics(QueenbeeTask):
    """Calculate annual irradiance metrics for annual irradiance simulation."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    timestep = luigi.Parameter(default='1')

    @property
    def folder(self):
        value = pathlib.Path('results')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance post-process annual-irradiance raw_results weather.wea --timestep {timestep} --sub-folder ../metrics'.format(timestep=self.timestep)

    def requires(self):
        return {'SynthesizeSolarTracking': SynthesizeSolarTracking(_input_params=self._input_params)}

    def output(self):
        return {
            'metrics': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix()
            ),
            
            'timestep_file': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/timestep.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False},
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'metrics', 'from': 'metrics',
                'to': pathlib.Path(self.execution_folder, 'metrics').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            },
                
            {
                'name': 'timestep-file', 'from': 'raw_results/timestep.txt',
                'to': pathlib.Path(self.execution_folder, 'results/timestep.txt').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateIndirectSky(QueenbeeTask):
    """Generate a sun-up sky matrix."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def sky_type(self):
        return 'no-sun'

    @property
    def output_type(self):
        return 'solar'

    @property
    def output_format(self):
        return 'ASCII'

    @property
    def sun_up_hours(self):
        return 'sun-up-hours'

    cumulative = luigi.Parameter(default='hourly')

    sky_density = luigi.Parameter(default='1')

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky mtx sky.wea --name sky --north {north} --sky-type {sky_type} --{cumulative} --{sun_up_hours} --{output_type} --output-format {output_format} --sky-density {sky_density}'.format(north=self.north, sky_type=self.sky_type, cumulative=self.cumulative, sun_up_hours=self.sun_up_hours, output_type=self.output_type, output_format=self.output_format, sky_density=self.sky_density)

    def output(self):
        return {
            'sky_matrix': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky_direct.mtx').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-matrix', 'from': 'sky.mtx',
                'to': pathlib.Path(self.execution_folder, 'resources/sky_direct.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class CreateSkyDome(QueenbeeTask):
    """Create a skydome for daylight coefficient studies."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    sky_density = luigi.Parameter(default='1')

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sky skydome --name rflux_sky.sky --sky-density {sky_density}'.format(sky_density=self.sky_density)

    def output(self):
        return {
            'sky_dome': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix()
            )
        }

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sky-dome', 'from': 'rflux_sky.sky',
                'to': pathlib.Path(self.execution_folder, 'resources/sky.dome').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class GenerateSunpath(QueenbeeTask):
    """Generate a Radiance sun matrix (AKA sun-path)."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def output_type(self):
        return '1'

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'gendaymtx -n -D sunpath.mtx -M suns.mod -O{output_type} -r {north} -v sky.wea'.format(output_type=self.output_type, north=self.north)

    def output(self):
        return {
            'sunpath': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/sunpath.mtx').resolve().as_posix()
            ),
            
            'sun_modifiers': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'wea', 'to': 'sky.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sunpath', 'from': 'sunpath.mtx',
                'to': pathlib.Path(self.execution_folder, 'resources/sunpath.mtx').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            },
                
            {
                'name': 'sun-modifiers', 'from': 'suns.mod',
                'to': pathlib.Path(self.execution_folder, 'resources/suns.mod').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class IncidentIrradianceCalcLoop(luigi.Task):
    """No description is provided."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def radiance_parameters(self):
        return self._input_params['radiance_parameters']

    @property
    def model_name(self):
        return self.item['name']

    @property
    def model(self):
        value = pathlib.Path(self._input_params['model_folder'], '{item_name}.hbjson'.format(item_name=self.item['name']))
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sunpath(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sunpath'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_dome(self):
        value = pathlib.Path(self.input()['CreateSkyDome']['sky_dome'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sky_matrix(self):
        value = pathlib.Path(self.input()['CreateIndirectSky']['sky_matrix'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    # get item for loop
    try:
        item = luigi.DictParameter()
    except Exception:
        item = luigi.Parameter()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder'], 'initial_results/{item_name}'.format(item_name=self.item['name'])).resolve().as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    @property
    def map_dag_inputs(self):
        """Map task inputs to DAG inputs."""
        inputs = {
            'simulation_folder': self.execution_folder,
            'model': self.model,
            'radiance_parameters': self.radiance_parameters,
            'sunpath': self.sunpath,
            'sun_modifiers': self.sun_modifiers,
            'sky_dome': self.sky_dome,
            'sky_matrix': self.sky_matrix,
            'model_name': self.model_name
        }
        try:
            inputs['__debug__'] = self._input_params['__debug__']
        except KeyError:
            # not debug mode
            pass

        return inputs

    def run(self):
        yield [IncidentIrradianceEntryPoint_15a1447bWorkerbee(_input_params=self.map_dag_inputs)]
        done_file = pathlib.Path(self.execution_folder, 'incident_irradiance_calc.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateIndirectSky': CreateIndirectSky(_input_params=self._input_params), 'ReadModelList': ReadModelList(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'incident_irradiance_calc.done').resolve().as_posix())
        }


class IncidentIrradianceCalc(luigi.Task):
    """No description is provided."""
    # global parameters
    _input_params = luigi.DictParameter()
    @property
    def data(self):
        value = pathlib.Path(self.input()['ReadModelList']['data'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def items(self):
        try:
            # assume the input is a file
            return QueenbeeTask.load_input_param(self.data)
        except:
            # it is a parameter
            return pathlib.Path(self.input()['ReadModelList']['data'].path).as_posix()

    def run(self):
        yield [IncidentIrradianceCalcLoop(item=item, _input_params=self._input_params) for item in self.items]
        done_file = pathlib.Path(self.execution_folder, 'incident_irradiance_calc.done')
        done_file.parent.mkdir(parents=True, exist_ok=True)
        done_file.write_text('done!')

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def requires(self):
        return {'CreateSkyDome': CreateSkyDome(_input_params=self._input_params), 'GenerateSunpath': GenerateSunpath(_input_params=self._input_params), 'CreateIndirectSky': CreateIndirectSky(_input_params=self._input_params), 'ReadModelList': ReadModelList(_input_params=self._input_params)}

    def output(self):
        return {
            'is_done': luigi.LocalTarget(pathlib.Path(self.execution_folder, 'incident_irradiance_calc.done').resolve().as_posix())
        }


class ParseSunUpHours(QueenbeeTask):
    """Parse sun up hours from sun modifiers file."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def sun_modifiers(self):
        value = pathlib.Path(self.input()['GenerateSunpath']['sun_modifiers'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance sunpath parse-hours suns.mod --name sun-up-hours.txt'

    def requires(self):
        return {'GenerateSunpath': GenerateSunpath(_input_params=self._input_params)}

    def output(self):
        return {
            'sun_up_hours': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results/sun-up-hours.txt').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'sun_modifiers', 'to': 'suns.mod', 'from': self.sun_modifiers, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'sun-up-hours', 'from': 'sun-up-hours.txt',
                'to': pathlib.Path(self.execution_folder, 'results/sun-up-hours.txt').resolve().as_posix(),
                'optional': False,
                'type': 'file'
            }]


class ReadModelList(QueenbeeTask):
    """Read the content of a JSON file as a list."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def src(self):
        value = pathlib.Path(self._input_params['models'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'echo parsing JSON information to a list...'

    def output(self):
        return {'data': luigi.LocalTarget(
                pathlib.Path(
                    self.params_folder,
                    'input_path').resolve().as_posix()
                )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'src', 'to': 'input_path', 'from': self.src, 'optional': False}]

    @property
    def output_parameters(self):
        return [{'name': 'data', 'from': 'input_path', 'to': pathlib.Path(self.params_folder, 'input_path').resolve().as_posix()}]


class SynthesizeSolarTracking(QueenbeeTask):
    """Synthesize a list of result folders to account for dynamic solar tracking."""

    # DAG Input parameters
    _input_params = luigi.DictParameter()

    # Task inputs
    @property
    def north(self):
        return self._input_params['north']

    @property
    def tracking_increment(self):
        return self._input_params['tracking_increment']

    @property
    def folder(self):
        value = pathlib.Path('results/states')
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def sun_up_hours(self):
        value = pathlib.Path(self.input()['ParseSunUpHours']['sun_up_hours'].path)
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def wea(self):
        value = pathlib.Path(self._input_params['wea'])
        return value.as_posix() if value.is_absolute() \
            else pathlib.Path(self.initiation_folder, value).resolve().as_posix()

    @property
    def execution_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def initiation_folder(self):
        return pathlib.Path(self._input_params['simulation_folder']).as_posix()

    @property
    def params_folder(self):
        return pathlib.Path(self.execution_folder, self._input_params['params_folder']).resolve().as_posix()

    def command(self):
        return 'honeybee-radiance post-process solar-tracking raw_results sun-up-hours.txt weather.wea --north {north} --tracking-increment {tracking_increment} --sub-folder ../final'.format(north=self.north, tracking_increment=self.tracking_increment)

    def requires(self):
        return {'ParseSunUpHours': ParseSunUpHours(_input_params=self._input_params), 'IncidentIrradianceCalc': IncidentIrradianceCalc(_input_params=self._input_params)}

    def output(self):
        return {
            'results': luigi.LocalTarget(
                pathlib.Path(self.execution_folder, 'results').resolve().as_posix()
            )
        }

    @property
    def input_artifacts(self):
        return [
            {'name': 'folder', 'to': 'raw_results', 'from': self.folder, 'optional': False},
            {'name': 'sun_up_hours', 'to': 'sun-up-hours.txt', 'from': self.sun_up_hours, 'optional': False},
            {'name': 'wea', 'to': 'weather.wea', 'from': self.wea, 'optional': False}]

    @property
    def output_artifacts(self):
        return [
            {
                'name': 'results', 'from': 'final',
                'to': pathlib.Path(self.execution_folder, 'results').resolve().as_posix(),
                'optional': False,
                'type': 'folder'
            }]


class _Main_15a1447bOrchestrator(luigi.WrapperTask):
    """Runs all the tasks in this module."""
    # user input for this module
    _input_params = luigi.DictParameter()

    @property
    def input_values(self):
        params = dict(_default_inputs)
        params.update(dict(self._input_params))
        return params

    def requires(self):
        yield [CalculateMetrics(_input_params=self.input_values)]
