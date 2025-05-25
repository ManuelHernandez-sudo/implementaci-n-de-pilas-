import tkinter as tk
from tkinter import messagebox
import webbrowser
from geopy.geocoders import Nominatim # type: ignore


class PlanificadorRutas:
    def __init__(self, master):
        self.master = master
        self.master.title("Planificador de Rutas de Entrega")
        self.geolocator = Nominatim(user_agent="planificador_rutas")
        self.paquetes = []

        # Campo para dirección de origen
        tk.Label(master, text="Ciudad de origen:").grid(row=0, column=0, sticky="e")
        self.origen_entry = tk.Entry(master, width=50)
        self.origen_entry.grid(row=0, column=1, padx=10, pady=5)

        # Campo para dirección de destino final
        tk.Label(master, text="Ciudad de destino final:").grid(row=1, column=0, sticky="e")
        self.destino_entry = tk.Entry(master, width=50)
        self.destino_entry.grid(row=1, column=1, padx=10, pady=5)

        # Campos para agregar paquetes
        tk.Label(master, text="Nombre del destinatario:").grid(row=2, column=0, sticky="e")
        self.nombre_entry = tk.Entry(master)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(master, text="Dirección de entrega:").grid(row=3, column=0, sticky="e")
        self.direccion_entry = tk.Entry(master, width=50)
        self.direccion_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(master, text="Agregar Paquete", command=self.agregar_paquete).grid(row=4, column=1, sticky="e", pady=5)

        # Lista de paquetes agregados
        self.lista_paquetes = tk.Listbox(master, width=80)
        self.lista_paquetes.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Botón para planificar ruta
        tk.Button(master, text="Planificar Ruta", command=self.planificar_ruta).grid(row=6, column=1, sticky="e", pady=10)

    def agregar_paquete(self):
        nombre = self.nombre_entry.get().strip()
        direccion = self.direccion_entry.get().strip()

        if nombre and direccion:
            self.paquetes.append((nombre, direccion))
            self.lista_paquetes.insert(tk.END, f"{nombre} - {direccion}")
            self.nombre_entry.delete(0, tk.END)
            self.direccion_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos del paquete.")

    def planificar_ruta(self):
        origen = self.origen_entry.get().strip()
        destino = self.destino_entry.get().strip()

        if not origen or not destino or not self.paquetes:
            messagebox.showerror("Error", "Debes ingresar origen, destino y al menos un paquete.")
            return

        try:
            ubicaciones = []

            loc_origen = self.geolocator.geocode(origen)
            if not loc_origen:
                raise ValueError("No se pudo verificar la ubicación de origen.")
            ubicaciones.append(f"{loc_origen.latitude},{loc_origen.longitude}")

            for _, direccion in self.paquetes:
                loc = self.geolocator.geocode(direccion)
                if not loc:
                    raise ValueError(f"No se pudo verificar la ubicación de {direccion}.")
                ubicaciones.append(f"{loc.latitude},{loc.longitude}")

            loc_destino = self.geolocator.geocode(destino)
            if not loc_destino:
                raise ValueError("No se pudo verificar la ubicación de destino.")
            ubicaciones.append(f"{loc_destino.latitude},{loc_destino.longitude}")

            url = f"https://www.google.com/maps/dir/" + "/".join(ubicaciones)
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error al calcular ruta", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanificadorRutas(root)
    root.mainloop()