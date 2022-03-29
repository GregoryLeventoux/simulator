from simple_launch import SimpleLauncher
import os

def generate_launch_description():

    sl = SimpleLauncher()
    
    # odometry noise
    sl.declare_arg('linear_noise', 0.01)
    sl.declare_arg('angular_noise', 0.01)
    sl.declare_arg('publish_tf',True)
    
    robot = 'r2d2'
    
    # run RViz
    this_dir = os.path.abspath(os.path.dirname(__file__))
    
    sl.node('rviz2','rviz2', arguments=['-d',this_dir + '/r2d2_beacons.rviz'])
    
    # run simulation
    sl.include('map_simulator','simulation2d_launch.py',launch_arguments={'map_server': 'True'})
    
    ## spawn a few beacons with default covariance / bounds
    beacons = {'beacon1': [-3.4,-4.5],
               'beacon2': [-3.7,3.7],
               'beacon3': [10, 3.6],
               'beacon4': [10, -5.8]}
    for beacon,(x,y) in beacons.items():
        sl.include('map_simulator','spawn_anchor_launch.py',launch_arguments={'frame': beacon, 'x': str(x), 'y': str(y)})
    
    with sl.group(ns=robot):
        
        # spawn in robot namespace to get robot_description
        sl.robot_state_publisher('map_simulator', 'r2d2.xacro', xacro_args={'prefix': robot+'/'})

        sl.node('map_simulator', 'spawn',
                parameters = {'radius': 0.4, 'shape': 'square','static_tf_odom': sl.arg('publish_tf'),
                              'linear_noise': sl.arg('linear_noise'),'angular_noise': sl.arg('angular_noise')})
        
        ## slider to cmd_vel
        sl.node('slider_publisher','slider_publisher',arguments=[sl.find('map_simulator','cmd_vel.yaml')])
        

    return sl.launch_description()
