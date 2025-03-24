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
    Home page view, providing links to various feature pages.
    """
    context = {}
    return render(request, 'logistics/index.html', context)

@login_required
def dashboard(request):
    """
    Dashboard view, displaying the current load of each dock and historical delivery data.
    Access is restricted to logged-in users. Historical delivery data is obtained by querying
    the LogisticsData model, and the accumulated delivery amount for each Dock is calculated.
    
    Parameters:
        request (HttpRequest): HTTP request object.
    
    Returns:
        HttpResponse: The rendered dashboard page.
    """
    docks = Dock.objects.all()
    
    # Statistics for accumulated delivery amount for each dock
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
    View for registering a new account, using Django's built-in UserCreationForm.
    If registration is successful, automatically logs in and redirects to the dashboard.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Automatically log in the user
            login(request, user)
            # Redirect to the dashboard page
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def cost_comparison(request):
    """
    Displays the cost comparison page (Bar Chart).
    Calculates the original and optimized path costs based on logistics data and passes them to the template.
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("No robot data available yet, please generate data first.")
    
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
    Displays the cumulative cost change page (Line Chart).
    Calculates the cumulative cost data for original and optimized paths and passes them to the template.
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("No robot data available yet, please generate data first.")
    
    # Get all logistics data, sorted by timestamp
    records = LogisticsData.objects.filter(robot=robot).order_by('timestamp')
    original_cum = []
    cumulative = 0
    for record in records:
        start, end = parse_route(record.route_taken)
        if start and end:
            d = euclidean_distance(start, end)
            cumulative += d
            original_cum.append(round(cumulative, 2))
    
    # Get optimized delivery results, flatten multiple trips' segments
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
    Displays the robot movement trajectory animation page (Scatter Chart animation).
    Prepares coordinate data for original and optimized paths for frontend animation display.
    """
    robot = Robot.objects.first()
    if not robot:
        return HttpResponse("No robot data available yet, please generate data first.")
    
    # Prepare original path coordinate data (sorted by timestamp)
    records = LogisticsData.objects.filter(robot=robot).order_by('timestamp')
    original_coords = [{'x': robot.current_x, 'y': robot.current_y}]
    for record in records:
        start, end = parse_route(record.route_taken)
        if end:
            original_coords.append({'x': end[0], 'y': end[1]})
    
    # Prepare optimized path coordinate data
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
