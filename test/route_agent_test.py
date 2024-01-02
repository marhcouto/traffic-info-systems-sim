import pytest

from model.route_agent import RouteAgent


#!
# \brief Tests the bpr method for empty road.
@pytest.mark.parametrize(
        ("capacity", "avg_speed", "distance", "expected"),
        [
            (5, 5, 5, 1),
            (100, 5, 5, 1),
            (5, 100, 5, 0.05),
            (5, 5, 100, 20),
        ]
)
def test_bpr_parametrized(capacity : int , avg_speed : int, distance : int, 
                          expected : float):
    assert RouteAgent(1, None, capacity, avg_speed, distance).bpr_function() \
        == expected
    
#!
# \brief Tests the bpr method with vehicles in the road.
@pytest.mark.parametrize(
        ("capacity", "avg_speed", "distance", "expected"),
        [
            (5, 5, 5, 1),
            (100, 5, 5, 1),
            (5, 100, 5, 0.05),
            (5, 5, 100, 20),
        ]
)
def test_bpr_with_vehicles(capacity : int , avg_speed : int, distance : int,
                           expected : float):

    route = RouteAgent(1, None, capacity, avg_speed, distance)

    route.add_new_vehicle()
    route.add_new_vehicle()

    assert route.bpr_function() == pytest.approx(expected, 0.01)
    assert route.bpr_function() != expected # Should differ slightly