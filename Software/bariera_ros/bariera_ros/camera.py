import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class Camera(Node):
    def __init__(self):
        super().__init__('camera_node')

        self.publisher = self.create_publisher(Image, 'senzor/imagine', 1)

        self.timer = self.create_timer(3.0, self.publica_imagine)
        self.cv_bridge = CvBridge()

    def publica_imagine(self):
        # Capturare imagine
        imagine = cv2.VideoCapture(0).read()[1]

        if imagine is None:
            self.get_logger().error('Nu am putut citi imaginea de la camera')
            return
        
        # Convertire imagine în format ROS și publicare
        image_message = self.cv_bridge.cv2_to_imgmsg(imagine, encoding='bgr8')
        self.publisher.publish(image_message)


def main(args=None):
    rclpy.init(args=args)
    node = Camera()
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