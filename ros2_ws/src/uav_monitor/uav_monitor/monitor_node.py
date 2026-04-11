import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

from px4_msgs.msg import VehicleStatus


class UavMonitorNode(Node):
    def __init__(self):
        super().__init__('uav_monitor_node')
        self.get_logger().info('UAV Monitor node started.')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.last_state = None

        self.subscription = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status_v3',
            self.vehicle_status_callback,
            qos_profile
        )

    def get_arming_state_label(self, arming_state):
        arming_map = {
            1: 'DISARMED',
            2: 'ARMED'
        }
        return arming_map.get(arming_state, f'UNKNOWN({arming_state})')

    def get_nav_state_label(self, nav_state):
        nav_map = {
            0: 'MANUAL',
            1: 'ALTCTL',
            2: 'POSCTL',
            3: 'AUTO_MISSION',
            4: 'AUTO_LOITER',
            5: 'AUTO_RTL',
            10: 'ACRO',
            14: 'OFFBOARD',
            15: 'STABILIZED',
            17: 'AUTO_TAKEOFF',
            18: 'AUTO_LAND',
            21: 'ORBIT'
        }
        return nav_map.get(nav_state, f'UNKNOWN({nav_state})')

    def vehicle_status_callback(self, msg):
        current_state = (
            msg.arming_state,
            msg.nav_state,
            msg.failsafe,
            msg.pre_flight_checks_pass
        )

        if current_state != self.last_state:
            arming_label = self.get_arming_state_label(msg.arming_state)
            nav_label = self.get_nav_state_label(msg.nav_state)

            self.get_logger().info(
                f'Arming: {arming_label} | '
                f'Nav: {nav_label} | '
                f'Failsafe: {msg.failsafe} | '
                f'Preflight checks pass: {msg.pre_flight_checks_pass}'
            )

            if not msg.pre_flight_checks_pass:
                self.get_logger().warn('Safety warning: preflight checks are not passing.')

            if msg.failsafe:
                self.get_logger().error('Safety alert: vehicle is in FAILSAFE state.')

            self.last_state = current_state


def main(args=None):
    rclpy.init(args=args)
    node = UavMonitorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Shutting down UAV Monitor node...')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()