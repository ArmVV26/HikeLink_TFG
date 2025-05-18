from hikelink_app.models import User, Route, RouteRating, RouteComments, ForoThread, ForoComment, Favorites

# Descripciones de las Rutas
descriptionR1 = """La ruta circular desde el Canal de la Espartera hasta el pico Trevenque combina historia rural, paisajes volcánicos y espectaculares vistas de Sierra Nevada. A lo largo del camino se atraviesan antiguos cortijos, refugios de montaña y fuentes naturales antes de culminar en una de las cimas más icónicas de la baja montaña granadina.

1. **Canal de la Espartera**: Punto de inicio bien señalizado y accesible desde Cumbres Verdes. Zona de pinares y senderos anchos al comienzo.  
2. **Cortijo de Rosales (5,8 km)**: Ruinas de una antigua finca agrícola rodeadas de vegetación autóctona. Buen lugar para tomar un respiro.  
3. **Refugio Rosales (6,4 km)**: Refugio de uso libre, protegido por árboles. Ideal para protegerse del sol o del viento momentáneamente.  
4. **Fuente Aguas Blanquillas (7,6 km)**: Manantial de agua natural. Punto clave para recargar cantimploras y descansar antes de la subida.  
5. **Pico Trevenque (8,7 km)**: Tramo final más técnico, con pendiente fuerte y terreno de arenas volcánicas. Desde la cima, vistas panorámicas del Parque Nacional y del Veleta.  
6. **Mirador del Trevenque (11,6 km)**: En el camino de regreso, ofrece una excelente perspectiva del pico y la cuenca del río Dílar. Perfecto para hacer fotos.
"""

# Usuarios
u1 = User.objects.create_user(username='Admin', email='admin@admin.com', password='1234', full_name='admin', profile_picture='Admin.jpg', bio='Soy Admin')
u2 = User.objects.create_user(username='ArmVV26', email='ditovaquero@gmail.com', password='1234', full_name='Armando Vaquero Vargas', profile_picture='ArmVV26.jpg', bio='Amante de la naturaleza')
u3 = User.objects.create_user(username='AnaCamina', email='anahike1998@gmail.com', password='1234', full_name='Ana Garcia Gomez', profile_picture='AnaCamina.jpg', bio='Exploradora de rutas')
u4 = User.objects.create_user(username='Jose', email='jose1991@gmail.com', password='1234', full_name='Jose Jose Jose', profile_picture='Jose.jpg', bio='Jose')

# Rutas
r1 = Route.objects.create(
    user=u2,
    title='Canal de la Espartera - Trevenque',
    type='Senderismo',
    description=descriptionR1,
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg'],
    difficulty='Difícil',
    duration=23880,
    distance=16510,
    origin='Wikiloc',
    gpx_file='canal-de-la-espartera-trevenque.gpx',
    start_latitude=37.082825,
    start_longitude=-3.524126
)

r2 = Route.objects.create(
    user=u2,
    title='Circular Refugio Tello Lanjarón',
    type='Senderismo',
    description='Ruta circular con salida desde Lanjarón...',
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg'],
    difficulty='Difícil',
    duration=17040,
    distance=14720,
    origin='Strava',
    gpx_file='circular-refugio-tello-lanjaron.gpx',
    start_latitude=36.921465,
    start_longitude=-3.471082
)

r3 = Route.objects.create(
    user=u2,
    title='Cruz de Alfacar - Cruz de Viznar - Cueva del Agua',
    type='Senderismo',
    description='Ruta lineal que conecta dos icónicas cruces serranas...',
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg'],
    difficulty='Fácil',
    duration=10860,
    distance=8520,
    origin='OutdoorActive',
    gpx_file='cruz-de-alfacar-cruz-de-viznar-cueva-del-agua.gpx',
    start_latitude=37.258907,
    start_longitude=-3.549653
)

r4 = Route.objects.create(
    user=u2,
    title='Guejar Sierra - Sendero del Tranvia',
    type='Senderismo',
    description='Ruta lineal que recorre la conocida "Ruta del Tranvia..."',
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg'],
    difficulty='Fácil',
    duration=12600,
    distance=13530,
    origin='AllTrails',
    gpx_file='guejar-sierra-sendero-del-tranvia.gpx',
    start_latitude=37.158132,
    start_longitude=-3.442760
)

r5 = Route.objects.create(
    user=u2,
    title='Ruta Vereda de la Estrella',
    type='Senderismo',
    description='Una de las rutas mas emblemáticas de Sierra Nevada...',
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg', '6_img.jpg'],
    difficulty='Difícl',
    duration=30240,
    distance=23800,
    origin='Komoot',
    gpx_file='ruta-vereda-de-la-estrella.gpx',
    start_latitude=37.13443,
    start_longitude=-3.39193
)

# Valoraciones
RouteRating.objects.create(user=u3, route=r1, rating=5)
RouteRating.objects.create(user=u3, route=r2, rating=4)
RouteRating.objects.create(user=u3, route=r3, rating=3.5)
RouteRating.objects.create(user=u3, route=r4, rating=5)
RouteRating.objects.create(user=u3, route=r5, rating=2.5)

# Comentarios de rutas
RouteComments.objects.create(user=u3, route=r1, content='Impresionante pero dura. ¡Recomiendo llevar bastones!')
RouteComments.objects.create(user=u4, route=r1, content='Ruta espectacular, pero hay que venir preparado. La subida al mirador se hace dura, aunque las vistas desde arriba lo compensan con creces. Muy recomendable para quienes buscan un reto')
RouteComments.objects.create(user=u3, route=r2, content='Muy bonita y accesible para todos.')

# Hilos del foro
thread1 = ForoThread.objects.create(user=u1, title='Lista básica de equipamiento para rutas de nivel medio',
                                    content='Estoy ayudando a unos amigos...')
thread2 = ForoThread.objects.create(user=u2, title='Animales peligrosos en rutas por Sierra Nevada',
                                    content='¡Buenas! El otro día me crucé con una cabra montesa...')

# Comentarios del foro
ForoComment.objects.create(user=u1, thread=thread2, content='Hola no hay animales peligrosos.')
ForoComment.objects.create(user=u2, thread=thread1, content='Hey si o no.')

# Favoritos
Favorites.objects.create(user=u2, route=r1)
Favorites.objects.create(user=u2, route=r2)