from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from time import sleep
from logistics.models import Dock, Robot, LogisticsData, Warehouse

class Command(BaseCommand):
    help = '產生原始運送資料 (隨機選擇 Dock，不考慮 Dock 是否滿載) 以便展示最佳化前後的差異'

    def handle(self, *args, **kwargs):
        self.stdout.write('開始建立原始模擬資料 (不考慮 Dock 滿載)...')
        
        # 1. 建立碼頭資料 (初始 current_load 設為 0)
        dock_data = [
            {"name": "Dock A", "location_x": 10.0, "location_y": 20.0, "current_load": 0, "max_capacity": 20},
            {"name": "Dock B", "location_x": 15.0, "location_y": 25.0, "current_load": 0, "max_capacity": 15},
            {"name": "Dock C", "location_x": 20.0, "location_y": 30.0, "current_load": 0, "max_capacity": 25},
            {"name": "Dock D", "location_x": 25.0, "location_y": 35.0, "current_load": 0, "max_capacity": 10},
        ]
        for dock in dock_data:
            Dock.objects.update_or_create(name=dock["name"], defaults=dock)
        self.stdout.write(self.style.SUCCESS('成功建立或更新碼頭資料'))
        
        # 2. 建立機器人資料
        robot_data = [
            {"identifier": "Robot001", "current_x": 0.0, "current_y": 0.0, "is_active": True},
            {"identifier": "Robot002", "current_x": 0.0, "current_y": 0.0, "is_active": True},
        ]
        for robot in robot_data:
            Robot.objects.update_or_create(identifier=robot["identifier"], defaults=robot)
        self.stdout.write(self.style.SUCCESS('成功建立或更新機器人資料'))
        
        # 3. 建立 Warehouse 模型（獨立於 Dock），固定位置為 (0,0)
        warehouse_obj, created = Warehouse.objects.get_or_create(
            id=1,
            defaults={"location_x": 0, "location_y": 0, "pending_cargo": 0}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('建立 Warehouse 成功'))
        else:
            self.stdout.write(self.style.SUCCESS('Warehouse 已存在'))
        
        # 4. 模擬原始運送資料：每趟運送從倉庫出發，隨機選擇 Dock (不考慮是否滿載)
        robot = Robot.objects.first()
        warehouse = (0.0, 0.0)
        ROBOT_CAPACITY = 5   # 每趟最多送 5 單位貨物
        NUM_TRIPS = 10       # 模擬 10 趟運送
        docks = list(Dock.objects.all())
        
        for trip in range(NUM_TRIPS):
            self.stdout.write(f'開始第 {trip+1} 趟運送...')
            trip_load = 0
            current_position = warehouse
            # 每趟運送前，將機器人位置設為倉庫
            robot.current_x, robot.current_y = warehouse
            robot.save()
            while trip_load < ROBOT_CAPACITY:
                # 隨機選擇一個 Dock（不檢查滿載狀況）
                selected = random.choice(docks)
                dock_position = (selected.location_x, selected.location_y)
                max_load_possible = ROBOT_CAPACITY - trip_load
                # 隨機產生本次送貨量，介於 1 到剩餘量之間
                deliver_amount = random.randint(1, max_load_possible)
                route = f"{current_position[0]},{current_position[1]} -> {dock_position[0]},{dock_position[1]}"
                LogisticsData.objects.create(
                    robot=robot,
                    dock=selected,
                    timestamp=timezone.now(),
                    route_taken=route,
                    load_delivered=deliver_amount
                )
                self.stdout.write(self.style.SUCCESS(
                    f'送貨 {deliver_amount} 單位至 {selected.name}，路徑：{route}'
                ))
                # 更新 Dock current_load (不檢查超出容量)
                selected.current_load += deliver_amount
                selected.save()
                trip_load += deliver_amount
                current_position = dock_position
            # 本趟送貨結束，機器人回到倉庫
            return_route = f"{current_position[0]},{current_position[1]} -> {warehouse[0]},{warehouse[1]}"
            LogisticsData.objects.create(
                robot=robot,
                dock=None,  # 回程記錄，dock 為 None，代表回倉庫
                timestamp=timezone.now(),
                route_taken=return_route,
                load_delivered=0
            )
            self.stdout.write(self.style.SUCCESS(f'第 {trip+1} 趟完成，機器人回倉庫：{return_route}'))
            sleep(0.5)
        
        self.stdout.write(self.style.SUCCESS('原始運送模擬資料已生成！'))
