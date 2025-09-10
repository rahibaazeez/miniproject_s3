from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.http import HttpResponse
from datetime import date
from django.core.mail import send_mail
import uuid
reset_links = {}


def create_admin(request):
    if not Login.objects.filter(username="admin@gmail.com").exists():
        Login.objects.create(
            username="admin@gmail.com",
            password=make_password("admin"),
            role="admin"
        )
    return HttpResponse("Admin user created or already exists.")
def loginview(request):
    return render(request, "login.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login   # Import your custom login model

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Login

def login_page(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")   # matches your form
        password = request.POST.get("password")

        # debug log (check your runserver console)
        print("LOGIN DEBUG -> username:", username, " password:", password, " role:", role)

        if not (username and password and role):
            messages.error(request, "Please enter username, password and select role.")
            return render(request, "login.html")

        try:
            user = Login.objects.get(username=username, role=role)
            print("LOGIN DEBUG -> found user:", user.username, " db-password:", user.password[:50] + "...")
        except Login.DoesNotExist:
            messages.error(request, "User not found for given role.")
            return render(request, "login.html")

        # Accept correct hashed password (preferred). Also allow legacy plain-text temporarily.
        if check_password(password, user.password) or password == user.password:
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role
            if user.role == "admin":
                return redirect("admin_home")
            else:
                return redirect("employeehome_page")
        else:
            messages.error(request, "Invalid password.")
            return render(request, "login.html")

    # GET -> show login form
    return render(request, "login.html")

def home_page(request):
    return render(request, 'home.html')


def admin_home(request):
    return render(request, "admin/admin_home.html")


def registration_page(request):
    return render(request, 'employee/registration.html')


def reset_password(request, uid):
    if uid not in reset_links:
        messages.error(request, "Invalid or expired reset link.")
        return redirect("forgot_password")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "reset_pass.html")

        emp_id = reset_links[uid]
        emp = Register.objects.get(id=emp_id)
        login = emp.login  
        login.password = make_password(password)
        login.save()

        del reset_links[uid]

        messages.success(request, "Password reset successful. Please login.")
        return redirect("login_page")

    return render(request, "reset_pass.html")


def employeehome_page(request):
    return render(request, 'employee/employee_home.html')

def event_add(request):
    return render(request, 'admin/add_event.html')

def register_employee(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')  # email will also be username
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        aadhaar_number = request.POST.get('aadhaar_number')
        password = request.POST.get('password')

        photo = request.FILES.get('photo')
        aadhaar_file = request.FILES.get('aadhaar_file')

        # ✅ Check first
        if Login.objects.filter(username=email).exists():
            messages.error(request, "This email is already registered. Please use another one.")
            return redirect("register_employee")

        # ✅ Then create login object
        login_obj = Login.objects.create(
            username=email,  
            password=make_password(password),
            role="employee"
        )

        # ✅ Create employee profile linked with login
        Register.objects.create(
            full_name=full_name,
            dob=dob,
            email=email,
            phone=phone,
            gender=gender,
            aadhaar_number=aadhaar_number,
            aadhaar_file=aadhaar_file,
            photo=photo,
            login=login_obj
        )

        messages.success(request, "Registration successful.")
        return redirect('loginview')

    return render(request, 'employee/registration.html')


    

def add_event(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)
        event_name = request.POST.get("event_name")   # matches form
        category = request.POST.get("eventCategory")  # corrected
        place_type = request.POST.get("eventPlace")   # corrected
        event_date = request.POST.get("eventDate")    # corrected
        event_time = request.POST.get("eventTime")    # corrected
        salary = request.POST.get("salary")           # matches form
        location = request.POST.get("eventLocation")
        vacancies = request.POST.get("vacancy")  
         # corrected
        # Save directly to DB
        Event.objects.create(
            event_name=event_name,
            category=category,
            place_type=place_type,
            event_date=event_date,
            event_time=event_time,
            salary=salary,
            location=location,
            vacancy=vacancies,
        )

        return redirect("exm")  # after saving go to list page

    return render(request, "admin/add_event.html")


def exm(request):
    events = Event.objects.all() 
    return render(request, "admin/exm.html", {"events": events})

def person_names(request):
    people = Register.objects.all()
    return render(request, "admin/personname_list.html", {"people": people})


def person_details(request, pk):
    person = Register.objects.get(id=pk)
    return render(request, "admin/persondetails_list.html", {"person": person})

def employee_event_details(request):
    events = Event.objects.all()
    today = date.today()

    for event in events:
        if event.event_date >= today:
            event.status = "Upcoming"
        else:
            event.status = "Completed"

    return render(request, "employee/eventview.html", {"events": events})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Appointment, Register

def apply_event(request, event_id):
    # 🔹 Check if user is logged in
    login_id = request.session.get("user_id")
    if not login_id:
        messages.error(request, "Please login first!")
        return redirect("login_page")

    # 🔹 Get employee and event objects
    employee = get_object_or_404(Register, login__id=login_id)
    event = get_object_or_404(Event, id=event_id)

    # 🔹 Check if employee has already applied for this event
    if Appointment.objects.filter(employee=employee, event=event).exists():
        messages.warning(request, "You have already applied for this event.")
        return redirect("employee_event_details")

    # 🔹 Check if employee has an event on the same date
    if Appointment.objects.filter(employee=employee, event__event_date=event.event_date).exists():
        messages.error(request, "You already have another event on this date.")
        return redirect("employee_event_details")

    # 🔹 Apply for the event
    Appointment.objects.create(employee=employee, event=event, status="Applied")
    messages.success(request, "Application submitted successfully!")

    return redirect("employee_event_details")


def respond_appointment(request, appointment_id, action):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    event = appointment.event

    if action not in ["Confirmed", "Declined"]:
        messages.error(request, "Invalid action.")
        return redirect("applied_persons")

    # if confirmed -> reduce vacancy
    if action == "Confirmed":
        if event.vacancy > 0:
            event.vacancy -= 1
            event.save()

            appointment.status = "Confirmed"
            appointment.save()

            # send confirmation mail
            subject = "Event Confirmation"
            message = f"""
            Hello {appointment.employee.full_name},

            You have been confirmed for the event:
            {event.event_name}
            Location: {event.location}
            Date: {event.event_date}

            Thank you!
            """
            recipient_list = [appointment.employee.email]

            try:
                send_mail(subject, message, None, recipient_list, fail_silently=False)
                messages.success(request, f"{appointment.employee.full_name} confirmed, vacancy updated, email sent!")
            except Exception as e:
                messages.warning(request, f"Confirmed & vacancy updated, but email failed: {e}")
        else:
            messages.error(request, "⚠️ No more vacancies available for this event.")

    elif action == "Declined":
        appointment.status = "Declined"
        appointment.save()

    # Send decline mail to employee
    subject = "Application Declined - Serve Smart"
    message = f"""
    Hello {appointment.employee.full_name},

    We regret to inform you that your application for the event has been declined.

    ❌ Event: {event.event_name}
    📅 Date: {event.event_date}
    📍 Location: {event.location}

    Please check other upcoming events and apply again.
    Thank you for your interest.
    """

    recipient_list = [appointment.employee.email]

    try:
        send_mail(subject, message, None, recipient_list, fail_silently=False)
        messages.success(request, f"{appointment.employee.full_name} has been declined and notified by email.")
    except Exception as e:
        messages.warning(request, f"{appointment.employee.full_name} declined, but email failed: {e}")

    return redirect("applied_persons")

def applied_persons(request):
    applied_list = Appointment.objects.select_related("employee", "event").all()
    return render(request, "admin/applied_persons.html", {"applied_list": applied_list})


def update_status(request, appointment_id, new_status):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = new_status
    appointment.save()
    return redirect("applied_persons")

def profile_view(request):
    login_id = request.session.get('user_id')
    print("Logged in user_id:", login_id)
    
    if login_id:
        try:
            login_user = Login.objects.get(id=login_id)
            user = Register.objects.get(login=login_user)
            return render(request, 'employee/profile.html', {'user': user})
        except (Login.DoesNotExist, Register.DoesNotExist):
            return redirect('loginview')
    else:
        return redirect('loginview')
    
def edit_profile(request):
    login_id = request.session.get('user_id')
    if not login_id:
        return redirect('loginview')

    login_user = get_object_or_404(Login, id=login_id)
    user = get_object_or_404(Register, login=login_user)

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.aadhaar_number = request.POST.get('aadhaar_number')
        user.gender = request.POST.get('gender')

        if request.FILES.get('photo'):
            user.photo = request.FILES.get('photo')
        if request.FILES.get('aadhaar_file'):
            user.aadhaar_file = request.FILES.get('aadhaar_file')

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'employee/edit_profile.html', {'user': user})


def employee_events(request):
    login_id = request.session.get("user_id")  
    if not login_id:
        return redirect("login_page")

    employee = get_object_or_404(Register, login_id=login_id)

    # 🔹 All applied events (regardless of confirmation)
    applied_events = Appointment.objects.filter(employee=employee).order_by('event__event_date')

    # 🔹 Only confirmed events
    confirmed_events = Appointment.objects.filter(employee=employee, status="Confirmed").order_by('event__event_date')
    declined_events = Appointment.objects.filter(
        employee=employee, status="Declined"
    ).order_by('event__event_date')


    context = {
        "applied_events": applied_events,
        "confirmed_events": confirmed_events,
        "declined_events": declined_events,
    }
    return render(request, "employee/appliedstatus.html", context)

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment

def decline_event(request, event_id):
    login_id = request.session.get("user_id")
    if not login_id:
        return redirect("login_page")

    # Find the confirmed appointment
    appointment = get_object_or_404(
        Appointment,
        employee__login_id=login_id,
        event_id=event_id,
        status="Confirmed"
    )

    # Update status to Can't Attend
    appointment.status = "Cant Attend"
    appointment.save()

    # Prepare email to admin
    subject = "Employee Can't Attend Event"
    message = (
        f"Hello Admin,\n\n"
        f"The following employee has declined a confirmed event:\n\n"
        f"👤 Employee: {appointment.employee.full_name}\n"
        f"📧 Email: {appointment.employee.email}\n"
        f"📞 Phone: {appointment.employee.phone}\n\n"
        f"❌ Declined Event:\n"
        f"📌 Event: {appointment.event.event_name}\n"
        f"📅 Date: {appointment.event.event_date}\n"
        f"📍 Location: {appointment.event.location}\n\n"
        f"Please assign another employee.\n\n"
        f"Regards,\nServeSmart System"
    )

    send_mail(subject, message, None, ["admin@gmail.com"], fail_silently=False)

    messages.success(request, "You declined this event. Admin has been notified.")
    return redirect("employee_events")

def not_attended_persons(request):
    """
    Display all employees who did not attend the events.
    """
    # Assuming 'status' field stores attendance status
    not_attended_list = Appointment.objects.filter(status='Cant Attend')
    
    context = {
        'not_attended_list': not_attended_list
    }
    return render(request, 'admin/notattended_persons.html', context)

def mark_attended(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Attended"
    appointment.save()
    return redirect('not_attended_persons')


def send_reminder(request, employee_id):
    employee = get_object_or_404(employee, id=employee_id)

    # Example mail sending
    send_mail(
        subject="Attendance Reminder",
        message="Dear {},\n\nThis is a reminder to attend your scheduled event.".format(employee.name),
        from_email="admin@example.com",
        recipient_list=[employee.email],
        fail_silently=False,
    )

    return redirect('not_attended_persons')
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    today = date.today()

    # ❌ block editing past events
    if event.event_date < today:
        messages.error(request, "⚠️ Past events cannot be edited.")
        return redirect("exm")

    if request.method == "POST":
        event.event_name = request.POST.get("event_name")
        event.category = request.POST.get("eventCategory")
        event.place_type = request.POST.get("eventPlace")
        event.event_date = request.POST.get("eventDate")
        event.event_time = request.POST.get("eventTime")
        event.salary = request.POST.get("salary")
        event.vacancy = request.POST.get("vacancy")
        event.location = request.POST.get("eventLocation")
        event.save()

        messages.success(request, "✅ Event updated successfully!")
        return redirect("exm")

    return render(request, "admin/edit_event.html", {"event": event})
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            emp = Register.objects.get(email=email)   # ✅ use Register model
            uid = str(uuid.uuid4())  # generate unique id
            reset_links[uid] = emp.id

            reset_url = request.build_absolute_uri(f"/reset_password/{uid}/")

            # send reset link to email
            send_mail(
                "Password Reset - Serve Smart",
                f"Click here to reset your password: {reset_url}",
                "admin@servesmart.com",  # change to your sender email
                [email],
                fail_silently=False,
            )
            messages.success(request, "Password reset link sent to your email.")
        except Register.DoesNotExist:
            messages.error(request, "This email is not registered.")
    return render(request, "employee/forgot_pass.html")