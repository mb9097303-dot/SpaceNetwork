import time

from space_network_lib import *


class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")
        if isinstance(packet,RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")

earth = Satellite("Earth",0)

class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)
        self.data = packet_to_relay
        self.sender = sender
        self.receiver = proxy

    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver}from {self.sender})"


class BrokenConnectionError(Exception):
    pass

def attempt_transmission(packet):
    while True:
        try:
            network.send(packet)
            break
        except TemporalInterferenceError:
            print("waiting ,Interference...")
            time.sleep(2.0)
        except DataCorruptedError:
            print("Data retrying ,corrupted...")
        except LinkTerminatedError:
            print("Link lost")
            raise BrokenConnectionError()
        except OutOfRangeError:
            print("Target out of range")
            raise BrokenConnectionError()


network = SpaceNetwork(level=3 )
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)
sat3 = Satellite("Sat3",300)
sat4 = Satellite("Sat4",400)

pack = Packet("The situation on the satellite",sat1,sat2)

p_final = Packet("hello from earth!!",sat3,sat4)
p_final_1 = RelayPacket(p_final,sat2,sat3)
p_final_2 = RelayPacket(p_final_1,sat1,sat2)
p_earth_to_sat1 = RelayPacket(p_final_2,earth,sat1)
# attempt_transmission(p_earth_to_sat1)

try:
    attempt_transmission(p_earth_to_sat1)
except BrokenConnectionError:
    print( "Transmission failed")
