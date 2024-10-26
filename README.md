# Web Scraping con Playwright, Django y SQLite

Este proyecto demuestra cómo realizar web scraping con Playwright para extraer datos de https://clerk.house.gov/, almacenarlos en una base de datos SQLite mediante Django y exponerlos a través de una API creada con Django REST framework para su acceso.

## Integrantes

- [Andres Parilli](https://github.com/andresparilli)
- [Carina Payleman](https://github.com/PaylemanC)
- [Elias Velazquez](https://github.com/eliasvelazquezdev)

## Requerimientos*

- Python 3.6 o superior
- Playwright
- Django
- Django REST framework
- SQLite

*_Instalación con archivo `requirements.txt` adelante._

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/PaylemanC/Proyecto-Final-BC-Python-Avanzado-g2.git

```

2. Crear un entorno virtual:

```bash
python -m venv .venv

```

3. Activar el entorno virtual:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Instalar dependencias:

```bash
pip install -r requirements.txt

```

## Ejecución

1. Aplicar las migraciones: `python manage.py makemigrations` y `python manage.py migrate`
2. Ejecutar el script de scraping: `python manage.py runscript scrape_data`   (validemos si solo se ejecuta una vez)
3. Iniciar el servidor de desarrollo: `python manage.py runserver`

## Pruebas

Se incluyen pruebas unitarias para asegurar la calidad del código. Para ejecutar las pruebas, usar: `python manage.py test`