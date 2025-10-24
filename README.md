# hadec-on-azel-grid
Given an earth location, plot lines of constant hour angle and declination on an azimuth-elevation grid

## How to use

From the package, import the `hadec_on_azel_grid` function, passing an `EarthLocation` object from `astropy.coordinates`.

This returns a plotly figure object which can be displayed, written to file, and edited further as desired.

## To do
- [x] Implement plotting of HA/Dec lines on Az/El grid
- [x] Add interactive features to the plot
- [x] Support southern hemisphere locations (SCP instead of NCP)
- [ ] Tidy up plot artifacts at various earth locations (lines suddenly veering off or disappearing)
- [ ] Add more documentation and usage examples
- [ ] Package as a pip-installable module
- [ ] Tidy up inline annotations on the plot (works well in north sky, but equator and south are funky) 