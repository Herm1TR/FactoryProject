"""
URL configuration for factory_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
這個模組定義了 factory_project 的 URL 路由配置。
包含了管理員、帳號認證、以及 logistics 應用的各種頁面路由。
"""

from django.contrib import admin
from django.urls import path, include
from logistics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('cost_comparison/', views.cost_comparison, name='cost_comparison'),
    path('cumulative_cost/', views.cumulative_cost, name='cumulative_cost'),
    path('trajectory_animation/', views.trajectory_animation, name='trajectory_animation'),
]
