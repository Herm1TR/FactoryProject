import math
from .models import LogisticsData, Dock, Robot, Warehouse

def parse_route(route_str):
    """
    Parse a string representing a route, formatted as 'x1,y1 -> x2,y2'.
    
    Parameters:
        route_str (str): A string representing a route, e.g. "10,20 -> 30,40".
        
    Returns:
        tuple: A tuple of two coordinates, representing the start and end points; returns (None, None) if parsing fails.
    """
    try:
        start_str, end_str = route_str.split("->")
        x1, y1 = [float(val) for val in start_str.strip().split(",")]
        x2, y2 = [float(val) for val in end_str.strip().split(",")]
        return (x1, y1), (x2, y2)
    except Exception:
        return None, None

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_original_cost(robot):
    """
    Calculate the total cost of the original path based on the robot's historical delivery data.

    This function retrieves all delivery records related to the robot from the LogisticsData model,
    and calculates the delivery distance by parsing the route string in each record, then sums all distances.

    Parameters:
        robot (Robot): The robot instance for which to calculate the delivery cost.

    Returns:
        tuple: A tuple containing the following two elements:
            - total_cost (float): The accumulated total distance cost.
            - original_routes (list): A list of detailed information for each delivery record, including dock name, 
              segment distance, route string, and delivery amount.
    """
    records = LogisticsData.objects.filter(robot=robot)
    total_cost = 0
    original_routes = []
    for record in records:
        start, end = parse_route(record.route_taken)
        if start and end:
            d = euclidean_distance(start, end)
            total_cost += d
            # If dock is None, display as Warehouse
            dock_name = record.dock.name if record.dock is not None else 'Warehouse'
            original_routes.append({
                'dock': dock_name,
                'distance': d,
                'route': record.route_taken,
                'load': record.load_delivered,
            })
    return total_cost, original_routes

def calculate_optimized_route(robot):
    """
    Calculate the optimized delivery route for a robot to reduce the total delivery cost.

    This function first retrieves or creates the warehouse coordinates, and resets the current load of all docks to 0.
    Then, it accumulates the delivery amount for each dock based on the data in LogisticsData, and adjusts it
    according to the maximum capacity of each dock. Finally, it simulates multiple trips of the robot from the 
    warehouse to various docks using a greedy algorithm, selecting the nearest dock for each trip until the 
    robot's load reaches its limit, and returns the optimized delivery results and total cost.

    Parameters:
        robot (Robot): The robot instance for which to calculate the optimized route.

    Returns:
        tuple: A tuple containing the following two elements:
            - total_cost (float): The accumulated total distance cost of all optimized delivery trips.
            - optimized_trips (list): A list of detailed information for each trip, each record containing the trip number,
              single trip cost, and detailed information for each segment (start point, end point, distance, 
              delivery amount, dock name and position).
    """
    # Get warehouse coordinates from the Warehouse model, create if it doesn't exist
    warehouse_obj, created = Warehouse.objects.get_or_create(
        id=1,
        defaults={'location_x': 0, 'location_y': 0, 'pending_cargo': 0}
    )
    warehouse = (warehouse_obj.location_x, warehouse_obj.location_y)
    
    docks = Dock.objects.all()
    for dock in docks:
        dock.current_load = 0
        dock.save()
    
    records = LogisticsData.objects.filter(robot=robot)
    deliveries = {}
    for record in records:
        if record.dock is None:
            continue
        dock_id = record.dock.id
        if dock_id in deliveries:
            deliveries[dock_id]['remaining'] += record.load_delivered
        else:
            deliveries[dock_id] = {
                'dock': record.dock,
                'remaining': record.load_delivered,
                'max_capacity': record.dock.max_capacity,
            }
    for item in deliveries.values():
        if item['remaining'] > item['max_capacity']:
            item['remaining'] = item['max_capacity']
    
    ROBOT_CAPACITY = 5
    optimized_trips = []
    total_cost = 0
    trip_number = 0

    while any(item['remaining'] > 0 for item in deliveries.values()):
        trip_number += 1
        trip_load = 0
        current_position = warehouse
        trip_cost = 0
        segments = []
        while trip_load < ROBOT_CAPACITY and any(item['remaining'] > 0 for item in deliveries.values()):
            nearest_item = None
            nearest_distance = None
            for item in deliveries.values():
                if item['remaining'] > 0:
                    dock_pos = (item['dock'].location_x, item['dock'].location_y)
                    d = euclidean_distance(current_position, dock_pos)
                    if nearest_item is None or d < nearest_distance:
                        nearest_item = item
                        nearest_distance = d
            if nearest_item is None:
                break
            deliver_amount = min(nearest_item['remaining'], ROBOT_CAPACITY - trip_load)
            nearest_item['remaining'] -= deliver_amount
            nearest_item['dock'].current_load += deliver_amount
            nearest_item['dock'].save()
            segment_info = {
                'from': current_position,
                'to': (nearest_item['dock'].location_x, nearest_item['dock'].location_y),
                'distance': nearest_distance,
                'delivered': deliver_amount,
                'dock': nearest_item['dock'].name,
                'position': (nearest_item['dock'].location_x, nearest_item['dock'].location_y)
            }
            segments.append(segment_info)
            trip_load += deliver_amount
            trip_cost += nearest_distance
            current_position = (nearest_item['dock'].location_x, nearest_item['dock'].location_y)
        return_distance = euclidean_distance(current_position, warehouse)
        trip_cost += return_distance
        segments.append({
            'from': current_position,
            'to': warehouse,
            'distance': return_distance,
            'delivered': 0,
            'dock': 'Warehouse',
            'position': warehouse
        })
        total_cost += trip_cost
        optimized_trips.append({
            'trip_number': trip_number,
            'trip_cost': trip_cost,
            'segments': segments,
        })
    return total_cost, optimized_trips
