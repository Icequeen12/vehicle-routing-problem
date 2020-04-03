"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import matplotlib.pyplot as plt
from urllib.request import urlopen


def create_data_model(url, truckNumber):
    trucks = truckNumber
    file = (urlopen(url).read().decode('utf-8'))
    separateLines = file.split('\n')
    capacity = []

    index = 0
    for i in separateLines:
        index = index + 1
        if "CAPACITY" in i:
            capacitance = int(i.split(": ", 1)[1])
        if "NODE_COORD_SECTION" in i:
            coord = index
        if "DEMAND_SECTION" in i:
            demand = index
        if "DEPOT_SECTION" in i:
            end = index

    for x in range(trucks):
        capacity.append(capacitance)

    allCoord = separateLines[coord:demand - 1]
    allDemands = separateLines[demand:end - 1]

    points = []
    for i in allCoord:
        i = i.split()
        points.append((float(i[1]), float(i[2])))

    demands = []
    for i in allDemands:
        i = i.split()
        demands.append((int(i[1])))

    distance_matrix = []

    for point in points:
        distance_vector = []
        for i in range(len(points)):
            distance_vector.append(abs(point[0] - points[i][0]) + abs(point[1] - points[i][1]))
        distance_matrix.append(distance_vector)

    data = {}
    data['distance_matrix'] = distance_matrix
    data['demands'] = demands
    data['vehicle_capacities'] = capacity
    data['num_vehicles'] = len(capacity)
    data['points'] = points

    return data


def get_routes(manager, routing, solution, num_routes):
    """Get vehicle routes from a solution and store them in an array."""
    routes = []
    for route_nbr in range(num_routes):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes


def plotSoluction(routes, points, method):
    plt.figure(1)
    x = []
    y = []

    startingPointX = points[0][0]
    startingPointY = points[0][1]

    for ii in range(len(routes)):

        l = "Ścieżka" + str(ii)
        for i in range(len(routes[ii])):
            x.append(points[routes[ii][i]][0])
            y.append(points[routes[ii][i]][1])
        plt.plot(x, y, marker="o", markerfacecolor="r", label=l)
        x = []
        y = []

    plt.plot(startingPointX, startingPointY, marker="o", markerfacecolor="b", label="zajezdnia")

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.legend(bbox_to_anchor=(1.1, 1.05))
    text(routes, method)
    plt.show()


def text(routes, method):
    plt.figure(2, figsize=(8, 6))

    resultText = "Metoda: " + method + "\n Rozwiązanie: \n"
    for i, route in enumerate(routes):
        resultText = resultText + 'Ścieżka ' + str(i) + ' ' + str(route) + '\n'
    plt.figtext(.0, .0, resultText, wrap=True)


def main(url, method, time, trucks):
    """Solve the CVRP problem."""

    data = create_data_model(url, trucks)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           trucks, 0)
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    # Setting first solution heuristic.

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    if method == "FIRST_SOLUTION":
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    else:
        if "AUTOMATIC" == method:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
        elif "GREEDY_DESCENT" == method:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT)
        elif "GUIDED_LOCAL_SEARCH" == method:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        elif "SIMULATED_ANNEALING" == method:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
        elif "TABU_SEARCH" == method:
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)

        search_parameters.time_limit.seconds = time
        search_parameters.log_search = True

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    routes = get_routes(manager, routing, assignment, data['num_vehicles'])
    # Display the routes.

    plotSoluction(routes, data['points'], method)
