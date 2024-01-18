import pytest
from model.network_model import NetworkModel
from model.vehicle import Vehicle
import s.scenarios.simple_model1
import s.scenarios.simple_model2
import s.scenarios.small_model1
import s.scenarios.small_model2
import s.scenarios.medium_model
from model.route_agent import RouteAgent, RouteState

class TestNetworkModel:
    @pytest.mark.parametrize(
        ("start_node", "end_node", "nodes", "roads", "expected"),
        [
            (s.scenarios.small_model1.start_node(), s.scenarios.small_model1.end_node(), s.scenarios.small_model1.nodes(), s.scenarios.small_model1.roads(), 20),
            (s.scenarios.small_model2.start_node(), s.scenarios.small_model2.end_node(), s.scenarios.small_model2.nodes(), s.scenarios.small_model2.roads(), 16),
        ]
    )
    def test_get_best_time(self, start_node, end_node, nodes, roads, expected):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": nodes,
            "roads": roads,
            "start_node": start_node,           
            "end_node": end_node,
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)
        assert model.get_best_time() == expected



    @pytest.mark.parametrize(
            ("start_node", "end_node", "nodes", "roads", "expected_nodes", "expected_roads"),
            [
                (s.scenarios.simple_model1.start_node(), s.scenarios.simple_model1.end_node(), s.scenarios.simple_model1.nodes(), s.scenarios.simple_model1.roads(), 2, 1),
                (s.scenarios.small_model1.start_node(), s.scenarios.small_model1.end_node(), s.scenarios.small_model1.nodes(), s.scenarios.small_model1.roads(), 4, 4),
                (s.scenarios.medium_model.start_node(), s.scenarios.medium_model.end_node(), s.scenarios.medium_model.nodes(), s.scenarios.medium_model.roads(), 6, 9),
            ]
        )
    def test_create_graph(self, start_node, end_node, nodes, roads, expected_nodes, expected_roads):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": nodes,
            "roads": roads,
            "start_node": start_node,
            "end_node": end_node,
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        assert model.G.number_of_nodes() == expected_nodes
        assert model.G.number_of_edges() == expected_roads
    


    @pytest.mark.parametrize(
        ("number_of_vehicles", "expected"),
        [
            (0, 0),
            (10, 10),
            (20, 20),
            (50, 50)

        ]
    )
    def test_create_vehicles(self, number_of_vehicles, expected):

        model_params = {
            "num_vehicles_s": number_of_vehicles,
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
        old_sched = len(model.schedule.agents)
        model.create_vehicles()

        assert len(model.active_vehicles) == expected
        assert len(model.schedule.agents) == expected + old_sched
        old_sched = len(model.schedule.agents)
        model.create_vehicles()

        assert len(model.active_vehicles) == expected + number_of_vehicles
        assert len(model.schedule.agents) == expected + old_sched

    @pytest.mark.parametrize(
    ("number_of_vehicles", "iterations", "expected"),
        [
            (10, 3, 10),
            (10, 4, 5),
            (10, 5, 3),

        ]
    )
    def test_kill_vehicles(self, number_of_vehicles, iterations, expected):

        print()
        model_params = {
            "num_vehicles_s": number_of_vehicles,
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

        model.step()

        assert len(model.active_vehicles) == number_of_vehicles




        for i in range(iterations):
            route.step()

        model.kill_vehicles()

        assert len(model.active_vehicles) == expected
            

    @pytest.mark.parametrize(
    ("number_of_vehicles", "iterations", "expected"),
        [
            (0, 0, 0),
            (2, 10, 13),
            (5, 20, 89),
            (3, 50, 128)

        ]
    )
    def test_step(self, number_of_vehicles, iterations, expected):

        model_params = {
            "num_vehicles_s": number_of_vehicles,
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

        for i in range(iterations):
            model.step()

        assert len(model.active_vehicles) == expected

    # @pytest.mark.parametrize(
    # ("number_of_vehicles", "iterations", "expected"),
    #     [
    #         (0, 0, 0),
    #         (2, 10, 13),
    #         (5, 20, 89),
    #         (3, 50, 134)

    #     ]
    # )
    # def test_avg_travel_efficiency(self, number_of_vehicles, iterations, expected):
    #     model_params = {
    #         "num_vehicles_s": number_of_vehicles,
    #         "alpha": 0.15,
    #         "beta": 4,
    #         "nodes": s.scenarios.simple_model1.nodes(),
    #         "roads": s.scenarios.simple_model1.roads(),
    #         "start_node": s.scenarios.simple_model1.start_node(),
    #         "end_node": s.scenarios.simple_model1.end_node(),
    #         "prob_gps": 0.0,
    #         "gps_delay": 0,
    #     }

    #     model = NetworkModel(**model_params)
    #     model = NetworkModel(**model_params)

    #     for i in range(iterations):
    #         model.step()
        
    #     assert model.avg_travel_efficiency() == expected


    # @pytest.mark.parametrize(
    # ("number_of_vehicles", "iterations", "expected"),
    #     [
    #         (0, 0, 0),
    #         (2, 10, 13),
    #         (5, 20, 89),
    #         (3, 50, 134)

    #     ]
    # )
    # def test_avg_travel_time(self, number_of_vehicles, iterations, expected):
    #     model_params = {
    #         "num_vehicles_s": number_of_vehicles,
    #         "alpha": 0.15,
    #         "beta": 4,
    #         "nodes": s.scenarios.simple_model1.nodes(),
    #         "roads": s.scenarios.simple_model1.roads(),
    #         "start_node": s.scenarios.simple_model1.start_node(),
    #         "end_node": s.scenarios.simple_model1.end_node(),
    #         "prob_gps": 0.0,
    #         "gps_delay": 0,
    #     }

    #     model = NetworkModel(**model_params)

    #     for i in range(iterations):
    #         model.step()

    #     assert model.avg_travel_time() == expected

    # @pytest.mark.parametrize(
    # ("number_of_vehicles", "iterations", "expected"),
    #     [
    #         (0, 0, 0),
    #         (2, 10, 13),
    #         (5, 20, 89),
    #         (3, 50, 134)

    #     ]
    # )
    # def test_avg_max_vc_ratio(self, number_of_vehicles, iterations, expected):
    #     model_params = {
    #         "num_vehicles_s": number_of_vehicles,
    #         "alpha": 0.15,
    #         "beta": 4,
    #         "nodes": s.scenarios.simple_model1.nodes(),
    #         "roads": s.scenarios.simple_model1.roads(),
    #         "start_node": s.scenarios.simple_model1.start_node(),
    #         "end_node": s.scenarios.simple_model1.end_node(),
    #         "prob_gps": 0.0,
    #         "gps_delay": 0,
    #     }

    #     model = NetworkModel(**model_params)
    #     model = NetworkModel(**model_params)

    #     for i in range(iterations):
    #         model.step()

    #     assert model.avg_max_vc_ratio() == expected

    # @pytest.mark.parametrize(
    # ("number_of_vehicles", "iterations", "expected"),
    #     [
    #         (0, 0, 0),
    #         (2, 10, 13),
    #         (5, 20, 89),
    #         (3, 50, 134)

    #     ]
    # )
    # def test_update_max_vc_ratio(self, number_of_vehicles, iterations, expected):
    #     model_params = {
    #         "num_vehicles_s": number_of_vehicles,
    #         "alpha": 0.15,
    #         "beta": 4,
    #         "nodes": s.scenarios.simple_model1.nodes(),
    #         "roads": s.scenarios.simple_model1.roads(),
    #         "start_node": s.scenarios.simple_model1.start_node(),
    #         "end_node": s.scenarios.simple_model1.end_node(),
    #         "prob_gps": 0.0,
    #         "gps_delay": 0,
    #     }

    #     model = NetworkModel(**model_params)
    #     model = NetworkModel(**model_params)

    #     for i in range(iterations):
    #         model.step()

    #     assert model.update_max_vc_ratio() == expected


