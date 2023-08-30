from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd

def chart_list(request):
    return render(request,'chart_list.html')

def chart_bar(request):
    #计算训练集中各种故障类型的数量
    l_0,l_1,l_2,l_3,l_4,l_5 = 0,0,0,0,0,0
    data = pd.read_csv('./app/dataset/train_in_use.csv',sep=',',usecols=[108]).values[0::][0::]
    for i in range(0,len(data)):
        if data[i][0]==0:
            l_0+=1
        elif data[i][0]==1:
            l_1+=1
        elif data[i][0]==2:
            l_2+=1
        elif data[i][0]==3:
            l_3+=1
        elif data[i][0]==4:
            l_4+=1
        else:
            l_5+=1
    legend=['此类型故障累计数']
    series_list = [
                    {
                        "name":'此类型故障累计数',
                        "type":'bar',
                        "data":[l_0,l_1,l_2,l_3,l_4,l_5]
                    },
                ]
    x_axis = ['0','1','2','3','4','5']
    result = {
        "status":True,
        "data":{
            'legend':legend,
            'series':series_list,
            'x_axis':x_axis
        }
    }
    return JsonResponse(result)

def chart_pie(request):
    #计算训练集中各种故障类型的数量
    l_0,l_1,l_2,l_3,l_4,l_5 = 0,0,0,0,0,0
    data = pd.read_csv('./app/dataset/train_in_use.csv',sep=',',usecols=[108]).values[0::][0::]
    for i in range(0,len(data)):
        if data[i][0]==0:
            l_0+=1
        elif data[i][0]==1:
            l_1+=1
        elif data[i][0]==2:
            l_2+=1
        elif data[i][0]==3:
            l_3+=1
        elif data[i][0]==4:
            l_4+=1
        else:
            l_5+=1
    db_data_list = [
        { "value": l_0, "name": '0' },
        { 'value': l_1, 'name': '1' },
        { 'value': l_2, 'name': '2' },
        {'value':l_3,'name':'3'},
        {'value':l_4,'name':'4'},
        {'value':l_5,'name':'5'},
    ]
    result = {
        "status":True,
        "data":db_data_list
    }
    return JsonResponse(result)

def chart_line(request):
    series_list = [
                    {
                        "name":'测试的macro_f1得分',
                        "type":'line',
                        "stack":"Total",
                        "data":[]
                    }
                ]
    if len(request.session["macro_f1"])>=6:
        array=[
            request.session["macro_f1"][5],
            request.session["macro_f1"][4],
            request.session["macro_f1"][3],
            request.session["macro_f1"][2],
            request.session["macro_f1"][1],
            request.session["macro_f1"][0],
        ]
        series_list[0]["data"]=array
    legend=['测试的macro_f1得分']
    x_axis = ['最近六次','最近五次','最近四次','最近三次','最近二次','最近一次']
    result = {
        "status":True,
        "data":{
            'legend':legend,
            'series':series_list,
            'x_axis':x_axis
        }
    }
    return JsonResponse(result)