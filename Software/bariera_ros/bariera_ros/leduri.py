import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from gpiozero import LED
from bariera_ros.config import PIN_LED_VERDE, PIN_LED_ALBASTRU, PIN_LED_PORTOCALIU


class Leduri(Node):
    def __init__(self):
        super().__init__('led_node')

        self.create_subscription(String, 'comanda/led', self.primire_comanda, 1)
        self.led_verde = LED(PIN_LED_VERDE)
        self.led_albastru = LED(PIN_LED_ALBASTRU)
        self.led_portocaliu = LED(PIN_LED_PORTOCALIU)

    def primire_comanda(self, msg):
        if msg.data == "Verde":
            self.led_verde.on()
            self.led_albastru.off()
            self.led_portocaliu.off()
        elif msg.data == "Albastru":
            self.led_verde.off()
            self.led_albastru.on()
            self.led_portocaliu.off()
        elif msg.data == "Portocaliu":
            self.led_verde.off()
            self.led_albastru.off()
            self.led_portocaliu.on()
        elif msg.data == "Oprit":
            self.led_verde.off()
            self.led_albastru.off()
            self.led_portocaliu.off()
        else:
            self.get_logger().warning("Comandă necunoscută pentru LED-uri.")

def main(args=None):
    rclpy.init(args=args)
    node = Leduri()
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