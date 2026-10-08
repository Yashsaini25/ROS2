import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from my_robot_interfaces.action import MoveRobot


class RobotActionServer(Node):

    def __init__(self):
        super().__init__('robot_action_server')

        self._action_server = ActionServer(
            self,
            MoveRobot,
            'move_robot',
            self.execute_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info(
            'Robot Action Server is ready!'
        )

    def cancel_callback(self, cancel_request):

        self.get_logger().warning(
            'Cancel request received!'
        )

        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):

        target = goal_handle.request.target_position

        self.get_logger().info(
            f'Goal received: Move to {target}'
        )

        feedback_msg = MoveRobot.Feedback()

        for position in range(0, target + 1, 10):

            # Check cancellation
            if goal_handle.is_cancel_requested:

                goal_handle.canceled()

                result = MoveRobot.Result()
                result.final_position = position
                result.success = False

                self.get_logger().warning(
                    f'Movement cancelled at position {position}'
                )

                return result

            feedback_msg.current_position = position
            feedback_msg.progress = int(
                (position / target) * 100
            )

            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f'Position: {position} | '
                f'Progress: {feedback_msg.progress}%'
            )

            time.sleep(1)

        goal_handle.succeed()

        result = MoveRobot.Result()
        result.final_position = target
        result.success = True

        self.get_logger().info(
            f'Reached target position: {target}'
        )

        return result


def main(args=None):

    rclpy.init(args=args)

    node = RobotActionServer()

    executor = MultiThreadedExecutor(
        num_threads=2
    )

    executor.add_node(node)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
