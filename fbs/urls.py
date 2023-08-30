"""
URL configuration for fbs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import admin, account, chart, bug, line
from django.urls import path

urlpatterns = [
    #path('admin/', admin.site.urls),
    
    # 用户的管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    #数据统计
    path("chart/list/",chart.chart_list),
    path("chart/bar/",chart.chart_bar),
    path("chart/pie/",chart.chart_pie),
    path("chart/line/",chart.chart_line),
    path("line/list/",line.line_list),

    #故障检测
    path("bug/list/",bug.bug_list),
    path("bug/download/",bug.bug_download)
]
