from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.users import (
    UserViewSet, FavoritesViewSet,
    update_user_profile, delete_account
)
from .views.routes import (
    RouteViewSet, RouteRatingViewSet, RouteCommentsViewSet,
    get_user_rating, get_routes_by_user, upload_route, update_route,
    delete_route, get_all_routes, filter_routes
)
from .views.forum import (
    ForoThreadViewSet, ForoCommentViewSet, get_all_threads,
    filter_threads, delete_thread
)
from .views.auth import (
    user_info, register_user, forgot_password, reset_password, validate_reset_token
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
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

    # USER
    # Ruta que llama a user_info para enviar los datos al Token del Login
    path('user/', user_info),

    # Ruta para personalizar el registro del usuario
    path('register/', register_user, name='register-user'),

     # Autenticacion y registro
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # RECOVER PASSWORD
    path('auth/forgot-password/', forgot_password, name='forgot-password'),
    path('auth/reset-password/', reset_password, name='reset-password'),
    path('auth/validate-reset/<str:uidb64>/<str:token>/', validate_reset_token, name='validate-reset-token'),

    # Ruta para actualizar un usuario
    path('profile/edit-profile/<int:user_id>/', update_user_profile, name='update-user-profile'),

    # Ruta para eliminar una cuenta
    path('delete-account/<int:user_id>/', delete_account, name='delete-account'),

    # Ruta para obtener el rating del usuario
    path('ratings/user/<int:route_id>/', get_user_rating, name='user-route-rating'),

    # ROUTES
    # Ruta para personalizar el registro de una ruta
    path('upload-route/', upload_route, name='upload-route'),

    # Ruta para personalizar el actualizar una ruta
    path('update-route/<int:route_id>/', update_route, name='update-route'),

    # Ruta para obtener solamente las rutas para un usuario
    path('routes/user/<int:user_id>/', get_routes_by_user, name='user-routes'),

    # Ruta para obtener todas las rutas
    path('all-routes/', get_all_routes, name='all_routes'),

    # Ruta para filtrar las rutas por parametros
    path('filter-routes/', filter_routes, name='filter_routes'),

    # Ruta para eliminar una ruta
    path('delete-route/<int:route_id>/', delete_route, name='delete-route'),

    # FORO
    # Ruta para obtener todos los hilos del foro
    path('all-threads/', get_all_threads, name='all_threads'),

    # Ruta para filtrar los hilos por titulo
    path('filter-threads/', filter_threads, name='filter_threads'),

    # Ruta para eliminar un hilo
    path('delete-thread/<int:thread_id>/', delete_thread, name='delete-filter'),
    
    # TOKENS
    # SimpleJWT - Endpoints para login con JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]