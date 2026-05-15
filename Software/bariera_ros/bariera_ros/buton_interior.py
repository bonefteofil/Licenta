import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gpiozero import Button

from bariera_ros.config import PIN_BUTON

class ButonInterior(Node):
    def __init__(self):
        super().__init__('buton_node')

        self.pub = self.create_publisher(Bool, 'senzor/buton', 4)
        
        self.buton_fizic = Button(PIN_BUTON, bounce_time=0.2)
        self.buton_fizic.when_pressed = self.actiune_buton

    def actiune_buton(self):
        msg = Bool()
        msg.data = True
        self.pub.publish(msg)
        self.get_logger().info("Buton fizic APĂSAT!")

def main(args=None):
    rclpy.init(args=args)
    node = ButonInterior()
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