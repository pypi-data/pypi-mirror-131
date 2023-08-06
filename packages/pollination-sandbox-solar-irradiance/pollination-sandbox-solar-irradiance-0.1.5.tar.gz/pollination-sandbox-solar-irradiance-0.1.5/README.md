# Incident Irradiance

A recipe to assess average solar irradiance beneath Sandbox Solar agrivoltaic panels.

## Methods

This recipe calculates the total amount of irradiance by calculating the direct solar
irradiance from sun disks and adding them to the contribution from indirect sky irradiance.

```console
incident_irradiance = direct_sun_irradiance + indirect_sky_irradiance
```

The recipe is structured in a manner that ambient bounces are NOT included.
