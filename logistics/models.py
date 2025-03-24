from django.db import models

class Dock(models.Model):
    """
    碼頭模型，用來存放各出貨碼頭的位置、名稱與當前載重狀況
    """
    name = models.CharField(max_length=100, unique=True)
    location_x = models.FloatField(help_text="X 軸座標")
    location_y = models.FloatField(help_text="Y 軸座標")
    current_load = models.IntegerField(default=0, help_text="當前載重")
    max_capacity = models.IntegerField(help_text="最大載重容量")

    def __str__(self):
        return self.name

class Robot(models.Model):
    """
    機器人模型，用來記錄機器人當前位置、狀態等資訊
    """
    identifier = models.CharField(max_length=50, unique=True)
    current_x = models.FloatField(help_text="當前 X 座標")
    current_y = models.FloatField(help_text="當前 Y 座標")
    is_active = models.BooleanField(default=True, help_text="是否啟動中")

    def __str__(self):
        return self.identifier

class LogisticsData(models.Model):
    """
    歷史運送資料模型，用來儲存運送記錄以便後續統計與 AI 分析
    """
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    dock = models.ForeignKey(Dock, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    route_taken = models.TextField(help_text="機器人運送路徑紀錄（例如：座標序列）")
    load_delivered = models.IntegerField(help_text="送貨量")

    def __str__(self):
        dock_name = self.dock.name if self.dock is not None else "Warehouse"
        return f"{self.robot.identifier} -> {dock_name} @ {self.timestamp}"


class Warehouse(models.Model):
    """
    倉庫模型，獨立於 Dock，用來記錄倉庫位置（固定為 (0,0)）
    與待運送貨物數量
    """
    location_x = models.FloatField(default=0, help_text="倉庫 X 軸座標")
    location_y = models.FloatField(default=0, help_text="倉庫 Y 軸座標")
    pending_cargo = models.IntegerField(default=0, help_text="待運送貨物數量")

    def __str__(self):
        return "Warehouse"
