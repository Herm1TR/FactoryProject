# logistics/optimization.py

import math
from .models import LogisticsData, Dock, Robot, Warehouse

def parse_route(route_str):
    """
    解析代表路徑的字串，格式為 'x1,y1 -> x2,y2'。
    
    參數:
        route_str (str): 表示路徑的字串，例如 "10,20 -> 30,40"。
        
    返回:
        tuple: 兩個座標的 tuple，分別表示起點和終點；如果解析失敗，則返回 (None, None)。
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
    根據機器人的歷史運送資料計算原始路徑的總成本。

    該函式從 LogisticsData 模型中取得與該機器人相關的所有運送記錄，
    並透過解析每筆記錄中的路徑字串計算運送距離，再將所有距離加總。

    參數:
        robot (Robot): 要計算運送成本的機器人實例。

    返回:
        tuple: 包含以下兩個元素的 tuple：
            - total_cost (float): 累計的總距離成本。
            - original_routes (list): 每筆運送記錄的詳細資料列表，包含碼頭名稱、單段距離、路徑字串以及送貨量。
    """
    records = LogisticsData.objects.filter(robot=robot)
    total_cost = 0
    original_routes = []
    for record in records:
        start, end = parse_route(record.route_taken)
        if start and end:
            d = euclidean_distance(start, end)
            total_cost += d
            # 如果 dock 為 None，顯示為 Warehouse
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
    計算機器人的最佳化運送路徑，以降低總運送成本。

    此函式先取得或建立倉庫座標，並將所有碼頭的當前載重重置為 0。接著，
    根據 LogisticsData 中的資料累積各碼頭的送貨量，並根據每個碼頭的最大容量做調整。
    最後，以貪婪法模擬機器人從倉庫出發到各個碼頭的多趟運送，每趟運送依據距離選擇
    最近的碼頭，直到機器人的載重達到上限，並返回最佳化後的運送結果與總成本。

    參數:
        robot (Robot): 要計算最佳化路徑的機器人實例。

    返回:
        tuple: 包含以下兩個元素的 tuple：
            - total_cost (float): 所有最佳化運送趟次累計的總距離成本。
            - optimized_trips (list): 每趟運送的詳細資料列表，每筆資料包含行程編號、單趟運送成本及
              每個段落的詳細資訊（起點、終點、距離、送貨量、碼頭名稱及位置）。
    """
    # 取得倉庫座標從 Warehouse 模型，若不存在則建立
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