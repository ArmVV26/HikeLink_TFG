from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Registro de conjuntos de vistas REST para que Django genere el CRUD automaticamente
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'ratings', RouteRatingViewSet)
router.register(r'comments', RouteCommentsViewSet)
router.register(r'threads', ForoThreadViewSet)
router.register(r'foro-comments', ForoCommentViewSet)
router.register(r'favorites', FavoritesViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Ruta que llama a user_info para enviar los datos al Token del Login1
    path('user/', user_info),

    # Ruta para obtener el rating del usuario
    path('ratings/user/<int:route_id>/', get_user_rating, name='user-route-rating'),

    # Ruta para personalizar el registro del usuario
    path('register/', register_user, name='register-user'),

    # Ruta para personalizar el registro de una ruta
    path('upload-route/', upload_route, name='upload-route'),

    # Ruta para personalizar el actualizar una ruta
    path('update-route/<int:route_id>/', update_route, name='update-route'),
]
