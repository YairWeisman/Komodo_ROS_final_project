#!/usr/bin/env python
import rospy
import math
from time import sleep
from std_msgs.msg import Float32,Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def turnToExit(data):
	global finalDist
	dist = data.ranges[len(data.ranges)/2]
	speed = 30
	angular_speed = math.radians(speed)
	msg = Twist()
	msg.angular.z = abs(angular_speed)
	if(dist<finalDist-0.5):
		pub.publish(msg)
	else:
		msg.angular.z = 0
		pub.publish(msg)
		pub_exitInfront.publish(True)
		scan_sub.unregister()


def turnAround(data):
	global maxDist
	global angle
	AbsAngle = float(abs(angle))
	speed = 20
	angular_speed = math.radians(speed)

	msg = Twist()
	if angle<0:
		msg.angular.z = abs(angular_speed)
	else:
		msg.angular.z = -abs(angular_speed)
	t0 = rospy.Time.now().to_sec()
	current_angle = 0
	
	relative_angle = math.radians(AbsAngle)
	deviation = 0.01*math.radians(AbsAngle)
	while(current_angle < relative_angle):
		pub.publish(msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)+deviation

		dist = data.ranges[len(data.ranges)/2]
		if maxDist<dist:
			maxDist = dist
	msg.angular.z = 0
	pub.publish(msg)

	if(angle==-110):
		pub_stopTurningToDoor.publish(True)
		scan_sub.unregister()
	elif(angle==-60):
		pub_stopTurningLeft.publish(True)
		scan_sub.unregister()
	elif(angle==128):
		pub_stopTurningRight.publish(maxDist)
		scan_sub.unregister()
	elif(angle==120):
		pub_stopTurningToHall.publish(True)
		scan_sub.unregister()
	elif(angle==80):
		pub_stopTurningToLobby.publish(True)
		scan_sub.unregister()
	elif(angle==-120):
		pub_stopTurningToElev.publish(True)
		scan_sub.unregister()
	elif(angle==-115):
		pub_stopTurningToRed.publish(True)
		scan_sub.unregister()


def callback(data):
	global angle
	global finalDist
	global scan_sub
	if(abs(data.data)<10):
		finalDist = data.data
		print("*******turnToExit******** finalDist:")
		print(finalDist)
		scan_sub = rospy.Subscriber("/scan", LaserScan, turnToExit)
	else:
		angle = data.data
		print("*******turnAround********")
		scan_sub = rospy.Subscriber("/scan", LaserScan, turnAround)

if __name__ == '__main__':
	global maxDist
	maxDist = 0
	rospy.init_node('turnningNode', anonymous=True)	
	rospy.Subscriber('turnAroundTopic', Float32, callback)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	pub_stopTurningToDoor = rospy.Publisher('stopTurningToDoor', Bool, queue_size=10)
	pub_stopTurningLeft = rospy.Publisher('stopLeftSearch', Bool, queue_size=10)
	pub_stopTurningRight = rospy.Publisher('stopRightSearch', Float32, queue_size=10)
	pub_exitInfront = rospy.Publisher('exitInfront', Bool, queue_size=10)
	pub_stopTurningToHall = rospy.Publisher('stopTurningToHall', Bool, queue_size=10)
	pub_stopTurningToLobby = rospy.Publisher('stopTurningToLobby', Bool, queue_size=10)
	pub_stopTurningToElev = rospy.Publisher('stopTurningToElev', Bool, queue_size=10)
	pub_stopTurningToRed = rospy.Publisher('stopTurningToRed', Bool, queue_size=10)
	
	rospy.spin()

