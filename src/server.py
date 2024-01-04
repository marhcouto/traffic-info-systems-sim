from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule, ChartModule
from model.network_model import NetworkModel
from model.route_agent import RouteState
from mesa import batch_run
import scenarios.simple_model
import scenarios.long_option
import scenarios.small_model
import scenarios.large_model


def network_portrayal(G):
    # The models ensures there is always 1 agent per node

    def node_color(node):
        if G.out_degree(node) == 0:
            return "#ff99ff"
        elif G.in_degree(node) == 0:
            return "#003399"
        else:
            return "#999999"

    def edge_color(node1, node2):
        if G.get_edge_data(node1, node2)['agent'].state == RouteState.FREE:
            return "#23b800"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.FULL:
            return "#ffd100"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.CONGESTED:
            return "#ff9900"
        elif G.get_edge_data(node1, node2)['agent'].state == RouteState.HIGHLY_CONGESTED:
            return "#dc0d0d"
        else:
            print(G[node1][node2]['agent'].state)
            return '#e8e8e8'

    def edge_width(node1, node2):
        return G.get_edge_data(node1, node2)['agent'].capacity / 100

    portrayal = dict()
    portrayal['nodes'] = [{'size': 2,
                           'color': node_color(node),
                           'tooltip': node.label,
                           'id': node.unique_id,
                           }
                          for node in G.nodes()]

    portrayal['edges'] = [{'source': source.unique_id,
                           'target': target.unique_id,
                           'color': edge_color(source, target),
                           'width': edge_width(source, target),
                           }
                          for (source, target) in G.edges()]

    return portrayal




model_params = {
    "num_vehicles_s": 10,
    "alpha": 0.15,
    "beta": 4,
    "nodes": scenarios.large_model.nodes(),
    "roads": scenarios.large_model.roads(),
    "start_node": scenarios.large_model.start_node(),
    "end_node": scenarios.large_model.end_node(),
    "prob_gps": 1.0,
    "gps_delay": 0,
    "prob_informed": 0.0,
    "tablet_delay": 0,
}
network = NetworkModule(network_portrayal, 500, 500)
chart = ChartModule([{"Label": "Average Time Travel", "Color": "Black"}],
                    data_collector_name='data_collector')



#
# results = batch_run(
#     NetworkModel,
#     parameters=model_params,
#     iterations=5,
#     max_steps=100,
#     number_processes=1,
#     data_collection_period=1,
#     display_progress=True,
# )

# batch_run = batch_run(NetworkModel,
#                         parameters=model_params,
#                         iterations=5,
#                         max_steps=100)

# batch_run.run_all()
#batch_results = batch_run.get_model_vars_dataframe()
#print(batch_results)


server : ModularServer = ModularServer(NetworkModel, [network, chart],
                                       "Network Model", model_params)
server.port : int = 8527 # The default
server.launch()
