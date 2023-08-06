# DimmerPatch

Create patch panels of virtual dimmable fixtures for use with protocols such as ESTA DMX or addressable light strips

## Usage

### Defining a new LightMap
A LightMap represents the capabilities of a light and how their addressing is offset relative to the starting address of the light; when this is added
to a patch panel, the capabilities will be mapped to the channel space.

```python
from lightmap import LightMap

# Define the mapping for the Mac Martin Entour in 8-bit mode
Mac350Entour8b = LightMap({
    "shutter": 0,
    "dimmer": 1,
    "wheel": 2,
    "gobo_select": 3,
    "gobo_rotate": 4,
    "iris": 5,
    "focus": 6
})

# Define the mapping for the Mac Martin Entour in 16-bit mode
# Because we don't natively support gobo_rotate_fine, we'll add it as a custom0 attribute
Mac350Entour16b = LightMap({
    "shutter": 0,
    "dimmer": 1,
    "wheel": 2,
    "gobo_select": 3,
    "gobo_rotate": 4,
    "custom0": 5,
    "iris": 6,
    "focus": 7
})

# Define the mapping for a standard RGB-addressable LED
RgbLed = LightMap({
    "r": 0,
    "g": 1,
    "b": 2
})
```

The currently supported attributes are: `dimmer, r, g, b, temperature, wheel, pan, pan_fine, tilt, tilt_fine, mode, shutter, iris, focus, gobo_select, gobo_rotate` as well as custom fields named `custom0, custom1, ..., custom9`

### Defining a new Patch Panel

A patch panel represents an array of lights, mapped to an array of channels (e.g. a single DMX universe, or a light strip). Lights can be added, removed, and repatched.

```python
from patchpanel import PatchPanel

# Create a Patch Panel of 512 channels
universe = PatchPanel(512)
```

You can initialize a patch panel in one of three ways: filled with a single type; with a sequential array of lights; or a more complex array of tuples, indicating lights and their starting addresses

```python
from lightmap import Rgb, Dimmer
from patchpanel import PatchPanel

# Initialize an LED strip of 3 RGB-addressable lights (for a 9-wide channel space)
simplestrip = PatchPanel()              # Size is optional - the channel space will be automatically sized
simplestrip.initialize_fill(Rgb, 3)
len(simplestrip.channels)               # 9

# Initialize a list of lights of different types (RGB and Simple dimmers), using None to specify gaps in the channel space
advancedstrip = PatchPanel()
advancedstrip.initialize_list([Rgb(), Rgb(), None, None, Dimmer(), Rgb(), Dimmer()])
len(advancedstrip.channels)             # 13

# Initialize from a complex mapping of lights: useful when you want to address lights in a different order to
# how they appear in the channel space. Be careful: you can clobber lights if their addresses overlap
complexstrip = PatchPanel()
complexstrip.initialize_map([
    (0, Rgb()),
    (3, Rgb()),
    (10, Rgb()),                        # This light is in the middle of the strip but at the end of the channel space
    (6, Dimmer()),
    (9, Rgb()),                         # A single channel dimmer
])
len(complexstrip.channels)              # 13

# Continued below...
```

### Controlling a Patch Panel
A Patch panel can be controlled via lights, or via the individual channels, as well as via specific attributes

```python
# ... Continued from above
complexstrip.channels                                   # [0,0,0,0,0,0,0,0,0,0,0,0,0]


complexstrip.set_light_color(2, r=255, g=127, b=127)    # Set the middle light - which is at the end of the addressable space
complexstrip.channels                                   # [0,0,0,0,0,0,0,0,0,0,255,128,128]

complexstrip.set_light(4, 99)                           # Set the last light, which is the single-channel dimmer in channel 6
complexstrip.channels                                   # [0,0,0,0,0,0,99,0,0,0,255,128,128]

complexstrip.set_color(1,2,3)                           # Only set lights with r,g,b attributes, leaving the single-channel dimmer untouched
complexstrip.channels                                   # [1,2,3,1,2,3,99,1,2,3,1,2,3]

complexstrip.set_all(5)                                 # Set all channels to 5, regardless of purpose
complexstrip.channels                                   # [5,5,5,5,5,5,5,5,5,5,5,5,5]

complexstrip.set_by_usage("tilt", 32)                   # Set all channels being used for tilt to 32
complexstrip.channels                                   # [5,5,5,5,5,5,5,5,5,5,5,5,5]     # No change

complexstrip.set_by_usage("g", 32)                      # Set all channels being used for green to 32
complexstrip.channels                                   # [5,32,5,5,32,5,5,5,32,5,5,32,5]

complexstrip.blackout()                                 # Blackout the channels
complexstrip.channels                                   # [0,0,0,0,0,0,0,0,0,0,0,0,0]
```

# Reference

## `LightMap`

### `__init__(channel_map={})`

Initialize how a fixtures attributes map to their addressing offset. E.g.

Note: addressing offsets are 0-indexed

```python
fixture = LightMap({
    "r": 0,
    "g": 1,
    "b": 2,
    "dimmer": 3
})
```

### `get_channel_map()`

Get the channel map that defines the light

```python
fixture.get_channel_map()
# >>    {
# >>        "b": 2,
# >>        "dimmer": 3,
# >>        "g": 1,
# >>        "r": 0
# >>    }
```

### `get_channel_usage()`

Returns a list of the channel usages, ordered by their channel mapping

```python
fixture.get_channel_usage()
# >> ["r", "g", "b", "dimmer"]
```

### `get_channel_usage_map()`

Get the channel map as a dictionary, ordered by channels

```python
fixture.get_channel_usage()
# >>    {
# >>        0: "r",
# >>        1: "g",
# >>        2: "b",
# >>        3: "dimmer"
# >>    }
```

### `get_channels()`

Returns a list of the channel offsets for this light

```python
fixture.get_channels()
# >> [0,1,2,3]
```

### `get_width()`

Returns the channel space size of this map

```python
fixture.get_width()
# >> 4
```

### `set_channel_map(channel_map = {})`

Sets/updates the channel map (same as initializing)

Note: If you change the channel map for lights already in a PatchPanel, those lights will need to be repatched

```python
fixture.set_channel_map({
    "r": 0,
    "g": 2,
    "b": 4,
    "dimmer": 6
})
```

## `PatchPanel()`

### `__init__(size=0)`

Initialize a new patch panel, sized to a specified number of channels

Note: the channel space will automatically resize up if you later add lights or initialize the panel using an `initialize_` function, but will not resize down

### `initialize_list(maplist)`
Initialize the panel from a list of LightMap objects, with None to specify gaps in channel space

```python
advancedstrip = PatchPanel() 
advancedstrip.initialize_list([Rgb(), Rgb(), None, None, Dimmer(), Rgb(), Dimmer()])
len(advancedstrip.channels)             # 13
```

### `initialize_fill(lightmap, count)`
Initialize the patch panel with duplicates of a given LightMap

```python
simplestrip = PatchPanel()
simplestrip.initialize_fill(Rgb, 3)
len(simplestrip.channels)               # 9
```

### `initialize_map(maplist)`
Initialize the channel space from a list of tuples containing channel start and LightMap

```python
complexstrip = PatchPanel()
complexstrip.initialize_map([
    (0, Rgb()),
    (3, Rgb()),
    (10, Rgb()),                        # This light is in the middle of the strip but at the end of the channel space
    (6, Dimmer()),
    (9, Rgb()),                         # A single channel dimmer
])
len(complexstrip.channels)              # 13
```

### `pad_to_max(max_channels)`
Resize the patch panel up to a given size, filling the channel space with unmapped channels

Note: you cannot resize the channel space to be _smaller_

### `append_light(lightmap, channel_start=None, patch=True)`
Add a new light to the end of the panel light list, and patch it into the channel space starting at `channel_start` (or resize and append to the channel space if `channel_start=None`) if `patch=True`

```python
complexstrip.append_light(Rgb())
```

### `insert_light(lightmap, channel_start=None, patch=True, light_index=None)`
Insert a light into the panel's light list, starting at a light index (or append, to the light list if `light_index=None`)

If `patch=True`, the light will then be patched at a given `channel_start` (or resize and append to the channel space if `channel_start=None`)

### `delete_light(light_index)`
Unpatches and removes a light from the panel light list

### `relocate_light(old_index, new_index)`
Moves a light in the panel's light list, without affecting its channel mappings

### `unpatch_light(self, light_index)`
Unpatch a light out of the channel space, without removing it from the panel's lights. Can be useful if you need to temporarily remove it and plan to patch it back in later

### `patch_light(self, light_index, channel_start=None)`
Patch the specified light into the channel space, starting at a specific address

If `channel_start=None`, the panel will attempt to patch the light back into the last place the light was mapped. If the light has never been mapped, the channel space will be resized and the light appended to the end.

_Note:_ The panel does not check if an existing light is mapped to the given address space - you may unpatch another light if their addresses collide
_Note:_ A light may be patched onto more than one channel space, so changing a light may affect multiple channels simultaneously.

### `repatch_light(self, light_index, new_start=None)`
Completely unpatches a light, then calls `patch_light(light_index, new_start)```

### `set_channel(channel, value)`
Set the value of a given channel

Note: By default, the accepted range of a channel is `0-255`

### `get_channel(channel, value)`
Get the current value of a given channel

### `blackout()`
Blackout the panel

### `set_light(light_index, usage, value)`
Set the value for a given light's attribute, updating the channel space accordingly

### `set_light_color(light_index, r=0, g=0, b=0)`
Set the channel space corresponding to the R, G and B channels of this light


### `set_dimmers(value)`
Set the value of _all_ dimmer channels in the panel

### `set_dimmables(value)`
Set the value of _all_ red, green, blue, and dimmer channels in the panel

### `set_color(r=0, g=0, b=0)`
Set the red green and blue channels in the panel

### `set_all(value)`
Set the value of all channels in the panel

### `set_by_usage(usage, value)`
Set the value of all channels that have a specific usage

### `@property channels`
Get a list of all channels and their current value
