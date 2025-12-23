import tkinter as tk
from PIL import Image, ImageTk
import csv
from datetime import datetime
import pandas as pd
from tkinter import messagebox
import os
import winsound
import threading
import serial
# -------------------------------------Funciones o definiciones--------------------------------------------------------


def actualizar_fecha_hora():
    # Obtener la fecha y la hora actuales
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    label_30.config(text=f"{fecha_actual}")
    ventana.after(1000, actualizar_fecha_hora)


def toggle_minimize(event=None):
    ventana.iconify()


def cerrar_ventana():
    ventana.destroy()


def on_restore(event=None):
    ventana.attributes("-fullscreen", True)


def obtener_configuracion(clave):
    try:
        with open("C:/INHEMETER_programmer/settings.ini", "r") as config:
            for linea in config:
                if linea.startswith(clave):
                    return linea.split("=")[1].strip()
    except FileNotFoundError:
        messagebox.showerror(
            "Error", "El archivo de configuración 'setting.txt' no fue encontrado.")
    except Exception as e:
        messagebox.showerror(
            "Error", f"Ocurrió un error al leer la configuración: {e}")
    return None


def ajustar_escala():
    # Obtener el tamaño de la pantalla
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    # Calcular el factor de escala basado en una resolución de referencia (1920x1080)
    escala_x = pantalla_ancho / 1920
    escala_y = pantalla_alto / 1080
    escala = min(escala_x, escala_y)
    frame.config(padx=0 * escala, pady=0 * escala)

    # Ajustar el tamaño de la fuente
    fuente_8 = int(8 * escala)
    fuente_10 = int(10 * escala)
    fuente_12 = int(12 * escala)
    fuente_14 = int(14 * escala)
    fuente_16 = int(16 * escala)
    fuente_20 = int(20 * escala)
    fuente_22 = int(22 * escala)
    fuente_30 = int(30 * escala)
    fuente_40 = int(40 * escala)
    fuente_50 = int(50 * escala)
    fuente_70 = int(70 * escala)

    label_0.config(font=("Arial", fuente_50, "bold"))
    label_1.config(font=("Arial", fuente_20, "bold"))
    label_2.config(font=("Arial", fuente_20, "bold"))
    label_3.config(font=("Arial", fuente_20, "bold"))
    label_4.config(font=("Arial", fuente_20, "bold"))
    label_5.config(font=("Arial", fuente_20, "bold"))
    label_6.config(font=("Arial", fuente_20, "bold"))
    label_7.config(font=("Arial", fuente_30, "bold"))
    label_8.config(font=("Arial", fuente_30, "bold"))
    label_9.config(font=("Arial", fuente_30, "bold"))
    label_10.config(font=("Arial", fuente_30, "bold"))
    label_11.config(font=("Arial", fuente_30, "bold"))
    label_12.config(font=("Arial", fuente_20, "bold"))
    label_13.config(font=("Arial", fuente_30, "bold"))
    label_14.config(font=("Arial", fuente_30, "bold"))
    label_15.config(font=("Arial", fuente_30, "bold"))
    label_16.config(font=("Arial", fuente_30, "bold"))

    entry_1.config(font=("Arial", fuente_20, "bold"))
    entry_2.config(font=("Arial", fuente_20, "bold"))
    entry_3.config(font=("Arial", fuente_20, "bold"))
    entry_4.config(font=("Arial", fuente_20, "bold"))
    label_20.config(font=("Arial", fuente_20, "bold"))
    label_21.config(font=("Arial", fuente_20,  "bold"))
    label_29.config(font=("Arial", fuente_20,  "bold"))
    label_30.config(font=("Arial", fuente_12,  "bold"))
    label_31.config(font=("Arial", fuente_20, "bold"))

    label_24.config(font=("Arial", fuente_20, "bold"))
    label_25.config(font=("Arial", fuente_20, "bold"))
    label_26.config(font=("Arial", fuente_20, "bold"))
    label_27.config(font=("Arial", fuente_20, "bold"))
    label_28.config(font=("Arial", fuente_20, "bold"))

    # entry_6.config(font=("Arial", fuente_12))
    label_23.config(font=("Arial", fuente_12, "bold"))


NUMERO_VALIDO = obtener_configuracion("Model")


def validar_codigo_socket_1(event=None):
    codigo = entry_1.get().strip()
    socket2_codigo = label_26.cget("text").strip()
    socket3_codigo = label_27.cget("text").strip()
    socket4_codigo = label_28.cget("text").strip()

    if len(codigo) >= 6 and codigo[:6] == str(NUMERO_VALIDO).strip() and codigo != socket2_codigo and codigo != socket3_codigo and codigo != socket4_codigo:
        label_7.config(text="PASS", bg="#C6EFCE", fg="green")
        label_11.config(text="Escanee la pieza del socket 2 o puede comenzar la programación",
                        fg="#0A0A09", bg="#C4C2C2")
        label_25.config(text=f"{codigo}")
        entry_1.delete(0, tk.END)
        entry_2.focus()
        play_pass()

    else:
        label_7.config(text="FAIL", bg="#FFC7CE", fg="red")
        label_11.config(
            text=f"ID incorrecto o duplicado, verifique por favor: '{codigo}'", fg="#0A0A09", bg="#C4C2C2")
        label_25.config(text=f"{codigo}")
        entry_1.delete(0, tk.END)
        play_fail()

    # label_7.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_8.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_9.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_10.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_15.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_13.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_14.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_15.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_16.config(text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
    label_26.config(text="", fg="black", bg="white")
    label_27.config(text="", fg="black", bg="white")
    label_28.config(text="", fg="black", bg="white")


def validar_codigo_socket_2(event=None):
    codigo = entry_2.get().strip()
    socket1_codigo = label_25.cget("text").strip()
    socket3_codigo = label_27.cget("text").strip()
    socket4_codigo = label_28.cget("text").strip()

    if len(codigo) >= 6 and codigo[:6] == str(NUMERO_VALIDO).strip() and codigo != socket1_codigo and codigo != socket3_codigo and codigo != socket4_codigo:
        label_8.config(text="PASS", bg="#C6EFCE", fg="green")
        label_11.config(text="Escanee la pieza del socket 3 o puede comenzar la programación",
                        fg="#0A0A09", bg="#C4C2C2")
        label_26.config(text=f"{codigo}")
        entry_2.delete(0, tk.END)
        entry_3.focus()
        play_pass()

    else:
        label_8.config(text="FAIL", bg="#FFC7CE", fg="red")
        label_11.config(
            text=f"ID incorrecto o duplicado, verifique por favor: '{codigo}'", fg="#0A0A09", bg="#C4C2C2")
        label_26.config(text=f"{codigo}")
        entry_2.delete(0, tk.END)
        play_fail()


def validar_codigo_socket_3(event=None):
    codigo = entry_3.get().strip()
    socket1_codigo = label_25.cget("text").strip()
    socket2_codigo = label_26.cget("text").strip()
    socket4_codigo = label_28.cget("text").strip()

    if len(codigo) >= 6 and codigo[:6] == str(NUMERO_VALIDO).strip() and codigo != socket1_codigo and codigo != socket2_codigo and codigo != socket4_codigo:
        label_9.config(text="PASS", bg="#C6EFCE", fg="green")
        label_11.config(text="Escanee la pieza del socket 4 o puede comenzar la programación",
                        fg="#0A0A09", bg="#C4C2C2")
        label_27.config(text=f"{codigo}")
        entry_3.delete(0, tk.END)
        entry_4.focus()
        play_pass()

    else:
        label_9.config(text="FAIL", bg="#FFC7CE", fg="red")
        label_11.config(
            text=f"ID incorrecto o duplicado, verifique por favor: '{codigo}'", fg="#0A0A09", bg="#C4C2C2")
        label_27.config(text=f"{codigo}")
        entry_3.delete(0, tk.END)
        play_fail()


def validar_codigo_socket_4(event=None):
    codigo = entry_4.get().strip()
    socket1_codigo = label_25.cget("text").strip()
    socket2_codigo = label_26.cget("text").strip()
    socket3_codigo = label_27.cget("text").strip()

    if len(codigo) >= 6 and codigo[:6] == str(NUMERO_VALIDO).strip() and codigo != socket1_codigo and codigo != socket2_codigo and codigo != socket3_codigo:
        label_10.config(text="PASS", bg="#C6EFCE", fg="green")
        label_11.config(text="Puede comenzar con la programación",
                        fg="#0A0A09", bg="#C6EFCE")
        label_28.config(text=f"{codigo}")
        entry_4.delete(0, tk.END)
        play_pass()

    else:
        label_10.config(text="FAIL", bg="#FFC7CE", fg="red")
        label_11.config(
            text=f"ID incorrecto o duplicado, verifique por favor: '{codigo}'", fg="#0A0A09", bg="#C4C2C2")
        label_28.config(text=f"{codigo}")
        entry_4.delete(0, tk.END)
        play_fail()


# Rutas desde tu settings.ini
ruta_fail = obtener_configuracion("son_fail")
ruta_pass = obtener_configuracion("son_pass")


def play_fail():
    try:
        if ruta_fail:
            winsound.PlaySound(
                ruta_fail, winsound.SND_FILENAME | winsound.SND_ASYNC)

    except Exception as e:
        print("Error sonido fail:", e)


def play_pass():
    try:
        if ruta_pass:
            winsound.PlaySound(
                ruta_pass, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print("Error sonido pass:", e)


def cerrar_ventana_principal():
    """Cerrar toda la aplicación si se cierra la ventana de datos."""
    if messagebox.askyesno("Confirmar salida", "¿Desea salir del programa completamente?"):
        ventana.destroy()


def ventana_datos(width=None, height=None):
    global ventana, label_20, label_21, entry_1
    ventanadat = tk.Toplevel(ventana)
    ventanadat.title("Inicio de sesión")
    ventanadat.grab_set()
    ventanadat.attributes("-topmost", True)
    ventanadat.resizable(True, True)
    ventanadat.configure(bg="red")
    ventanadat.attributes("-toolwindow", True)
    ventanadat.protocol("WM_DELETE_WINDOW", cerrar_ventana_principal)

    ventanadat.grid_rowconfigure(0, weight=1)
    ventanadat.grid_columnconfigure(0, weight=1)
    framedat = tk.Frame(ventanadat, bg="#D9D9D9")
    framedat.grid_columnconfigure(0, weight=1)
    framedat.grid_columnconfigure(1, weight=1)
    framedat.grid_rowconfigure(0, weight=1)
    framedat.grid_rowconfigure(1, weight=1)
    framedat.grid_rowconfigure(2, weight=1)
    # ---------------Framedat Row0
    label_18 = tk.Label(framedat, text="Número de empleado:",
                        fg="black", bg="#D9D9D9")
    label_18.config(font=("Arial", 18, "bold"))
    label_18.grid(row=0, column=0, padx=10, pady=20, sticky="e")
    entry_7 = tk.Entry(framedat, width=15, justify="center", fg="#0A0A09", bg="#A6A6A6",
                       border=3)
    entry_7.config(font=("Arial", 18, "bold"))
    entry_7.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
    entry_7.focus()

    # ---------------Framedat Row1
    label_19 = tk.Label(framedat, text="Orden de producción:",
                        fg="black", bg="#D9D9D9")
    label_19.config(font=("Arial", 18, "bold"))
    label_19.grid(row=1, column=0, padx=10, pady=20, sticky="e")
    entry_8 = tk.Entry(framedat, width=15, justify="center", fg="#0A0A09", bg="#A6A6A6",
                       border=3)
    entry_8.config(font=("Arial", 18, "bold"))
    entry_8.grid(row=1, column=1, padx=10, pady=20, sticky="nsew")

    def aceptar():
        op = entry_7.get().strip()
        od = entry_8.get().strip()
        if not op or not od:
            # No permitir salir si alguno está vacío
            messagebox.showwarning(
                "Datos incompletos", "Debe ingresar Número de operador y Orden de producción.")
            # dejar el foco en el primer campo vacío
            if not op:
                entry_7.focus_set()
            else:
                entry_8.focus_set()
            return
        # Copiar a labels de la ventana principal
        try:
            label_20.config(text=f"Número de empleado: {op}")
            label_21.config(text=f"Orden de producción: {od}")
            global operador_actual, orden_actual
            operador_actual = op
            orden_actual = od
        except Exception:
            # Si las labels no existen, las guardamos en variables globales por si las usas luego
            globals()["OPERADOR_VAL"] = op
            globals()["ORDEN_VAL"] = od

        entry_1.focus()
        ventanadat.destroy()

    # ---------------Framedat Row2
    button_entrar = tk.Button(framedat, text="Entrar", height=0, width=0,
                              border=5, background="deepskyblue", command=aceptar)
    button_entrar.grid(row=2, column=0, columnspan=2,
                       padx=10, pady=20, sticky="nsew")
    button_entrar.config(font=("Arial", 20, "bold"))

    framedat.grid(row=0, column=0, sticky="nsew")

    # --- centrar ---
    ventanadat.update_idletasks()
    if width is None:
        width = ventanadat.winfo_reqwidth()
    if height is None:
        height = ventanadat.winfo_reqheight()
    screen_w = ventanadat.winfo_screenwidth()
    screen_h = ventanadat.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 4) - (height // 2)
    ventanadat.geometry(f"{width}x{height}+{x}+{y}")


# -------------------------------------UART----------------------------------------------------------------------------

COMP = obtener_configuracion('COMP')

ser = serial.Serial(COMP, 115200, bytesize=8,
                    parity='N', stopbits=1, timeout=1)


def leer_uart():
    try:
        while True:
            bytes_recibidos = ser.read(300)

            if b"255" in bytes_recibidos:
                ventana.after(0, act_run)

            if b"355,33" in bytes_recibidos:
                ventana.after(0, act_pass_s1)
            elif b"355,43" in bytes_recibidos:
                ventana.after(0, act_fail_s1)

            if b"455,33" in bytes_recibidos:
                ventana.after(0, act_pass_s2)
            elif b"455,43" in bytes_recibidos:
                ventana.after(0, act_fail_s2)

            if b"555,33" in bytes_recibidos:
                ventana.after(0, act_pass_s3)
            elif b"555,43" in bytes_recibidos:
                ventana.after(0, act_fail_s3)

            if b"655,33" in bytes_recibidos:
                ventana.after(0, act_pass_s4)
                ser.reset_input_buffer()
                continue
            elif b"655,43" in bytes_recibidos:
                ventana.after(0, act_fail_s4)
                ser.reset_input_buffer()
                continue

    except serial.SerialException as e:
        print("Error de comunicación serial:", e)
    finally:
        ser.close()


def act_run():
    label_11.config(text="Programando.... Espere por favor....",
                    fg="#0A0A09", bg="yellow")


def act_pass_s1():
    label_13.config(text="PASS", bg="#C6EFCE", fg="green")


def act_pass_s2():
    label_14.config(text="PASS", bg="#C6EFCE", fg="green")


def act_pass_s3():
    label_15.config(text="PASS", bg="#C6EFCE", fg="green")


def act_pass_s4():
    label_16.config(text="PASS", bg="#C6EFCE", fg="green")
    guardar_datos()


def act_fail_s1():
    label_13.config(text="FAIL", bg="#FFC7CE", fg="red")


def act_fail_s2():
    label_14.config(text="FAIL", bg="#FFC7CE", fg="red")


def act_fail_s3():
    label_15.config(text="FAIL", bg="#FFC7CE", fg="red")


def act_fail_s4():
    label_16.config(text="FAIL", bg="#FFC7CE", fg="red")
    guardar_datos()


hilo_uart = threading.Thread(target=leer_uart, daemon=True)
hilo_uart.start()
# -------------------------------------LogFile-------------------------------------------------------------------------
# Ruta del segundo archivo CSV
csv_file = obtener_configuracion("LogFile")

# Crear o abrir el primer archivo CSV, LogFile
if not os.path.isfile(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Socket_1', 'ID_S1', 'Program_S1', 'Socket_2', 'ID_S2', 'Program_S2', 'Socket_3',
                        'ID_S3', 'Program_S3', 'Socket_4', 'ID_S4', 'Program_S4', 'Date', 'Operator', 'Order', 'Model'])

# Cargar el primer archivo CSV
data = pd.read_csv(csv_file, encoding='latin1')


def guardar_datos(event=None):
    try:
        # Obtener datos
        Socket_1 = label_25.cget("text").strip() or "0"
        ID_S1 = label_7.cget("text").strip() or "0"
        Program_S1 = label_13.cget("text").strip() or "0"

        Socket_2 = label_26.cget("text").strip() or "0"
        ID_S2 = label_8.cget("text").strip() or "0"
        Program_S2 = label_14.cget("text").strip() or "0"

        Socket_3 = label_26.cget("text").strip() or "0"
        ID_S3 = label_9.cget("text").strip() or "0"
        Program_S3 = label_15.cget("text").strip() or "0"

        Socket_4 = label_28.cget("text").strip() or "0"
        ID_S4 = label_10.cget("text").strip() or "0"
        Program_S4 = label_16.cget("text").strip() or "0"

        Date_Time = label_30.cget("text").strip() or "0"
        Operator = operador_actual
        Order = orden_actual
        Model = NUMERO_VALIDO

        # Verificar si los datos están completos
        if Socket_1 and ID_S1 and Program_S1 and Socket_2 and ID_S2 and Program_S2 and Socket_3 and ID_S3 and Program_S3 and Socket_4 and ID_S4 and Program_S4 and Date_Time and Operator and Order and Model:
            # Guardar en el archivo CSV
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([Socket_1, ID_S1, Program_S1, Socket_2, ID_S2, Program_S2, Socket_3,
                                ID_S3, Program_S3, Socket_4, ID_S4, Program_S4, Date_Time, Operator, Order, Model])

        label_11.config(text="Para comenzar escanee el ID de la pieza del socket 1",
                        fg="#0A0A09", bg="#C4C2C2")
        entry_1.focus()

    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {e}")


# -------------------------------------Ventana principal---------------------------------------------------------------
# Crear la ventana principal
ventana = tk.Tk()
# Configurar la ventana para estar siempre al frente
ventana.attributes("-topmost", False)
# Iniciar en pantalla completa
ventana.attributes("-fullscreen", True)
# Mostrar los botones de minimizar y cerrar
ventana.overrideredirect(False)
# Configurar para no permitir redimensionar manualmente
ventana.resizable(False, False)
# Detectar cuando la ventana es restaurada desde la barra de tareas
ventana.bind("<Map>", on_restore)
# Color ventana
ventana.configure(bg="#F0F0F0")
# Configurar el grid de la ventana principal con diferentes pesos
ventana.grid_rowconfigure(0, weight=0)
ventana.grid_rowconfigure(1, weight=0)
ventana.grid_rowconfigure(2, weight=1)
ventana.grid_columnconfigure(0, weight=1)
# -------------------------------------Frame---------------------------------------------------------------------------
# Crear frame
frame = tk.Frame(ventana, bg="white")
frame2 = tk.Frame(ventana, bg="white")
frame3 = tk.Frame(ventana, bg="white", pady=30)

# Configurar el grid para el frame
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)
frame.grid_columnconfigure(3, weight=1)
frame.grid_columnconfigure(4, weight=1)
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_rowconfigure(5, weight=1)
frame.grid_rowconfigure(6, weight=0)


frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_rowconfigure(0, weight=1)

frame3.grid_columnconfigure(0, weight=1)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_columnconfigure(2, weight=1)
frame3.grid_rowconfigure(0, weight=1)


# -------------------------------------Frame2-Row0---------------------------------------------------------------------
# Cargar de logo ELRAD
logo_elrad = Image.open(obtener_configuracion("LogoELRAD"))
logo_elrad = logo_elrad.resize((150, 75), Image.LANCZOS)  # Ajuste de tamaño
logo_elrad_tk = ImageTk.PhotoImage(logo_elrad)

# Imagen ELRAD como boton de minimizar
boton_minimizar = tk.Button(
    frame2, image=logo_elrad_tk, command=toggle_minimize, borderwidth=0, bg="white")
boton_minimizar.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

# Label_0: Titulo
label_0 = tk.Label(
    frame2, text="Programador INHEMETER", fg="black", bg="white")
label_0.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

# Cargar de logo INHEMETER
logo_inhemeter = Image.open(obtener_configuracion("LogoIn"))
logo_inhemeter = logo_inhemeter.resize(
    (150, 75), Image.LANCZOS)  # Ajuste de tamaño
logo_inhemeter_tk = ImageTk.PhotoImage(logo_inhemeter)

# Imagen INHEMETER como boton de cerrado
boton_cerrar = tk.Button(
    frame2, image=logo_inhemeter_tk, command=cerrar_ventana, borderwidth=0, bg="white")
boton_cerrar.grid(row=0, column=2, padx=0, pady=0, sticky="ne")

# -------------------------------------Frame1-Row0---------------------------------------------------------------------
# label_1: Socket 1
label_1 = tk.Label(frame, text="Socket 1",
                   fg="black", bg="white")
label_1.grid(row=0, column=1, padx=5, pady=0, sticky="s")

# label_2: Socket 2
label_2 = tk.Label(frame, text="Socket 2",
                   fg="black", bg="white")
label_2.grid(row=0, column=2, padx=5, pady=0, sticky="s")

# label_3: Socket 3
label_3 = tk.Label(frame, text="Socket 3",
                   fg="black", bg="white")
label_3.grid(row=0, column=3, padx=5, pady=0, sticky="s")

# label_4: Socket 4
label_4 = tk.Label(frame, text="Socket 4",
                   fg="black", bg="white")
label_4.grid(row=0, column=4, padx=5, pady=0, sticky="s")
# -------------------------------------Frame-Row1---------------------------------------------------------------------
# label_5: Escanee ID
label_5 = tk.Label(frame, text="Escanee ID:",
                   fg="black", bg="white")
label_5.grid(row=1, column=0, padx=0, pady=0, sticky="e")

# entry_1: ID Socket 1
entry_1 = tk.Entry(frame, width=25, justify="center", background="springgreen",
                   border=3)
entry_1.grid(row=1, column=1, padx=10, pady=0, sticky="nsew")
entry_1.bind("<Return>", validar_codigo_socket_1)
# entry_1.focus()

# entry_2: ID Socket 2
entry_2 = tk.Entry(frame, width=25, justify="center", background="springgreen",
                   border=3)
entry_2.grid(row=1, column=2, padx=10, pady=0, sticky="nsew")
entry_2.bind("<Return>", validar_codigo_socket_2)

# entry_3: ID Socket 3
entry_3 = tk.Entry(frame, width=25, justify="center", background="springgreen",
                   border=3)
entry_3.grid(row=1, column=3, padx=10, pady=0, sticky="nsew")
entry_3.bind("<Return>", validar_codigo_socket_3)

# entry_4: ID Socket 4
entry_4 = tk.Entry(frame, width=25, justify="center", background="springgreen",
                   border=3)
entry_4.grid(row=1, column=4, padx=10, pady=0, sticky="nsew")
entry_4.bind("<Return>", validar_codigo_socket_4)

# -------------------------------------Frame-Row2---------------------------------------------------------------------
# label_24: ID
label_24 = tk.Label(frame, text="ID:",
                    fg="black", bg="white")
label_24.grid(row=2, column=0, padx=0, pady=10, sticky="e")

# label_25: ID Socket 1
label_25 = tk.Label(frame, text="", fg="black", bg="white")
label_25.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

# label_26: ID Socket 2
label_26 = tk.Label(frame, text="", fg="black", bg="white")
label_26.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

# label_27: ID Socket 3
label_27 = tk.Label(frame, text="", fg="black", bg="white")
label_27.grid(row=2, column=3, padx=10, pady=10, sticky="nsew")

# label_28: ID Socket 4
label_28 = tk.Label(frame, text="", fg="black", bg="white")
label_28.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

# -------------------------------------Frame-Row3---------------------------------------------------------------------
# label_6: Validación ID
label_6 = tk.Label(frame, text="Validación ID:",
                   fg="black", bg="white")
label_6.grid(row=3, column=0, padx=0, pady=10, sticky="e")

# label_7: Result Socket 1
label_7 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_7.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

# label_8: Result Socket 2
label_8 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_8.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

# label_9: Result Socket 3
label_9 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_9.grid(row=3, column=3, padx=10, pady=10, sticky="nsew")

# label_10: Result Socket 4
label_10 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_10.grid(row=3, column=4, padx=10, pady=10, sticky="nsew")

# -------------------------------------Frame-Row5---------------------------------------------------------------------
# label_31: Notificaciones
label_31 = tk.Label(frame, text="Notificaciones:",
                    fg="black", bg="white")
label_31.grid(row=5, column=0, padx=0, pady=0, sticky="e")

# label_11: Notificaciones
label_11 = tk.Label(
    frame, text="Para comenzar escanee el ID de la pieza del socket 1", fg="#0A0A09", bg="#C4C2C2")
label_11.grid(row=5, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")
# -------------------------------------Frame-Row4---------------------------------------------------------------------
# label_12: Programación
label_12 = tk.Label(frame, text="Programación:",
                    fg="black", bg="white")
label_12.grid(row=4, column=0, padx=0, pady=10, sticky="e")

# label_13: Programación Socket 1
label_13 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_13.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# label_14: Programación Socket 2
label_14 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_14.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

# label_15: Programación Socket 3
label_15 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_15.grid(row=4, column=3, padx=10, pady=10, sticky="nsew")

# label_16: Programación Socket 4
label_16 = tk.Label(frame, text="EN ESPERA", fg="#9C5700", bg="#FFEB9C")
label_16.grid(row=4, column=4, padx=10, pady=10, sticky="nsew")
# -------------------------------------Frame-Row6---------------------------------------------------------------------

# label_30:
label_30 = tk.Label(frame, fg="black", bg="white")
label_30.grid(row=6, column=0, padx=0, pady=0, sticky="w")


# label_23: Revision
label_23 = tk.Label(frame, text="ELRAD Electronics México Rev1.0",
                    fg="black", bg="white")
label_23.grid(row=6, column=4, padx=10, pady=0, sticky="e")

# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------Frame3-Row0---------------------------------------------------------------------
# label_20:
label_20 = tk.Label(frame3, fg="black", bg="white")
label_20.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

# label_21:
label_21 = tk.Label(frame3, fg="black", bg="white")
label_21.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

# label_29:
label_29 = tk.Label(
    frame3, text=f"Número de parte: {NUMERO_VALIDO}", fg="black", bg="white")
label_29.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")

# ---------------------------------------------------------------------------------------------------------------------

frame2.grid(row=0, column=0, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame.grid(row=2, column=0, sticky="nsew")

if __name__ == "__main__":
    actualizar_fecha_hora()
    ajustar_escala()
    ventana_datos()
    ventana.mainloop()
