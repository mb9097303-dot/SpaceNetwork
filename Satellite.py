import time

from space_network_lib import *


class RelayPacket(Packet):
    def __init__(self, packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay, sender, proxy)
        self.data = packet_to_relay
        self.sender = sender
        self.receiver = proxy

    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver}from {self.sender})"

class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")
        if isinstance(packet,RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")



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

network = SpaceNetwork(level=6 )
earth = Satellite("Earth", 0)
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)
sat3 = Satellite("Sat3",300)
sat4 = Satellite("Sat4",400)

def smart_send_packet(entities, packet_request):
    sorted_entities = sorted(entities, key=lambda x: x.distance_from_earth)

    last_sender = sorted_entities[-2]
    final_dest = sorted_entities[-1]

    current_packet = Packet(packet_request.data, last_sender, final_dest)
    for i in range(len(sorted_entities) - 3, -1, -1):
        sender = sorted_entities[i]
        proxy = sorted_entities[i + 1]
        current_packet = RelayPacket(current_packet, sender, proxy)
    print(f"Smart route calculated via {len(sorted_entities) - 1} hops. Sending...")
    try:
        attempt_transmission(current_packet)
    except BrokenConnectionError:
        print("Smart transmission failed")


all_entities = [earth,sat1,sat2,sat3,sat4]
request_packet = Packet("Hello Smart World!!", earth,sat4)
smart_send_packet(all_entities, request_packet)

all_entities = [earth,sat1,sat2,sat3,sat4]

request_packet = Packet("Hello Smart World!!", earth,sat4)


smart_send_packet(all_entities, request_packet)
# def smart_send_packet(packet:Packet, entities:list):
#     graph =
#     for i in range(len(entities)):
#
#     try:
#         attempt_transmission()
#     except BrokenConnectionError:
#         print( "Transmission failed")



# pack = Packet("The situation on the satellite",sat1,sat2)
# p_final = Packet("hello from earth!!",sat3,sat4)
# p_final_1 = RelayPacket(p_final,sat2,sat3)
# p_final_2 = RelayPacket(p_final_1,sat1,sat2)
# attempt_transmission(p_earth_to_sat1)

# p_earth_to_sat1 = RelayPacket(p_final_2,earth,sat1)


