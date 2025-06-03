# coord2state

coord2state is a single-file JS library with no dependencies for quickly looking up which state a given latitude and longitude point is in. You can read my blog post about why I built this: [Mapping latitude and longitude to country, state, or city](http://austinhenley.com/latlong.html)

## Installation

You can install it via NPM:

```
npm install coord2state
```

Or include it directly with a CDN:

```
<script src="https://unpkg.com/coord2state/dist/coord2state.min.js"></script>
```

## Usage

Once the script is loaded, simply call `getState(lat, lon)`, like so:

```
const state = getState(40.7128, -74.0060); // returns "NY"
```

## Building

To generate the JS library, install `geopandas` and run `build_state_lookup.py`:

```
python3 scripts/build_state_lookup.py \
  --shapefile tl_2024_us_state.shp \
  --template src/coord2state.template.js \
  --tolerance 0.01 \           
  --out dist/coord2state.js
```
You can then minify it using:

```
terser dist/coord2state.js \
  --compress \
  --mangle \
  --output dist/coord2state.min.js \
  --comments false
```

## Evaluate

The Jupyter notebook for evaluating the borders is `benchmark_borders.ipynb`

<img width="1392" alt="bordersnotebook" src="https://github.com/user-attachments/assets/08e8f426-8110-4a6e-9a6e-8ada940eb04f" />

For comparing the vertices, run `count_points.py`:

```
python3 scripts/count_points.py
```

For generating the border comparison visualizations, run `visualize_state.py`:

```
python3 scripts/visualize_state.py
open compare.png
```
![borderstexas50](https://github.com/user-attachments/assets/f757cb54-a1a2-4e74-a04b-10835b3306dc)
