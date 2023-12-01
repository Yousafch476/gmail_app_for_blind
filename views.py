import email
from http import server
from pyexpat.errors import messages
from re import sub
from telnetlib import STATUS
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
# Create your views here.
from .functions import SearchMail, isBlank,userExist,FetchMail,fetchLatest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib .auth .models import User
from .models import app_password
def reg(request):
    if not request.user.is_authenticated:
        return render(request,'reg.html')
    else:
        return render(request,'reg.html')
def wc(request):
    if not request.user.is_authenticated:
        return render(request,'wc.html')
    else:
        return render(request,'wc.html')
def index(request):
    if request.user.is_authenticated:
        return render(request,'main.html')
    else:
        return render(request,'login.html')
def home(request):
     if request.user.is_authenticated:
        return render(request,'main.html')
     else:
        return render(request,'login.html')

def composeEmailView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render (request,'compose.html')

def inboxView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render (request,'inbox.html')

def sentMAilVeiw(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render (request,'sent.html')

def TrashMailView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    return render (request,'trash.html')

def logoutView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
       logout(request)
       print('logout done')
    return render(request, 'login.html')
@api_view(['POST'])
def loginView(request):
        Messages=""
        data=None
        status_code=0
        
        if request.method=='POST':
              if "username" in request.data and "password" in request.data:
                     username=request.data["username"]
                     password=request.data["password"]

                     if not isBlank(username) and not isBlank(password):
                        user=userExist(username)
                        if user is not None:

                            auth=authenticate(username=username,password=password)
                            if auth is not None:
                                login(request,auth)
                                Messages="Sucess"
                                status_code=200
                            else:
                                Messages="wrong username or password"
                                status_code=500
                        else:
                            Messages="user not found"
                            status_code=505
        
        return JsonResponse({"Message":Messages,"status_code":status_code,"response":data})
  
@api_view(['POST'])
def ComposeView(request):
        Messages=""
        status_code=0
        if request.method=='POST':
              if "subject" in request.data and "to" in request.data and "message" in request.data:
                     subject=request.data["subject"]
                     to=request.data["to"]
                     msg=request.data["message"]
                     try:
                        user=app_password.objects.get(user=request.user)
                        customized_user=User.objects.get(username=to)
                        FROM_EMAIL = request.user.email 
                        FROM_PWD = user.password
                        print(FROM_EMAIL,FROM_PWD)
                        import imp
                        import smtplib
                        from email.message import EmailMessage
                        server=smtplib.SMTP('smtp.gmail.com',587)
                        server.starttls()
                        email=EmailMessage()
                        email['From']=FROM_EMAIL
                        email['To']=customized_user.email
                        email['subject']=subject
                        email.set_content(msg)

                        server.login(FROM_EMAIL,FROM_PWD)
                        server.send_message(email)
                        Messages="success"
                        status_code=200
                        print("sent")
                     except:
                        Messages="mail    not   sent"
                        status_code=500
                        print(Messages)
              else:
                    Messages="bad parameters"
                    status_code=0
        return JsonResponse({"Message":Messages,"status_code":status_code})

def ReadAllMail(request):
    if request.method=='POST':
        user=app_password.objects.get(user=request.user)
        FROM_EMAIL = request.user.email 
        FROM_PWD = user.password
        print(FROM_EMAIL,FROM_PWD)
        res=fetchLatest(FROM_EMAIL,FROM_PWD,'inbox')
        if res is not None:
            status_code=200
            messages="Success"
            print(res)
        else:
            res=[]
            status_code=500
            messages="Success"
        return JsonResponse({"Message":messages,"status_code":status_code,'data':res})

def ReadSentMail(request):
    if request.method=='POST': 
        user=app_password.objects.get(user=request.user)
        FROM_EMAIL = request.user.email 
        FROM_PWD = user.password
        print(FROM_EMAIL,FROM_PWD)
        
        res=fetchLatest(FROM_EMAIL,FROM_PWD,'Sent Mail')
        if res is not None:
            status_code=200
            messages="Success"
            print(res)
        else:
            res=[]
            status_code=500
            messages="Success"
        return JsonResponse({"Message":messages,"status_code":status_code,'data':res})

def ReadTrashedMail(request):
    if request.method=='POST': 
        user=app_password.objects.get(user=request.user)
        FROM_EMAIL = request.user.email 
        FROM_PWD = user.password
        print(FROM_EMAIL,FROM_PWD)

        res=fetchLatest(FROM_EMAIL,FROM_PWD,'Trash')
        if res is not None:
            status_code=200
            messages="Success"
        else:
            res=[]
            status_code=500
            messages="Success"
        return JsonResponse({"Message":messages,"status_code":status_code,'data':res})


@api_view(['POST'])
def findmail(request):
    if request.method=='POST':
        if "email" in request.data and "action" in request.data:
                     email=request.data["email"]
                     action=request.data["action"]
                     user=app_password.objects.get(user=request.user)
                     FROM_EMAIL = request.user.email 
                     FROM_PWD = user.password
                     print(FROM_EMAIL,FROM_PWD)
                     res=SearchMail(FROM_EMAIL,FROM_PWD,action,email)
                     if res is not None:
                        status_code=200
                        messages="Success"
                     else:
                        status_code=500
                        messages="Success"
    return JsonResponse({"Message":messages,"status_code":status_code,'data':res})
