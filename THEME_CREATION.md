# theme creation guide

Valid op1-glitter themes must have at least a key "global" in the top-level object. Optionally, additional keys can be added which have the same name as a .svg in an unpacked OP-1 firmware's /content/display/ directory. Any keys not associated with a file in this directory will be ignored.

> to unpack a firmware, run `op1unpacker unpack (firmware)`.

The values of these keys must be objects. The keys can either be a color in hex notation (ex. #1049e8, #ffffff), or the name of a SVG element's ID.

If the key is a hex color, the value must be another color in hex notation. If the key is an SVG element ID, the value must be a table containing the attribute to modify (usually `stroke` or `fill`), then the hex color.

> check out the example themes in `examples/` if you're confused!

## finding a UI element's SVG ID

[Inkscape](https://inkscape.org/) is a good tool for the job! Open the .svg and click on the element you'd like to get the ID of, and it should highlight the ID in the Layers and Objects panel.

## OP-1 SVGs

Some of the SVGs in `content/display/` are pretty self explanatory, although most are named weirdly:

- `bode.svg`: cwo effect
- `cls.svg`: cluster synth engine
- `drum2.svg`: drum sample editor
- `ftwo.svg`: nitro effect
- `id.svg`: dna synth engine
- `lander.svg`: chop lifter!
- `mllp.svg`: punch effect
- `ok.svg`: finger sequencer
- `pd.svg`: phase synth engine
- `pls.svg`: pulse synth engine
- `ptch.svg`: phone effect
- `rymd.svg`: spring effect
- `simple.svg`: arpeggio sequencer
- `slump.svg`: voltage synth engine
- `st.svg`: string synth engine
- `t10.svg`: digital synth engine

## commonly used OP-1 colors

- 00ed95: green encoder
- ff3a5d: red encoder
- 698eff: blue encoder
- dfd9ff: white encoder
- ffffff: white
- aeb1dc: "text" white
- 9256d7: purple background
- 4d9eff: alternate, lighter blue
- 383572: dull dark purple
