# TP Integrador BUSTURISTICO
Integrantes Grupo 2:
- Joaquín Chayle
- Juan Loza
- Benicio Manzotti
- Guido Morero
  
El trabajo práctico consiste en crear un proyecto django, en este caso, diseñado para un bus turistico de Buenos Aires. 

Estas deberian ser las funcionalidades que tendria que cumplir el proyecto (en proceso):
- visualizacion de recorridos, atractivos y paradas del lado del usuario
- creacion de viajes, reportes diarios del lado del administrador, ademas de poder llevar un registro de los colectivos habilitados y los choferes que esta activos
- carga de tiempo de viajes de los chofferes y generacion de tickets

<details>
<summary>Diagrama ER</summary>

```mermaid
erDiagram

  
    Viaje}|--||Recorrido : ejecutan

    Recorrido{
        varchar codigo_alfanumerico PK
        time hora_inicio
        time hora_fin
        int id_ord_parada FK
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
