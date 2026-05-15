from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bariera_ros',
            executable='controller',
            name='controller_node',
            output='screen'
        ),
        Node(
            package='bariera_ros',
            executable='camera',
            name='camera_node',
            output='screen'
        ),
        Node(
            package='bariera_ros',
            executable='identificare_numar',
            name='identificator_node',
            output='screen'
        ),
        Node(
            package='bariera_ros',
            executable='client',
            name='client_node',
            output='screen'
        ),
        # Node(
        #     package='bariera_ros',
        #     executable='display',
        #     name='display_node',
        #     output='screen'
        # ),
        Node(
            package='bariera_ros',
            executable='control_motor',
            name='control_motor_node',
            output='screen'
        ),
        # Node(
        #     package='bariera_ros',
        #     executable='buton_interior',
        #     name='buton_node',
        #     output='screen'
        # ),
        # Node(
        #     package='bariera_ros',
        #     executable='senzor_masina',
        #     name='senzor_masina_node',
        #     output='screen'
        # ),
        # Node(
        #     package='bariera_ros',
        #     executable='leduri',
        #     name='led_node',
        #     output='screen'
        # ),
    ])
