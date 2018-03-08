#!/usr/bin/env python
import rospy
from time import sleep
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan	
from std_msgs.msg import Float32
import math

def goForward(data):
	msg = Twist()
	msg.linear.x = 0.1
	angular_speed = math.radians(0.5)
	msg.angular.z = -abs(angular_speed)

	for i in range(0,int(data.data*8)):
		pub.publish(msg)
		sleep(1)

	msg.linear.x = 0.0
	msg.angular.z = 0.0
	pub.publish(msg)

	if(data.data==1.5):
		print(data.data)
		pub_stopGettingCloserToDoor.publish(True)
	elif(data.data==3.75):
		pub_stopMovingToLobby.publish(True)
	elif(data.data==10):
		pub_stopMovingToElev.publish(True)


if __name__ == '__main__':
	rospy.init_node('forwardByMetersNode', anonymous=True)	
	rospy.Subscriber('moveForwardMetersTopic', Float32, goForward)
	
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	pub_stopGettingCloserToDoor = rospy.Publisher('stopGettingCloserToDoor', Bool, queue_size=10)
	pub_stopMovingToLobby = rospy.Publisher('stopMovingToLobby', Bool, queue_size=10)
	pub_stopMovingToElev = rospy.Publisher('stopMovingToElev', Bool, queue_size=10)
	
	rospy.spin()
