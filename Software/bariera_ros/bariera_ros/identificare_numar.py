import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from fast_alpr import ALPR

class IdentificareNumar(Node):
    def __init__(self):
        super().__init__('indentificator_node')

        self.primire_imagine = self.create_subscription(Image, 'senzor/imagine', self.primire_imagine, 1)
        self.trimitere_numar = self.create_publisher(String, 'senzor/numar', 2)

        self.cv_bridge = CvBridge()
        self.alpr = ALPR(
            detector_model="yolo-v9-t-384-license-plate-end2end",
            ocr_model="cct-xs-v1-global-model",
        )

    def primire_imagine(self, msg):
            imagine = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            rezultate = self.alpr.predict(imagine)
            numar = "".join(filter(str.isalnum, rezultate[0].ocr.text)).upper() if rezultate else ""
            self.trimitere_numar.publish(String(data=numar or ""))

def main(args=None):
    rclpy.init(args=args)
    node = IdentificareNumar()
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
