'''
作者: 小鱼
公众号: 鱼香ROS
QQ交流群: 2642868461
描述: RoateAnimation类
'''
from threading import Thread
from queue import Queue
import transforms3d as tfs
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
import rclpy
import math


class RoateAnimation(Node):
    def __init__(self,name="roatate",div=0.001):
        super().__init__(name)
        self.queue = Queue()
        self.trans_frames = {}
        self.broadcaster = TransformBroadcaster(self)
        self.rate = self.create_rate(100)
        self.thread = Thread(name="t_thread",target=self.transform_thread)
        self.thread.start()
        self.div = div

        
    def add_transform(self,parent,name,tran=[0.0,0.0,0.0],rotate=[0.0,0.0,0.0],order="sxyz"):
        if len(rotate)==3:
            for i in range(3):
                rotate[i] = math.radians(rotate[i])
        self.trans_frames[name] = {"name":name,"parent":parent,
                                   "target_rotate":rotate,"target_tran":tran,
                                   "current_rotate":[0.0,0.0,0.0],"current_tran":[0.0,0.0,0.0],
                                   "order":order}
        
        
    def destory_all(self):
        """
        取消所有的旋转变换
        """
        self.trans_frames.clear()
    
    def _get_transform_msg(self,parent,name,tran=[0.0,0.0,0.0],rotate=[0.0,0.0,0.0],order="sxyz"):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = parent
        t.child_frame_id = name
        t.transform.translation.x = tran[0]
        t.transform.translation.y = tran[1]
        t.transform.translation.z = tran[2]
        if len(rotate)==3:
            rotate = tfs.euler.euler2quat(rotate[0],rotate[1],rotate[2],order)
            t.transform.rotation.x = rotate[1]
            t.transform.rotation.y = rotate[2] 
            t.transform.rotation.z = rotate[3]
            t.transform.rotation.w = rotate[0]
        return t
    
    def _tick_once(self):
        for name in self.trans_frames.keys():
            if self.trans_frames[name]["current_tran"][0]<self.trans_frames[name]["target_tran"][0]:
                self.trans_frames[name]["current_tran"][0] += self.div
            elif self.trans_frames[name]["current_tran"][1]<self.trans_frames[name]["target_tran"][1]:
                self.trans_frames[name]["current_tran"][1] += self.div
            elif self.trans_frames[name]["current_tran"][2]<self.trans_frames[name]["target_tran"][2]:
                self.trans_frames[name]["current_tran"][2] += self.div
                
            elif self.trans_frames[name]["current_rotate"][0]<self.trans_frames[name]["target_rotate"][0]:
                self.trans_frames[name]["current_rotate"][0] += self.div    
            elif self.trans_frames[name]["current_rotate"][1]<self.trans_frames[name]["target_rotate"][1]:
                self.trans_frames[name]["current_rotate"][1] += self.div                
            elif self.trans_frames[name]["current_rotate"][2]<self.trans_frames[name]["target_rotate"][2]:
                self.trans_frames[name]["current_rotate"][2] += self.div 
            else:
                self.trans_frames[name]["current_rotate"] = [0.0,0.0,0.0]
                self.trans_frames[name]["current_tran"] = [0.0,0.0,0.0]
            
    def transform_thread(self):
        while rclpy.ok():
            self._tick_once()
            for name in self.trans_frames.keys():
                msg = self._get_transform_msg(self.trans_frames[name]['parent'],self.trans_frames[name]['name'],
                                                self.trans_frames[name]['current_tran'],
                                                self.trans_frames[name]['current_rotate'],
                                                self.trans_frames[name]['order'])
                self.broadcaster.sendTransform(msg)
            self.rate.sleep()