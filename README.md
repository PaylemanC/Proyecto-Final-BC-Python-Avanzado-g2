# Dashboard y ETL - Análisis de Proyectos Legislativos del Congreso USA

Un Dashboard interactivo para explorar bills/proyectos legislativos y miembros del Congreso de EE.UU, desarrollado con Pandas, Django y Vega-Altair. A partir de un proceso ETL, se extrae la información desde la API oficial de [congress.gov](https://api.congress.gov/), almacenando una parcialidad del dataset en SQLite. La interfaz gráfica proporciona resúmenes, tablas completas y gráficos dinámicos.

### Integrantes

- [Carina Payleman (PaylemanC)](https://github.com/PaylemanC)
- [Elias Velazquez (esvdev)](https://github.com/eliasvelazquezdev)

## Instalación

1. Clona el repositorio, y accede al nuevo subdirectorio creado:

```bash
git clone https://github.com/PaylemanC/Proyecto-Final-BC-Python-Avanzado-g2.git

```

2. Crea y activa tu entorno virtual:

```bash
# Crear entorno: 
python -m venv venv

# Activación en Windows:
cd venv 
Scripts/activate 
cd .. 

# Activación en Linux & MacOS
source venv/bin/activate

```

3. Instala las dependencias desde el directorio raíz:

```bash
pip install -r requirements.txt 

```

### Tecnologías utilizadas

| Librería/Framework | Uso  |
| --- | --- |
| **Django** | Dashboard interactivo y UI.  |
| **Pandas** | Extracción y transformación de datos.  |
| **Vega-Altair** | Generación de gráficos con Python y JS. |
| **Loguru** | Implementación de logs y debugging.  |
| **Dotenv (Python)** | Manejo de variables de entorno.  |
| **Requests** | Peticiones GET a la API.  |

## Levantar Web

Para ver el Dashboard y proyecto en general:

```bash
cd rollcall_votes

python manage.py runserver

```

### Correr tests unitarios
Para la app de graphics, verificar que los gráficos se generan correctamente:

```bash
cd rollcall_votes

python manage.py test graphics
```

## Correr extracción de datos*

Debido a que la base de datos ya se encuentra inicializada e incluida en la raíz del repositorio, “`house_votes_db.sqlite`", este paso es *__opcional__. Sin embargo, para corroborrar y ver el proceso de extracción de datos (ETL), se pueden seguir los siguientes pasos:

1. Elimina el archivo de la base de datos `house_votes_db.sqlite`.
2. Crea un archivo `.env` a la altura del archivo `.env-dist`, con la siguiente estructura:

```bash
CONGRESS_API_KEY="API KEY (STR)" 
ENVIRONMENT="The environment, being either PROD or DEV (STR)" 
CONGRESS="The congress number (INT)" 
SETUP_SCHEMA="Whether to setup the schema in the database (BOOL)"

```

**Recomendación**:

```bash
CONGRESS_API_KEY="EE6i06Z939y8B9bzhLcgsTT93faX1SP5CHDr34Ze" 
ENVIRONMENT=DEBUG
SETUP_SCHEMA=TRUE
CONGRESS=117

```

Consideraciones:

- La API KEY puedes obtenerla [aquí](https://api.congress.gov/sign-up/); a fines académicos, se proporciona: **`EE6i06Z939y8B9bzhLcgsTT93faX1SP5CHDr34Ze`**
- La variable `ENVIROMENT` determina el comportamiento del módulo logging.
- La variable `CONGRESS` puede ser cualquier número entre el 101 y el 115.
- La variable `SETUP_SCHEMA` debe estar en FALSE si ya está creada la base de datos, y en TRUE si se debe crear.

3. Ejecutar la extracción:

```bash
python -m scraper.main_scraper

```

## Estructura del Proyecto

Carpetas y archivos relevantes:

```bash
/
|-- rollcall_votes/
|   |-- dashboard/
|   |-- data/
|   |-- graphics/
|   |-- rollcall_votes/
|   |-- static/
|   |-- templates/
|-- scraper/
|-- house_votes_db.sqlite
|-- requirements.txt


```

* __rollcall_votes__: Proyecto de Django.
   * **dashboard**: Contiene las vistas y urls de todas las páginas.
   * **data**: Contiene los modelos que conectan a la base de datos SQLite.
   * **graphics**: Clases que generan gráficos con Vega-Altair.
   * __rollcall_votes__: Configuración del proyecto de Django.
   * **static**: Archivos estáticos (CSS).
   * **templates**: Templates HTML del Django (UI).

* **scraper**: Módulo de extracción de datos.
* __house_votes_db.sqlite__: Base de datos SQLite con los datos extraídos.

Tu entorno virtual y archivo .env debe estar a la altura de la carpeta raíz.