 #!/usr/bin/env python
import rospy
import roslib
import sys
from std_msgs.msg import Bool,Float32


def returnDist(data):
  global checkDistSub
  distance = float(data.data)
  if(distance == -1):
    print("No red object has found.")
  else:
    print("Distance to red object: %f" %distance)
  checkDistSub.unregister()

def returnFinalDist(data):
  distance = float(data.data)
  if(distance != -1):
    print("Found a red object! Distance to the object: %f" %distance)
    findRedSub.unregister()


def getCommand():
  global checkDistSub
  global findRedSub
  rospy.init_node('manager', anonymous=True)
  pub_1 = rospy.Publisher('moveForwardTopic', Bool, queue_size=10)
  pub_2 = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  pub_3 = rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
  pub_4 = rospy.Publisher('findRedTopic', Bool, queue_size=10)
  while(1):
    commandNum = raw_input("Please choose command number: \n 1. Move forward \n 2. Turn around \n 3. Distance to red object \n 4. Find red object \n")
    if commandNum=='1':
      print 'Moving forward'
      pub_1.publish(True)
    elif commandNum=='2':
      degree = float(raw_input('please choose an angle:\n'))
      print("Turning %d degrees" %degree)
      pub_2.publish(degree)
    elif commandNum=='3':
      pub_3.publish(True)
      print 'Checking distance...'
      checkDistSub = rospy.Subscriber('returnDistanceTopic', Float32, returnDist)
    elif commandNum=='4':
      print 'Searching for a red object...'
      findRedSub = rospy.Subscriber('returnDistanceTopic', Float32, returnFinalDist)
      pub_4.publish(True)
    else:
      print 'Wrong input'

if __name__ == '__main__':
    try:
      getCommand()
    except rospy.ROSInterruptException:
      pass 
    
# ~/catkin_ws: roslaunch robotican_komodo komodo.launch gazebo:=true world_name:=/users/studs/bsc/2016/nagler/catkin_ws/src/robotican/robotican_common/worlds/assg2.world
