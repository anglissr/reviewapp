from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Register your models here.
from .models import Contact_us, Restaurant, Review, Tag
from django.views import generic
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from reviews.forms import ReviewForm, SignUpForm, showForm
from django.db.models import Q # new
#For defining views requiring the user to be logged in. use @login_required above def to do so
from django.contrib.auth.decorators import login_required 
# For signup
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.shortcuts import render, redirect
# For Pass reset
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
import sys



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

# Lets user change pass
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            #messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        #else:
            #messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "reviews/registration/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("main:homepage")
	password_reset_form = PasswordResetForm()
    # TemplateDoesNotExist error (idk why, the html file is in the template folder)
	return render(request=request, template_name="reviews/registration/password_reset.html", context={"password_reset_form":password_reset_form})

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
    #print(Restaurant.objects.get(name='El Gato and Quesadillas').get_tags())
    #print(Restaurant.objects.filter(tag=(Tag.objects.filter(name="Tacos"))))
    print(Restaurant.objects.get(name='El Gato and Quesadillas').get_tags())
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
            if Tag.objects.filter(name__icontains=query_name).exists():
                results = Restaurant.objects.filter(Q(name__icontains=query_name) | Q(tag=(Tag.objects.get(name__icontains=query_name).id)))
            else:
                results = Restaurant.objects.filter(Q(name__icontains=query_name))
            return render(request, 'reviews/restaurant_search.html', {"results":results, "query":query_name})
        else:
            results = Restaurant.objects.all()
            return render(request, 'reviews/restaurant_search.html', {"results":results})


# The details of a single restaurant (restaurant_details.html)
def RestaurantDetails(request, restaurant_id):
    restaurantObj = get_object_or_404(Restaurant, pk=restaurant_id)
    reviews = Review.objects.filter(resturaunt=restaurantObj).order_by('-date')
    # If the form was submitted
    if request.method == 'POST' and 'submit1' in request.POST:
        print(request.POST, file=sys.stderr)

        # Create a form instance and populate it with data from the request (binding):
        form = ReviewForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            review = form.save(commit=False)

            #Set username as default anonymous else use their First name + Last initial
            if request.user.is_authenticated:
                review.username = request.user.first_name + " " + request.user.last_name[0] + "."
                review.user = request.user
            else:
                review.username = 'Anonymous'

            review.text = form.cleaned_data['text']
            review.rating = form.cleaned_data['rating']
            review.resturaunt = restaurantObj
            review.save()

            # redirect to a new URL:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if request.method == 'POST' and 'btnform2' in request.POST:
        print(request.POST, file=sys.stderr)
        form2 = showForm(request.POST)
        form = ReviewForm()
        if form2.is_valid():
            display = form2.cleaned_data['display']
            print(display, file=sys.stderr)
            if display == '1':
                print("here", file=sys.stderr)
                reviews = Review.objects.filter(resturaunt=restaurantObj).order_by('rating')
                context = {
                    'form': form,
                    'restaurant': restaurantObj,
                    'reviews': reviews,
                    'form2': form2 
                }

                return render(request, 'reviews/restaurant_details.html', context=context)                
            elif display == '2':
                reviews = Review.objects.filter(resturaunt=restaurantObj).order_by('-rating')
                context = {
                    'form': form,
                    'restaurant': restaurantObj,
                    'reviews': reviews,
                    'form2': form2 
                }
                return render(request, 'reviews/restaurant_details.html', context=context)
            elif display == '3':
                reviews = Review.objects.filter(resturaunt=restaurantObj).order_by('date')
                context = {
                    'form': form,
                    'restaurant': restaurantObj,
                    'reviews': reviews,
                    'form2': form2 
                }
                return render(request, 'reviews/restaurant_details.html', context=context)
            else:
                reviews = Review.objects.filter(resturaunt=restaurantObj).order_by('-date')
                context = {
                    'form': form,
                    'restaurant': restaurantObj,
                    'reviews': reviews,
                    'form2': form2 
                }
                
                return render(request, 'reviews/restaurant_details.html', context=context)    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
        form = ReviewForm()
        form2 = showForm()
       
    context = {
        'form': form,
        'restaurant': restaurantObj,
        'reviews': reviews,
        'form2': form2 
    }

    return render(request, 'reviews/restaurant_details.html', context=context)