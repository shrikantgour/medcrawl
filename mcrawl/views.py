from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import paged,pgparam
import os
# Create your views here.
# def index(request):
#     context = {
#         "variable" : "shrikant var"
#     }
#     return render(request,'index.html',context)

def index(request):
    tagg = 'gaming'
    numm = 1
    a = pgparam(tag = tagg, num = numm)
    a.save()
    os.system('python ../medcrawl/mcrawl/medium_spider.py')
    os.system('python ../medcrawl/mcrawl/page_spider.py')
    a = pgparam.objects.latest('id').relatedtags
    al = a.split(',')
    for i in range(0,9):
        al[i] = al[i][2:-1]
        print(al[i])
    al[8] = al[8][:-1]
    st=paged.objects.all() # Collect all records from table
    return render(request,'index.html',{'st':st, 'al':al})
    # if request.method == 'POST' and 'run_script' in request.POST:
        
        # return HttpResponseRedirect(reverse(mcrawl:index)
    # return user to required page
    
    # os.system('python ../medcrawl/mcrawl/medium_spider.py')
    # os.system('python ../medcrawl/mcrawl/page_spider.py')
    st=pagedata.objects.all() # Collect all records from table 
    return render(request,'index.html',{'st':st})
def tagger(request):
    if request.method=='GET':
        newtag = request.GET.get('sts.bgtag')
        if not newtag:
            pass
        else:
            tagg = newtag
            numm = 1
            a = pgparam(tag = tagg, num = numm)
            a.save()
            os.system('python ../medcrawl/mcrawl/medium_spider.py')
            os.system('python ../medcrawl/mcrawl/page_spider.py')
            a = pgparam.objects.latest('id').relatedtags
            al = a.split(',')
            for i in range(0,9):
                al[i] = al[i][2:-1]
                print(al[i])
            al[8] = al[8][:-1]
            st=paged.objects.all() # Collect all records from table
            return render(request,'index.html',{'st':st, 'al':al})
            

