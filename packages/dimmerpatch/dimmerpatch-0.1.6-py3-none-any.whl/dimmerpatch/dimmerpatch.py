from collections import OrderedDict

class LightMap():
    """The mapping of a light's channels relative to its address (zero-offset)    

    Note: the channel map itself doesn't 
    """
    _map_by_use = None
    _map_by_channel = None
    _valid_channel_types = [
        "r",            # Red
        "g",            # Green
        "b",            # Blue
        "dimmer",       # White (or primary) dimmer
        "temperature",  # Color temperature
        "wheel",        # Color wheel
        "pan",          # Pan
        "pan_fine",     # Pan fine
        "tilt",         # Tilt
        "tilt_fine",    # Tilt fine
        "gobo_select",  # Gobo Selector
        "gobo_rotate",  # Gobo Rotator
        "iris",         # Iris
        "focus",        # Focus
        "mode",         # Control mode
        "shutter",      # Shutter,
        "custom0",
        "custom1",
        "custom2",
        "custom3",
        "custom4",
        "custom5",
        "custom6",
        "custom7",
        "custom8",
        "custom9",
    ]

    def __init__(self, channel_map = {}):
        self._map_by_use = OrderedDict()
        self._map_by_channel = {}
        self.set_channel_map(channel_map)

    def get_channel_map(self):
        """Get the channel map as a dictionary"""
        return dict(self._map_by_use)
    
    def get_channel_usage(self):
        """Get the channel usage in the order of the channels"""
        return [usage for usage in self._map_by_use.keys()]
    
    def get_channel_usage_map(self):
        """Get the channel map as a dictionary, ordered by channels"""
        return dict(self._map_by_channel)
    
    def get_channels(self):
        """Get the channels used by this light map"""
        return [k for k in sorted(self._map_by_channel.keys())]

    def get_width(self):
        """Get the channel space width of the light map

            Note that not all addresses in this channel space
            may be used
        """
        channels = self.get_channels()
        return channels[-1] - channels[0] + 1

    def set_channel_map(self, channel_map = {}):
        """Reviews and sets the channel map based on supported capabilities"""
        channel_map_filtered = {usage: channel for usage, channel in channel_map.items() if usage in self._valid_channel_types}
        self._map_by_use = OrderedDict(sorted(channel_map_filtered.items(), key = lambda t: t[1]))
        self._map_by_channel = {channel: usage for usage, channel in channel_map_filtered.items()}

class Rgb(LightMap):
    """A simple RGB-addressable light"""
    def __init__(self):
        super().__init__({
            "r": 0,
            "g": 1,
            "b": 2
        })

class Dimmer(LightMap):
    """A single-channel dimmer """
    def __init__(self):
        super().__init__({
            "dimmer": 0,
        })


class LightPatch():
    # Represents a lighting patch and its starting index

    _lightmap = None
    _channel_start = None

    def __init__(self, lightmap, channel_start = None):
        self._lightmap = lightmap
        self._channel_start = channel_start

    def set_start(self, channel_start):
        """Patch the object to the associated channels"""
        self._channel_start = channel_start
    
    @property
    def light(self):
        return self._lightmap
    
    @property
    def channel_start(self):
        return self._channel_start

    def __repr__(self):
        return "LightPatch({}, {})".format(type(self._lightmap), self._channel_start)

class Channel():
    # Tightly integrated with LightPatch

    _valid_usage_types = LightMap._valid_channel_types

    _lightpatch = None
    _value = None
    _usage = None

    VALUE_MAX=255
    VALUE_MIN=0

    def __init__(self, lightpatch=None, usage="dimmer", value=None):
        self._lightpatch = lightpatch
        if value is None:
            value = self.VALUE_MIN
        self.value = value
        self.usage = usage

    def unpatch(self):
        del self.patch

    @property
    def patch(self):
        return self._lightpatch
    
    @patch.setter
    def patch(self, lightpatch):
        self._lightpatch = lightpatch
    
    @patch.deleter
    def patch(self):
        self._lightpatch = None
        self._usage = "dimmer"  # Revert to dimmer as default

    @property
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        if value in self._valid_usage_types:
            self._usage = value
        else:
            raise ValueError("Invalid usage type")
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if self.VALUE_MIN <= value <= self.VALUE_MAX:
            self._value = value
        else:
            raise ValueError("Value must be between {} and {}".format(self.VALUE_MIN, self.VALUE_MAX))
    
    def blackout(self):
        self.value = self.VALUE_MIN
    
    def __repr__(self):
        return "{}.{}: {}".format(self._lightpatch, self.usage, self.value)


class PatchPanel():

    # We use lists over tuples to allow these to be mutable
    _lights = []        # A list of LightPatch objects
    _channels = []      # A list of Channel objects

    def initialize_list(self, maplist):
        """Initialize the panel from a list of LightMap objects, with None to specify gaps in channel space"""
        # Will clobber existing panel
        for lightmap in maplist:
            if lightmap is None:
                self.pad_to_max(len(self._channels) + 1)
            else:
                self.append_light(lightmap)

    def initialize_fill(self, lightmap, count=1):
        """Initialize the patch panel with duplicates of a given LightMap"""
        # Will clobber existing panel
        for i in range(count):
            self.append_light(lightmap)

    def initialize_map(self, maplist):
        """Initialize the channel space from a list of tuples containing channel start and LightMap"""
        # Will clobber existing panel
        for light_tuple in maplist:
            # We have a tuple containing (channel_start, lightmap)
            self.append_light(light_tuple[1], channel_start=light_tuple[0])

    def __init__(self, size=0):
        """Defines a patch panel of lights and a channel space"""
        self._lights = []
        self._channels = []
        self.pad_to_max(size)
    
    def pad_to_max(self, max_channels):
        """Pad the channel space to the max number of channels"""
        if len(self._channels) < max_channels:
            for i in range(max_channels - len(self._channels)):
                self._channels.append(Channel())       # Add a blank channel

    def append_light(self, lightmap, channel_start=None, patch=True):
        """Append a light at the end of the light array and get the starting address"""
        self.insert_light(lightmap, channel_start, patch, light_index=None)

    def insert_light(self, lightmap, channel_start=None, patch=True, light_index=None):
        """Insert a light, starting at a channel address and light index
        
            channel_start = None, light_index = None will append to respective lists
        """

        if not isinstance(lightmap, LightMap):
            raise TypeError("lightmap must be of type LightMap")
        
        if channel_start is None:
            channel_start = len(self._channels)
        
        light = LightPatch(lightmap, channel_start)
        if light_index is None:
            self._lights.append(light)
            light_index = len(self._lights) - 1
        else:
            self._lights.insert(light)
        
        if patch:
            self.patch_light(light_index)

    def delete_light(self, light_index):
        """Remove a light from the light index and channel space"""
        self.unpatch_light(light_index)
        del self._lights[light_index]
    
    def relocate_light(self, old_index, new_index):
        """Move a light in the light order without changing its channel configuration"""
        self._lights.insert(new_index, self._lights.pop(old_index))
    
    def unpatch_light(self, light_index):
        """Unpatch a light from all tied channels without deleting it"""
        patch = self._lights[light_index]
        [channel.unpatch() for channel in self._channels if channel.patch == patch]
    
    def patch_light(self, light_index, channel_start = None):
        """Patch a light starting at a specific address or the light's previous offset 
        
          Note that a light can be be patched into multiple places in the channel space.
          If you only want it patched once, use repatch_light"""
        patch = self._lights[light_index]
        light = patch.light
        if channel_start is None:
            channel_start = patch.channel_start

        if channel_start is None:
            # We still don't know what our channel start is, so we'll assume
            # it's sequential, at the end of the channel list
            channel_start = len(self._channels)
        
        patch.set_start(channel_start)

        width = light.get_width()
        channel_max = channel_start + width
        self.pad_to_max(channel_max)

        usage_map = light.get_channel_usage_map()
        for (offset, usage) in usage_map.items():
            # This will clobber existing patches
            self._channels[channel_start + offset].patch = patch
            self._channels[channel_start + offset].usage = usage
        
    def repatch_light(self, light_index, new_start=None):
        """Completely unpatch and patch a light, starting at a new channel address or the light's previous offset
        
            If the light is mapped into multiple locations in the channel space, it will be unpatched entirely
        """
        patch = self._lights[light_index]
        if new_start is None:
            new_start = patch.channel_start

        if new_start is None:
            # We still don't know what our channel start is, so we'll assume
            # it's sequential, at the end of the channel list
            channel_start = len(self._channels)
        self.unpatch_light(light_index)
        self.patch_light(light_index, new_start)
    
    def set_channel(self, channel, value):
        """Set a channel to a specific value"""
        self._channels[channel].value = value
    
    def get_channel(self, channel):
        """Get the value of a channel"""
        return self._channels[channel].value

    @property
    def channels(self):
        """Get the live channel values"""
        return [channel.value for channel in self._channels]

    def blackout(self):
        """Blackout all channels"""
        [channel.blackout() for channel in self._channels]

    def set_light(self, light_index, usage, value):
        """Set the attributes of a light"""
        patch = self._lights[light_index]
        for channel in self._channels:
            if channel.patch == patch and channel.usage == usage:
                channel.value = value
    
    def set_light_color(self, light_index, r=0, g=0, b=0):
        """Set the color of a light"""
        patch = self._lights[light_index]
        for channel in self._channels:
            if channel.patch == patch:
                if channel.usage == "r":
                    channel.value = r
                elif channel.usage == "g":
                    channel.value = g
                elif channel.usage == "b":
                    channel.value = b

    def set_dimmers(self, value):
        """Set the value of standard dimmers"""
        for channel in self._channels:
            if channel.usage == "dimmer":
                channel.value = value

    def set_dimmables(self, value):
        """Set all red, green, blue, and dimmer values to the same value"""
        for channel in self._channels:
            if channel.usage in ["r", "g", "b", "dimmer"]:
                channel.value = value

    def set_color(self, r=0,g=0,b=0):
        """Set the color along the strip"""
        # We do it this way instead of via set_attribute so we can
        # go along and set r, g, and b sequently along the channel
        # space rather than setting all red channels, then all green
        # channels, then all blue channels
        for channel in self._channels:
            if channel.usage == "r":
                channel.value = r
            elif channel.usage == "g":
                channel.value = g
            elif channel.usage == "b":
                channel.value = b

    def set_all(self, value):
        """Set all channels to a value"""
        for channel in self._channels:
            channel.value = value
    
    def set_by_usage(self, usage, value):
        """Set all channels with a specific usage to a value"""
        for channel in self._channels:
            if channel.usage == usage:
                channel.value = value

    def __repr__(self):
        return "PatchPanel\n\tChannels : {}\n\tLights : {}".format(self._channels, self._lights)


