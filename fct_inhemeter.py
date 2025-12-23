import time
import xml.etree.ElementTree as ET
import serial


def reverse_bcd(hex_str):
    """Invierte el orden de bytes para DLT645 (IsReverse='1')"""
    return "".join(reversed([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])).upper()


def encode_data(data_hex):
    """Aplica la codificación DLT645 (sumar 0x33 a cada byte)"""
    encoded = ""
    for i in range(0, len(data_hex), 2):
        b = int(data_hex[i:i+2], 16)
        b = (b + 0x33) & 0xFF
        encoded += f"{b:02X}"
    return encoded


def checksum(frame_hex):
    total = sum(int(frame_hex[i:i+2], 16) for i in range(0, len(frame_hex), 2))
    return f"{total & 0xFF:02X}"


def build_dlt645_frame(address_hex, data_hex):
    """
    Construye un frame DLT645 completo:
    68 AA AA AA AA AA 68 C L DATA CS 16
    """

    # Dirección (6 bytes invertidos)
    address_inv = reverse_bcd(address_hex)

    # Byte de control para envío (0x11 = lectura)
    control = "11"

    # Longitud de datos
    length = f"{len(data_hex)//2:02X}"

    # Codificar datos (+0x33)
    encoded_data = encode_data(data_hex)

    # Armar sin checksum
    frame = (
        "68" +
        address_inv +
        "68" +
        control +
        length +
        encoded_data
    )

    # Calcular checksum
    cs = checksum(frame)

    # Frame final
    final_frame = frame + cs + "16"
    return final_frame.upper()


def read_commands_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    commands = []

    for cmd in root.findall(".//COMMAND"):

        send = cmd.find("SEND")
        if send is None:
            continue

        cmd_description = send.get("CmdDescription", "")
        cmd_datavalue = send.get("DataValue", "")

        address = ""
        data_field = ""

        for item in send.findall("ITEM"):
            value = item.get("DataValue", "")
            is_reverse = item.get("IsReverse", "0")
            desc = item.get("Description", "")

            # Detectar dirección de medidor
            if "dirección" in desc.lower() or "identificación" in desc.lower() or len(value) == 12:
                address = value

            # Reconocer FE0000xx (comandos)
            if len(value) >= 6 and value.startswith("FE"):
                data_field = reverse_bcd(value)
                continue

            # Más campos de datos
            if value and not value.startswith("FE"):
                if is_reverse == "1":
                    value = reverse_bcd(value)
                data_field += value

        commands.append({
            "description": cmd_description,
            "send_value": cmd_datavalue,
            "address": address,
            "data": data_field
        })

    return commands


def main():
    XML_PATH = "parametros.xml"
    PORT = "COM7"

    commands = read_commands_from_xml(XML_PATH)
    print("Comandos cargados:", len(commands))

    ser = serial.Serial(PORT, 9600, timeout=5)

    for cmd in commands:

        description = cmd["description"]
        send_value = cmd["send_value"]
        address = cmd["address"]
        data_hex = cmd["data"]

        if not address or not data_hex:
            continue

        # Encabezado para cada comando
        print("\n--- Enviando comando ---")
        print(f'CmdDescription="{description}"')
        print(f'DataValue="{send_value}"')
        print("Address:", address)
        print("Data:", data_hex)

        frame = build_dlt645_frame(address, data_hex)
        print("Frame TX:", frame)

        # Enviar frame
        ser.write(bytes.fromhex(frame))
        time.sleep(0.2)

        # Leer respuesta
        rx = ser.read(500)
        rx_hex = rx.hex().upper()
        print("Frame RX:", rx_hex)
        # Extraer campo de datos (después de control y longitud)
        if len(rx_hex) > 20:
            data_section = rx_hex[22:-4]  # ajustar según longitud real

        texto = dlt645_decode_data(data_section)
        print("Decodificado:", texto)

        # Validación básica: si hay respuesta → PASS
        if len(rx_hex) > 0:
            print("PASS")
        else:
            print("FAIL")

    ser.close()


def dlt645_decode_data(data_hex):
    """
    Decodifica datos DLT645:
    - Resta 0x33 a cada byte
    - Convierte a ASCII cuando sea posible
    """
    decoded_bytes = []

    # Convertir de hex string a bytes reales
    for i in range(0, len(data_hex), 2):
        b = int(data_hex[i:i+2], 16)
        dec = (b - 0x33) & 0xFF
        decoded_bytes.append(dec)

    # 2. Ignorar los primeros 3 bytes basura
    if len(decoded_bytes) > 3:
        decoded_bytes = decoded_bytes[3:]
    # Convertir a texto ASCII cuando sea posible
    texto = ""
    for b in decoded_bytes:
        if 32 <= b <= 126:   # rango ASCII imprimible
            texto += chr(b)
        else:
            texto += f"[{b:02X}]"

    return texto


if __name__ == "__main__":
    main()
