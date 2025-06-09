import re
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class RouteType(models.TextChoices):
    PARA_TODOS = 'Para-Todos'
    SENDERISMO = 'Senderismo'
    CICLISMO = 'Ciclismo'
    TRAIL_RUNNING = 'Trail-Running'
    ALPINISMO = 'Alpinismo'

class RouteDifficulty(models.TextChoices):
    FACIL = 'Fácil'
    MODERADA = 'Moderada'
    DIFICIL = 'Difícil'

class RouteOrigin(models.TextChoices):
    STRAVA = 'Strava'
    WIKILOC = 'Wikiloc'
    OUTDOORACTIVE = 'OutdoorActive'
    ALLTRAILS = 'AllTrails'
    KOMOOT = 'Komoot'

class User(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300 ,unique=True, blank=True)
    type = models.CharField(max_length=20, choices=RouteType.choices)
    description = models.TextField(max_length=3000 ,blank=True, null=True)
    img = ArrayField(models.TextField(), blank=True, null=True)  
    difficulty = models.CharField(max_length=20, choices=RouteDifficulty.choices)
    duration = models.FloatField(blank=True, null=True)  
    distance = models.FloatField(blank=True, null=True)  
    origin = models.CharField(max_length=20, choices=RouteOrigin.choices)
    gpx_file = models.TextField(blank=True, null=True)
    start_latitude = models.FloatField(blank=True, null=True)
    start_longitude = models.FloatField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class RouteRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    rating = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)

class RouteComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class ForoThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            clean_title = re.sub(r'[^\w\s-]', '', self.title)
            self.slug = slugify(clean_title)
        super().save(*args, **kwargs)

class ForoComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForoThread, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'route')
