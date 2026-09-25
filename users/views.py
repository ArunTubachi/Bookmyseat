from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from .forms import UserRegisterForm, UserUpdateForm
from .models import Booking, Movie, Seat, Show


def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form=UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form=AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form, 'bookings': request.user.bookings.all()})

def home(request):
    return render(request, 'home.html', {'movies': Movie.objects.all()[:6]})


def movie_list(request):
    return render(request, 'movies/list.html', {'movies': Movie.objects.all()})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    shows = movie.shows.select_related('theatre').filter(date__gte=timezone.localdate())
    return render(request, 'movies/detail.html', {'movie': movie, 'shows': shows})


@login_required
def seat_selection(request, show_id):
    show = get_object_or_404(Show.objects.select_related('movie', 'theatre'), pk=show_id)
    seat_numbers = [f'{row}{number}' for row in 'ABCD' for number in range(1, 7)]
    for number in seat_numbers:
        Seat.objects.get_or_create(show=show, number=number)
    seats = list(show.seats.all())
    booked_ids = set(Seat.objects.filter(show=show, bookings__status='confirmed').values_list('id', flat=True))
    if request.method == 'POST':
        selected_ids = request.POST.getlist('seats')
        if not selected_ids:
            messages.error(request, 'Select at least one seat.')
        else:
            with transaction.atomic():
                selected = list(Seat.objects.select_for_update().filter(show=show, id__in=selected_ids))
                already_booked = Booking.objects.filter(seats__in=selected, status='confirmed').exists()
                if len(selected) != len(set(selected_ids)) or already_booked:
                    messages.error(request, 'One or more selected seats were just booked. Please choose again.')
                else:
                    booking = Booking.objects.create(user=request.user, show=show)
                    booking.seats.set(selected)
                    return redirect('booking_confirmation', booking_id=booking.id)
    return render(request, 'bookings/seats.html', {'show': show, 'seats': seats, 'booked_ids': booked_ids})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking.objects.select_related('show__movie', 'show__theatre').prefetch_related('seats'), pk=booking_id, user=request.user)
    return render(request, 'bookings/confirmation.html', {'booking': booking})