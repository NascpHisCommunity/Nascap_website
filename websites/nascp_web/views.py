# myproject/views.py
from django.shortcuts import render

def spa_view(request):
    return render(request, 'index.html')

def vision_mission_mandate(request):
    return render(request, "vision_mission_mandate.html")

def nascp_brief(request):
    return render(request, "nascp_brief.html")