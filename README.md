# Standible #

An anagram for Automated BLENDer-based raSTerIzer.

# Prerequisites #

[Zsh](https://www.zsh.org/) and
[Blender](https://www.blender.org/)

# Usage #

`git clone` this repository. 

Customize the [configuration files](#configuration-and-customization).

Run `make`.

## Continue from an interruption ##
To continue from an interruption, run `make renders`.

To render a new style for a given set of renders, run
`make STYLES=new-style render-partials`. The rendering
corresponding to the `new-style` should be defined
using blender configurations. More on this later.


# Output format #

All images are stored as a filesystem database with
indexing as follows, given `PREFIX` as output path
prefix:

`${PREFIX}/renders/${KEY}/r_${STYLE}/${NUM}.png`

where `KEY` is an 8-digit random hex,  
`STYLE` is one of `contour`, `diffuse`, `gnomon`,
`highlights`, `midtones`, `shades`, `shadow`, `sketch`,
`sketch_geom`, `sketch_geom_no_free`, `sketch_no_free`;
representing different styles of render.  
`NUM` is a 3-digit decimal index of (video) sequence.


# Makefile Targets #

`all`: Default target. Creates both keys and renders
for each key

`keys`: Create a set of unique keys, one for each set
of renders of one geometry.

`renders` : Defined by a key, create a render folder,
generate random params and create renders for all
defined styles. Job completion indicated by existance
of a file `${PREFIX}/renders/${KEY}/complete`

`render-partials` : Given params in the render folder
`${PREFIX}/renders/${KEY}`, create renders for all
defined styles. Job completion indicated by existance
of a file `${PREFIX}/renders/${KEY}/complete`  
This target differs from `renders`, in that it does not
create params. Useful to resume an incomplete make
session.

# Configuration and customization #

## `config.Makefile` ##

High-level configuration handles are available with
[`config.Makefile`](./config.Makefile), and the most significant
variables are listed below:

```makefile
PREFIX         := dist

NUM_KEYS       := 8

NUM_FRAMES     := 5
NUM_KEYFRAMES  := 3

STYLES         := contour gnomon 
STYLES         += highlights midtones shades shadow
STYLES         += sketch diffuse

KEYS_FOLDER    := ${PREFIX}/keys
RENDERS_FOLDER := ${PREFIX}/renders

DATA_PREFIX    := ${PREFIX}/params
FRAMES_DATA    := ${DATA_PREFIX}/frames.ndjson
SCENE_DATA     := ${DATA_PREFIX}/meta.ndjson
```

## `config.json` ##

The detailed configuration can be found and customized
in the file [`config.json`](./sample.config.json).


### To specify geometry import path ###
Modify key `geometry.prefix` in [`config.json`](./sample.config.json)  
Note: each geometry is used once to generate all
renders.


### To specify gnomon geometry ###
Modify key `gnomon.geometry` in [`config.json`](./sample.config.json)  
Note: Require to render `gnomon`. If not required,
remove key `gnomon` from var `STYLES` in
[`config.Makefile`](./sample.config.Makefile).
