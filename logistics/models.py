from django.db import models

class Dock(models.Model):
    """
    Dock model, used to store the location, name and current load status of each shipping dock
    """
    name = models.CharField(max_length=100, unique=True)
    location_x = models.FloatField(help_text="X-axis coordinate")
    location_y = models.FloatField(help_text="Y-axis coordinate")
    current_load = models.IntegerField(default=0, help_text="Current load")
    max_capacity = models.IntegerField(help_text="Maximum load capacity")

    def __str__(self):
        return self.name

class Robot(models.Model):
    """
    Robot model, used to record the robot's current position, status and other information
    """
    identifier = models.CharField(max_length=50, unique=True)
    current_x = models.FloatField(help_text="Current X coordinate")
    current_y = models.FloatField(help_text="Current Y coordinate")
    is_active = models.BooleanField(default=True, help_text="Whether it is active")

    def __str__(self):
        return self.identifier

class LogisticsData(models.Model):
    """
    Historical delivery data model, used to store delivery records for subsequent statistics and AI analysis
    """
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    dock = models.ForeignKey(Dock, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    route_taken = models.TextField(help_text="Robot delivery route record (e.g., coordinate sequence)")
    load_delivered = models.IntegerField(help_text="Delivery amount")

    def __str__(self):
        dock_name = self.dock.name if self.dock is not None else "Warehouse"
        return f"{self.robot.identifier} -> {dock_name} @ {self.timestamp}"


class Warehouse(models.Model):
    """
    Warehouse model, independent of Dock, used to record warehouse location (fixed at (0,0))
    and the amount of cargo pending for delivery
    """
    location_x = models.FloatField(default=0, help_text="Warehouse X-axis coordinate")
    location_y = models.FloatField(default=0, help_text="Warehouse Y-axis coordinate")
    pending_cargo = models.IntegerField(default=0, help_text="Amount of cargo pending for delivery")

    def __str__(self):
        return "Warehouse"
