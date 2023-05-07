#! /usr/bin/env python3
import rospy
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from math import atan2
from math import atan
 
#start is x:0, y:0
x = 0.0
y = 0.0
theta = atan2(y, x)    #current angle of robot
 
#import ipdb; ipdb.set_trace()
 
def callback(msg):
    goal = Point()
    goal.x = 2.0
    goal.y = 3.1
    speed = Twist()
    global x
    global y
    global theta
 
    x = msg.pose[1].position.x
    y = msg.pose[1].position.y
    rot_q = msg.pose[1].orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    
    inc_x = goal.x - x                      #distance robot to goal in x
    inc_y = goal.y - y                      #distance robot to goal in y
    angle_to_goal = atan2 (inc_y, inc_x)    #calculate angle through distance from robot to 
    
    if abs(angle_to_goal - theta) > 0.1:
    	
    	speed.linear.x = 0.0
    	speed.angular.z = 1.0
    else:
        speed.linear.x = 0.3                #drive towards goal
        speed.angular.z = 0.0
        
        if (inc_x==0):
        	speed.linear.x = 0.0
        	speed.angular.z = 0.0
    pub.publish(speed)
 
 
if __name__=='__main__':
    rospy.init_node ('subscriber')
    sub = rospy.Subscriber('/gazebo/model_states', ModelStates, callback)
    pub = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=1)
 
    
 
    r = rospy.Rate(4)
    rospy.spin()
 

 

 
