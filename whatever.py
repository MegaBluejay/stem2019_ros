#!/usr/bin/env python

import os
import rospy
import time
from duckietown_msgs.msg import AprilTagsWithInfos, BoolStamped, WheelsCmdStamped
from duckietown_msgs.srv import SetFSMState
from std_msgs.msg import Header
from sensor_msgs.msg import CompressedImage

should_take_photo = False

rospy.init_node('whatever')

just_stop_already = rospy.Publisher('/kfc/wheels_driver_node/emergency_stop', BoolStamped, queue_size=10)
the_thing = rospy.ServiceProxy('/kfc/fsm_node/set_state', SetFSMState)
vel= rospy.Publisher('/kfc/wheels_driver_node/wheels_cmd', WheelsCmdStamped, queue_size = 1)
a=0
def listener(msg):
	global should_take_photo
	vel_msg = WheelsCmdStamped()
	if any(info.traffic_sign_type==5 for info in msg.infos):
		os.system("~/killThing.sh")
		time.sleep(3.63)
		vel_msg.vel_right = 0.0
		vel_msg.vel_left = 0.0
		time.sleep(0.1)
		vel.publish(vel_msg)
		the_thing('JOYSTICK_CONTROL')
		vel.publish(vel_msg)
		should_take_photo=True
				
def camera_sub_callback(msg):
	global should_take_photo
	global a
	
	if not should_take_photo or a:
		return
	a=1
	time.sleep(1.3)
	photo = open('/home/user/Desktop/cam'+str(rospy.get_time())+'.jpg', 'w+')
	photo.write(msg.data)

sub = rospy.Subscriber("/kfc/apriltags_postprocessing_node/apriltags_out", AprilTagsWithInfos, listener)
camera_sub = rospy.Subscriber("/kfc/camera_node/image/compressed", CompressedImage, camera_sub_callback)

rospy.spin()
