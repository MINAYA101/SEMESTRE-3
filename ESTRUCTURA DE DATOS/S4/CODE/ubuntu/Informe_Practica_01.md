# GUÍA DE PRÁCTICAS DEL COMPONENTE PRÁCTICO-EXPERIMENTAL
## N° Práctica: 01
**Asignatura:** Estructura de datos  
**Nombre de la Unidad:** Tipos de datos  
**Título de la práctica:** Guía de Prácticas #01: Identificación de tipos de datos.

---

### 1. Introducción
La Programación Orientada a Objetos (POO) y las estructuras de datos fundamentales son los pilares de la ingeniería de software moderna. En esta práctica, se explora la implementación de sistemas de gestión de información utilizando estructuras lineales como vectores y registros.


---

### 2. Desarrollo
Para la resolución de la problemática, se seleccionó el caso de estudio: **Agenda de turnos de pacientes de una clínica**.

#### Procedimiento Aplicado
1. **Análisis de Requerimientos:** Se identificó la necesidad de registrar pacientes con datos personales y agendar turnos asociados a una especialidad médica.
2. **Diseño de Clases:** Se definieron las clases `Paciente` (como registro de datos) y `Turno` (que asocia un paciente con una cita).
3. **Implementación de Lógica:** Se utilizó una clase controladora `GestionClinica` que utiliza listas (vectores) para almacenar los objetos creados.
4. **Interfaz de Usuario:** Se desarrolló un menú interactivo por consola para facilitar el registro y consulta de información.

#### Análisis de Estructuras de Datos Utilizadas
| Estructura | Implementación en Código | Justificación | Ventajas | Limitaciones |
|---|---|---|---|---|
| **Registro (Estructura)** | Clases `Paciente` y `Turno` | Permite encapsular atributos de diferentes tipos en una sola entidad. | Organización clara y reutilización de código. | Mayor consumo de memoria que tipos primitivos. |
| **Vector (Lista)** | `self.pacientes` y `self.turnos` | Almacena colecciones de objetos de forma secuencial. | Acceso rápido por índice y facilidad de iteración. | La búsqueda lineal es ineficiente en grandes volúmenes de datos ($O(n)$). |

---

### 3. Resultados
El sistema implementado permite las siguientes funciones evidenciadas en las capturas de pantalla:
- Registro exitoso de pacientes con validación de datos.
- Agendamiento de turnos vinculados a pacientes existentes.
- Visualización tabular de los turnos programados.
- Generación de estadísticas básicas sobre el uso del sistema.

**Evidencia de Ejecución:**
```text
--- LISTADO DE TURNOS AGENDADOS ---
FECHA        | HORA     | ESPECIALIDAD         | PACIENTE
----------------------------------------------------------------------
2026-06-20   | 09:00    | Cardiología          | Juan Pérez
2026-06-21   | 10:30    | Odontología          | Maria Lopez
```

---

### 4. Conclusiones
- La aplicación de la POO facilita la traducción de entidades del mundo real a modelos computacionales manejables.
- El uso de vectores (listas) es fundamental para la gestión de colecciones de datos, aunque para sistemas de mayor escala se recomendaría el uso de estructuras de búsqueda más avanzadas como tablas hash o bases de datos relacionales.
- Se logró cumplir con el objetivo de la práctica al integrar tipos de datos abstractos y estructuras de control en una solución funcional.

---


