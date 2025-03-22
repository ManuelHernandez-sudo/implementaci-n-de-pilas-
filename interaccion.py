import heapq1


class Paciente:
    def __init__(self, nombre, edad, dpi, tipo_sangre, prioridad):
        self.nombre = nombre
        self.edad = edad
        self.dpi = dpi
        self.tipo_sangre = tipo_sangre
        self.prioridad = prioridad  # Menor número = Mayor prioridad

    def __lt__(self, otro):
        return self.prioridad < otro.prioridad

    def __str__(self):
        return f"{self.nombre} (Edad: {self.edad}, DPI: {self.dpi}, Sangre: {self.tipo_sangre}, Prioridad: {self.prioridad})"

class ColaPrioridad:
    def __init__(self):
        self.cola = []

    def agregar_paciente(self, paciente):
        heapq.heappush(self.cola, paciente)

    def atender_paciente(self):
        if self.cola:
            return heapq.heappop(self.cola)
        return None

    def mostrar_pacientes(self):
        return [str(p) for p in sorted(self.cola)]

class Enfermeria:
    def __init__(self):
        self.cola_pacientes = ColaPrioridad()

    def registrar_paciente(self, nombre, edad, dpi, tipo_sangre, prioridad):
        paciente = Paciente(nombre, edad, dpi, tipo_sangre, prioridad)
        self.cola_pacientes.agregar_paciente(paciente)
        print(f"Paciente {nombre} registrado con prioridad {prioridad}.")

    def atender_siguiente(self):
        paciente = self.cola_pacientes.atender_paciente()
        if paciente:
            print(f"Atendiendo a: {paciente}")
        else:
            print("No hay pacientes en espera.")

    def mostrar_lista_pacientes(self):
        pacientes = self.cola_pacientes.mostrar_pacientes()
        if pacientes:
            print("Lista de pacientes en espera:")
            for p in pacientes:
                print(p)
        else:
            print("No hay pacientes en espera.")

def menu():
    enfermeria = Enfermeria()
    while True:
        print("\nSistema de Atención a Pacientes")
        print("1. Registrar Paciente")
        print("2. Atender Paciente")
        print("3. Mostrar Pacientes en Espera")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            dpi = input("DPI: ")
            tipo_sangre = input("Tipo de Sangre: ")
            prioridad = int(input("Prioridad (Menor número = Mayor urgencia): "))
            enfermeria.registrar_paciente(nombre, edad, dpi, tipo_sangre, prioridad)
        elif opcion == "2":
            enfermeria.atender_siguiente()
        elif opcion == "3":
            enfermeria.mostrar_lista_pacientes()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
