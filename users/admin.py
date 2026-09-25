from django.contrib import admin
from .models import Booking, Movie, Seat, Show, Theatre

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ('title', 'genre', 'language', 'rating')
	search_fields = ('title', 'genre')


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
	list_display = ('name', 'location')
	search_fields = ('name', 'location')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
	list_display = ('movie', 'theatre', 'date', 'time')
	list_filter = ('date', 'theatre')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
	list_display = ('show', 'number')
	list_filter = ('show',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'show', 'status', 'booked_at')
	list_filter = ('status', 'booked_at')
