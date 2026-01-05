Sports News Keyword Scanner   
🏆📰Este proyecto es un escáner automatizado diseñado para monitorear sitios web de noticias deportivas (como ESPN, Bleacher Report y CBS Sports) en busca de palabras clave específicas. Utiliza tecnologías modernas de web scraping para extraer titulares, subtitulares y menciones de videos de forma asíncrona.

✨ Características  
Monitoreo Multi-sitio: Configurado para rastrear múltiples portales deportivos simultáneamente.  
Navegación Asíncrona: Utiliza Playwright para cargar contenido dinámico (JavaScript) de manera eficiente.  
Búsqueda por Palabras Clave: Filtra contenido basado en una lista personalizada proporcionada por el usuario.  
Exportación de Datos: Guarda los hallazgos en un archivo scan_results.csv para su posterior análisis en Excel o herramientas de datos.  
Detección de Bots: Incluye Headers de User-Agent realistas para mejorar la tasa de éxito en las peticiones.  

🛠️ Requisitos
Asegúrate de tener instalada la versión 3.8 o superior de Python.  
Bibliotecas Necesarias  
playwright: Para la automatización del navegador.  
beautifulsoup4: Para el análisis del HTML.  
pandas: Para la manipulación y guardado de datos.  

Instalación
Clona este repositorio o descarga el código.

Instala las dependencias:
```Bash
pip install playwright beautifulsoup4 pandas
```
Instala los navegadores necesarios para Playwright:

```Bash
playwright install chromium
```
🚀 Configuración y Uso
1. Preparar las Palabras Clave  
Crea un archivo llamado keywords.txt en el mismo directorio que el script. Añade una palabra o frase por línea. Ejemplo:  
Plaintext  
Messi  
Lakers  
Super Bowl  
Transfer news  

2. Ejecutar el Escáner
Inicia el proceso con el siguiente comando:

```Bash
python nombre_de_tu_archivo.py
```
3. Resultados
El script navegará por los sitios configurados y, si encuentra coincidencias, las guardará en scan_results.csv. Los campos guardados son:  
Timestamp: Fecha y hora del hallazgo.  
Source: Sitio web de origen.  
Type: Categoría (Titular, Subtítulo, Video).  
Matched Text: El texto completo encontrado.  
Keyword: La palabra clave que activó la coincidencia.

⚙️ Estructura del Código
El script funciona siguiendo este flujo de procesamiento:
SITE_PROFILES: Diccionario donde puedes agregar nuevos sitios web y sus selectores CSS específicos.  
get_site_content: Maneja la lógica de navegación y espera a que el contenido dinámico se cargue.  
parse_and_match: Analiza el HTML buscando coincidencias exactas (sin distinguir mayúsculas/minúsculas).  
main: Coordina la ejecución, gestiona la persistencia de datos y elimina duplicados.

⚠️ Notas y Recomendaciones
Ética de Scraping: Asegúrate de revisar los términos de servicio de los sitios web antes de realizar escaneos frecuentes.

Tiempos de espera: El script incluye un asyncio.sleep(3) para permitir que los scripts de los sitios terminen de cargar los titulares. Puedes ajustar este valor si tu conexión es lenta.

Headless Mode: Por defecto, el navegador se ejecuta en segundo plano (headless=True). Puedes cambiarlo a False para observar el proceso en tiempo real.
