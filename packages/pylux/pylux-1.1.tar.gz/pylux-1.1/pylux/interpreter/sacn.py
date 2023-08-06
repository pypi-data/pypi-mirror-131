from pylux.interpreter import InterpreterExtension, RegularCommand, NoRefsCommand
from pylux import document, clihelper
import pylux.lib.keyword as kw
import sacn
import time


class PacketManager:

    def __init__(self):
        self.packets = []

    def apply_level(self, univ: int, addr: int, value: int):
        selected_packet = None
        for packet in self.packets:
            if packet.univ == univ:
                selected_packet = packet
        if not selected_packet:
            selected_packet = DmxPacket(univ)
            self.packets.append(selected_packet)
        # Our addresses are 1-index based
        selected_packet.chans[addr - 1] = value


class DmxPacket:

    def __init__(self, univ: int = 1):
        self.univ = univ
        self.chans = [0] * 512


class SacnExtension(InterpreterExtension):

    def __init__(self, *args):
        super().__init__(*args)
        self.sender = sacn.sACNsender(source_name=self.config['sacn']['source-name'])

    def shutdown(self):
        self.stop_output()
        return True

    def register_commands(self):
        self.commands.append(RegularCommand((kw.CUE, kw.OUTPUT), self.output_cue))
        self.commands.append(NoRefsCommand((kw.CUE, kw.OUTPUT_STOP), self.stop_output))

    def output_cue(self, cues):
        if len(cues) > 1:
            self.post_feedback(['Only one cue can be output at a time. ' 
                                'The first in the selection will be used'])
        cue = cues[0]
        packet_manager = PacketManager()
        for level in cue.levels:
            function = self.file.get_function_by_uuid(level.function)
            reg, addr = self.file.get_function_patch(function)
            val = self.file.get_raw_cue_level(cue, function)
            if len(addr) == 1:
                packet_manager.apply_level(int(reg.ref) + 1, addr[0], val)
            elif len(addr) == 2:
                msb = int((val-1)/255)
                lsb = val % 255
                packet_manager.apply_level(int(reg.ref) + 1, addr[0], msb)
                packet_manager.apply_level(int(reg.ref) + 1, addr[1], lsb)
        self.sender.start()
        for packet in packet_manager.packets:
            self.sender.activate_output(packet.univ)
            self.sender[packet.univ].destination = self.config['sacn']['unicast-ip']
            self.sender[packet.univ].dmx_data = tuple(packet.chans)

    def stop_output(self):
        self.sender.stop()


def register_extension(interpreter):
    return SacnExtension(interpreter).register_extension()
