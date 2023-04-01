from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import requests
from . import spoonacular
# Create your views here.

def search_recipes(request):
    query = request.GET.get('query')
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': '8eca12a5acfe4b7d91fe5a6cb93fd52f',
        'ingredients': query,
        'number': 10  # Return 10 recipes
    }
    response = requests.get(url, params=params)
    recipes = response.json()
    return render(request, 'search_results.html', {'recipes': recipes})



def home(request):
    return render(request, 'home.html')
# def search(request):
#     if 'ingredient' in request.GET:
#         ingredient = request.GET['ingredient']
#         url = f'https://api.spoonacular.com/recipes/complexSearch?query={ingredient}&includeNutrition=true&apiKey=<8eca12a5acfe4b7d91fe5a6cb93fd52f>'
#         response = requests.get(url)
#         data = response.json()
#     else:
#         data = None

#     context = {
#         'data': data,
#         'request': request,
#     }
#     return render(request, 'search.html', context)

# def search(request):
#     if 'query' in request.GET:
#         query = request.GET['query']
#         api_key = '8eca12a5acfe4b7d91fe5a6cb93fd52f'
#         url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={query}&apiKey={api_key}'
#         response = requests.get(url)
#         data = response.json()

#         context = {'data': data}
#         return render(request, 'search.html', context)

#     return render(request, 'search.html')
# def get_recipes(request):
#     api_key = '8eca12a5acfe4b7d91fe5a6cb93fd52f'
#     url = 'https://api.spoonacular.com/recipes/?apiKey=' + api_key
#     response = requests.get(url)
#     data = response.json()
#     return render(request, 'recipes.html', {'data': data})
# def get_recipes(request):
#     api_key = '8eca12a5acfe4b7d91fe5a6cb93fd52f'
#     ingredient = request.GET.get('ingredient', '')
#     ingredients = ingredient.split(',')
#     ingredients_str = '%2C'.join(ingredients)
#     url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={ingredients_str}&addRecipeInformation=true&fillIngredients=true'
#     response = requests.get(url)
#     data = response.json()
#     return render(request, 'recipes.html', {'data': data})

# def get_recipes(request):
#     api_key = '8eca12a5acfe4b7d91fe5a6cb93fd52f'
#     if 'ingredient' in request.GET:
#         ingredient = request.GET['ingredient']
#         url = f'https://api.spoonacular.com/recipes/complexSearch?query={ingredient}&includeNutrition=true&apiKey=<8eca12a5acfe4b7d91fe5a6cb93fd52f>'
#         response = requests.get(url)
#         data = response.json()
#     else:
#         data = None

#     context = {
#         'data': data,
#         'request': request,
#     }
#     return render(request, 'recipes.html', context)
# def password_reset_request(request):
#     if request.method == 'POST':
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             data = password_form.cleaned_data['email']
#             user_email = User.objects.filter(Q(email=data))
#             if user_email.exists():
#                 for user in user_email:
#                     subject = 'Password Resquest'
#                     email_template_name = 'password_reset_email.html'
#                     parameters = {
#                         'email': user.email,
#                         'domain': '127.0.0.1:8000',
#                         'site_name': 'Freshsave',
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',

#                     }
#                     email = render_to_string(email_template_name, parameters)
#                     try:
#                         send_mail(subject, email, '', [user.email], fail_silently=False)
#                     except:
#                         return HttpResponse('Invalid Header')
#                     return redirect('password_reset_done')

#     else:
#         password_form = PasswordResetForm()
#     context = {
#         'password_form': password_form,
    
#     }
#     return render(request, 'password_reset_form.html', context)

@login_required(login_url="/signup")
def loginhome(request):
    now = datetime.datetime.now()
    date_string = now.strftime("%m/%d/%y, %A")
    context = {'date_string': date_string}
    return render(request, 'lhome.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'signup.html', {'error':'*Username already been taken'})
        except User.DoesNotExist:
            User.objects.create_user(username=username, password=password, email=email, )
            return redirect('login')
        # User.objects.create_user(username=username, password=password, email=email )
        # return redirect('login')
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('loginhome')
        else:
            return render(request, 'login.html', {'error':'*Username or password is not correct.'})

    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')