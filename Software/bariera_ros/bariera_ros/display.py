import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from RPLCD.i2c import CharLCD
from gpiozero import CPUTemperature 

class Display(Node):
    def __init__(self):
        super().__init__('display_node')

        self.mesaj_ocupare = "L:--/--"

        self.create_subscription(String, 'comanda/display', self.afisare_mesaj, 1)
        self.create_subscription(String, 'client/ocupare', self.afisare_ocupare, 1)
        
        self.LCD = CharLCD('PCF8574', 0x27, cols=16, rows=2, backlight_enabled=True)
        self.LCD.clear()
        self.LCD.write_string("Bine ati venit!")
        self.refresh_data()
        
        self.create_timer(3.0, self.refresh_data)

    def afisare_mesaj(self, msg):
        self.LCD.cursor_pos = (0, 0)
        self.LCD.write_string(" " * 16)
        self.LCD.cursor_pos = (0, 0)
        self.LCD.write_string(msg.data)
        self.refresh_data()

    def afisare_ocupare(self, msg):
        self.LCD.cursor_pos = (1, 0)
        self.LCD.write_string(msg.data)
        self.refresh_data()

    def refresh_data(self):
        cpu = CPUTemperature()
        self.LCD.cursor_pos = (1, 10)
        self.LCD.write_string(f"T:{int(cpu.temperature)}\xdfC")

def main(args=None):
    rclpy.init(args=args)
    node = Display()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            node.destroy_node()
            rclpy.shutdown()
        except Exception:
            pass

if __name__ == '__main__':
    main()