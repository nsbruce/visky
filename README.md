# visky

A library to help generate **VI**sualize the celestial **SKY**. Given an earth location, plot lines of constant hour angle and declination on an azimuth-elevation grid.

An example output for the Canadian Dominion Radio Astrophysical Observatories 26 m telescope location.
![example-from-DRAO-26m](./assets/26m.png)

An example output for the Australian Telescope National Facilities Parkes telescope location.
![example-from-parkes](./assets/parkes.png)

## Installation

It is available on pip. Otherwise you can clone this repo and figure it out yourself - this library is a `uv` project.

```shell
pip install visky
```

## How to use

```python
from visky import hadec_on_azel_grid, EarthLocation

# EarthLocation is a thin wrapper around astropy.coordinates.EarthLocation and can be used in a few ways:
location = EarthLocation.of_site('parkes')
location = EarthLocation.from_geodetic(lat = 49.32102306, lon = -119.61898028, height = 546.566)

figure = hadec_on_azel_grid(location)  # this is a plotly figure
figure.show()  # will plot it using the default plotly backend
figure.update_layout(title="My plot title")
figures.write_image('myplot.png')
```

## To do
- [x] Implement plotting of HA/Dec lines on Az/El grid
- [x] Add interactive features to the plot
- [x] Support southern hemisphere locations (SCP instead of NCP)
- [ ] Tidy up plot artifacts at various earth locations (lines suddenly veering off or disappearing)
- [ ] Add more documentation and usage examples
- [ ] Package as a pip-installable module
- [ ] Tidy up inline annotations on the plot (works well in north sky, but equator and south are funky)

## Credit

Tim Robishaw had generated a plot like this that I referenced a lot, and I ripped many elements from it.