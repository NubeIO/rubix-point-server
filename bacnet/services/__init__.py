from bacnet.models.network import NetworkModel
from bacnet.services.network import Network

network_service = Network.get_instance()
for network in NetworkModel.query.all():
    network_service.add_network(network)
