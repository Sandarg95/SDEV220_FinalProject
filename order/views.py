from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FoodItem, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .templatetags.custom_filters import base64encode  
from django.utils import timezone

# Check if the user is an admin (is_staff attribute)
def is_admin(user):
    return user.is_staff

# For Admin: Show special menu
@user_passes_test(is_admin)
@login_required
def menu_admin(request):
    food_items = FoodItem.objects.filter(available=True)  
    return render(request, 'order/menu_admin.html', {'food_items': food_items})

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
    if request.user.is_staff:
        return redirect('menu_admin')
    return render(request, 'order/menu.html', {'food_items': food_items})

def login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated
    return menu(request)

# For customer: Place an order
@login_required
def place_order(request):
    if request.method == "POST":
        food_ids = request.POST.getlist('food_items')  
        if not food_ids:
            messages.error(request, "You must select at least one food item.")
            return redirect('menu')
        order = Order.objects.create(customer=request.user)
        order.food_items.add(*food_ids)
        return redirect('order_history')

# For admin: Place an order
@user_passes_test(is_admin)
@login_required
def place_order_admin(request):
    if request.method == "POST":
        food_ids = request.POST.getlist('food_items')  
        if not food_ids:
            messages.error(request, "You must select at least one food item.")
            return redirect('menu_admin')
        order = Order.objects.create(customer=request.user)
        order.food_items.add(*food_ids)
        return redirect('order_history_admin')

# For customers: View order history
@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'order/order_history.html', {'orders': orders})

# For admin: View order history
@user_passes_test(is_admin)
@login_required
def order_history_admin(request):
    orders = Order.objects.filter().order_by('-created_at')
    return render(request, 'order/order_history_admin.html', {'orders': orders})


def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)

        # Get the status from the form
        status = request.POST.get('status')
        
        # Validate the status before updating
        if status not in ['Pending', 'Processing', 'Completed', 'Canceled']:
            messages.error(request, "Invalid status update.")
            return redirect('order_history_admin')

        order.status = status
        order.save()
        messages.success(request, f"Order status {order_id} changed to {status}.")

        return redirect('order_history_admin')



@login_required
@user_passes_test(is_admin)
def update_food_item(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)

    # Handle GET request: display the form with the current food item data
    if request.method == 'GET':
        return render(request, 'order/update_food_item.html', {'food_item': food_item})

    # Handle POST request: update the food item
    elif request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        available = request.POST.get("available") == "on"  

        # Validate data before saving
        if not name or not price:
            messages.error(request, "Name and price are required.")
            return redirect('update_food_item', food_id=food_id)

        food_item.name = name
        food_item.price = price
        food_item.available = available
        food_item.save()

        messages.success(request, f"{food_item.name} has been updated successfully.")
        return redirect('menu_admin')  
 
@login_required
@user_passes_test(is_admin)   
def summary(request):
    # Get today's date
    today = timezone.now().date()

    # Get all orders data
    orders = Order.objects.all()
    
    # Get today's orders
    orders_today = Order.objects.filter(created_at__date=today)

    # Create a Pandas DataFrame for all orders
    data_all = {
        'Order ID': [order.id for order in orders],
        'Status': [order.status for order in orders],
        'Total Price': [order.total_price() for order in orders],
    }
    df_all = pd.DataFrame(data_all)

    # Generate the status summary for all orders (count of orders per status)
    status_summary_all = df_all['Status'].value_counts()

    # Create a plot for the bar chart (all orders)
    fig_all, ax_all = plt.subplots(figsize=(10, 6))  # Adjust size
    status_summary_all.plot(kind='bar', ax=ax_all, color='skyblue')
    ax_all.set_title('Order Status Summary (All Orders)')
    ax_all.set_xlabel('Status')
    ax_all.set_ylabel('Number of Orders')

    # Create a Pandas DataFrame for today's orders
    data_today = {
        'Order ID': [order.id for order in orders_today],
        'Status': [order.status for order in orders_today],
        'Total Price': [order.total_price() for order in orders_today],
    }
    df_today = pd.DataFrame(data_today)

    # Generate the status summary for today's orders
    status_summary_today = df_today['Status'].value_counts()

    # Create a pie chart for today's orders
    fig_today, ax_today = plt.subplots(figsize=(8, 8))  # Adjust size
    ax_today.pie(status_summary_today, labels=status_summary_today.index, autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'orange', 'lightcoral'])
    ax_today.set_title('Order Status Summary for Today')

    # Save the bar chart to a BytesIO object (all orders)
    buf_all = BytesIO()
    plt.figure(fig_all)
    plt.savefig(buf_all, format='png', bbox_inches='tight', dpi=300)
    buf_all.seek(0)

    # Save the pie chart to a BytesIO object (today's orders)
    buf_today = BytesIO()
    plt.figure(fig_today)
    plt.savefig(buf_today, format='png', bbox_inches='tight', dpi=300)
    buf_today.seek(0)

    # Convert both charts to base64
    plot_url_all = base64.b64encode(buf_all.getvalue()).decode('utf-8')
    plot_url_today = base64.b64encode(buf_today.getvalue()).decode('utf-8')

    # Pass both the status summaries and both plot URLs to the template
    return render(request, 'order/summary.html', {
        'status_summary_all': status_summary_all,
        'status_summary_today': status_summary_today,
        'plot_url_all': plot_url_all,
        'plot_url_today': plot_url_today
    })


# python manage.py runserver
