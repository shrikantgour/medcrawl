from django.shortcuts import render,HttpResponse
from .models import paged
# Create your views here.
def index(request):
    context = {
        "variable" : "shrikant var"
    }
    return render(request,'index.html',context)