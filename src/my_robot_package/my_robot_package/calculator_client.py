import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class CalculatorClient(Node):

    def __init__(self):
        super().__init__('calculator_client')

        self.client = self.create_client(
            AddTwoInts,
            'add_two_ints'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for calculator server...')

        self.get_logger().info('Connected to calculator server')

    def send_request(self, a, b):
        request = AddTwoInts.Request()

        request.a = a
        request.b = b

        self.future = self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)

    node = CalculatorClient()

    x = int(input("Enter 1st value: "))
    y = int(input("Enter 2nd value: "))

    node.send_request(x, y)

    rclpy.spin_until_future_complete(node, node.future)

    if node.future.result() is not None:
        response = node.future.result()
        node.get_logger().info(f'Result: {response.sum}')
    else:
        node.get_logger().error('Service call failed')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
