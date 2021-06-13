from .forms import MyForm, NameForm, NameForm2
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import paged,pgparam
import os
from spellchecker import SpellChecker
# Create your views here.
# def index(request):
#     context = {
#         "variable" : "shrikant var"
#     }
#     return render(request,'index.html',context)

def index(request):

    if request.method == 'POST':
        form = MyForm(request.POST)
        nameof = request.POST.get('next10')
        if not ('next10' in request.POST):
            form = MyForm()
        else:
            print("IN NEXT 10 form else")
            # if form.is_valid():
            #     nextval = form.cleaned_data.get("next10")
            # print("VALUE OF VAL IS:"+nextval)
            x = pgparam.objects.latest('id')
            tagg = x.tag
            numm = x.num
            numm = numm+1
            endat = numm*10 +1
            startfrom = endat-10
            tempval = pgparam.objects.latest('id').tag
            if tempval:
                print("PREVIOUS TAG FOUND!: "+tempval)
            else:
                tempval = ""
            a = pgparam(tag = tagg, num = numm,startnum = startfrom,endnum = endat,prevtag = tempval,subfromtoday = 1,remainingarticles = 0,errcode = 945,loopcount = 0)
            a.save()
            i = 1  
            while True:  
                print("IN DO WHILE LOOP GOING "+str(i))
                pgvar = pgparam.objects.latest('id')
                pgvar.loopcount = i
                pgvar.save()
                os.system('python ../medcrawl/mcrawl/medium_spider.py')
                print("ERRORCODE:"+ str(pgparam.objects.latest('id').errcode))
                if(pgparam.objects.latest('id').errcode == 945):
                    spell = SpellChecker()
                    words = spell.candidates(tagg)
                    print(str(words))
                    if not words:
                        words = "something else"
                    else:
                        strt = ""
                        for ele in words:
                            if(ele == tagg):
                                strt = "something else.  "
                                break
                            strt = strt+ele+", "
                        strt = strt[:-2]
                        words = strt
                    msg = "Could Not Find Any Articles. Try "+str(words)
                    return render(request,'index.html',{'msg':msg})
                    break
                checkrem = pgparam.objects.latest('id').remainingarticles
                if checkrem == 0:
                    break
                i= i+1
            os.system('python ../medcrawl/mcrawl/page_spider.py')
            a = pgparam.objects.latest('id').relatedtags
            al = None
            if a :
                al = a.split(',')
                # al[0] = al[0][1:]
                for i in range(0,len(al)):
                    al[i] = al[i][2:-1]
                    print(al[i])
                al[len(al)-1] = al[len(al)-1][:-1]
            pgs = pgparam.objects.latest('id')
            st=paged.objects.all() # Collect all records from table
            if(st):
                enable = "enabled"
                return render(request,'index.html',{'st':st, 'al':al,'enable':enable, 'pgs':pgs})
            else:
                noarts = "No Articles Found!"
                return render(request,'index.html',{'st':st, 'al':al,'noarts':noarts})
            # return render(request,'index.html',{'st':st, 'al':al})

    else:
        form = MyForm()

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm2(request.POST)
        nameof = request.POST.get('inputtagname')
        if nameof:
            print("TAG TO SEARCH :"+nameof)
            tagg = nameof 
            numm = 1
            endat = numm*10 +1
            startfrom = endat-10
            tempval = None
            if(pgparam.objects.all()):
                tempval = pgparam.objects.latest('id').tag
            if tempval:
                print("PREVIOUS TAG FOUND!: "+tempval)
            else:
                tempval = ""
            a = pgparam(tag = tagg, num = numm,startnum = startfrom,endnum = endat,prevtag = tempval,subfromtoday = 1,remainingarticles = 0,errcode = 945,loopcount = 0)
            a.save()
            i = 1  
            while True:  
                print("IN DO WHILE LOOP GOING "+str(i))
                pgvar = pgparam.objects.latest('id')
                pgvar.loopcount = i
                pgvar.save()
                os.system('python ../medcrawl/mcrawl/medium_spider.py')
                print("ERRORCODE:"+ str(pgparam.objects.latest('id').errcode))
                if(pgparam.objects.latest('id').errcode == 945):
                    spell = SpellChecker()
                    words = spell.candidates(tagg)
                    print(str(words))
                    if not words:
                        words = "something else"
                    else:
                        strt = ""
                        for ele in words:
                            if(ele == tagg):
                                strt = "something else.  "
                                break
                            strt = strt+ele+", "
                        strt = strt[:-2]
                        words = strt
                    msg = "Could Not Find Any Articles. Try "+str(words)
                    return render(request,'index.html',{'msg':msg})
                    break
                checkrem = pgparam.objects.latest('id').remainingarticles
                if checkrem == 0:
                    break
                i= i+1
            os.system('python ../medcrawl/mcrawl/page_spider.py')
            a = pgparam.objects.latest('id').relatedtags
            al = None
            if a :
                al = a.split(',')
                # al[0] = al[0][1:]
                for i in range(0,len(al)):
                    al[i] = al[i][2:-1]
                    print(al[i])
                al[len(al)-1] = al[len(al)-1][:-1]
            pgs = pgparam.objects.latest('id')
            st=paged.objects.all() # Collect all records from table
            if(st):
                enable = "enabled"
                return render(request,'index.html',{'st':st, 'al':al,'enable':enable, 'pgs':pgs})
            else:
                noarts = "No Articles Found!"
                return render(request,'index.html',{'al':al,'noarts':noarts})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm2()

   

    return render(request,'index.html')

    st=pagedata.objects.all() # Collect all records from table 
    return render(request,'index.html',{'st':st})
def tagger(request):
    if request.method=='POST':
        return index(request)
    if request.method=='GET':
        newtag = request.GET.get('sts.bgtag')
        if not newtag:
            pass
        else:
            print("TAG TO SEARCH :"+newtag)
            tagg = newtag 
            numm = 1
            endat = numm*10 +1
            startfrom = endat-10
            tempval = None
            if(pgparam.objects.all()):
                tempval = pgparam.objects.latest('id').tag
            if tempval:
                print("PREVIOUS TAG FOUND!: "+tempval)
            else:
                tempval = ""
            a = pgparam(tag = tagg, num = numm,startnum = startfrom,endnum = endat,prevtag = tempval,subfromtoday = 1,remainingarticles = 0,errcode = 945,loopcount = 0)
            a.save()
            i = 1  
            while True:  
                print("IN DO WHILE LOOP GOING "+str(i))
                pgvar = pgparam.objects.latest('id')
                pgvar.loopcount = i
                pgvar.save()
                os.system('python ../medcrawl/mcrawl/medium_spider.py')
                print("ERRORCODE:"+ str(pgparam.objects.latest('id').errcode))
                if(pgparam.objects.latest('id').errcode == 945):
                    spell = SpellChecker()
                    words = spell.candidates(tagg)
                    print(str(words))
                    if not words:
                        words = "something else"
                    else:
                        strt = ""
                        for ele in words:
                            if(ele == tagg):
                                strt = "something else.  "
                                break
                            strt = strt+ele+", "
                        strt = strt[:-2]
                        words = strt
                    msg = "Could Not Find Any Articles. Try "+str(words)
                    return render(request,'index.html',{'msg':msg})
                    break
                checkrem = pgparam.objects.latest('id').remainingarticles
                if checkrem == 0:
                    break
                i= i+1
            os.system('python ../medcrawl/mcrawl/page_spider.py')
            a = pgparam.objects.latest('id').relatedtags
            al = None
            if a :
                al = a.split(',')
                # al[0] = al[0][1:]
                for i in range(0,len(al)):
                    al[i] = al[i][2:-1]
                    print(al[i])
                al[len(al)-1] = al[len(al)-1][:-1]
            pgs = pgparam.objects.latest('id')
            st=paged.objects.all() # Collect all records from table
            if(st):
                enable = "enabled"
                return render(request,'index.html',{'st':st, 'al':al,'enable':enable, 'pgs':pgs})
            else:
                noarts = "No Articles Found!"
                return render(request,'index.html',{'al':al,'noarts':noarts})
            
#  if request.method == 'POST':
#         form = NameForm(request.POST)
#         ameof = request.POST.get('reltag')
#         if not nameof:
#             form = NameForm()
#         else:
#             if form.is_valid():
#                 val = form.cleaned_data.get("reltag")
#                 print("VALUE OF VAL IS:"+val)
#                 # tagg = val
#                 # a = pgparam(tag = tagg, num = numm)
#                 # a.save()
#                 # os.system('python ../medcrawl/mcrawl/medium_spider.py')
#                 # os.system('python ../medcrawl/mcrawl/page_spider.py')
#     else:
#         form = NameForm()
