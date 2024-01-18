import pytest
import networkx as nx
from model.route_agent import RouteAgent
from model.vehicle import Vehicle
from model.network_model import NetworkModel
from model.network_node import NetworkNode

#RouteAgent(self, unique_id : int, model : Model, capacity : int, 
  #               free_flow_time: int, tablet: bool = False, alpha : float = 0.15, beta : float = 4,
   #              origin : NetworkNode = None, destination : NetworkNode = None)

#!
# \brief Tests the bpr method for empty road.
@pytest.mark.parametrize(
        ("capacity", "free_flow_time", "alpha", "beta", "expected"),
        [
            #(200, 4, 0.15, 4, 4),
            #(1, 4, 0.15, 4, 4),
            #(200, 10, 0.15, 4, 10),
            (100, 4, 0.2, 3, 4)

        ] 
)

def test_bpr_parametrized(capacity : int, free_flow_time : int, alpha : float, beta : float, expected : float):
    assert RouteAgent(1, None, capacity, free_flow_time, False, alpha, beta, None, None).travel_time() \
        == expected
    
#!
# \brief Tests the travel time method with vehicles in the road.
@pytest.mark.parametrize(
        ("number_of_vehicles", "capacity", "free_flow_time", "alpha", "beta", "expected", "variation"),
        [
            (1, 200, 4, 0.15, 4, 4.0, 0.01),
            #(2, 200, 4, 0.15, 4, 4.0, 0.01),
            #(10, 200, 4, 0.15, 4, 4.0, 0.01),
            #(300, 200, 4, 0.15, 4, 7, 1),
        ]
)

def test_travel_time_with_vehicles(number_of_vehicles: int, capacity : int, free_flow_time : int, alpha : float, beta : float,  expected : float, variation: float):

    nodes = [0, 1]
    route = [0, 1, capacity, free_flow_time, False]
    model = NetworkModel(0, 0, 1, nodes, [route], 0, 0, alpha, beta)
    route = model.get_routes()[0]
    for i in range(number_of_vehicles):
        print(number_of_vehicles)
        route.add_vehicle(Vehicle(i, model, 0, 0))  
    # Use the correct method for testing travel time
    assert route.travel_time() == pytest.approx(expected, variation)
    assert route.travel_time() != expected  # Should differ slightly

#           (5) -  1
#          -            - (10)
#        0                      - 3
#
#        (6)  -            - (2)
#               -  2
#
# this is the graph we are testing on 4 nodes and 4 edges with the following weights
def test_dijkstra_path():
    nodes = [0, 1, 2, 3]
    r1 = [0, 1, 1, 5, False]
    r2 = [0, 2, 1, 6, False]
    r3 = [1, 3, 1, 10, False]
    r4 = [2, 3, 1, 2, False]
    roads = [r1, r2, r3, r4]
    model = NetworkModel(0, 0, 1, nodes, roads, 0, 0, 0, 0)
    graph = model.getGraph()
    model.get_best_path(graph, 0, 3, "free_flow_time")
    #vehicle = Vehicle(0, model, 0, 0)
    #print(vehicle.next_route_dumb(model.start).unique_id)
    assert 1 != 1



