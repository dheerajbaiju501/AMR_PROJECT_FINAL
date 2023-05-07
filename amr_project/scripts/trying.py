#! /usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from math import atan2

#start is x:0, y:0
x = 0.0
y = 0.0
theta = 0.0  # current angle of robot

#import ipdb; ipdb.set_trace()


def callback(msg):
    global x
    global y
    global theta

    x = msg.pose[1].position.x
    y = msg.pose[1].position.y
    rot_q = msg.pose[1].orientation
    (roll, pitch, theta) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])


rospy.init_node('subscriber')
sub = rospy.Subscriber('/gazebo/model_states', ModelStates, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

speed = Twist()

r = rospy.Rate(4)

goal = Point()
goal.x = -5
goal.y = -1

while not rospy.is_shutdown():
    inc_x = goal.x - x  # distance robot to goal in x
    inc_y = goal.y - y  # distance robot to goal in y
    # calculate angle through distance from robot to goal in x and y
    angle_to_goal = atan2(inc_y, inc_x)
    
    # 0.1 because it too exact for a robot if both angles should be exactly 0
    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.0
        speed.angular.z = 0.3
    else:
        speed.linear.x = 0.3  # drive towards goal
        speed.angular.z = 0.0

    pub.publish(speed)

r.sleep()
