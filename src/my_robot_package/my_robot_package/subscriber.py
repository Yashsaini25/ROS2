import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('temperature_subscriber')
        
        self_subscription = self.create_subscription(
            String,
            'temperature',
            self.listener_callback,
            10
        )
        
    def listener_callback(self, msg):
        self.get_logger().info(
            f'Received: {msg.data}'
        )
        
    
def main(args = None):
    rclpy.init(args = args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
    
        
