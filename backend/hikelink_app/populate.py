import os
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

descriptionR6 = """La ruta del Río Dúrcal hasta la Cascada de los Bolos es una espectacular aventura acuática que combina senderismo tradicional con elementos de barranquismo suave. Esta ruta transcurre por uno de los ríos más salvajes del Parque Natural de Sierra Nevada, ofreciendo una experiencia refrescante y única a tan solo media hora de Granada capital.

El recorrido comienza en el área de Los Mondarinos, siguiendo el sendero local SL-A 236, que serpentea por el valle del río Dúrcal ofreciendo amplias y hermosas vistas del entorno montañoso.

1. **Área recreativa Los Mondarinos (0 km)**: Punto de inicio con aparcamiento y zona de descanso. Lugar ideal para preparar el equipo antes de adentrarse en el sendero acuático.
2. **Puente de Lata (1,2 km)**: Antiguo puente que cruza el río Dúrcal, punto donde comienza a intensificarse el carácter acuático de la ruta.
3. **Sendero Nico Molina (2,1 km)**: Tramo del sendero dedicado al deportista durqueño del Club de Montaña Cerro del Caballo, que discurre paralelo al río entre formaciones rocosas.
4. **Primera zona de pozas (3,5 km)**: Serie de pozas naturales perfectas para un primer chapuzón y descanso. El agua permanece fría durante todo el año.
5. **Garganta estrecha (4,2 km)**: El valle se estrecha considerablemente, creando un ambiente más íntimo y espectacular. Aquí comienza la parte más técnica de la ruta.
6. **Cascada de los Bolos (4,8 km)**: Impresionante salto de agua que forma pozas naturales rodeadas de rocas redondeadas que dan nombre al lugar. La cascada bloquea el paso río arriba, marcando el final natural de la ruta.

Durante el recorrido se alternan tramos de sendero tradicional con pasos por el propio cauce del río, requiriendo en ocasiones caminar por el agua o sobre las rocas pulidas por la corriente. Es recomendable llevar calzado específico para agua y una bolsa estanca para los objetos de valor.
"""

# Usuarios
u1 = User.objects.create_user(username='ArmVV26', email='armvv26@gmail.com', password=os.environ.get('DJANGO_PASSWORD_1'), full_name='Armando Vaquero Vargas', profile_picture='ArmVV26.jpg', bio='Amante de la naturaleza')
u2 = User.objects.create_user(username='AnaCamina', email='anahike1998@gmail.com', password=os.environ.get('DJANGO_PASSWORD_2'), full_name='Ana Garcia Gomez', profile_picture='AnaCamina.jpg', bio='Exploradora de rutas')
u3 = User.objects.create_user(username='JoseTravel', email='joseTravel1996@gmail.com', password=os.environ.get('DJANGO_PASSWORD_3'), full_name='Jose Manuel Perez Jose', profile_picture='JoseTravel.jpg', bio='En busca de un nuevo viaje')

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

r6 = Route.objects.create(
    user=u1,
    title='Rio Dúrcal - Cascada de los Bolos',
    type='Senderismo',
    description=descriptionR6,
    img=['1_img.jpg', '2_img.jpg', '3_img.jpg', '4_img.jpg', '5_img.jpg'],
    difficulty='Moderada',
    duration= 14400,
    distance=9950,
    origin='Wikiloc',
    gpx_file='rio-durcal-cascada-de-los-bolos.gpx',
    start_latitude=37.002232,
    start_longitude=-3.566983
)

# Valoraciones
# AnaCamina valora: r1, r2, r3, r4, r5
RouteRating.objects.create(user=u2, route=r1, rating=5)
RouteRating.objects.create(user=u2, route=r2, rating=4)
RouteRating.objects.create(user=u2, route=r3, rating=3.5)
RouteRating.objects.create(user=u2, route=r4, rating=5)
RouteRating.objects.create(user=u2, route=r5, rating=2.5)

# JoseTravel valora: r1, r3, r4, r5, r6
RouteRating.objects.create(user=u3, route=r1, rating=4.5)
RouteRating.objects.create(user=u3, route=r3, rating=4)
RouteRating.objects.create(user=u3, route=r4, rating=3.5)
RouteRating.objects.create(user=u3, route=r5, rating=4)
RouteRating.objects.create(user=u3, route=r6, rating=5)

# Comentarios de AnaCamina
RouteComments.objects.create(user=u2, route=r1, content='Impresionante pero dura. ¡Recomiendo llevar bastones! Las vistas desde el Trevenque son espectaculares.')
RouteComments.objects.create(user=u2, route=r2, content='Muy bonita y accesible. El refugio Tello es perfecto para descansar y las vistas al Mediterráneo son increíbles en días despejados.')
RouteComments.objects.create(user=u2, route=r3, content='Ruta tranquila y familiar. Perfecta para iniciarse en el senderismo. La Cueva del Agua es curiosa.')
RouteComments.objects.create(user=u2, route=r4, content='Me encantó seguir el trazado del antiguo tranvía. Los puentes colgantes son emocionantes.')
RouteComments.objects.create(user=u2, route=r5, content='Demasiado larga para mi nivel actual. Aunque "El Abuelo" es impresionante, no pude completar toda la ruta.')

# Comentarios de JoseTravel
RouteComments.objects.create(user=u3, route=r1, content='Ruta espectacular, pero hay que venir preparado. La subida al mirador se hace dura, aunque las vistas desde arriba lo compensan con creces. Muy recomendable para quienes buscan un reto.')
RouteComments.objects.create(user=u3, route=r3, content='Excelente para pasar el día en familia. Los paisajes de la Sierra de Huétor son preciosos.')
RouteComments.objects.create(user=u3, route=r4, content='La historia del tranvía hace muy interesante la ruta. Recomiendo informarse antes sobre su historia.')
RouteComments.objects.create(user=u3, route=r5, content='Una de las mejores rutas que he hecho en Sierra Nevada. El Cortijo de la Estrella tiene mucha historia.')
RouteComments.objects.create(user=u3, route=r6, content='¡Increíble experiencia acuática! La Cascada de los Bolos es impresionante. Llevar calzado adecuado para el agua es fundamental.')

# Comentarios de ArmVV26
RouteComments.objects.create(user=u1, route=r1, content='¡Muchas gracias por vuestros comentarios! Me alegra que hayáis disfrutado de la ruta tanto como yo. Efectivamente, los bastones son muy recomendables para la bajada.')
RouteComments.objects.create(user=u1, route=r5, content='Gracias Jose por tu valoración. Es cierto que tiene mucha historia minera, me alegra que te haya gustado conocerla.')
RouteComments.objects.create(user=u1, route=r6, content='¡Gracias Jose! Totalmente de acuerdo con lo del calzado, es fundamental para disfrutar de la experiencia acuática sin riesgos.')

# Hilos del foro
thread1 = ForoThread.objects.create(
    user=u1, 
    title='Lista básica de equipamiento para rutas de nivel medio',
    content='''Estoy ayudando a unos amigos que se quieren iniciar en el senderismo de montaña y me han pedido consejo sobre qué equipamiento necesitan para rutas de dificultad media. He pensado en hacer una lista básica pero completa para que no se olviden de nada esencial.

Por mi experiencia, creo que lo imprescindible sería:
- Botas de montaña con buen agarre
- Bastones telescópicos 
- Mochila de 25-30L
- Cantimplora o sistema de hidratación
- Ropa técnica transpirable
- Chubasquero
- Manta térmica
- Botiquín básico
- Linterna frontal
- Silbato

¿Qué opináis? ¿Añadiríais algo más o sobra algo de la lista? Quiero que vayan bien equipados pero sin cargar demasiado peso innecesario.'''
)

thread2 = ForoThread.objects.create(
    user=u2, 
    title='Encuentros con fauna en Sierra Nevada - Experiencias y consejos',
    content='''¡Buenas! El otro día haciendo la ruta de Vereda de la Estrella me crucé con una cabra montés que se quedó observándome un buen rato. Fue una experiencia increíble, pero me hizo pensar en qué otros animales podemos encontrar en nuestras rutas por Sierra Nevada y cómo debemos actuar.

He visto que hay jabalíes, zorros, jinetas y una gran variedad de aves. También leí que hay algunas víboras, aunque parece que son poco agresivas.

¿Habéis tenido encuentros interesantes con la fauna local? ¿Qué recomendaciones daríais para observar animales respetando su espacio? Me gustaría saber más sobre este tema para futuras rutas.'''
)

thread3 = ForoThread.objects.create(
    user=u3,
    title='Mejor época para hacer rutas en la Alpujarra',
    content='''Hola a todos. Estoy planeando un fin de semana largo para hacer varias rutas por la Alpujarra granadina y no tengo claro cuál es la mejor época del año. He oído que en verano hace mucho calor y en invierno puede haber nieve en las zonas altas.

Me interesan especialmente las rutas que pasen por los pueblos blancos y que tengan buen acceso a fuentes naturales. ¿Qué me recomendáis? ¿Primavera u otoño? ¿Hay algún mes en particular que sea ideal?

También me gustaría aprovechar para probar la gastronomía local, así que si conocéis buenos sitios para comer en los pueblos, ¡acepto sugerencias!'''
)

thread4 = ForoThread.objects.create(
    user=u1,
    title='Rutas accesibles con niños en Granada',
    content='''Mi hermana viene de visita con sus hijos (8 y 12 años) y me ha pedido si conozco rutas de senderismo aptas para hacer en familia. Buscan algo que no sea muy duro pero que sea bonito y entretenido para los niños.

He pensado en la ruta de Cruz de Alfacar o quizás algo por el río Dúrcal, pero no estoy seguro de si son adecuadas para esa edad. Los niños están acostumbrados a caminar pero no tienen experiencia en montaña.

¿Qué rutas recomendaríais para una primera experiencia de senderismo con niños? ¿Algún consejo específico para motivarlos durante la caminata?'''
)

thread5 = ForoThread.objects.create(
    user=u2,
    title='Apps y tecnología útil para senderismo',
    content='''Cada vez uso más el móvil para mis rutas de senderismo y me gustaría conocer qué aplicaciones y gadgets recomendáis para mejorar la experiencia.

Actualmente uso Wikiloc para seguir tracks GPS y está muy bien, pero he visto que hay muchas otras opciones. También he empezado a usar una pulsera con GPS para registrar mis rutas.

¿Qué apps usáis vosotros? ¿Merece la pena invertir en un GPS específico para montaña o con el móvil es suficiente? También me interesa saber sobre powerbanks, fundas impermeables y ese tipo de accesorios tecnológicos.'''
)

thread6 = ForoThread.objects.create(
    user=u3,
    title='Preparación física específica para rutas de alta montaña',
    content='''El próximo año tengo como objetivo hacer algunas rutas más exigentes en Sierra Nevada, incluyendo subir al Mulhacén. El tema es que aunque hago senderismo habitualmente, siento que me falta preparación física específica para rutas de más de 6-7 horas.

¿Qué tipo de entrenamiento recomendáis? ¿Es suficiente con hacer más rutas o debería complementar con gimnasio? He leído sobre entrenamientos específicos para montaña pero hay tanta información que no sé por dónde empezar.

También me interesa saber sobre la aclimatación a la altitud. ¿Cómo os preparáis vosotros para rutas de alta montaña?'''
)

# Comentarios del 1º Hilo
ForoComment.objects.create(user=u2, thread=thread1, content='¡Excelente lista! Yo añadiría unas gafas de sol y crema solar, especialmente para rutas de montaña donde el reflejo del sol es más intenso. También unas simples bridas de plástico pueden salvar el día si se rompe algo del equipo.')
ForoComment.objects.create(user=u3, thread=thread1, content='Totalmente de acuerdo con la lista. Para rutas de medio nivel yo también llevaría un mapa físico como backup del GPS del móvil. Y quizás una navaja multiusos pequeña, que siempre viene bien.')

# Comentarios del 2º Hilo
ForoComment.objects.create(user=u1, thread=thread2, content='¡Qué suerte con la cabra montés! Yo he tenido varios encuentros y siempre son especiales. Lo más importante es mantener la distancia y no hacer movimientos bruscos. He visto zorros y jinetas también, pero son más esquivos. Respecto a las víboras, son muy raras de ver y huyen antes que atacar.')
ForoComment.objects.create(user=u3, thread=thread2, content='Una vez vi un águila real en la Vereda de la Estrella, fue impresionante. Para la observación de fauna recomiendo llevar unos prismáticos pequeños y madrugar, al amanecer es cuando más actividad hay.')

# Comentarios del 3º Hilo
ForoComment.objects.create(user=u1, thread=thread3, content='Sin duda, abril-mayo y octubre-noviembre son las mejores épocas para la Alpujarra. Las temperaturas son perfectas y hay menos turistas. En primavera además tienes la ventaja de ver todo florido. Para comer, en Lanjarón hay varios sitios muy buenos.')
ForoComment.objects.create(user=u2, thread=thread3, content='Yo fui en octubre el año pasado y fue perfecto. Los colores del otoño en los castaños son espectaculares. Evita julio y agosto si puedes, el calor es realmente intenso durante el día.')

# Comentarios del 4º Hilo
ForoComment.objects.create(user=u2, thread=thread4, content='La ruta de Cruz de Alfacar es perfecta para niños! Es fácil, no muy larga y las vistas les van a encantar. También la del río Dúrcal es genial porque pueden jugar con el agua. Mi consejo: lleva snacks y haz paradas frecuentes para que no se aburran.')

# Comentarios del 5º Hilo
ForoComment.objects.create(user=u3, thread=thread5, content='Yo uso Komoot además de Wikiloc y me gusta mucho para planificar rutas. Para GPS específico, si haces muchas rutas merece la pena, la batería dura mucho más que el móvil. Un powerbank de 10000mAh es suficiente para rutas de un día.')

# Comentarios del 6º Hilo
ForoComment.objects.create(user=u1, thread=thread6, content='Para prepararme para rutas largas combino senderismo regular con ejercicios de cardio y fortalecimiento de piernas. Subir escaleras con mochila cargada también ayuda mucho. La clave está en la progresión gradual, no quieras hacerlo todo de golpe.')

# Favoritos de AnaCamina
Favorites.objects.create(user=u2, route=r1)
Favorites.objects.create(user=u2, route=r2)
Favorites.objects.create(user=u2, route=r4)

# Favoritos de JoseTravel
Favorites.objects.create(user=u3, route=r1)
Favorites.objects.create(user=u3, route=r3)

# Script para popular muchos datos en la base de datos
# def crear_rutas_masivas(base_user, base_description, cantidad=20):
#     for i in range(cantidad):
#         Route.objects.create(
#             user=base_user,
#             title=f'Ruta Vereda de la Estrella - Variante {i + 1}',
#             type='Senderismo',
#             description=base_description,
#             img=[
#                 '1_img.jpg', '2_img.jpg', '3_img.jpg',
#                 '4_img.jpg', '5_img.jpg', '6_img.jpg'
#             ],
#             difficulty='Difícil',
#             duration=30240 + i * 60,  # cada ruta tarda un poco mas
#             distance=23800 + i * 10,  # y recorre un poco mas
#             origin='Komoot',
#             gpx_file=f'vereda-estrella-variante-{i + 1}.gpx',
#             start_latitude=37.13443 + (i * 0.0001),
#             start_longitude=-3.39193 - (i * 0.0001)
#         )

# crear_rutas_masivas(u1, descriptionR5, cantidad=50)