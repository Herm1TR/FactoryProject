from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Dock, LogisticsData, Robot
from .optimization import calculate_original_cost, calculate_optimized_route, parse_route, euclidean_distance
import json


def index(request):
    """
    首頁 view，提供連結到各個功能頁面。
    """
    context = {}
    return render(request, 'logistics/index.html', context)

@login_required
def dashboard(request):
    """
    Dashboard 視圖，展示各碼頭的當前載重與歷史運送數據
    僅限已登入使用者存取，透過查詢 LogisticsData 模型取得歷史運送資料，
    並計算每個 Dock 的累計送貨量。
    
    參數:
        request (HttpRequest): HTTP 請求物件。
    
    返回:
        HttpResponse: 渲染後的 dashboard 頁面。
    """
    docks = Dock.objects.all()
    
    # 統計每個碼頭累計送貨量
    dock_data = []
    for dock in docks:
        total_load = LogisticsData.objects.filter(dock=dock).aggregate(total=Sum('load_delivered'))['total'] or 0
        dock_data.append({
            'name': dock.name,
            'current_load': dock.current_load,
            'total_load': total_load,
        })

    context = {
        'dock_data': dock_data,
    }
    return render(request, 'logistics/dashboard.html', context)

def register(request):
    """
    註冊新帳號的視圖，使用 Django 內建的 UserCreationForm。
    若註冊成功，則自動登入並導向 dashboard。
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 儲存新使用者
            user = form.save()
            # 自動登入該使用者
            login(request, user)
            # 導向 dashboard 頁面
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def cost_comparison(request):
    """
    顯示成本比較頁面 (Bar Chart)。
    根據物流資料計算原始與最佳化路徑成本，並傳入模板。
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("尚無機器人資料，請先產生資料。")
    
    orig_cost, orig_routes = calculate_original_cost(robot)
    opt_cost, _ = calculate_optimized_route(robot)
    
    context = {
        'robot': robot,
        'orig_cost': orig_cost,
        'opt_cost': opt_cost,
    }
    return render(request, 'logistics/cost_comparison.html', context)

@login_required
def cumulative_cost(request):
    """
    顯示累積成本變化頁面 (Line Chart)。
    計算原始與最佳化路徑累積成本資料，傳入模板。
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("尚無機器人資料，請先產生資料。")
    
    # 取得所有物流資料，依 timestamp 排序
    records = LogisticsData.objects.filter(robot=robot).order_by('timestamp')
    original_cum = []
    cumulative = 0
    for record in records:
        start, end = parse_route(record.route_taken)
        if start and end:
            d = euclidean_distance(start, end)
            cumulative += d
            original_cum.append(round(cumulative, 2))
    
    # 取得最佳化運送結果，將多趟的 segments 扁平化
    _, opt_trips = calculate_optimized_route(robot)
    flat_segments = []
    for trip in opt_trips:
        flat_segments.extend(trip['segments'])
    
    optimized_cum = []
    cumulative_opt = 0
    for segment in flat_segments:
        cumulative_opt += segment['distance']
        optimized_cum.append(round(cumulative_opt, 2))
    
    context = {
        'robot': robot,
        'original_cum': original_cum,
        'optimized_cum': optimized_cum,
    }
    return render(request, 'logistics/cumulative_cost.html', context)

@login_required
def trajectory_animation(request):
    """
    顯示機器人移動軌跡動畫頁面 (Scatter Chart 動畫)。
    準備原始與最佳化路徑的座標資料，供前端動畫展示使用。
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("尚無機器人資料，請先產生資料。")
    
    # 準備原始路徑座標資料（依照 timestamp 排序）
    records = LogisticsData.objects.filter(robot=robot).order_by('timestamp')
    original_coords = [{'x': robot.current_x, 'y': robot.current_y}]
    for record in records:
        start, end = parse_route(record.route_taken)
        if end:
            original_coords.append({'x': end[0], 'y': end[1]})
    
    # 準備最佳化路徑座標資料
    _, opt_trips = calculate_optimized_route(robot)
    flat_segments = []
    for trip in opt_trips:
        flat_segments.extend(trip['segments'])
    optimized_coords = [{'x': robot.current_x, 'y': robot.current_y}]
    for segment in flat_segments:
        optimized_coords.append({'x': segment['to'][0], 'y': segment['to'][1]})
    
    context = {
        'robot': robot,
        'original_coords': json.dumps(original_coords),
        'optimized_coords': json.dumps(optimized_coords),
    }
    return render(request, 'logistics/trajectory_animation.html', context)