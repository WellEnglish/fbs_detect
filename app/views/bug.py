from django.shortcuts import render
from app.utils.train import train, predict
from app.utils.pagination import Pagination
from app.models import outcome
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def bug_list(request):
    outcomes = {
        # "msg":"",
        # "train_accuracy": 1,
        # "predict_accuracy": 2,
        # "predict_f1": 3,
        # "result_dict": {"test":"test","test2":"test2"},
        # "page_string":1,
    }

    file_object = request.FILES.get("csv1")
    if file_object:
        #写入文件
        path = './app/dataset/train_in_use.csv'
        f = open(path,mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
        #训练模型
        train()
        outcomes = {
            "msg":"新模型已训练成功",
        }
        return render(request, "bug.html", outcomes)

    file_object = request.FILES.get("csv")
    if file_object:
        #写入文件
        path = './app/dataset/'+file_object.name
        f = open(path,mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
        
        #模型预测
        predict_accuracy,macro_f1,queryset = predict(path)
        #使用分页组件
        page_object = Pagination(request,queryset,page_size=3)
        
        temp = request.session['macro_f1']
        temp = temp.insert(0,macro_f1)
        request.session['predict_accuracy'] = predict_accuracy
        outcomes = {
            "predict_accuracy": predict_accuracy,
            "macro_f1": macro_f1,
            "queryset":page_object.page_queryset,
            "page_string":page_object.html(),
        }
    if request.GET.get("page"):
        page_object = Pagination(request,outcome.objects.all(),page_size=3)
        outcomes = {
            "predict_accuracy": request.session["predict_accuracy"],
            "macro_f1": request.session["macro_f1"][0],
            "queryset":page_object.page_queryset,
            "page_string":page_object.html(),
        }
    return render(request, "bug.html", outcomes)

def bug_download(request):
    file_path = './app/to_download/outcome.csv'
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404

