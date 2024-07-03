import math, time, rclpy
from rclpy.node import Node
from rclpy.exceptions import ParameterNotDeclaredException

import rclpy.utilities
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class DrawSquare(Node):

    # ===== CONSTRUCTORS =====
    def __init__(self):
        super().__init__('draw_square_control')
        self.declare_parameter("model_name", "")

        self.__setModelName()

        self.__pubs = {
            "cmd_vel": {
                "pub": None,
                "topic": "/diff_drive_controller/cmd_vel_unstamped",
                "type": Twist,
                "QoS": 10,
                "rate": None
            }
        }

        self.setPublishers()

    # ===== SETTERS =====

    def __setModelName(self):
        try:
            self.__model_name = self.get_parameter("model_name").get_parameter_value().string_value
        except ParameterNotDeclaredException:
            self.__model_name = None
            self.get_logger().warning("model_name parameter not declared. Declare it in run command using --ros-args -p model_name:=my_model. Not using model_name as namespace.")

    def setPublishers(self):
        for tag, pub_info in self.__pubs.items():
            if(pub_info["rate"] == None):

                if self.getModelName() == None:
                    topic_prefix = ""
                else:
                    topic_prefix = "/"+self.getModelName()

                pub_info["pub"] = self.create_publisher(pub_info["type"], topic_prefix + pub_info["topic"], pub_info["QoS"])
            else:
                pass

    # ===== GETTERS =====

    def getModelName(self):
        return self.__model_name

    # ===== METHODS =====

    def setVelocities(self, clock, v_x = 0.0, v_y = 0.0, omega_z = 0.0):
        vels = Twist()
        vels.linear.x = v_x
        vels.linear.y = v_y
        vels.angular.z = omega_z

        startTime = time.time()
        while(time.time() - startTime < clock):
            self.__pubs["cmd_vel"]["pub"].publish(vels)

def main(args=None):
    rclpy.init(args=args)
    control_node = DrawSquare()

    #rclpy.spin(control_node)
    for i in range(4):
        control_node.setVelocities(6, v_x = 0.5)
        control_node.setVelocities(10.5, omega_z=math.radians(15))
    control_node.setVelocities(1)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()