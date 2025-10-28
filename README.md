# visky

A library to help generate **VI**sualize the celestial **SKY**. Given an earth location, plot lines of constant hour angle and declination on an azimuth-elevation grid.

An example output for the Canadian Dominion Radio Astrophysical Observatories 26 m telescope location.
![example-from-DRAO-26m](./assets/26m.png)

An example output for the Australian Telescope National Facilities Parkes telescope location.
![example-from-parkes](./assets/parkes.png)

**Note:** there are plotting artifacts for some locations. Pull requests are welcome!

## Installation

It is available on pip. Otherwise you can clone this repo and figure it out yourself - this library is a `uv` project.

```shell
pip install visky
```

## How to use

In it's simplest form,

```python
from visky import hadec_on_azel_grid, EarthLocation
hadec_on_azel_grid(EarthLocation.of_site('parkes')).show()
```

But you can also do more complex things, like set custom Earth locations, and edit the returned plotly figure.

```python
from visky import hadec_on_azel_grid, EarthLocation

# EarthLocation is a thin wrapper around astropy.coordinates.EarthLocation and can be used in a few ways:
location = EarthLocation.of_site('parkes')
location = EarthLocation.from_geodetic(lat = 49.32102306, lon = -119.61898028, height = 546.566)

figure = hadec_on_azel_grid(location)  # this is a plotly figure
figure.show()  # will plot it using the default plotly backend
figure.update_layout(title="My plot title")
figure.update_layout(width=1754, height=1240, margin=dict(l=60,r=40, b=60,t=60))  # good for A4 paper
figures.write_image('myplot.png')
```

## Credit

Tim Robishaw had generated a plot like this that I referenced a lot, and I ripped many elements from it.