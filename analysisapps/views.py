from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

email_master = 'sam.klump@outlook.com'
email_href = 'mailto:' + email_master
# test change
### HOME PAGE
@csrf_exempt
def home(request):
    return render(request, 'home.html', context={'email':email_master, 'email_link':email_href})

### ABOUT PAGE
@csrf_exempt
def about(request):
    return render(request, 'about.html', context={'email':email_master, 'email_link':email_href})
    
### POWER BI PAGE
def powerbi(request):
    return render(request, 'powerbi.html', context={'email':email_master, 'email_link':email_href})