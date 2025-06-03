# coord2state

To use the library, ...

To generate the JS library, install `geopandas` and run `build_state_lookup.py`:

```
python3 build_state_lookup.py \
  --shapefile tl_2024_us_state.shp \
  --template state-lookup.template.js \
  --tolerance 0.000 \           
  --out state-lookup.js
```
You can then minify it using:

```
terser state-lookup.js \
  --compress \
  --mangle \
  --output state-lookup.min.js \
  --comments false
```

For comparing the vertices, run `count_points.py`:

```
python3 count_points.py
```

For generating the border comparison visualizations, run `visualize_state.py`:

```
python3 visualize_state.py
open compare.png
```
