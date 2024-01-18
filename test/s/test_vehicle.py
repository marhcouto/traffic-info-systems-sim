import pytest

from model.network_model import NetworkModel
from model.vehicle import Vehicle
import s.scenarios.simple_model
import s.scenarios.small_model1
import s.scenarios.small_model2


class TestVehicle:

    def test_step(self):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.simple_model.nodes(),
            "roads": s.scenarios.simple_model.roads(),
            "start_node": s.scenarios.simple_model.start_node(),
            "end_node": s.scenarios.simple_model.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        v = Vehicle(0, model, 0)

        for i in range(10):
            v.step()

        assert v.travel_time == 10

    def test_next_route_dumb(self):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.small_model1.nodes(),
            "roads": s.scenarios.small_model1.roads(),
            "start_node": s.scenarios.small_model1.start_node(),
            "end_node": s.scenarios.small_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        v = Vehicle(0, model, 0)
        assert v.next_route_dumb(model.start).destination.label == "B"

        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.small_model2.nodes(),
            "roads": s.scenarios.small_model2.roads(),
            "start_node": s.scenarios.small_model2.start_node(),
            "end_node": s.scenarios.small_model2.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        v = Vehicle(0, model, 0)z
        assert v.next_route_dumb(model.start).destination.label == "C"

    def test_next_route_gps(self):
        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.small_model1.nodes(),
            "roads": s.scenarios.small_model1.roads(),
            "start_node": s.scenarios.small_model1.start_node(),
            "end_node": s.scenarios.small_model1.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        v = Vehicle(0, model, 0)

        assert v.next_route_gps(model.start).destination.label == "B"

        model_params = {
            "num_vehicles_s": 20,
            "alpha": 0.15,
            "beta": 4,
            "nodes": s.scenarios.small_model2.nodes(),
            "roads": s.scenarios.small_model2.roads(),
            "start_node": s.scenarios.small_model2.start_node(),
            "end_node": s.scenarios.small_model2.end_node(),
            "prob_gps": 0.0,
            "gps_delay": 0,
        }

        model = NetworkModel(**model_params)

        v = Vehicle(0, model, 0)
        assert v.next_route_gps(model.start).destination.label == "C"

    def test_change_road(self):
        assert True
