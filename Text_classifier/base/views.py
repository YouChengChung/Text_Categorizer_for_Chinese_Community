from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages #login時的error message
from django.contrib.auth.decorators import login_required #用@控制必須login

# Create your views here.

# def home(request):
#     return render (request,"base/home.html")


def classify_text(request):
    if request.method == 'POST':
        # 從表單中取得輸入的文字
        text_input = request.POST.get('text_input', '')

        # 假設這裡是你的文本分類模型，返回文字類別
        # 這裡使用的是假想的分類函式 classify_text_function
        # result = classify_text_function(text_input)
        result = text_input

        # 將結果傳遞回模板中顯示
        context = {
            'result':result
        }
        return render(request, 'base/home.html', context)

    # 如果是 GET 請求，顯示空的表單
    return render(request, 'base/home.html')
