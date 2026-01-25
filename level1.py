from space_network_lib import SpaceEntity, SpaceNetwork, Packet


class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")

network = SpaceNetwork(level=1)
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2", 200)
pack = Packet("The situation on the satellite",sat1,sat2)
network.send(pack)