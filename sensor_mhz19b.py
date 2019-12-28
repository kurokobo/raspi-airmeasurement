import serial

# Define onstant values
STARTING_BYTE = int.from_bytes(b"\xff", "big")
COMMAND_BYTE = int.from_bytes(b"\x86", "big")


def read():
    ser = serial.Serial(
        "/dev/ttyS0",
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0,
    )
    ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    s = ser.read(9)

    if s[0] == STARTING_BYTE and s[1] == COMMAND_BYTE:
        co2concentration = s[2] * 256 + s[3]
        return {"co2concentration": co2concentration}

    return {"co2concentration": 0}
