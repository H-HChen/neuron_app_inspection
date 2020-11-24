import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, GroupAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions.node import Node

import pdb
def generate_launch_description():
    # Path
    nb2_launch_dir = os.path.join(get_package_share_directory('neuronbot2_bringup'), 'launch')
    nb2nav_launch_dir = os.path.join(get_package_share_directory('neuronbot2_nav'), 'launch')
    nb2nav_map_dir = os.path.join(get_package_share_directory('neuronbot2_nav'), 'map')

    # Parameters
    open_rviz = LaunchConfiguration('open_rviz', default='True')
    map_path = LaunchConfiguration('map', default=nb2nav_map_dir+'/mememan.yaml')

    neuron_app_bringup = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nb2_launch_dir, 'bringup_launch.py'))),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nb2nav_launch_dir, 'bringup_launch.py')),
            launch_arguments={'open_rviz': open_rviz,
                              'map': map_path}.items()),
    ])

    image_saver = Node(
        package='image_view',
        executable='image_saver',
        parameters=[{'image': 'ros2_openvino_toolkit/image_rviz'}],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(neuron_app_bringup)
    ld.add_action(image_saver)
    return ld
