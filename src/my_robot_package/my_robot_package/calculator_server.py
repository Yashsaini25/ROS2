import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class CalculatorServer(Node):

    def __init__(self):
        super().__init__('calculator_server')

        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_callback
        )

        self.get_logger().info('Calculator server is ready')

    def add_callback(self, request, response):
        response.sum = request.a + request.b

        self.get_logger().info(
            f'Received: {request.a} + {request.b}'
        )

        return response


def main(args=None):
    rclpy.init(args=args)

    node = CalculatorServer()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
