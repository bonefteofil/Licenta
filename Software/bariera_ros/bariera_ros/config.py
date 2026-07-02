
# Motor
PIN_ENABLE = 17
PIN_FORWARD = 27
PIN_BACKWARD = 22
DURATA_ACTIUNE = 12.0 # secunde
VITEZA_MOTOR = 1.0

# Display
PIN_SDA = 2
PIN_SCL = 3

# Senzor masină
PIN_TRIGGER = 23
PIN_ECHO = 24
DISTANTA_MAX = 2.0 # metri
DISTANTA_PRAG = 0.5 # metri

# LED-uri
PIN_LED_PORTOCALIU = 12
PIN_LED_ALBASTRU = 16
PIN_LED_VERDE = 20

# Buton de urgență
PIN_BUTON = 5

# Senzor cap de cursa
DETECTOR_DESCHIS = 13
DETECTOR_INCHIS = 26

# Camera
INTERVAL_FOTOGRAFIERE = 4.0 # secunde


# Client
BARIERA_ID = 6512
IP_SERVER = "172.20.10.3:8000"

URL_HTTP = f"http://{IP_SERVER}/api/bariere/{BARIERA_ID}/validare"
URL_WS = f"ws://{IP_SERVER}/api/bariere/ws/{BARIERA_ID}"
