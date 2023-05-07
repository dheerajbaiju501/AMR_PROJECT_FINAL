#! /usr/bin/env python3


# TODO: import odom msg
# FIXME: find correct odom spelling
# TODO: can we make classes type of stuff?


import rospy
from nav_msgs.msg import Odometry
# from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from math import atan2
from pattern_formation2 import *


def move(goal, x, y, theta, speed, need_reach=False):
    if need_reach:
        reached = False
    inc_x = goal.x - x  # distance robot to goal in x
    inc_y = goal.y - y  # distance robot to goal in y
    angle_to_goal = atan2(inc_y, inc_x)  # calculate angle through distance from robot to
    # print(str(angle_to_goal) + " " + str(theta))

    if (angle_to_goal - theta) > 0.1:
        speed.linear.x, speed.angular.z = 0.0, 0.05

    elif (theta - angle_to_goal) > 0.1:
        speed.linear.x, speed.angular.z = 0.0, -0.05

    else:
        speed.linear.x, speed.angular.z = 0.1, 0.0  # drive towards goal

        if (inc_x == 0):
            reached = True
            speed.linear.x, speed.angular.z = 0.0, 0.0

    if need_reach:
        return speed, reached

    return speed


def callback0(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll,pitch,theta)


def callback1(msg):
    global x1
    global y1
    global theta1

    x1 = msg.pose.pose.position.x
    y1 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll1, pitch1, theta1) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll1,pitch1,theta1)


def callback2(msg):
    global x2
    global y2
    global theta2

    x2 = msg.pose.pose.position.x
    y2 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll2, pitch2, theta2) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll2,pitch2,theta2)


def callback3(msg):
    global x3
    global y3
    global theta3

    x3 = msg.pose.pose.position.x
    y3 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll3, pitch3, theta3) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


def callback4(msg):
    global x4
    global y4
    global theta4

    x4 = msg.pose.pose.position.x
    y4 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll4, pitch4, theta4) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


def callback5(msg):
    global x5
    global y5
    global theta5

    x5 = msg.pose.pose.position.x
    y5 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll5, pitch5, theta5) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])


def callback6(msg):
    global x6
    global y6
    global theta6

    x6 = msg.pose.pose.position.x
    y6 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll6, pitch6, theta6) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])



rospy.init_node('subscriber')
sub0 = rospy.Subscriber('/tb3_0/odom', Odometry, callback0)  # use odom topic
pub0 = rospy.Publisher('/ros0xrobot/cmd_vel', Twist, queue_size=10)
sub1 = rospy.Subscriber('/tb3_1/odom', Odometry, callback1)  # use odom topic
pub1 = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=10)
sub2 = rospy.Subscriber('/tb3_2/odom', Odometry, callback2)  # use odom topic
pub2 = rospy.Publisher('/tb3_2/cmd_vel', Twist, queue_size=10)
sub3 = rospy.Subscriber('/tb3_3/odom', Odometry, callback3)  # use odom topic
pub3 = rospy.Publisher('/tb3_3/cmd_vel', Twist, queue_size=10)
sub4 = rospy.Subscriber('/tb3_4/odom', Odometry, callback4)  # use odom topic
pub4 = rospy.Publisher('/tb3_4/cmd_vel', Twist, queue_size=10)
sub5 = rospy.Subscriber('/tb3_5/odom', Odometry, callback5)  # use odom topic
pub5 = rospy.Publisher('/tb3_5/cmd_vel', Twist, queue_size=10)
sub6 = rospy.Subscriber('/tb3_6/odom', Odometry, callback6)  # use odom topic
pub6 = rospy.Publisher('/tb3_6/cmd_vel', Twist, queue_size=10)


speed0, speed1, speed2, speed3, speed4, speed5, speed6 = Twist(), Twist(), Twist(), Twist(), Twist(), Twist(), Twist()
goal, goal1, goal2, goal3, goal4, goal5, goal6, prev = Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point()
#goal.x, goal.y = 500, 500
r = rospy.Rate(4)

# start is x:0, y:0
x, y = 0.0, 0.0
x1, y1 = 4.0, 4.0
x2, y2 = -4.0, 7.0
x3, y3 = 8.0, 5.0
x4, y4 = 8.0, -5.0
x5, y5 = 6.0, -2.0
x6, y6 = 3.0, -3.0
old_x, old_y = x, y  # TODO: New code
theta1 = atan2(y1, x1)  # current angle of leader
theta2 = atan2(y2, x2)
theta3 = atan2(y3, x3)
theta4 = atan2(y4, x4)
theta5 = atan2(y5, x5)
theta6 = atan2(y6, x6)

formed = False
num = 6
vertices = pattern(x, y)
coords = who_goes_where(((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6)), vertices, num)
((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y), (goal4.x, goal4.y), (goal5.x, goal5.y), (goal6.x, goal6.y)) = coords
print(coords)
#speeds = [speed0, speed1, speed2, speed3, speed4, speed5, speed6]
#reached = [False, False, False, False, False, False]

while not rospy.is_shutdown():

    if not formed:
        speed1, reached1 = move(goal1, x1, y1, theta1, speed1, True)
        speed2, reached2 = move(goal2, x2, y2, theta2, speed2, True)
        speed3, reached3 = move(goal3, x3, y3, theta3, speed3, True)
        speed4, reached4 = move(goal4, x4, y4, theta4, speed4, True)
        speed5, reached5 = move(goal5, x5, y5, theta5, speed5, True)
        speed6, reached6 = move(goal6, x6, y6, theta6, speed6, True)
        print(goal1)
        print(goal2)
        if reached1 and reached2 and reached3 and reached4 and reached5 and reached6:
            formed = True
            print("Formation Successful!!")

    else:
        diff = delta((old_x, old_y), (x, y))
        ((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y), (goal4.x, goal4.y), (goal5.x, goal5.y), (goal6.x, goal6.y)) = new_position(
            ((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y), (goal4.x, goal4.y), (goal5.x, goal5.y), (goal6.x, goal6.y)), diff)

        #speed0 = move(goal, x, y, theta, speed0)
        speed1 = move(goal1, x1, y1, theta1, speed1)
        speed2 = move(goal2, x2, y2, theta2, speed2)
        speed3 = move(goal3, x3, y3, theta3, speed3)
        speed4 = move(goal3, x4, y4, theta4, speed4)
        speed5 = move(goal3, x5, y5, theta5, speed5)
        speed6 = move(goal3, x6, y6, theta6, speed6)
        old_x, old_y = x, y


    #pub0.publish(speed0)
    pub1.publish(speed1)
    pub2.publish(speed2)
    pub3.publish(speed3)
    pub4.publish(speed4)
    pub5.publish(speed5)
    pub6.publish(speed6)
