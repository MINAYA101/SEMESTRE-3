import os
from datetime import datetime

class Paciente:
    """Clase que representa a un paciente (Registro/Estructura)"""
    def __init__(self, cedula, nombre, apellido, edad, telefono):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.telefono = telefono

    def __str__(self):
        return f"{self.cedula} | {self.nombre} {self.apellido} | {self.edad} años | {self.telefono}"

class Turno:
    """Clase que representa un turno médico"""
    def __init__(self, paciente, fecha, hora, especialidad):
        self.paciente = paciente
        self.fecha = fecha
        self.hora = hora
        self.especialidad = especialidad

    def __str__(self):
        return f"{self.fecha} {self.hora} | {self.especialidad} | Paciente: {self.paciente.nombre} {self.paciente.apellido}"

class GestionClinica:
    """Clase principal para gestionar la agenda (Uso de Vectores/Listas)"""
    def __init__(self):
        # Usamos una lista como estructura de vector para almacenar objetos
        self.pacientes = []
        self.turnos = []

    def registrar_paciente(self, cedula, nombre, apellido, edad, telefono):
        nuevo_paciente = Paciente(cedula, nombre, apellido, edad, telefono)
        self.pacientes.append(nuevo_paciente)
        return nuevo_paciente

    def buscar_paciente(self, cedula):
        for p in self.pacientes:
            if p.cedula == cedula:
                return p
        return None

    def agendar_turno(self, cedula, fecha, hora, especialidad):
        paciente = self.buscar_paciente(cedula)
        if paciente:
            nuevo_turno = Turno(paciente, fecha, hora, especialidad)
            self.turnos.append(nuevo_turno)
            return True
        return False

    def listar_turnos(self):
        if not self.turnos:
            print("\nNo hay turnos registrados.")
        else:
            print("\n--- LISTADO DE TURNOS AGENDADOS ---")
            print(f"{'FECHA':<12} | {'HORA':<8} | {'ESPECIALIDAD':<20} | {'PACIENTE'}")
            print("-" * 70)
            for t in self.turnos:
                print(f"{t.fecha:<12} | {t.hora:<8} | {t.especialidad:<20} | {t.paciente.nombre} {t.paciente.apellido}")

    def mostrar_estadisticas(self):
        print(f"\nTotal de pacientes registrados: {len(self.pacientes)}")
        print(f"Total de turnos agendados: {len(self.turnos)}")

def menu():
    gestion = GestionClinica()
    
    # Datos iniciales de prueba (Seed data)
    p1 = gestion.registrar_paciente("1712345678", "Juan", "Pérez", 30, "0998877665")
    gestion.agendar_turno("1712345678", "2026-06-20", "09:00", "Cardiología")
    
    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE GESTIÓN DE TURNOS - CLÍNICA")
        print("="*40)
        print("1. Registrar Paciente")
        print("2. Agendar Turno")
        print("3. Ver Lista de Turnos")
        print("4. Ver Estadísticas")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            print("\n--- REGISTRO DE PACIENTE ---")
            cedula = input("Cédula: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            try:
                edad = int(input("Edad: "))
                telefono = input("Teléfono: ")
                gestion.registrar_paciente(cedula, nombre, apellido, edad, telefono)
                print("¡Paciente registrado con éxito!")
            except ValueError:
                print("Error: La edad debe ser un número.")

        elif opcion == "2":
            print("\n--- AGENDAR TURNO ---")
            cedula = input("Cédula del paciente: ")
            paciente = gestion.buscar_paciente(cedula)
            if paciente:
                fecha = input("Fecha (AAAA-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                especialidad = input("Especialidad: ")
                gestion.agendar_turno(cedula, fecha, hora, especialidad)
                print("¡Turno agendado con éxito!")
            else:
                print("Error: Paciente no encontrado. Debe registrarlo primero.")

        elif opcion == "3":
            gestion.listar_turnos()

        elif opcion == "4":
            gestion.mostrar_estadisticas()

        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
