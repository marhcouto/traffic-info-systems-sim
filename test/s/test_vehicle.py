from model.network_model import NetworkModel
from model.vehicle import Vehicle
import s.scenarios.simple_model1
import s.scenarios.small_model1
import s.scenarios.small_model2

# Test the Vehicle class
class TestVehicle:

    def test_step(self):
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

        v = Vehicle(0, model, 0)
        assert v.next_route_dumb(model.start).destination.label == "C"

    def test_next_route_gps(self):

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

        number_of_vehicles = 10
        for i in range(number_of_vehicles):
            v = Vehicle(i, model, 0)
            assert v.next_route_gps(model.start).destination.label == "C"
            v.step()

        v = Vehicle(i, model, 0)
        assert v.next_route_gps(model.start).destination.label == "B"

    def test_change_road(self):
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

        number_of_vehicles = 10
        for i in range(number_of_vehicles):
            v = Vehicle(i, model, 1.0)
            v.change_road()
            assert v.pos.destination.label == "C"


        for i in range(3):
            v = Vehicle(i, model, 1.0)
            v.change_road()
            assert v.pos.destination.label == "B"
            v = Vehicle(i, model, 0.0)
            v.change_road()
            assert v.pos.destination.label == "C"
