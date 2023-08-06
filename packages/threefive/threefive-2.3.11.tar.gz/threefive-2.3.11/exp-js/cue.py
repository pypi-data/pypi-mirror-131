"""
threefive.Cue Class
"""
from base64 import b64decode, b64encode
#import json
from sys import stderr
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map


class Cue(SCTE35Base):
    """
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    Example usage:

    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)

    # cue.decode() returns True on success,or False if decoding failed

    >>>> cue.decode()
    True

    # After Calling cue.decode() the instance variables can be accessed via dot notation.

    >>>> cue.command
    {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
    'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'

    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a instance passed from a Stream instance
        """
        self.info_section = SpliceInfoSection()
        self.command = None
        self.descriptors = []
        if data:
            self.bites = self._mk_bits(data)
        self.packet_data = packet_data

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        self.descriptors = []
        # self.bites after_info section decoding
        after_info = self.mk_info_section(self.bites)
        # self.bites = self.bites[0 : self.info_section.section_length + 3]
        if after_info:
            after_cmd = self._set_splice_command(after_info)
            if after_cmd:
                after_dscrptrs = self._mk_descriptors(after_cmd)
                if after_dscrptrs:
                    crc = hex(int.from_bytes(after_dscrptrs[0:4], byteorder="big"))
                    self.info_section.crc = crc
                    return True
        return False


    def _descriptorloop(self, bites, dll):
        """
        Cue._descriptorloop parses all splice descriptors
        """
        tag_n_len_bites = 2  # 1 byte for descriptor tag,
        # 1 byte for descriptor length
        while dll:
            spliced = splice_descriptor(bites)
            if not spliced:
                return
            sdl = spliced.descriptor_length
            sd_size = tag_n_len_bites + sdl
            dll -= sd_size
            bites = bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def get(self):
        """
        Cue.get returns the SCTE-35 Cue
        data as a dict of dicts.
        """
        if self.command and self.info_section:
            scte35 = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            if self.packet_data is not None:
                scte35["packet_data"] = self.packet_data.get()
            return scte35
        return False

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def get_json(self):
        """
        Cue.get_json returns the Cue instance
        data in json.
        """
        return self.get()

    @staticmethod
    def _mk_bits(data):
        """
        cue._mk_bits Converts
        Hex and Base64 strings into bytes.
        """
        try:
            # Handles hex byte strings
            i = int(data, 16)
            i_len = i.bit_length() >> 3
            bites = int.to_bytes(i, i_len, byteorder="big")
            return bites
        except (LookupError, TypeError, ValueError):
            if data[:2].lower() == "0x":
                data = data[2:]
            if data[:2].lower() == "fc":
                return bytes.fromhex(data)
        try:
            return b64decode(data)
        except (LookupError, TypeError, ValueError):
            return data

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptorloop
        """
        try:
            dll = (bites[0] << 8) | bites[1]
        except (LookupError, TypeError, ValueError):
            return False
        self.info_section.descriptor_loop_length = dll
        bites = bites[2:]
        self._descriptorloop(bites, dll)
        return bites[dll:]

    def mk_info_section(self, bites):
        """
        Cue.mk_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = 14
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        Cue._set_splice_command parses
        the command section of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return False
        self.command = command_map[sct](bites)
        self.command.decode()
        del self.command.bites
        bites = bites[self.command.command_length :]
        return bites

    def show(self):
        """
        Cue.show prints the Cue as JSON
        """
        print(self.get())

    def to_stderr(self):
        """
        Cue.to_stderr prints the Cue
        as JSON to sys.stderr
        """
        print(self.get(), file=stderr)
