from .import views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('loginview/', views.loginview, name='loginview'),
    path('login_page/', views.login_page, name='login_page'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('event_add/', views.event_add, name='event_add'),
    path('add_event/', views.add_event, name='add_event'),
    path('registration_page/', views.registration_page, name='registration_page'),
    path('reset_password/<str:uid>/', views.reset_password, name='reset_password'),
    path('employeehome_page/', views.employeehome_page, name='employeehome_page'),
    path('register_employee/', views. register_employee, name='register_employee'),
    path('exm/', views. exm, name='exm'),
    path('personname_list/', views. register_employee, name='personname_list'),
    path("person_names/", views.person_names, name="person_names"),
    path("persondetails_list/", views.register_employee, name="persondetails_list"),
    path("person_details/<int:pk>/", views.person_details, name="person_details"),
    path("employee_event_details/", views.employee_event_details, name="employee_event_details"),
    path("apply_event/<int:event_id>/", views.apply_event, name="apply_event"),
    path("applied_persons/", views.applied_persons, name="applied_persons"),
    path("update_status/<int:appointment_id>/<str:new_status>/", views.update_status, name="update_status"),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('respond/<int:appointment_id>/<str:action>/', views.respond_appointment, name='respond_appointment'),
    path("employee_events/", views.employee_events, name="employee_events"),
    path("decline_event/<int:event_id>/", views.decline_event, name="decline_event"),
    path('not_attended/', views.not_attended_persons, name='not_attended_persons'),
    path("mark_attended/<int:appointment_id>/", views.mark_attended, name="mark_attended"),
    path("send_reminder/<int:employee_id>/", views.send_reminder, name="send_reminder"),
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send_urgent_email/<int:event_id>/', views.send_urgent_email, name='send_urgent_email'),
    path('mark_event_urgent/<int:event_id>/', views.mark_event_urgent, name='mark_event_urgent'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)