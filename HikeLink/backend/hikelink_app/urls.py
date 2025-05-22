from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


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

    # Ruta que llama a user_info para enviar los datos al Token del Login
    path('user/', user_info),

    # Ruta para obtener el rating del usuario
    path('ratings/user/<int:route_id>/', get_user_rating, name='user-route-rating'),

    # Ruta para personalizar el registro del usuario
    path('register/', register_user, name='register-user'),

    # Ruta para personalizar el registro de una ruta
    path('upload-route/', upload_route, name='upload-route'),

    # Ruta para personalizar el actualizar una ruta
    path('update-route/<int:route_id>/', update_route, name='update-route'),

    # Ruta para obtener solamente las rutas para un usuario
    path('routes/user/<int:user_id>/', get_routes_by_user, name='user-routes'),

    # SimpleJWT - Endpoints para login con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Autenticacion y registro
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    # Ruta para actualizar un usuario
    path('profile/edit-profile/<int:user_id>/', update_user_profile, name='update-user-profile'),

    # Ruta para eliminar una ruta
    path('delete-route/<int:route_id>/', delete_route, name='delete-route'),
    
    # Ruta para eliminar una cuenta
    path('delete-account/<int:user_id>/', delete_account, name='delete-account'),
]