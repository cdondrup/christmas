#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import roslib
from bayes_people_tracker.msg import PeopleTracker
from sound_play.libsoundplay import SoundClient
from threading import Thread
import actionlib
import topological_navigation.msg


class Santa(object):
    def __init__(self, name):
        rospy.loginfo("Starting %s ..." % name)
        self.sound = roslib.packages.get_pkg_dir('christmas') + '/sounds/santa.wav'
        self.sub = rospy.Subscriber("/people_tracker/positions", PeopleTracker, self.callback, queue_size=1)
        self.client = actionlib.SimpleActionClient('topological_navigation', topological_navigation.msg.GotoNodeAction)
        self.client.wait_for_server()
        self.thread = Thread(target=self.drive)
        rospy.loginfo("... done")

    def callback(self, msg):
        if msg.min_distance < 2.0:
            soundhandle = SoundClient()
            rospy.sleep(rospy.Duration(1))
            soundhandle.playWave(self.sound)
            rospy.sleep(rospy.Duration(2))
            soundhandle.stopAll()

    def drive(self):
        targets = ["Sofas", "Kitchen"]
        cnt = 0
        while not rospy.is_shutdown():
            navgoal = topological_navigation.msg.GotoNodeGoal()
            navgoal.target = targets[cnt]
            cnt += 1
            cnt = cnt % 2
            self.client.send_goal(navgoal)#,self.done_cb, self.active_cb, self.feedback_cb)
            self.client.wait_for_result()
            rospy.sleep(60.)


if __name__ == "__main__":
    rospy.init_node("santa")
    Santa(rospy.get_name())
    rospy.spin()

