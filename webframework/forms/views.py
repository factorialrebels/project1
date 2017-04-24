from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import MealForm
from .forms import UserForm
# from .forms import ConfirmForm
from .forms import TripForm
from .forms import DailyExpensesForm
from .models import Meal
from .models import Trip
from .models import Post
from .models import DailyExpenses
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime


#TODO copy views from expenses
def register(request):
	# if this is a post request we need to process the form data

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# confirm = UserForm(request.POST)
		# check whether it's valid:

		if  form.is_valid():
			 # & confirm.is_valid()
			# save data as an instance in a database
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			# confirm_password = form.cleaned_data['confirm_password']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']


			user = User.objects.create_user(username, email, password,  first_name = first_name, last_name  = last_name)
			# save data as an instance in a database

			user.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/')
		else:
			return HttpResponse('oops youre stupid that username is already taken <a href="/forms/register/">Return</a>')

	else:
		# We'll create a blank form if we have a GET
		form = UserForm()
		# confirm = UserForm()
		return render(request, 'register.html', {'form': form})

@login_required(login_url='/')
def index(request):
	current_user = request.user;
	name = current_user.first_name;
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		recent = Post.objects.select_related('meal', 'dailyexpenses').all().order_by('-Added')[:3]
		return render(request, 'main.html', {'recent': recent, 'name' : name, 'active' : active})
	else:
		popuperror= 'True'
		trip = 'None'
		category = 'No Active Trip'
		na = 'N/A'
		return render(request, 'main.html', {'name' : name, 'trip': trip, 'category': category, 'na': na, 'popuperror': popuperror})




@login_required(login_url='/')
def addtrip(request):
	current_user = request.user;
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		# if this is a post request we need to process the form data
		return redirect('/forms/')
	else:
		if request.method == 'POST':

			# create a form instance and populate it with data from the request:
			form = TripForm(request.POST)
			# check whether it's valid:
			if form.is_valid():
				# save data as an instance in a database
				form.save()
				# reply with thank you, offer them a chance to enter again
				return redirect('/forms/trip/')
		else:
			# We'll create a blank form if we have a GET
			form = TripForm()
		return render(request, 'addtrip.html', {'form': form})

@login_required(login_url='/')
def trip(request):
	current_user = request.user
	if Trip.objects.filter(Is_Active = True, Username = current_user.id).exists():
		active = Trip.objects.get(Is_Active = True, Username = current_user.id)
		recent = Meal.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Meal_ID')[:3]
		recentexp = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-DailyExpense_ID')[:3]
		return render(request, 'trip.html', {'recent': recent, 'active': active, 'recentexp': recentexp})
	else:
		return redirect('/forms/')


@login_required(login_url='/')
def addexpense(request):
	# if not request.user.is_authenticated:
	# 	return redirect('/')
	return render(request, 'addexpenses.html', {})

@login_required(login_url='/')
def addmeal(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = MealForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
		else:
			return HttpResponse('nope')
	else:
		# We'll create a blank form if we have a GET
		form = MealForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = Meal.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'addmeal.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp})

@login_required(login_url='/')
def dailyexpenses(request):
	# if this is a post request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = DailyExpensesForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# save data as an instance in a database
			form.save()
			# reply with thank you, offer them a chance to enter again
			return redirect('/forms/trip/')
			# return HttpResponse('Thank you! <a href="/forms/trip/">Return</a>')
	else:
		# We'll create a blank form if we have a GET
		form = DailyExpensesForm()
		current_user = request.user
		active = Trip.objects.get(Is_Active = "True", Username=current_user.id)
		timestamp = DailyExpenses.objects.filter(Trip_ID_id = active.Trip_ID).order_by('-Added')
		return render(request, 'dailyexpenses.html', {'form': form, 'active': active.Trip_ID, 'timestamp': timestamp })


@login_required(login_url='/')
def triplist(request):
	current_user = request.user
	trips = Trip.objects.filter(Username = current_user.id).order_by('-Trip_ID')
	return render(request, 'triplist.html', {'trips': trips})


@login_required(login_url='/')
def finalconfirm(request):
	return render(request, 'finalconfirm.html', {})


def signout(request):
	logout(request)
	return redirect('/')

def finalize(request):
	current_user = request.user
	active = Trip.objects.get(Is_Active = True, Username = current_user.id)
	active.Is_Active = "False"
	active.save()
	return HttpResponse('Nice bro')
