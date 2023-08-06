from pollination.sandbox_solar_irradiance.entry import SandboxSolarIrradianceEntryPoint
from queenbee.recipe.dag import DAG


def test_sandbox_solar_irradiance():
    recipe = SandboxSolarIrradianceEntryPoint().queenbee
    assert recipe.name == 'sandbox-solar-irradiance-entry-point'
    assert isinstance(recipe, DAG)
