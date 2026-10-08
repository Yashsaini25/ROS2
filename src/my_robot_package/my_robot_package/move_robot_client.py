import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from my_robot_interfaces.action import MoveRobot


class RobotActionClient(Node):

    def __init__(self):
        super().__init__('robot_action_client')

        self._action_client = ActionClient(
            self,
            MoveRobot,
            'move_robot'
        )

        self.goal_handle = None
        self._cancel_timer = None

    def send_goal(self):

        self.get_logger().info(
            'Waiting for action server...'
        )

        self._action_client.wait_for_server()

        goal_msg = MoveRobot.Goal()
        goal_msg.target_position = 100

        self.get_logger().info(
            'Sending goal: 100'
        )

        send_goal_future = (
            self._action_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback
            )
        )

        send_goal_future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:

            self.get_logger().warning(
                'Goal rejected'
            )

            return

        self.get_logger().info(
            'Goal accepted'
        )

        self.goal_handle = goal_handle

        # Cancel after 3 seconds
        self._cancel_timer = self.create_timer(
            3.0,
            self.cancel_goal
        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Position: {feedback.current_position} | '
            f'Progress: {feedback.progress}%'
        )

    def cancel_goal(self):

        # Stop the timer so cancellation happens only once
        self._cancel_timer.cancel()

        self.get_logger().warning(
            'Sending cancellation request...'
        )

        cancel_future = (
            self.goal_handle.cancel_goal_async()
        )

        cancel_future.add_done_callback(
            self.cancel_callback
        )

    def cancel_callback(self, future):

        cancel_response = future.result()

        self.get_logger().info(
            f'Cancel response: {cancel_response}'
        )

        if len(cancel_response.goals_canceling) > 0:

            self.get_logger().info(
                'Cancellation accepted by server.'
            )

        else:

            self.get_logger().warning(
                'Cancellation was not accepted.'
            )

        # Now wait for the final action result
        result_future = self.goal_handle.get_result_async()

        result_future.add_done_callback(
            self.result_callback
        )

    def result_callback(self, future):

        result = future.result()

        status = result.status
        action_result = result.result

        self.get_logger().info(
            f'Action finished with status: {status}'
        )

        self.get_logger().info(
            f'Final position: '
            f'{action_result.final_position}'
        )

        self.get_logger().info(
            f'Success: '
            f'{action_result.success}'
        )

        rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    node = RobotActionClient()

    node.send_goal()

    rclpy.spin(node)

    node.destroy_node()


if __name__ == '__main__':
    main()
