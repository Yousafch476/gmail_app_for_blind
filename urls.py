from django.urls import path
from main_app import views
urlpatterns = [
    path('', views.wc, name='weclome'), 
    path('reg', views.reg, name='registration'),       
    #path('', views.index, name='login_interface'),
    path('login', views.index, name='login_interface'),
    path('auth', views.loginView, name='login'),
    path('sendmail', views.ComposeView, name='sendMail'),
    path('fetchmail', views.ReadAllMail, name='fetchMail'),
    path('FetchSentMail', views.ReadSentMail, name='FetchSentMail'),
    path('FetchTrashedMail', views.ReadTrashedMail, name='FetchTrashedMail'),
    path('findmail', views.findmail, name='findmail'),
    path('home', views.home, name='home'),
    path('compose', views.composeEmailView, name='compose'),
    path('inbox', views.inboxView, name='inbox'),
    path('sent', views.sentMAilVeiw, name='sent'),
    path('trash', views.TrashMailView, name='trash'),
    path('logout', views.logoutView, name='logout'),
   
] 