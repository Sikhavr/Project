from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')
def userhome(request):
    return render(request,'userhome.html')
def driverhome(request):
    return render(request,'driverhome.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')

        if email and pwd:
            check_user = usersignup.objects.filter(email=email, password=pwd)

            if check_user:
                request.session['usersignup'] = email
                return redirect('userhome')
            else:
                msg = "Wrong Username or password!"
                return render(request, 'userlogin.html', {'msg': msg})
        else:
            msg = "Please provide both email and password!"
            return render(request, 'userlogin.html', {'msg': msg})

    return render(request, 'userlogin.html')


def driver_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        check_user = driversignup.objects.filter(email=email, password=pwd)
        if check_user:
            request.session['driversignup'] = email
            return redirect('driverhome')
        else:
            msg = "Wrong Username or password!"
            return render(request, 'driverlogin.html', {'msg': msg})
    return render(request,'driverlogin.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if all fields are filled in
        if username and email and password:
            client = usersignup(username=username, email=email, password=password)
            client.save()
            return redirect('user_login')
        else:
            error_msg = "Please fill in all required fields"
            return render(request, 'user_reg.html', {'error_msg': error_msg})

    return render(request, 'user_reg.html')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')




from django.contrib import messages

@login_required(login_url='admin_login')
def admin_dashboard(request):
    complaints = complaint_register.objects.all()
    drivers = driversignup.objects.all()

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        driver_id = request.POST.get('driver_id')
        message = request.POST.get('message')

        # Save the message to the database
        driver = driversignup.objects.get(id=driver_id)
        complaint = complaint_register.objects.get(id=complaint_id)
        driver_message = DriverMessage(driver=driver, complaint=complaint, message=message)
        driver_message.save()

        messages.success(request, 'Message sent successfully.')  # Add success message

        # Redirect or display a success message

    return render(request, 'admin_dashboard.html', {'complaints': complaints, 'drivers': drivers})

from .models import DriverMessage

def driver_messages(request):
    driver = request.user  # Assuming the driver is authenticated and the user model represents the driver
    messages = DriverMessage.objects.filter(driver=driver)
    return render(request, 'driver_messages.html', {'messages': messages})




def driver_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if all fields are filled in
        if username and email and password:
            client = driversignup(username=username, email=email, password=password)
            client.save()
            return redirect('driver_login')
        else:
            error_msg = "Please fill in all required fields"
            return render(request, 'driver_reg.html', {'error_msg': error_msg})

    return render(request, 'driver_reg.html')

def dustbin_table(request):
    dustbins = dustbin.objects.all()
    return render(request, 'dustbin.html', {'dustbins': dustbins})

def save_dailywaste(request):
    if request.method == 'POST':
        place = request.POST.get('place')
        route = request.POST.get('route')
        name = request.POST.get('name')
        plastic_waste = request.POST.get('plastic_waste')
        food_waste = request.POST.get('food_waste')

        # Create a new instance of the DailyWaste model
        daily_waste = dailywaste(
            place=place,
            route=route,
            name=name,
            plastic_waste=plastic_waste,
            food_waste=food_waste
        )
        daily_waste.save()  # Save the data to the model

        return HttpResponse('success')  # Redirect to a success page

    return render(request, 'dailywaste.html')

from django.shortcuts import render, redirect

def dailywaste_table(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        wastes = dailywaste.objects.filter(place=location)
        if wastes:
            context = {'dailywastes': wastes}
            return render(request, 'dailywaste_table.html', context)
        else:
            error_message = 'The details not found'
            return render(request, 'dailywaste_table.html', {'error_message': error_message})
    return render(request, 'driver_location.html')


def driver_location(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        # Perform any additional processing with the location data
        # For example, you can save it to a model or perform some business logic

        return redirect('dailywaste_table')  # Redirect to a success page

    return render(request, 'driver_location.html')


def user_complaint(request):
    if request.method == 'POST':
        name = request.POST['name']
        place = request.POST['place']
        date = request.POST['date']
        complaint = request.POST['complaint']

        complaint_entry = complaint_register(name=name, place=place, date=date, complaint=complaint)
        complaint_entry.save()

        return redirect('complaint_success')  # Redirect to a success page

    return render(request, 'complaint_register.html')

def complaint_success(request):
    return render(request, 'complaint_success.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import DriverMessage


@login_required
def driver_home(request):
    # Retrieve the driver's messages
    driver_messages = DriverMessage.objects.all()
    return render(request, 'driver_home.html', {'driver_messages': driver_messages})





from datetime import datetime
from django.shortcuts import render
from .models import complaint_register

def compliant_search(request):
    search_results = []

    if request.method == 'GET':
        place = request.GET.get('place')
        date_str = request.GET.get('date')


        try:
            # Convert the date string to the desired format (YYYY-MM-DD HH:MM)
            date = datetime.strptime(date_str, '%B %d, %Y, %I:%M %p').strftime('%Y-%m-%d %H:%M')

            if place and date:
                search_results = complaint_register.objects.filter(place=place,date=date)
        except ValueError:
            # Handle the case where the date string is not in the expected format
            return HttpResponse("invalid")

    context = {'search_results': search_results}
    return render(request, 'complaint_result.html', context)
def admin_home(request):
    return render(request,'admin_home.html')

def driversignup_list(request):
    drivers = driversignup.objects.all()
    context = {'drivers': drivers}
    return render(request, 'driversignup_list.html', context)

def user_list(request):
    users = usersignup.objects.all()
    context = {'users': users}
    return render(request, 'user_list.html', context)

from django.shortcuts import render, redirect
from .models import Complaint

def update_status(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        place = request.POST['place']
        status = request.POST['status']

        complaint = Complaint(name=name, date=date, place=place, status=status)
        complaint.save()

        return HttpResponse('status updated')  # Replace 'complaint_list' with your desired URL name for the complaint list page

    return render(request, 'update_status.html')

def view_complaint_status(request):
    if request.method == 'POST':
        name = request.POST['name']
        place = request.POST['place']

        complaints = Complaint.objects.filter(name=name, place=place)

        if complaints.exists():
            return render(request, 'complaint_status.html', {'complaints': complaints})
        else:
            return render(request, 'complaint_status.html', {'error': 'No complaints found.'})

    return render(request, 'view_complaint_status.html')
