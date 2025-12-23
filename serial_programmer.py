import serial
import time

# Abre el puerto COM donde aparece el GDM-9061
ser = serial.Serial(
    port='COM3',      # <-- cambia al COM que te aparezca
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Función para enviar SCPI


def enviar(cmd):
    ser.write((cmd + '\n').encode())   # SCPI requiere terminación LF
    time.sleep(0.05)

# Función para consultar SCPI


def preguntar(cmd):
    ser.write((cmd + '\n').encode())
    time.sleep(0.1)
    return ser.readline().decode().strip()


# ------------------------------------
# PRUEBAS SCPI
# ------------------------------------

# Identificación
idn = preguntar("*IDN?")
print("IDN:", idn)

# Configurar medición de voltaje DC
enviar("CONF:VOLT:DC")

# Leer el voltaje DC
volt = preguntar("MEAS:VOLT:DC?")
valor = float(volt)
truncado = int(valor * 1000) / 1000  # deja 3 decimales

print("Voltaje DC:", truncado)

# Regresar a modo local
enviar("SYSTEM:LOCAL")

if 5 <= truncado <= 10:
    print("PASS")
else:
    print("FAIL")
# Cerrar puerto
ser.close()
