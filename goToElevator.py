 #!/usr/bin/env python
import rospy
import roslib
import sys
from std_msgs.msg import Bool,Float32
from time import sleep


#! def findRed(data):
#!   pub_findRed = rospy.Publisher('findRedTopic', Bool, queue_size=10)
#!   rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
#!   findRedSub = rospy.Subscriber('returnDistanceTopic', Float32, returnFinalDist)
#!   #! wait for end of moving to elev
#!   sleep(10)
#!   pub_findRed.publish(True)

def returnFinalDist(data):
  distance = float(data.data)
  if(distance != -1):
    print("Found a red object! Distance to the object: %f" %distance)
  else:
    print("could not find")

def findRed(data):
  pub_findRed = rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
  rospy.Subscriber('returnDistanceTopic', Float32, returnFinalDist)
  #! wait for end of turn to red
  sleep(8)
  print("findRed")
  pub_findRed.publish(True)

def turnToRed(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopTurningToRed', Bool, findRed)
  #! wait for end of moving to elev
  sleep(8)
  print("turnToRed")
  pub_turn.publish(-115)

def moveToElev(data):
  pub_forwardMeters = rospy.Publisher('moveForwardMetersTopic', Float32, queue_size=10)
  stopMovingToElev = rospy.Subscriber('stopMovingToElev', Bool, turnToRed)
  #! wait for end of turning to elev
  sleep(4)
  print("moveToElev")
  pub_forwardMeters.publish(10)

def turnLeft(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopTurningToElev', Bool, moveToElev)
  #! wait for end of moving to lobby
  sleep(8)
  print("turnLeft")
  pub_turn.publish(-120)

def moveToLobby(data):
  pub_forwardMeters = rospy.Publisher('moveForwardMetersTopic', Float32, queue_size=10)
  stopMovingToLobby = rospy.Subscriber('stopMovingToLobby', Bool, turnLeft)
  #! wait for end of turn to lobby
  sleep(4)
  print("moveToLobby")
  pub_forwardMeters.publish(3.75)

def turnToLobby(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopTurningToLobby', Bool, moveToLobby)
  #! wait for end of moving in hall
  sleep(6)
  print("turnToLobby")
  pub_turn.publish(80)

def moveInHall(data):
  pub_forward = rospy.Publisher('moveForwardTopic', Float32, queue_size=10)
  rospy.Subscriber('downTheHall', Bool, turnToLobby)
  #! wait for end of turn to hall
  sleep(6)
  print("moveInHall")
  pub_forward.publish(float(1))

def turnToHall(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopTurningToHall', Bool, moveInHall)
  #! wait for end of exit the door
  sleep(6)
  print("turnToHall")
  pub_turn.publish(120)

def exitDoor(data):
  pub_forward = rospy.Publisher('moveForwardTopic', Float32, queue_size=10)
  rospy.Subscriber('outOfRoom', Bool, turnToHall)
  #! wait for end of aiming to door
  sleep(10)
  print("exit door")
  pub_forward.publish(float(0.7))

def aimToDoor(maxDist):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('exitInfront', Bool, exitDoor)
  #! wait for end of spining right
  sleep(10)
  print("maxDist:")
  print(maxDist)
  print("turnning - aiming to door")

  pub_turn.publish(maxDist)

def searchDoorRight(maxDistLeft):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopRightSearch', Float32, aimToDoor)
  #! wait for end of spining left
  sleep(10)
  print("turnning - search door right")

  pub_turn.publish(128)

def searchDoorLeft(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopLeftSearch', Bool, searchDoorRight)
  #! wait for end of getting closer
  sleep(10)
  print("turnning - search door left")
  pub_turn.publish(-60)

def getCloserToDoor(data):
  pub_forwardMeters = rospy.Publisher('moveForwardMetersTopic', Float32, queue_size=10)
  stopGettingCloserToDoor = rospy.Subscriber('stopGettingCloserToDoor', Bool, searchDoorLeft)
  #! wait for end of spining
  sleep(6)
  pub_forwardMeters.publish(1.5)

def turnToDoor(data):
  pub_turn = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
  rospy.Subscriber('stopTurningToDoor', Bool, getCloserToDoor)
  #! wait for end of moving forward
  sleep(6)
  pub_turn.publish(-110)

def startMovement():
  global checkDistSub
  global findRedSub

  
  rospy.init_node('manager', anonymous=True)
  
  pub_forward = rospy.Publisher('moveForwardTopic', Float32, queue_size=10)
  #! pub_checkDist = rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
  #! pub_findRed = rospy.Publisher('findRedTopic', Bool, queue_size=10)
  
  rospy.Subscriber('stopFirstMove', Bool, turnToDoor)
  while(1):
    commandNum = raw_input("Please choose command number: \n 1. Move \n 2. Exit\n")
    if commandNum=='1':
      print 'Moving...'
      pub_forward.publish(float(1.4))
    else: 
      print 'Wrong input'

if __name__ == '__main__':
    try:
      startMovement()
    except rospy.ROSInterruptException:
      pass 


#!       pub_turn.publish(float(90))
#!       sleep(20)
#!       pub_forward.publish(float(1))
#!       sleep(30)
#!       pub_turn.publish(float(90))
#!       sleep(20)
#!       pub_forwardMeters.publish(float(3))
  #! 
  #! pub_turn.publish(float(-90));
  #! pub_forwardMeters.publish(float(9));
  #! pub_turn.publish(float(-90));
  #! print 'Searching for a red object...'
  #! findRedSub = rospy.Subscriber('returnDistanceTopic', Float32, returnFinalDist)
  #! pub_findRed.publish(True);













#! ~/catkin_ws: roslaunch robotican_komodo komodo.launch gazebo:=true world_name:=/users/studs/bsc/2016/nagler/catkin_ws/src/robotican/robotican_common/worlds/assg2.world

#! 1. while(dist>1.5):forward
#! 2. turn -90
#! 3. while(dist>0.5):forward
#! 4. turn 90
#! 5. while(dist>0.5):forward
#! 6. turn 90
#! 7. forward 3m
#! 8. turn -90
#! 9. forward 9m
#! 10. turn -90
#! 11. findRed



#! def getCommand():
#!   global checkDistSub
#!   global findRedSub
#!   rospy.init_node('manager', anonymous=True)
#!   pub_1 = rospy.Publisher('moveForwardTopic', Bool, queue_size=10)
#!   pub_2 = rospy.Publisher('turnAroundTopic', Float32, queue_size=10)
#!   pub_3 = rospy.Publisher('checkDistanceTopic', Bool, queue_size=10)
#!   pub_4 = rospy.Publisher('findRedTopic', Bool, queue_size=10)
#!   while(1):
#!     commandNum = raw_input("Please choose command number: \n 1. Move forward \n 2. Turn around \n 3. Distance to red object \n 4. Find red object \n")
#!     if commandNum=='1':
#!       print 'Moving forward'
#!       pub_1.publish(True)
#!     elif commandNum=='2':
#!       degree = float(raw_input('please choose an angle:\n'))
#!       print("Turning %d degrees" %degree)
#!       pub_2.publish(degree)
#!     elif commandNum=='3':
#!       pub_3.publish(True)
#!       print 'Checking distance...'
#!       checkDistSub = rospy.Subscriber('returnDistanceTopic', Float32, returnDist)
#!     elif commandNum=='4':
#!       print 'Searching for a red object...'
#!       findRedSub = rospy.Subscriber('returnDistanceTopic', Float32, returnFinalDist)
#!       pub_4.publish(True)
#!     else:
#!       print 'Wrong input'


#! def returnDist(data):
#!   global checkDistSub
#!   distance = float(data.data)
#!   if(distance == -1):
#!     print("No red object has found.")
#!   else:
#!     print("Distance to red object: %f" %distance)
#!   checkDistSub.unregister()