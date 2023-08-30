from django.shortcuts import render

def line_list(request):
    return render(request,'line_list.html')