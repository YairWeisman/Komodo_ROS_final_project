#!/usr/bin/env python
import rospy
import sys
import math
import struct
import numpy as np
import sensor_msgs.point_cloud2 as pc2
from std_msgs.msg import Bool,Float32
from sensor_msgs.msg import PointCloud2

checkedDistFlag = 0

def callback(pc2msg):
	rMax = 255
	rMin = 90
	gMax = 60
	gMin = 0
	bMax = 60
	bMin = 0
	global checkedDistFlag
	if(checkedDistFlag):
		pub_dist = rospy.Publisher('returnDistanceTopic', Float32, queue_size=10)
		checkedDistFlag=0
		n=0
		minDist = sys.maxint
		points = list(pc2.read_points(pc2msg, skip_nans = True,field_names=("x","y","z")))
		for point in points:
			b = np.fromstring(pc2msg.data[n+16], np.uint8)[0]
			g = np.fromstring(pc2msg.data[n+17], np.uint8)[0]
			r = np.fromstring(pc2msg.data[n+18], np.uint8)[0]
			if ((bMin<=b<=bMax) and (gMin<=g<=gMax) and (rMin<=r<=rMax)):
				x = point[0]
				y = point[1]
				z = point[2]
				dist=math.sqrt(pow(x,2)+pow(y,2)+pow(z,2))
				if (dist < minDist):
					minDist = dist
			n+=pc2msg.point_step
		if minDist<sys.maxint:
			print(minDist)
			pub_dist.publish(minDist)
		else:
			print("could not find")
			pub_dist.publish(-1)
		

def checkDistance(data):
	global checkedDistFlag
	checkedDistFlag=1
	scan_sub = rospy.Subscriber("/torso_camera/depth_registered/points", PointCloud2, callback)

if __name__ == '__main__':
	rospy.init_node('checkdistanceNode', anonymous=True)	
	rospy.Subscriber('checkDistanceTopic', Bool, checkDistance)
	rospy.spin()
