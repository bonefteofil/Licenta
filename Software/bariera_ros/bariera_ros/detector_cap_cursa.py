import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gpiozero import Button

from bariera_ros.config import DETECTOR_INCHIS, DETECTOR_DESCHIS

class DetectorCapCursa(Node):
    def __init__(self):
        super().__init__('detector_cap_cursa')
        
        self.pub_stare = self.create_publisher(Bool, 'senzor/capat', 4)

        # Inițializare butoanele pentru capetele de cursă
        self.detector_inchis = Button(DETECTOR_INCHIS, pull_up=True, bounce_time=0.1)
        self.detector_deschis = Button(DETECTOR_DESCHIS, pull_up=True, bounce_time=0.1)

        # La detectarea capătului de cursă, se publică starea
        self.detector_inchis.when_pressed = lambda: self.publica_capat(True)
        self.detector_deschis.when_pressed = lambda: self.publica_capat(False)

    def publica_capat(self, capat):
        self.pub_stare.publish(Bool(data=capat))

def main(args=None):
    rclpy.init(args=args)
    node = DetectorCapCursa()
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
