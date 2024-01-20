import scenarios.large_model
import scenarios.medium_model
import scenarios.small_model
from model.network_model import NetworkModel

# This file is used to run multiple scenarios with multiple policies

# List of scenarios to run
scenarios = [
    ["Small Model", scenarios.small_model, 15],
    ["Medium Model", scenarios.medium_model, 20],
    ["Large Model", scenarios.large_model, 15]
]

# List of policies to run
policies = [
    ["DUMB", 0.0],
    ["HALF_SMART", 0.5],
    ["SMART", 1.0],
]


iterations = 500 # Number of iterations to run each scenario

# Run each scenario with each policy
for scenario in scenarios:
    print()
    print("SCENARIO: " + str(scenario[0]))
    for policy in policies:
        model = NetworkModel(**{
            "num_vehicles_s": scenario[2],
            "alpha": 0.15,
            "beta": 4,
            "nodes": scenario[1].nodes(),
            "roads": scenario[1].roads(),
            "start_node": scenario[1].start_node(),
            "end_node": scenario[1].end_node(),
            "prob_gps": policy[1],
            "gps_delay": 0,
        })

        for i in range(iterations):
            model.step()

        print()
        print("POLICY: " + str(policy[0]))
        print("Average Travel Time: ", model.avg_travel_time())
        print("Average Maximum V/C Ratio: ", model.avg_max_vc_ratio())
        print("Average Travel Efficiency: ", model.avg_travel_efficiency())
        print("Vehicles Killed: ", model.num_killed_vehicles)

    print()
