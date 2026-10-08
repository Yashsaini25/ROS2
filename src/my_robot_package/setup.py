from setuptools import find_packages, setup

package_name = 'my_robot_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
	('share/' + package_name + '/config',
		['config/motor_params.yaml']),
	('share/' + package_name + '/launch',
		['launch/robot_launch.py']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yash',
    maintainer_email='yash@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
       		 'publisher = my_robot_package.publisher:main',
		'subscriber = my_robot_package.subscriber:main',
		'calculator_server = my_robot_package.calculator_server:main',
		'calculator_client = my_robot_package.calculator_client:main',
		'motor_controller = my_robot_package.motor_controller:main',
		'move_robot_server = my_robot_package.move_robot_server:main',
		'move_robot_client = my_robot_package.move_robot_client:main',
        ],
    },
)
