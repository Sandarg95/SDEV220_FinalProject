from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Log the user in after sign up
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('menu')
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# For customers: Show available food items
@login_required
def menu(request):
    food_items = FoodItem.objects.filter(available=True)
    return render(request, 'order/menu.html', {'food_items': food_items})

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated
    return menu(request)


# For customers: Place an order
@login_required
def place_order(request):
    if request.method == "POST":
        food_ids = request.POST.getlist('food_items')  
        order = Order.objects.create(customer=request.user)
        order.food_items.add(*food_ids)
        food_items = FoodItem.objects.filter(id__in=food_ids)
        return redirect('order_history')

    food_items = FoodItem.objects.filter(available=True)
    return render(request, 'order/place_order.html', {'food_items': food_items})

# For customers: View order history
@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'order/order_history.html', {'orders': orders})



# python manage.py runserver
