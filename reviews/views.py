from django.shortcuts import render
from django.http import HttpResponseRedirect
# Register your models here.
from .models import Contact_us, Restaurant, Review 
from django.views import generic
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from reviews.forms import ReviewForm, SignUpForm
from django.db.models import Q # new
#For defining views requiring the user to be logged in. use @login_required above def to do so
from django.contrib.auth.decorators import login_required 
# For signup
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def Account(request):
    context = {}
    if request.user.is_authenticated:
        userReviews = Review.objects.filter(user=request.user)
        context = {
            'reviews': userReviews
        }
    return render(request, 'reviews/account.html', context)

def Logout(request):
    return render(request, 'reviews/logged_out.html')

def Login(request):
    return render(request, 'reviews/login.html')

def PassReset(request):
    return render(request, 'reviews/password_reset.html')

# Index page for creating an account. Sends user back to the account page
def Signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def Home(request):
    return render(request, 'reviews/home.html')

def About(request):
    return render(request,'reviews/about.html')

def Cafes(request):
    return render(request,'reviews/cafes.html')  

def Campus(request):
    return render(request,'reviews/campus.html')     

def Contact(request):
    if request.method == "POST":
        Contact = Contact_us()
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.name = name
        Contact.email = email
        Contact.message = message
        Contact.save()
        
    return render(request, 'reviews/contact.html')
    
# The list of restaurants (restaurant_list.html)
class RestaurantListView(generic.ListView):
    model = Restaurant

def RestaurantList(request):
    """View function for home page of site."""

    # Generate lists of different types of restaurants
    restaurants = Restaurant.objects.all()
    restaurantsRestaurant = Restaurant.objects.filter(style='Restaurant')
    restaurantsCafe = Restaurant.objects.filter(style='Café')
    restaurantsMarket = Restaurant.objects.filter(style='Market')
    

    context = {
        'restaurants': restaurants,
        'restaurantsRestaurant': restaurantsRestaurant,
        'restaurantsCafe': restaurantsCafe,
        'restaurantsMarket': restaurantsMarket,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'reviews/restaurant_list.html', context=context)

def RestaurantSearch(request):
    """View function for home page of site."""

    if request.method == "GET":
        query_name = request.GET.get('q', None)
        if query_name:
            if query_name.lower() == "cafe":
                query_name = "Café"
            results = Restaurant.objects.filter(
            Q(name__icontains=query_name) | Q(style__icontains=query_name)
            )
            return render(request, 'reviews/restaurant_search.html', {"results":results, "query":query_name})
        else:
            results = Restaurant.objects.all()
            return render(request, 'reviews/restaurant_search.html', {"results":results})


# The details of a single restaurant (restaurant_details.html)
def RestaurantDetails(request, restaurant_id):
    restaurantObj = get_object_or_404(Restaurant, pk=restaurant_id)
    reviews = Review.objects.filter(resturaunt=restaurantObj)

    # If the form was submitted
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ReviewForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            review = form.save(commit=False)

            #Set username as default anonymous else use their username
            if request.user.is_authenticated:
                review.username = request.user.username
                review.user = request.user
            else:
                review.username = 'Anonymous'

            review.text = form.cleaned_data['text']
            review.rating = form.cleaned_data['rating']
            review.resturaunt = restaurantObj
            review.save()

            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        form = ReviewForm()

       
    context = {
        'form': form,
        'restaurant': restaurantObj,
        'reviews': reviews, 
    }

    return render(request, 'reviews/restaurant_details.html', context=context)