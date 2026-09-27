import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TemperaturePublisher(Node):

    def __init__(self):
        super().__init__('temperature_publisher')

        self.publisher = self.create_publisher(
            String,
            'temperature',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_temperature
        )

        self.temperature = 25

    def publish_temperature(self):

        msg = String()

        msg.data = f'Temperature: {self.temperature} C'

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Publishing: {msg.data}'
        )

        self.temperature += 1


def main(args=None):

    rclpy.init(args=args)

    node = TemperaturePublisher()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
