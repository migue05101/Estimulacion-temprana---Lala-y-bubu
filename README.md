# Estimulación temprana Lala y Bubu

App de estimulación temprana para niños de 2 años en adelante, con los personajes de la serie **Lala y Bubu** (Lala, Juan, Lucía y Bubu) como guías. Funciona en celular, tablet y computador, en vertical y horizontal.

## Cómo abrirla

Es una app web de un solo archivo: `index.html` y sus imágenes y videos están en la misma carpeta.

- **En el computador:** sirve la carpeta con un servidor local (por ejemplo `python3 -m http.server`) y abre `http://localhost:8000`. Abrir el archivo con doble clic también funciona, pero algunos navegadores bloquean los videos así.
- **En línea:** se puede publicar tal cual con GitHub Pages (Settings → Pages → rama `main`, carpeta raíz).

## Estructura

| Archivos | Para qué |
|---|---|
| `index.html` | Toda la app: pantallas, 40 juegos, partículas, sonidos y panel de papás |
| `intro.mp4`, `intro-v.mp4` | Intro (horizontal y vertical con cámara que sigue a los niños) |
| `elegir-*.mp4/jpg` | Menú "¿Con quién quieres jugar?" con los cuatro personajes |
| `sel-<personaje>-*.mp4` | Celebración al elegir a cada personaje |
| `menu-<personaje>-*.mp4`, `mundo-<personaje>*.jpg` | Menú animado de actividades de cada personaje |
| `col-<personaje>-*.jpg`, `globo-*.webp` | Juego Globos de colores |
| `btn-*.webp`, `cara-*.webp`, `logo.webp` | Botones, caras de los personajes y logo |
| `menu-*`, `mundo.*`, `puzzle-*`, `colores.jpg` | Escenas usadas en rompecabezas y pantallas anteriores |

Los archivos terminados en `-v` son para pantalla vertical y en `-h` para horizontal.

## Personajes y mundos

- **Lala**: El jardín de Lala
- **Juan**: La aventura de Juan
- **Lucía**: El cielo de Lucía
- **Bubu**: El bosque mágico de Bubu

Cada personaje tiene las mismas 40 actividades, con sus colores, objetos y nombres propios, organizadas en: Aprendo, Cuerpo y emociones, Memoria y atención, Lógica y números, Motricidad fina, Letras y palabras, Arte y música, y Hábitos y juego.

## Pendiente

- Voces naturales grabadas o generadas para reemplazar la voz del navegador.
- Imágenes propias para el resto de los juegos (por ahora solo Globos de colores tiene escena por personaje).
- Empaquetado para Play Store y App Store (Capacitor).
