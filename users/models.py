from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	genre = models.CharField(max_length=100)
	language = models.CharField(max_length=50)
	duration = models.PositiveIntegerField(help_text='Duration in minutes')
	rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
	poster = models.ImageField(upload_to='posters/', blank=True)
	release_date = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return self.title


class Theatre(models.Model):
	name = models.CharField(max_length=150)
	location = models.CharField(max_length=150)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return f'{self.name} - {self.location}'


class Show(models.Model):
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
	theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='shows')
	date = models.DateField()
	time = models.TimeField()

	class Meta:
		ordering = ['date', 'time']

	def __str__(self):
		return f'{self.movie} at {self.theatre} on {self.date} {self.time}'


class Seat(models.Model):
	show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seats')
	number = models.CharField(max_length=5)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['show', 'number'], name='unique_seat_per_show')]
		ordering = ['number']

	def __str__(self):
		return self.number


class Booking(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
	show = models.ForeignKey(Show, on_delete=models.PROTECT, related_name='bookings')
	seats = models.ManyToManyField(Seat, related_name='bookings')
	booked_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, default='confirmed')

	class Meta:
		ordering = ['-booked_at']

	def __str__(self):
		return f'Booking #{self.pk} by {self.user}'

# Create your models here.
