from django.shortcuts import render
from django.http import HttpResponseRedirect
# Register your models here.
from .models import FoodType, Restaurant, Review 
from django.views import generic
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from reviews.forms import ReviewForm

# Main index page for the reviews app
def index(request):
    return render(request, 'reviews/index2.html')
    
# The list of restaurants (restaurant_list.html)
class RestaurantListView(generic.ListView):
    model = Restaurant

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