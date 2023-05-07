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
from pattern_formation import *
# from math import atan


def move(goal, x, y, theta, speed, need_reach=False):
    if need_reach:
        reached = False
    inc_x = goal.x - x  # distance robot to goal in x
    inc_y = goal.y - y  # distance robot to goal in y
    # calculate angle through distance from robot to
    angle_to_goal = atan2(inc_y, inc_x)
    # print(str(angle_to_goal) + " " + str(theta))

    if (angle_to_goal - theta) > 0.1:
        speed.linear.x, speed.angular.z = 0.0, 0.5

    elif (theta - angle_to_goal) > 0.1:
        speed.linear.x, speed.angular.z = 0.0, -0.5

    else:
        speed.linear.x, speed.angular.z = 0.3, 0.0  # drive towards goal

        if (abs(inc_x) <= 0.2 and abs(inc_y) <= 0.2):
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
    (roll, pitch, theta) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll,pitch,theta)


def callback1(msg):
    global x1
    global y1
    global theta1

    x1 = msg.pose.pose.position.x
    y1 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll1, pitch1, theta1) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll1,pitch1,theta1)


def callback2(msg):
    global x2
    global y2
    global theta2

    x2 = msg.pose.pose.position.x
    y2 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll2, pitch2, theta2) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll2,pitch2,theta2)


def callback3(msg):
    global x3
    global y3
    global theta3

    x3 = msg.pose.pose.position.x
    y3 = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll3, pitch3, theta3) = euler_from_quaternion(
        [rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll3,pitch3,theta3)


rospy.init_node('subscriber')
sub0 = rospy.Subscriber('/tb3_0/odom', Odometry, callback0)  # use odom topic
pub0 = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=10)
sub1 = rospy.Subscriber('/tb3_1/odom', Odometry, callback1)  # use odom topic
pub1 = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=10)
sub2 = rospy.Subscriber('/tb3_2/odom', Odometry, callback2)  # use odom topic
pub2 = rospy.Publisher('/tb3_2/cmd_vel', Twist, queue_size=10)
sub3 = rospy.Subscriber('/tb3_3/odom', Odometry, callback3)  # use odom topic
pub3 = rospy.Publisher('/tb3_3/cmd_vel', Twist, queue_size=10)


speed0, speed1, speed2, speed3 = Twist(), Twist(), Twist(), Twist()
goal, goal1, goal2, goal3 = Point(), Point(), Point(), Point()
goal.x, goal.y = 2.0, 3.1
r = rospy.Rate(4)

# start is x:0, y:0
x, y = 0.0, 0.0
theta = atan2(y, x)  # current angle of leader

bot1 = (x1, y1) = (4.0, 4.0)
theta1 = atan2(y1, x1)  # current angle of robot1
bot2 = (x2, y2) = (7.0, -5.0)
theta2 = atan2(y2, x2)  # current angle of robot2
bot3 = (x3, y3) = (-6.0, 5.0)
theta3 = atan2(y3, x3)  # current angle of robot3

formed = False
vertices = pattern1(x, y)
coords = who_goes_where((bot1, bot2, bot3), vertices)
((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y)) = coords

di = {1: [], 2: [], 3: []}

while not rospy.is_shutdown():
    if not formed:
        speed1, reached1 = move(goal1, x1, y1, theta1, speed1, True)
        speed2, reached2 = move(goal2, x2, y2, theta2, speed2, True)
        speed3, reached3 = move(goal3, x3, y3, theta3, speed3, True)
        """if reached1:
            print("bot 1 reached", goal1.x, goal1.y, x1, y1)
        if reached2:
            print("bot 2 reached", goal2.x, goal2.y, x2, y2)
        if reached3:
            print("bot 3 reached", goal3.x, goal3.y, x3, y3)"""

        if reached1 and reached2 and reached3:
            formed = True
            print("Formation Successful!!")

    else:
        vertices = pattern1(x, y)
        coords = who_goes_where(((x1,y1), (x2,y2), (x3,y3)), vertices)
        ((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y)) = coords
        #speed0 = move(goal, x, y, theta, speed0)
        """
        di[1].append((x1, y1, goal1.x, goal1.y))
        di[2].append((x2, y2, goal2.x, goal2.y))
        di[3].append((x3, y3, goal3.x, goal3.y))
        """
        #print(str(x) + " " + str(y))
        

        speed1 = move(goal1, x1, y1, theta1, speed1)
        speed2 = move(goal2, x2, y2, theta2, speed2)
        speed3 = move(goal3, x3, y3, theta3, speed3)

    #pub0.publish(speed0)
    pub1.publish(speed1)
    pub2.publish(speed2)
    pub3.publish(speed3)

# speed = Twist()
# pub0.publish(speed)

print(di[1])
print(di[2])
print(di[3])



