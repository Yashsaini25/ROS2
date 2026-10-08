from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    motor_controller = Node(
        package='my_robot_package',
        executable='motor_controller',
        name='motor_controller',
        output='screen',
        parameters=[
            'config/motor_params.yaml'
        ]
    )

    return LaunchDescription([
        motor_controller
    ])
