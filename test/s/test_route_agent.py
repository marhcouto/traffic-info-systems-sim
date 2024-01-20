import pytest
from model.network_model import NetworkModel
from model.vehicle import Vehicle
import s.scenarios.simple_model1
import s.scenarios.simple_model2
from model.route_agent import RouteAgent, RouteState

# Test the RouteAgent class
class TestRouteAgent:

    @pytest.mark.parametrize(
        ("number_of_vehicles", "steps", "expected"),
        [
            (5, 300, 1),
            (5, 301, 0),
        ]
    )
    def test_step(self, number_of_vehicles: int, steps: int, expected: int):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model2.nodes(),
            "roads": s.scenarios.simple_model2.roads(),
            "start_node": s.scenarios.simple_model2.start_node(),
            "end_node": s.scenarios.simple_model2.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)
        route = model.G[model.start][model.end]['agent']

        for i in range(number_of_vehicles):
            v = Vehicle(i, model, 0)
            v.step()

        for i in range(steps):
            route.step()

        assert route.volume() == expected

        


    @pytest.mark.parametrize(
        ("number_of_vehicles", "expected_volume", "expected_last_time"),
        [
            (10, 10, 10),
            (5,5, 4),
            (7,7, 5),
        ]
    )
    def test_add_vehicle(self, number_of_vehicles: int, expected_volume: int, expected_last_time):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
            route.add_vehicle(Vehicle(i, model, 0))
        
        assert route.volume() == expected_volume
        assert route.queue[0][0].unique_id == 0
        assert route.queue[0][1] == 4.0
        assert route.queue[number_of_vehicles - 1][1] == expected_last_time

    @pytest.mark.parametrize(
        ("number_of_vehicles","gps_delay", "expected"),
        [
            (5, 1, 4.07776),
            (7, 3, 4.07776),
            (14, 5, 7.93216),

        ]
    )
    def test_update_history(self, number_of_vehicles: int, gps_delay: int, expected: float):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": gps_delay,
        }

        model = NetworkModel(**model_params)

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
            route.add_vehicle(Vehicle(i, model, 0))
        
        assert pytest.approx(model.G[model.start][model.end]['travel_time'], 0.00001) == expected


    @pytest.mark.parametrize(
        ("number_of_vehicles", "expected"),
        [
            (0, RouteState.FREE),
            (4, RouteState.FREE),
            (5, RouteState.FULL),
            (6, RouteState.CONGESTED),
            (8, RouteState.HIGHLY_CONGESTED),
            (14, RouteState.HIGHLY_CONGESTED),

        ]
    )
    def test_update_state(self, number_of_vehicles: int, expected: RouteState):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
            route.add_vehicle(Vehicle(i, model, 0))
        
        print(route.volume_to_capacity_ratio())
        assert route.state == expected


    @pytest.mark.parametrize(
    ("number_of_vehicles", "expected"),
    [
        (0, 4.0),
        (1, 4.00096),
        (5, 4.6),
        (10, 13.6),
        (300, 7776004.0)
    ]
    )
    def test_travel_time(self, number_of_vehicles: int, expected: float):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0.0,
        }

        model = NetworkModel(**model_params)
        route = model.G[model.start][model.end]['agent']

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
          route.add_vehicle(Vehicle(i, model, 0))
          
        assert route.travel_time() == expected
    
    @pytest.mark.parametrize(
        ("number_of_vehicles", "expected"),
        [
            (5, 1.0),
            (6, 1.2),
            (0, 0),
            (3,0.6),
        ]
    )
    def test_volume_to_capacity_ratio(self, number_of_vehicles: int, expected: float):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
            route.add_vehicle(Vehicle(i, model, 0))
        
        assert route.volume_to_capacity_ratio() == expected

    @pytest.mark.parametrize(
        ("number_of_vehicles", "expected"),
        [
            (10, 10),
            (5, 5),
            (0, 0),
        ]
    )
    def test_volume(self, number_of_vehicles: int, expected: int):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model1.nodes(),
            "roads": s.scenarios.simple_model1.roads(),
            "start_node": s.scenarios.simple_model1.start_node(),
            "end_node": s.scenarios.simple_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        route = model.G[model.start][model.end]['agent']
        for i in range(number_of_vehicles):
            route.add_vehicle(Vehicle(i, model, 0))
        
        assert route.volume() == expected
