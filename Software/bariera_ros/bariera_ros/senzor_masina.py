import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gpiozero import DistanceSensor

PIN_TRIGGER = 17
PIN_ECHO = 18
DISTANTA_MAX = 2.0 # metri
DISTANTA_PRAG = 0.5 # metri

class SenzorMasina(Node):
    def __init__(self):
        super().__init__('senzor_masina')
        
        self.pub_prezenta = self.create_publisher(Bool, 'senzor/masina', 4)
        self.senzor_distanta = DistanceSensor(
            echo=PIN_ECHO,
            trigger=PIN_TRIGGER,
            max_distance=DISTANTA_MAX,
            threshold_distance=DISTANTA_PRAG
        )
        
        self.senzor_distanta.when_in_range = lambda: self.publica_stare(True)
        self.senzor_distanta.when_out_of_range = lambda: self.publica_stare(False)

    def publica_stare(self, masina_prezenta):
        msg = Bool()
        msg.data = masina_prezenta
        self.pub_prezenta.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SenzorMasina()
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
