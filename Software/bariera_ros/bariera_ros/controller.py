import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool

class Controller(Node):
    def __init__(self):
        super().__init__('controller_node')
        
        self.create_subscription(String, 'senzor/numar', self.primire_numar, 1)
        self.create_subscription(Bool, 'senzor/buton', self.primire_autorizare, 1)
        self.create_subscription(Bool, 'client/permisiune', self.primire_autorizare, 1)
        
        self.pub_led = self.create_publisher(String, 'comanda/led', 1)
        self.pub_actiune = self.create_publisher(Bool, 'comanda/miscare', 1)
        self.pub_display = self.create_publisher(String, 'comanda/display', 1)
        self.pub_validare = self.create_publisher(String, 'client/verificare', 1)
        
        self.timer = None
        self.ultimul_numar = None
        self.bariera_deschisa = False
        self.reset()


    def primire_numar(self, msg):
        self.get_logger().info(f'Numar primit: {msg.data}, ultimul numar: {self.ultimul_numar}')
        if self.ultimul_numar is None:
            self.pub_led.publish(String(data="Albastru"))
            self.pub_display.publish(String(data=f'Validare:{msg.data}'))
            self.pub_validare.publish(msg)
            self.ultimul_numar = msg.data

    def primire_autorizare(self, msg):
        if self.timer is not None:
            self.timer.cancel()

        if msg.data:
            self.get_logger().info('Acces aprobat - Ridicare bariera')
            self.pub_led.publish(String(data="Verde"))
            self.pub_actiune.publish(Bool(data=True))
            self.pub_display.publish(String(data="Acces permis!"))
            
            self.bariera_deschisa = True
            self.timer = self.create_timer(12.0, self.reset)
        else:
            self.get_logger().info('Acces refuzat - Bariera ramane inchisa')
            self.pub_display.publish(String(data="Acces refuzat!"))
            self.pub_led.publish(String(data="Portocaliu"))
            self.timer = self.create_timer(5.0, self.reset)

    def reset(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
            
        self.pub_led.publish(String(data="Oprit"))
        self.pub_display.publish(String(data="Bine ati venit!"))
        self.pub_actiune.publish(Bool(data=False))
        
        self.ultimul_numar = None
        self.bariera_deschisa = False

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
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