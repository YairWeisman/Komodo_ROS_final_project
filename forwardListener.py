#!/usr/bin/env python
import rospy
import math
from time import sleep
from std_msgs.msg import Float32,Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

goForwardFlag = 0
minDist = 0
def callback(data):
	global goForwardFlag
	global minDist
	global scan_subscriber
	
	center=data.ranges[len(data.ranges)/2]
	msg = Twist()
	print(center)
	if((math.isnan(center))or(center>minDist and goForwardFlag)):
		msg.linear.x = 0.1
		#! changes
		angular_speed = math.radians(0.1)
		msg.angular.z = -abs(angular_speed)
		#!end changes
		pub.publish(msg)
	else:
		msg.linear.x = 0.0
		#! changes
		msg.angular.z - 0.0
		#!end changes
		pub.publish(msg)
		goForwardFlag = 0
		if(minDist<1.45 and minDist>1.35):
			pub_finishstopFirstMove.publish(True)
			scan_subscriber.unregister()
		elif(minDist>0.65 and minDist<0.75):
			pub_outOfRoom.publish(True)
			scan_subscriber.unregister()
		elif(minDist>0.95 and minDist<1.05):
			pub_downTheHall.publish(True)
			scan_subscriber.unregister()

	

def goForward(data):
	global goForwardFlag
	global minDist
	global scan_subscriber
	goForwardFlag=1
	minDist = data.data
	scan_subscriber = rospy.Subscriber("/scan", LaserScan, callback)
	


if __name__ == '__main__':
	rospy.init_node('forwardNode', anonymous=True)	
	rospy.Subscriber('moveForwardTopic', Float32, goForward)
	
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	pub_finishstopFirstMove = rospy.Publisher('stopFirstMove', Bool, queue_size=10)
	pub_outOfRoom = rospy.Publisher('outOfRoom', Bool, queue_size=10)
	pub_downTheHall = rospy.Publisher('downTheHall', Bool, queue_size=10)
	
	rospy.spin()
