from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('manager/', views.manager_page, name='manager'),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),

    path('logout/', views.logout_, name='logout'),

    path('profile/<int:id>', views.profile, name='profile'),

    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('password_reset_success', views.password_reset_success, name='password_reset_success'),
    path('password_change/<uidb64>/<token>/', views.change_password, name='password_change'),
    
    path('location/', views.location, name='location'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('about_us/', views.about_us, name='about_us'),  # New path for About Us
    path('contact/', views.contact, name='contact'),

    path('generate_report/', views.generate_report, name='generate_report'),

    path('photographers/', views.photographers, name='photographers'),
    path('decorators/', views.decorators, name='decorators'),
    path('menu_bar/', views.menu_bar, name='menu_bar'),
    path('choreographers/', views.choreographers, name='choreographers'),
    path('designers/', views.designers, name='designers'),
    path('venue_planners/', views.venue_planners, name='venue_planners'),
    path('makeup_artists/', views.makeup_artists, name='makeup_artists'),
]