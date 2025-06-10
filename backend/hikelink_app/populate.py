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

descriptionR2 = """La ruta circular Refugio Tello - Lanjarón es una de las más encantadoras de la Alpujarra granadina, combinando historia rural, paisajes de montaña y la frescura de las acequias tradicionales. Este recorrido ofrece una experiencia sensorial completa, ideal para los amantes del senderismo que buscan conectar con la naturaleza y la cultura local.

La ruta comienza en Lanjarón, ascendiendo por el Camino de la Sierra, una antigua vereda empedrada que serpentea entre castaños centenarios y ofrece vistas panorámicas del valle.

1. **Fuente Matemarques (2,4 km)**: Primera parada para refrescarse y disfrutar del entorno natural.
2. **Fuente de Matomarque (2,6 km)**: Otra fuente cercana que proporciona agua fresca, ideal para reponer fuerzas antes de continuar el ascenso.
3. **Cortijo Vadillo (3,4 km)**: Antiguo cortijo que testimonia la vida rural de la zona, rodeado de vegetación autóctona.
4. **Puente sobre el río Lanjarón (4,3 km)**: Cruzando este puente se accede a la margen derecha del río, donde el sonido del agua acompaña el caminar.
5. **Refugio Tello (4,7 km)**: Ubicado a aproximadamente 1.500 metros de altitud, este refugio forestal es un lugar perfecto para descansar y disfrutar de las vistas hacia el Cerro del Caballo y el Mediterráneo en días despejados.
6. **Fuente y Merendero Huerta Monjas (8,4 km)**: Área recreativa equipada con mesas y una fuente, ideal para hacer una pausa y disfrutar de un picnic en plena naturaleza.
7. **Estanque de la acequia (8,9 km)**: Pequeño estanque que forma parte del sistema de acequias tradicionales, reflejando la importancia del agua en la agricultura local.

El regreso a Lanjarón se realiza siguiendo la Acequia Nueva, un sendero que discurre paralelo a esta histórica canalización, ofreciendo vistas impresionantes del valle y la costa tropical.
"""

descriptionR3 = """La ruta Cruz de Alfacar - Cruz de Víznar - Cueva del Agua es un recorrido circular que transcurre por la Sierra de Huétor, en la provincia de Granada. Este itinerario combina paisajes naturales, puntos de interés histórico y vistas panorámicas, siendo ideal para senderistas que buscan una experiencia enriquecedora en contacto con la naturaleza.

La ruta comienza en el municipio de Alfacar, ascendiendo por senderos bien trazados hacia la Cruz de Alfacar, un punto elevado que ofrece vistas panorámicas de 360° de la Vega de Granada, Sierra Elvira y Sierra Nevada. 

Desde la Cruz de Alfacar, el camino continúa hacia el Collado de la Rata, un paso de montaña que conecta con la Cueva del Agua, una formación geológica ubicada en un entorno de roca caliza. Desde este punto, se pueden disfrutar de impresionantes vistas de la Sierra de Huétor y, en días despejados, de Sierra Nevada.

El recorrido prosigue hacia la Cruz de Víznar, otro punto elevado que ofrece vistas del entorno natural circundante. Desde allí, el sendero desciende de regreso a Alfacar, completando un circuito que combina ascensos y descensos moderados.
"""

descriptionR4 = """La ruta circular Güéjar Sierra - Sendero del Tranvía es un recorrido que combina historia, naturaleza y aventura. Siguiendo el antiguo trazado del tranvía que conectaba Granada con Sierra Nevada, este sendero ofrece paisajes espectaculares, puentes colgantes y la frescura del río Genil.

El recorrido comienza en el centro de Güéjar Sierra, descendiendo por el antiguo trazado del tranvía:

1. **Puente de la Fabriquilla (0,9 km)**: Primer punto de interés, un puente histórico que formaba parte del antiguo tranvía.
2. **Puente Colgante del Barranco de las Ánimas (5,3 km)**: Un puente colgante que ofrece vistas impresionantes del barranco y el río Genil.
3. **Puente sobre el río Genil (5,7 km)**: Cruzando el río Genil, este puente marca el punto de retorno hacia Güéjar Sierra.
"""

descriptionR5 = """La Ruta Vereda de la Estrella es uno de los itinerarios más emblemáticos y espectaculares de Sierra Nevada. Con un trazado que serpentea por la ladera norte del valle del Genil, este sendero ofrece vistas impresionantes de las cumbres más altas de la península ibérica, como el Mulhacén, la Alcazaba y el Veleta. Ideal para realizar en otoño o primavera, la ruta combina historia minera, paisajes de alta montaña y una rica biodiversidad.

El recorrido comienza en el Barranco de San Juan, accesible desde Güéjar Sierra, donde se encuentra un aparcamiento cercano al antiguo trazado del tranvía de Sierra Nevada.

1. **Inicio en el Barranco de San Juan**: El sendero comienza cruzando el río Genil por un puente de madera, adentrándose en un bosque de castaños y robles.
2. **El Abuelo**: A aproximadamente media hora de caminata, se encuentra un castaño centenario conocido como "El Abuelo", un punto emblemático para una breve parada.
3. **Cortijo de la Estrella**: Antiguo cortijo que da nombre al sendero, vinculado a las explotaciones mineras de galena y pirita del siglo XIX
4. **Confluencia de los ríos Guarnón y Real**: El sendero continúa hasta la unión de estos ríos, donde nace el río Genil.
5. **Refugio de Cueva Secreta**: Punto final habitual de la ruta lineal, situado a una altitud de aproximadamente 1.800 metros, ofreciendo vistas panorámicas de las cumbres nevadas.
"""

# Usuarios
u1 = User.objects.create_user(username='ArmVV26', email='armvv26@gmail.com', password='1234', full_name='Armando Vaquero Vargas', profile_picture='ArmVV26.jpg', bio='Amante de la naturaleza')
u2 = User.objects.create_user(username='AnaCamina', email='anahike1998@gmail.com', password='1234', full_name='Ana Garcia Gomez', profile_picture='AnaCamina.jpg', bio='Exploradora de rutas')
u3 = User.objects.create_user(username='Jose123', email='jose15101991@gmail.com', password='1234', full_name='Jose Jose Jose', profile_picture='Jose123.jpg', bio='Jose')

# Rutas
r1 = Route.objects.create(
    user=u1,
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
    user=u1,
    title='Circular Refugio Tello Lanjarón',
    type='Senderismo',
    description=descriptionR2,
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
    user=u1,
    title='Cruz de Alfacar - Cruz de Viznar - Cueva del Agua',
    type='Senderismo',
    description=descriptionR3,
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
    user=u1,
    title='Guejar Sierra - Sendero del Tranvia',
    type='Senderismo',
    description=descriptionR4,
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
    user=u1,
    title='Ruta Vereda de la Estrella',
    type='Senderismo',
    description=descriptionR5,
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg', '6_img.jpg'],
    difficulty='Difícil',
    duration=30240,
    distance=23800,
    origin='Komoot',
    gpx_file='ruta-vereda-de-la-estrella.gpx',
    start_latitude=37.13443,
    start_longitude=-3.39193
)

# Valoraciones
RouteRating.objects.create(user=u2, route=r1, rating=5)
RouteRating.objects.create(user=u2, route=r2, rating=4)
RouteRating.objects.create(user=u2, route=r3, rating=3.5)
RouteRating.objects.create(user=u2, route=r4, rating=5)
RouteRating.objects.create(user=u2, route=r5, rating=2.5)

# Comentarios de rutas
RouteComments.objects.create(user=u2, route=r1, content='Impresionante pero dura. ¡Recomiendo llevar bastones!')
RouteComments.objects.create(user=u3, route=r1, content='Ruta espectacular, pero hay que venir preparado. La subida al mirador se hace dura, aunque las vistas desde arriba lo compensan con creces. Muy recomendable para quienes buscan un reto')
RouteComments.objects.create(user=u2, route=r2, content='Muy bonita y accesible para todos.')

# Hilos del foro
thread1 = ForoThread.objects.create(user=u1, title='Lista básica de equipamiento para rutas de nivel medio',
                                    content='Estoy ayudando a unos amigos...')
thread2 = ForoThread.objects.create(user=u2, title='Animales peligrosos en rutas por Sierra Nevada',
                                    content='¡Buenas! El otro día me crucé con una cabra montesa...')

# Comentarios del foro
ForoComment.objects.create(user=u1, thread=thread2, content='Hola no hay animales peligrosos.')
ForoComment.objects.create(user=u2, thread=thread1, content='Hey si o no.')
ForoComment.objects.create(user=u2, thread=thread1, content='No lo se bro.')

# Favoritos
Favorites.objects.create(user=u2, route=r1)
Favorites.objects.create(user=u2, route=r2)