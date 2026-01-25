import time

from space_network_lib import *


class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")

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


network = SpaceNetwork(level=2 )
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2", 200)
pack = Packet("The situation on the satellite",sat1,sat2)

attempt_transmission(pack)