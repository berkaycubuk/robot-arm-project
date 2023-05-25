import yaml
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
from robo_arm.servo import Servo
import math

# load config file
with open(r'/home/jnuu/robot-arm/config.yaml') as file:
    config = yaml.safe_load(file)

robot_config = config["robot"]

class Controls():
    def __init__(self):
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(robot_config["pwm_frequency"])
        self.base_servo = Servo(self.pwm, robot_config["base"]["pin"], robot_config["base"]["start_angle"])
        self.left_servo = Servo(self.pwm, robot_config["left"]["pin"], robot_config["left"]["start_angle"])
        self.right_servo = Servo(self.pwm, robot_config["right"]["pin"], robot_config["right"]["start_angle"])
        self.gripper_servo = Servo(self.pwm, robot_config["gripper"]["pin"], robot_config["gripper"]["start_angle"])

        self.base_offset = robot_config["base"]["offset"]
        self.left_offset = robot_config["left"]["offset"]
        self.right_offset = robot_config["right"]["offset"]

        self.angle_base = 0
        self.angle_left = 0
        self.angle_right = 0

        # in millimeter
        self.pos_x = 80
        self.pos_y = 0
        self.pos_z = 80

        # initial position
        self.move_to(80, 0, 80)

    def set_angles(self, base, left, right):

        # if self.angle_base == 0 and self.angle_left == 0 and self.angle_right == 0:
        #     self.angle_base = base
        #     self.angle_left = left
        #     self.angle_right = right

        #     self.base_servo.setAngle(base, True)
        #     self.left_servo.setAngle(left, True)
        #     self.right_servo.setAngle(right, True)
        #     return

        # running = True
        # while running:
        #     if self.angle_base != base:
        #         if self.angle_base > base:
        #             self.angle_base -= 1            
        #         else:
        #             self.angle_base += 1            

        #     if self.angle_left != left:
        #         if self.angle_left > left:
        #             self.angle_left -= 1            
        #         else:
        #             self.angle_left += 1            

        #     if self.angle_right != right:
        #         if self.angle_right > right:
        #             self.angle_right -= 1            
        #         else:
        #             self.angle_right += 1            

        #     if self.angle_base == base and self.angle_left == left and self.angle_right == right:
        #         running = False

        self.left_servo.setAngle(left, True)
        self.right_servo.setAngle(right, True)
        self.base_servo.setAngle(base, True)

    def move_to(self, x, y, z):
        b = math.atan2(y, x) * (180/math.pi) # base angle
        l = math.sqrt(x*x + y*y) # - gripper_length # x and y extension
        h = math.sqrt(l*l + z*z)
        phi = math.atan(z/l) * (180/math.pi)
        theta = math.acos((h/2)/80) * (180/math.pi)
        # theta = (backarm_length*backarm_length + h*h - forearm_length*forearm_length) / (2 * backarm_length * h) * (180/math.pi)

        a1 = phi + theta
        a2 = phi - theta

        a1 *= -1
        b *= -1

        b_servo = b + self.base_offset
        l_servo = a2 + self.left_offset
        r_servo = a1 + self.right_offset

        self.set_angles(int(b_servo), int(l_servo), int(r_servo))
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def move_up(self, length):
        self.move_to(self.pos_x, self.pos_y, self.pos_z + length)

    def move_down(self, length):
        self.move_to(self.pos_x, self.pos_y, self.pos_z - length)

    def move_left(self, length):
        self.move_to(self.pos_x, self.pos_y - length, self.pos_z)

    def move_right(self, length):
        self.move_to(self.pos_x, self.pos_y + length, self.pos_z)

    def move_forward(self, length):
        self.move_to(self.pos_x + length, self.pos_y, self.pos_z)

    def move_backward(self, length):
        self.move_to(self.pos_x - length, self.pos_y, self.pos_z)

    def gripper_pick(self):
        self.gripper_servo.setAngle(robot_config["gripper"]["min_angle"], True)

    def gripper_drop(self):
        self.gripper_servo.setAngle(robot_config["gripper"]["max_angle"], True)

    def __del__(self):
        self.pwm.exit_PCA9685()
        GPIO.cleanup()
