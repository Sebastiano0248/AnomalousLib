import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def mostrar_variables():
    var1 = 42
    var2 = np.pi
    messagebox.showinfo("Variables", f"Variable 1: {var1}\nVariable 2: {var2}")

def grafico_2d():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Gráfico 2D: Seno")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()

def grafico_3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title("Gráfico 3D: Superficie")
    plt.show()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Aplicación con Ventana")
ventana.geometry("400x300")

# Botones
boton_variables = tk.Button(ventana, text="Mostrar Variables", command=mostrar_variables)
boton_variables.pack(pady=10)

boton_2d = tk.Button(ventana, text="Mostrar Gráfico 2D", command=grafico_2d)
boton_2d.pack(pady=10)

boton_3d = tk.Button(ventana, text="Mostrar Gráfico 3D", command=grafico_3d)
boton_3d.pack(pady=10)

boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_salir.pack(pady=10)

# Ejecutar el loop principal
ventana.mainloop()
