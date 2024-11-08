# TP Integrador BUSTURISTICO
Integrantes Grupo 2:
- Joaquín Chayle
- Juan Loza
- Benicio Manzotti
- Guido Morero

Este proyecto es una aplicación de bus turístico desarrollada en Django, que permite a los usuarios explorar distintos recorridos turísticos en Buenos Aires, asi pudiendo ver los distintos tipos asignados con colores. Cada uno tiene sus distintas paradas, las cuales pueden ser compartidas entre los distintos recorridos, y dentro de cada una se encuentran los atractivos con sus calificaciones. 

## Índice

- [Integrantes del Grupo](#integrantes-del-grupo)
- [Requisitos Previos](#requisitos-previos)
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Instalación](#instalación)


## Requisitos Previos

- Python 3.10
- pipenv
- MySQL


## Instalación

1. **Clonar el repositorio y abrirlo:**
    ```bash
    git clone https://github.com/Villada-PG3/tp-integrador-busturistico.git
    cd tp-integrador-empresa-de-bus-turistico
    cd BUSTURISTICO
    ```
    Una vez clonado el repositorio, meterse en la carpeta de tp-integrador-busturistico y meterse en la carpeta BUSTURISTICO.

2. **Configurar el entorno virtual y las dependencias:**
    ```bash
    pipenv install
    pipenv shell
    ```

3. **Crear la base de datos en MySQL:**
   Crear un usuario dedicado (`public_user`) que otros puedan usar para conectarse a la base de datos. 

    - Abrí MySQL en tu terminal:
      ```bash
      mysql -u root -p
      ```
      Ingresá tus datos

    - Creá la base de datos para el proyecto:
      ```sql
      CREATE DATABASE busturistico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
      ```

    - Crea un usuario de prueba con permisos sobre esta base de datos:
      ```sql
      CREATE USER 'public_user'@'localhost' IDENTIFIED BY 'contraseña';
      GRANT ALL PRIVILEGES ON busturistico.* TO 'public_user'@'localhost';
      FLUSH PRIVILEGES;
      GRANT SELECT, LOCK TABLES ON busturistico.* TO 'public_user'@'localhost';
      FLUSH PRIVILEGES;
      GRANT PROCESS ON *.* TO 'public_user'@'localhost';
      FLUSH PRIVILEGES;
      EXIT;
      ```

4. **Configurar las variables de entorno en Django:**
   Configura las variables de entorno de tu aplicación Django para que utilicen la base de datos y el usuario creados. Cambiá estas líneas en tu archivo `settings.py` SI ES QUE NO ESTAN IGUAL:

   Para ello ingresa dentro del archivo proyecto
    ```bash
      cd proyecto/

      code .
    ```
Ingresar a  Config, ahi deberia encontrar el archivo settings.py, buscar la parte de DATABASES y cambiar las lineas por precausión y guardar (ctrl + s).
    

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'busturistico',
            'USER': 'public_user',
            'PASSWORD': 'contraseña',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

6. **Migrar las tablas a la base de datos:**
   Asegúrate de que las migraciones de tu aplicación estén listas y aplícalas para crear la estructura de las tablas en la base de datos:

    ```bash
    python manage.py migrate
    ```

7. **Importar datos desde un archivo SQL:**
   Hay muestras iniciales, importalos a la base de datos recién creada:

    ```bash
    python manage.py loaddata > db.json
    ```

8. **Ejecutar el servidor:**
   Ahora podes iniciar el servidor de desarrollo para probar que todo funcione correctamente, el usuario administrador es joacochayle, contraseña jnch1206:

    ```bash
    python manage.py runserver
    ```

Con estos pasos, los usuarios podrán configurar y usar la base de datos `busturistico`.

---

A continuacion la presentacion del proyecto [aqui.](https://www.canva.com/design/DAGU3IV5P-M/LEJ5PI1A-aX7SgZvf09yeg/view?utm_content=DAGU3IV5P-M&utm_campaign=designshare&utm_medium=link&utm_source=editor)

---
<details>
<summary>Diagrama ER</summary>

```mermaid
erDiagram

  
    Viaje}|--||Recorrido : ejecutan

    Recorrido{
        varchar nombre
        varchar codigo_alfanumerico PK
        time hora_inicio
        time hora_fin
        time frecuencia
    }
    
    Recorrido||--|{Orden_parada : tienen
    

    Chofer||--|{Viaje : realiza

    Viaje{
        int id_viaje PK
        int legajo FK
        int num_unidad FK
        varchar codigo_alfanumerico FK
        int id_estadoV FK
        time horario_inicio_programado
        time horario_fin_programado
        date fecha_viaje
        datetime marca_inicio_viaje_real
        datetime marca_fin_viaje_real
    }

    Viaje}|--||Estado_viaje : tienen

    Estado_viaje{
        int id_estadoV PK
        varchar nombre
        varchar descripcion
    }
    

    Viaje}|--||Bus : se_le_asigna

    Chofer{
        int legajo PK
        varchar nombre
        varchar apellido
        
    }
    Bus{
        varchar patente 
        int num_unidad PK
        date fecha_compra
        int id_estadoB FK
    }

    Bus}|--||Estado_bus : tienen

    Estado_bus{
        int id_estadoB PK
        varchar nombre
        varchar descripcion
    }

    Parada}|--||Tipo_parada : tiene

    Tipo_parada{
        int id_tipo_parada PK
        varchar nombre_tipo_parada
        varchar descripcion
    }
    Parada{
        int id_parada PK
        int id_tipo_parada FK
        varchar nombre
        varchar direccion
        varchar descripcion
        longblob imagen
    }

    Parada||--|{atractivoXparada : tiene
    Parada||--|{Orden_parada : esta

    atractivoXparada{
        int id_atractivoXparada PK
        int id_atractivo FK
        int id_parada FK
    }
    
    atractivoXparada}|--||Atractivo : tienen

    Atractivo{
        int id_atractivo PK
        varchar nombre
        varchar descripcion
        float calificacion
    }

    Orden_parada{
        int id_ord_parada PK
        int id_parada FK
        int codigo_alfanumerico FK
        int asignacion_paradas
    }

```
</details>
