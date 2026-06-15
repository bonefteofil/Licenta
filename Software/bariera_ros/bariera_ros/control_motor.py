import rclpy
from time import sleep
from rclpy.node import Node
from std_msgs.msg import Bool
from gpiozero import Motor

from bariera_ros.config import PIN_FORWARD, PIN_BACKWARD, PIN_ENABLE, DURATA_ACTIUNE

class ControlMotor(Node):
    def __init__(self):
        super().__init__('control_motor_node')

        self.create_subscription(Bool, 'comanda/motor', self.pornire_motor, 1)
        self.create_subscription(Bool, 'senzor/capat', self.oprire_motor, 1)  # Oprire motor la atingerea capătului

        # Inițializare motor
        self.motor = Motor(forward=PIN_FORWARD, backward=PIN_BACKWARD, enable=PIN_ENABLE)
        self.timer = None

    def pornire_motor(self, msg):
        if self.timer is not None:
            self.timer.cancel()

        if msg.data:
            self.motor.forward(1.0)  # Ridicare bariera
        else:
            self.motor.backward(1.0)  # Coborâre bariera

        self.timer = self.create_timer(DURATA_ACTIUNE, self.oprire_motor)  # Oprire motor de siguranță

    def oprire_motor(self, msg=None):
        self.motor.stop()
        if self.timer is not None:
            self.timer.cancel()
        self.timer = None

def main(args=None):
    rclpy.init(args=args)
    node = ControlMotor()
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
