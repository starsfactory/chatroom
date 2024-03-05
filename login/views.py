from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from login.models import User


# Create your views here.

def go_login(request):
    print('welcome our web')
    return render(request, 'login.html')


def login(request):
    print('logining...')
    if request.method == 'GET':
        userName = request.GET.get('username')
        userPassword = request.GET.get('userpassword')
        print(userName, userPassword)
        user = User.objects.filter(name=userName).first()
        if user is not None and user.password == userPassword:
            print('set session', user.id)
            request.session['userid'] = user.id
            print("have find user")
            print(user.name)
            print(user.password)
            print('success!')
            return JsonResponse({'success': True, 'userid': user.id})
        else:
            print('None')
            return JsonResponse({'success': False})