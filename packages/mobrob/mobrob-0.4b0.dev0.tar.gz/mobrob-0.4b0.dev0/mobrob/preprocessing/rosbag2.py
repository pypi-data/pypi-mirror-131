import numpy as np
import pandas as pd
from mobrob.utils import euler_from_quaternion


# https://github.com/ros2/rosbag2/issues/473
import sqlite3
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message

class BagFileParser():
    def __init__(self, bag_file):
        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

        ## create a message type map
        topics_data = self.cursor.execute("SELECT id, name, type FROM topics").fetchall()
        self.topic_type = {name_of:type_of for id_of,name_of,type_of in topics_data}
        self.topic_id = {name_of:id_of for id_of,name_of,type_of in topics_data}
        self.topic_msg_message = {name_of:get_message(type_of) for id_of,name_of,type_of in topics_data}

    def __del__(self):
        self.conn.close()

    # Return [(timestamp0, message0), (timestamp1, message1), ...]
    def get_messages(self, topic_name):
        
        topic_id = self.topic_id[topic_name]
        # Get from the db
        rows = self.cursor.execute("SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
        # Deserialise all and timestamp them
        return [ (timestamp,deserialize_message(data, self.topic_msg_message[topic_name])) for timestamp, data in rows]  


def df_from_twist(twist, t0=0): # t0 is a time offset that is subtracted
    twist_df = pd.DataFrame(columns=['time', 'v', 'omega'])
    for (t, twist) in twist:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        v = twist.linear.x
        omega = twist.angular.z
        twist_df = twist_df.append({'time': time, 'v': v, 'omega': omega}, ignore_index=True)
    return twist_df


def df_from_joy(joy, t0=0): # t0 is a time offset that is subtracted
    joy_df = pd.DataFrame(columns=['time', 'x', 'y'])
    for (t, joy) in joy:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        y = joy.axes[0]
        x = joy.axes[1]
        joy_df = joy_df.append({'time': time, 'x': x, 'y': y}, ignore_index=True)
    return joy_df

    
def df_from_odometry(odom, t0=0): # t0 is a time offset that is subtracted
    odom_df = pd.DataFrame(columns=['time', 'x', 'y', 'yaw'])
    for (t, odom) in odom:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        x = odom.pose.pose.position.x
        y = odom.pose.pose.position.y
        roll, pitch, yaw = euler_from_quaternion(odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w)
        v = odom.twist.twist.linear.x
        omega = odom.twist.twist.angular.z
        odom_df = odom_df.append({'time': time, 'x': x, 'y': y, 'yaw': yaw, 'v': v, 'omega': omega}, ignore_index=True)
    return odom_df  
    
    
def df_from_int32(int_32, t0=0): # t0 is a time offset that is subtracted
    int32_df = pd.DataFrame(columns=['time', 'value'])
    for (t, int_32) in int_32:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        value = int_32.data
        int32_df = int32_df.append({'time': time, 'value': value}, ignore_index=True)
    return int32_df


def df_from_float32(float_32, t0=0): # t0 is a time offset that is subtracted
    float32_df = pd.DataFrame(columns=['time', 'value'])
    for (t, float_32) in float_32:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        value = float_32.data
        float32_df = float32_df.append({'time': time, 'value': value}, ignore_index=True)
    return float32_df


# TODO: move to separate file
# t265-specific 
# https://github.com/IntelRealSense/librealsense/blob/master/doc/t265.md

def df_from_t265_accel(imu, t0=0):
    imu_df = pd.DataFrame(columns=['time',  'a_x', 'a_y'])
    for (t, imu) in imu:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        a_x = -imu.linear_acceleration.z
        a_y = -imu.linear_acceleration.x
        imu_df = imu_df.append({'time': time, 'a_x': a_x, 'a_y': a_y}, ignore_index=True)
    return imu_df

def df_from_t265_gyro(imu, t0=0):
    imu_df = pd.DataFrame(columns=['time', 'omega'])
    for (t, imu) in imu:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        omega = imu.angular_velocity.y
        imu_df = imu_df.append({'time': time, 'omega': omega}, ignore_index=True)
    return imu_df


def df_from_t265_odom(odom, t0=0): # t0 is a time offset that is subtracted
    odom_df = pd.DataFrame(columns=['time', 'x', 'y', 'yaw', 'v', 'omega'])
    for (t, odom) in odom:
        time = (t - t0) / 1000000 # time in nano-seconds (10^-9) - > / 10^6 -> milli-seconds
        x = odom.pose.pose.position.x
        y = odom.pose.pose.position.y
        roll, pitch, yaw = euler_from_quaternion(odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w)
        v = - odom.twist.twist.linear.z
        omega = odom.twist.twist.angular.y
        odom_df = odom_df.append({'time': time, 'x': x, 'y': y, 'yaw': yaw, 'v': v, 'omega': omega}, ignore_index=True)
    return odom_df  








