import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

# Emulate some control implemented by robot base driver
# 1. Accel pedal used as movement enable/disable control.
#    Filter cmd_vel message based on mock 'accel_pedal_pressed'
#    topic and 'driver_control_mode' topic which is normally
#    used to select this mode.

class ControlFilter(Node):

    def __init__(self):
        super().__init__('elsabot_jeep_control_sim')
        self.sub_accel_pedal_pressed = self.create_subscription(
            Bool,
            '/accel_pedal_pressed',
            self.listener_accel_pedal_pressed,
            10)
        self.sub_accel_pedal_pressed  # prevent unused variable warning

        self.sub_driver_control_mode = self.create_subscription(
            Int8,
            '/driver_control_mode',
            self.listener_driver_control_mode,
            10)
        self.sub_driver_control_mode  # prevent unused variable warning

        self.sub_cmd_vel = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_cmd_vel,
            1)
        self.sub_cmd_vel  # prevent unused variable warning


        self.pub_cmd_vel = self.create_publisher(Twist, 'cmd_vel_filtered', 1)

        self.pedal_pressed = False
        self.driver_control_mode = 0


    def listener_accel_pedal_pressed(self, msg):
        self.pedal_pressed = msg.data

    def listener_driver_control_mode(self, msg):
        self.driver_control_mode = msg.data

    def listener_cmd_vel(self, msg):
        if self.driver_control_mode == 2:
            if not self.pedal_pressed:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                self.get_logger().debug("Accel pedal not pressed, forcing stop")

        self.get_logger().debug("Pub cmd_vel: %f, mode: %d, pressed: %d" \
            % (msg.linear.x, self.driver_control_mode, self.pedal_pressed))
        self.pub_cmd_vel.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    control_filter = ControlFilter()

    rclpy.spin(control_filter)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control_filter.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()