import tkinter as tk
from tkinter import filedialog, messagebox
import os
from airSpace import AirSpace
from kml_export import export_airspace_to_kml
import subprocess
import platform

def choose_file_and_generate_kml():
    filepath = filedialog.askopenfilename(title="Selecciona un archivo _nav.txt", filetypes=[("Nav files", "*.txt")])
    if not filepath or not filepath.endswith("_nav.txt"):
        messagebox.showerror("Error", "Debes seleccionar un archivo que termine en _nav.txt")
        return

    try:
        airspace = AirSpace()
        airspace.load_all(filepath)

        # Exportar a KML
        kml_filename = filepath.replace("_nav.txt", "_airspace.kml")
        export_airspace_to_kml(airspace, kml_filename)

        messagebox.showinfo("Éxito", f"KML generado: {kml_filename}")

        # Preguntar si se desea abrir en Google Earth
        if messagebox.askyesno("Abrir en Google Earth", "¿Deseas abrir el archivo en Google Earth?"):
            open_in_google_earth(kml_filename)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def open_in_google_earth(kml_path):
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["start", "", kml_path], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", kml_path])
        elif system == "Linux":
            subprocess.run(["xdg-open", kml_path])
        else:
            messagebox.showwarning("No compatible", "No se pudo detectar tu sistema operativo para abrir Google Earth.")
    except Exception as e:
        messagebox.showerror("Error al abrir", f"No se pudo abrir Google Earth:\n{e}")

def main():
    root = tk.Tk()
    root.title("Exportar Espacio Aéreo a Google Earth")
    root.geometry("400x200")

    label = tk.Label(root, text="Exportar espacio aéreo a Google Earth", font=("Helvetica", 14))
    label.pack(pady=20)

    btn = tk.Button(root, text="Seleccionar archivo .txt", command=choose_file_and_generate_kml)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
