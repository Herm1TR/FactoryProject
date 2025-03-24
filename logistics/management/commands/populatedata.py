from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from time import sleep
from logistics.models import Dock, Robot, LogisticsData, Warehouse

class Command(BaseCommand):
    help = 'Generate original delivery data (randomly select Docks, regardless of whether they are at full capacity) to demonstrate differences before and after optimization'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to create original simulation data (ignoring Dock capacity limits)...')
        
        # 1. Create dock data (initial current_load set to 0)
        dock_data = [
            {"name": "Dock A", "location_x": 10.0, "location_y": 20.0, "current_load": 0, "max_capacity": 20},
            {"name": "Dock B", "location_x": 15.0, "location_y": 25.0, "current_load": 0, "max_capacity": 15},
            {"name": "Dock C", "location_x": 20.0, "location_y": 30.0, "current_load": 0, "max_capacity": 25},
            {"name": "Dock D", "location_x": 25.0, "location_y": 35.0, "current_load": 0, "max_capacity": 10},
        ]
        for dock in dock_data:
            Dock.objects.update_or_create(name=dock["name"], defaults=dock)
        self.stdout.write(self.style.SUCCESS('Successfully created or updated dock data'))
        
        # 2. Create robot data
        robot_data = [
            {"identifier": "Robot001", "current_x": 0.0, "current_y": 0.0, "is_active": True},
            {"identifier": "Robot002", "current_x": 0.0, "current_y": 0.0, "is_active": True},
        ]
        for robot in robot_data:
            Robot.objects.update_or_create(identifier=robot["identifier"], defaults=robot)
        self.stdout.write(self.style.SUCCESS('Successfully created or updated robot data'))
        
        # 3. Create Warehouse model (independent from Dock), fixed position at (0,0)
        warehouse_obj, created = Warehouse.objects.get_or_create(
            id=1,
            defaults={"location_x": 0, "location_y": 0, "pending_cargo": 0}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Warehouse created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Warehouse already exists'))
        
        # 4. Simulate original delivery data: each trip starts from warehouse, randomly selects Docks (regardless of capacity)
        robot = Robot.objects.first()
        warehouse = (0.0, 0.0)
        ROBOT_CAPACITY = 5   # Maximum 5 units of cargo per trip
        NUM_TRIPS = 10       # Simulate 10 delivery trips
        docks = list(Dock.objects.all())
        
        for trip in range(NUM_TRIPS):
            self.stdout.write(f'Starting trip {trip+1}...')
            trip_load = 0
            current_position = warehouse
            # Before each trip, set robot position to warehouse
            robot.current_x, robot.current_y = warehouse
            robot.save()
            while trip_load < ROBOT_CAPACITY:
                # Randomly select a Dock (without checking if it's at full capacity)
                selected = random.choice(docks)
                dock_position = (selected.location_x, selected.location_y)
                max_load_possible = ROBOT_CAPACITY - trip_load
                # Randomly generate delivery amount, between 1 and remaining capacity
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
                    f'Delivered {deliver_amount} units to {selected.name}, route: {route}'
                ))
                # Update Dock current_load (without checking if exceeding capacity)
                selected.current_load += deliver_amount
                selected.save()
                trip_load += deliver_amount
                current_position = dock_position
            # Trip completed, robot returns to warehouse
            return_route = f"{current_position[0]},{current_position[1]} -> {warehouse[0]},{warehouse[1]}"
            LogisticsData.objects.create(
                robot=robot,
                dock=None,  # Return trip record, dock is None, indicating return to warehouse
                timestamp=timezone.now(),
                route_taken=return_route,
                load_delivered=0
            )
            self.stdout.write(self.style.SUCCESS(f'Trip {trip+1} completed, robot returned to warehouse: {return_route}'))
            sleep(0.5)
        
        self.stdout.write(self.style.SUCCESS('Original delivery simulation data generated!'))
