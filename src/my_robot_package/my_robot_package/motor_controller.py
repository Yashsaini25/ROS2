import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult


class MotorController(Node):

    def __init__(self):
        super().__init__('motor_controller')

        self.declare_parameter('motor_speed', 50)

        speed = self.get_parameter('motor_speed').value
        self.get_logger().info(f'Motor speed is {speed}%')

        self.add_on_set_parameters_callback(
            self.parameter_callback
        )

    def parameter_callback(self, params):

        for param in params:

            if param.name == 'motor_speed':

                if param.value < 0 or param.value > 100:
                    self.get_logger().warning(
                        'Motor speed must be between 0 and 100!'
                    )

                    return SetParametersResult(
                        successful=False,
                        reason='Motor speed must be between 0 and 100'
                    )

                self.get_logger().info(
                    f'Motor speed changed to {param.value}%'
                )

        return SetParametersResult(successful=True)


def main(args=None):
    rclpy.init(args=args)

    node = MotorController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
