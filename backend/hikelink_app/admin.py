from django.contrib import admin
from .models import User, Route, RouteRating, RouteComments, ForoThread, ForoComment, Favorites

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'created_date', 'is_staff')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('created_date', 'is_staff', 'is_superuser')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'difficulty', 'distance', 'origin', 'created_date')
    search_fields = ('title', 'description', 'origin')
    list_filter = ('type', 'difficulty', 'origin', 'created_date')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('user',)


@admin.register(RouteRating)
class RouteRatingAdmin(admin.ModelAdmin):
    list_display = ('route', 'user', 'rating', 'created_date')
    list_filter = ('rating', 'created_date')
    autocomplete_fields = ('user', 'route')


@admin.register(RouteComments)
class RouteCommentsAdmin(admin.ModelAdmin):
    list_display = ('route', 'user', 'created_date')
    search_fields = ('content',)
    list_filter = ('created_date',)
    autocomplete_fields = ('user', 'route')


@admin.register(ForoThread)
class ForoThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_date')
    search_fields = ('title', 'content')
    list_filter = ('created_date',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('user',)


@admin.register(ForoComment)
class ForoCommentAdmin(admin.ModelAdmin):
    list_display = ('thread', 'user', 'created_date')
    search_fields = ('content',)
    list_filter = ('created_date',)
    autocomplete_fields = ('user', 'thread')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'route')
    autocomplete_fields = ('user', 'route')