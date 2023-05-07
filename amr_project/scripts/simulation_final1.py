#! /usr/bin/env python3


# TODO: import odom msg
# FIXME: find correct odom spelling
# TODO: can we make classes type of stuff?


import rospy
# from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from math import atan2
from pattern_formation import *

# TODO: New Code below till 27
#from flocking import *
import cv2
import sys
import argparse
from imutils.video import VideoStream
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
                default="DICT_ARUCO_ORIGINAL",
                help="type of ArUCo tag to detect")
args = vars(ap.parse_args())


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

    x = msg.pose.position.x
    y = msg.pose.position.y
    rot_q = msg.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll,pitch,theta)


def callback1(msg):
    global x1
    global y1
    global theta1

    x1 = msg.pose.position.x
    y1 = msg.pose.position.y
    rot_q = msg.pose.orientation
    (roll1, pitch1, theta1) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll1,pitch1,theta1)


def callback2(msg):
    global x2
    global y2
    global theta2

    x2 = msg.pose.position.x
    y2 = msg.pose.position.y
    rot_q = msg.pose.orientation
    (roll2, pitch2, theta2) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll2,pitch2,theta2)


def callback3(msg):
    global x3
    global y3
    global theta3

    x3 = msg.pose.position.x
    y3 = msg.pose.position.y
    rot_q = msg.pose.orientationq
    (roll3, pitch3, theta3) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # print(roll3,pitch3,theta3)


rospy.init_node('subscriber')
#sub0 = rospy.Subscriber('/tb3_0/odom', odom, callback0)  # use odom topic
pub0 = rospy.Publisher('/ros0xrobot/cmd_vel', Twist, queue_size=10)
#sub1 = rospy.Subscriber('/tb3_1/odom', odom, callback1)  # use odom topic
#pub1 = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=10)
#sub2 = rospy.Subscriber('/tb3_2/odom', odom, callback2)  # use odom topic
#pub2 = rospy.Publisher('/tb3_2/cmd_vel', Twist, queue_size=10)
#sub3 = rospy.Subscriber('/tb3_3/odom', odom, callback3)  # use odom topic
#pub3 = rospy.Publisher('/tb3_3/cmd_vel', Twist, queue_size=10)

speed0, speed1, speed2, speed3 = Twist(), Twist(), Twist(), Twist()
goal, goal1, goal2, goal3, prev = Point(), Point(), Point(), Point(), Point()
goal.x, goal.y = 500, 500
r = rospy.Rate(4)

# start is x:0, y:0
x, y = 0.0, 0.0
old_x, old_y = x, y  # TODO: New code
theta = atan2(y, x)  # current angle of leader

"""bot1 = (x1, y1) = (0.0, 0.0)
theta1 = atan2(y1, x1)  # current angle of robot1
bot2 = (x2, y2) = (0.0, 0.0)
theta2 = atan2(y2, x2)  # current angle of robot2
bot3 = (x3, y3) = (0.0, 0.0)
theta3 = atan2(y3, x3)  # current angle of robot3
"""

formed = True
goaled = False
#vertices = pattern1(x, y)
#coords = who_goes_where((bot1, bot2, bot3), vertices)
#goal1.x, goal1.y, goal2.x, goal2.y, goal3.x, goal3.y = coords
# TODO: New code below till 231
bots = {}
test = True

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
        args["type"]))
    sys.exit(0)

print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(5.0)

while not rospy.is_shutdown():
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)
    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            bots[markerID] = (cX, cY)

            cv2.putText(frame, str(markerID),
                        (topLeft[0], topLeft[1] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    x, y = bots[11]
    #x1, y1 = bots[2]
    #x2, y2 = bots[3]
    #x3, y3 = bots[4]

    if test:
        speed0, reached0 = move(goal.x, goal.y, x, y, atan2(y, x), speed0, True)
        if reached0:
            print("Reached!!")
            break
        continue

    if not formed:
        speed1, reached1 = move(goal1, x1, y1, theta1, speed1, True)
        speed2, reached2 = move(goal2, x2, y2, theta2, speed2, True)
        speed3, reached3 = move(goal3, x3, y3, theta3, speed3, True)
        if reached1 and reached2 and reached3:
            formed = True
            print("Formation Successful!!")

    else:
        diff = delta((old_x, old_y), (x, y))
        ((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y)) = new_position(
            ((goal1.x, goal1.y), (goal2.x, goal2.y), (goal3.x, goal3.y)), diff)

        #speed0 = move(goal, x, y, theta, speed0)
        speed1 = move(goal1, x1, y1, theta1, speed1)
        speed2 = move(goal2, x2, y2, theta2, speed2)
        speed3 = move(goal3, x3, y3, theta3, speed3)
        old_x, old_y = x, y


    pub0.publish(speed0)
    #pub1.publish(speed1)
    #pub2.publish(speed2)
    #pub3.publish(speed3)

# speed = Twist()
# pub0.publish(speed)
