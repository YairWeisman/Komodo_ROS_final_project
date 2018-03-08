


#!/usr/bin/env python
import rospy
import sys
import numpy as np
from std_msgs.msg import Bool,Float32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from time import sleep

foundObject = 0
degreeSpined = 0
distance = -1

def spinAndFind(data):
	global foundObject
	global degreeSpined
	global distance
	pub_checkDist.publish(True)
	rospy.Subscriber('returnDistanceTopic', Float32, updateDistance)
	sleep(5)
	if(distance != -1):
		print("object is in front!")
		foundObject = 1
	while((not foundObject) and degreeSpined<360):
		print("searching...")
		pub_checkDist.publish(True)
		sleep(5)
		# print('dis: ' + str(distance))
		# print('deg: ' + str(degreeSpined))
		# print('found: ' + str(foundObject))
		if(distance != -1):
			foundObject = 1
		else:
			pub_turn.publish(15)
			degreeSpined += 14
		sleep(2)
	if (not(foundObject)):
		print("didn't find red object!")
	foundObject = 0
	degreeSpined = 0
	distance = -1

def updateDistance(data):
	global distance
	global foundObject
	if(float(data.data)!=-1):
		distance = float(data.data)
		foundObject = 1
		# print(distance)

if __name__ == '__main__':
	rospy.init_node('findRedNode', anonymous=True)	
	rospy.Subscriber('findRedTopic', Bool, spinAndFind)
	pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
	pub_checkDist = rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
	rospy.spin()