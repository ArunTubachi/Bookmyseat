from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import booking_confirmation, home, login_view, movie_detail, movie_list, profile, register, seat_selection

urlpatterns = [
    path('', home, name='home'),
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:pk>/', movie_detail, name='movie_detail'),
    path('register/', register,name='register'),
    path('login/', login_view,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('shows/<int:show_id>/seats/', seat_selection, name='seat_selection'),
    path('bookings/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
]
