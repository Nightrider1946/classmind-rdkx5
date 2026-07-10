import json
import os
import time
import requests
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


# =====================================
# ESP32 CONFIGURATION
# =====================================

ESP32_IP = os.getenv(
    "CLASSMIND_ESP32_IP",
    "10.139.104.208"
)


class DecisionNode(Node):

    def __init__(self):

        super().__init__(
            "classmind_decision_node"
        )

        # =====================================
        # MQ SENSOR CONFIGURATION
        # =====================================

        self.baseline_samples = deque(
            maxlen=10
        )

        self.baseline = None

        # Relative ADC rise required for alert
        self.alert_delta = 250

        # =====================================
        # ALERT STATE
        # =====================================

        self.alert_active = False

        self.alert_start_time = None

        # Minimum visible alert duration
        self.alert_hold_seconds = 10.0

        # =====================================
        # ROS SUBSCRIBER
        # =====================================

        self.gas_subscription = (
            self.create_subscription(
                String,
                "/classmind/gas",
                self.gas_callback,
                10
            )
        )

        self.get_logger().info(
            "ClassMind Decision Node started"
        )

        self.get_logger().info(
            f"ESP32 IP: {ESP32_IP}"
        )

        self.get_logger().info(
            "Waiting for MQ sensor baseline..."
        )

        self.clear_alert()

        self.get_logger().info(
            "ESP32 startup state reset"
        )


    # =====================================
    # GAS SENSOR CALLBACK
    # =====================================

    def gas_callback(self, message):

        try:

            sensor_data = json.loads(
                message.data
            )

            raw_adc = int(
                sensor_data["raw_adc"]
            )

            # =================================
            # BASELINE CALIBRATION
            # =================================

            if self.baseline is None:

                self.baseline_samples.append(
                    raw_adc
                )

                self.get_logger().info(
                    "MQ calibration "
                    f"{len(self.baseline_samples)}/10 "
                    f"ADC={raw_adc}"
                )

                if (
                    len(self.baseline_samples)
                    == 10
                ):

                    self.baseline = int(
                        sum(self.baseline_samples)
                        / len(self.baseline_samples)
                    )

                    self.get_logger().info(
                        "MQ baseline established: "
                        f"{self.baseline}"
                    )

                return


            # =================================
            # SENSOR DELTA
            # =================================

            sensor_delta = (
                raw_adc
                - self.baseline
            )

            self.get_logger().info(
                f"MQ ADC={raw_adc} | "
                f"Baseline={self.baseline} | "
                f"Delta={sensor_delta}"
            )


            # =================================
            # ALERT ACTIVATION
            # =================================

            if (
                sensor_delta >= self.alert_delta
                and not self.alert_active
            ):

                self.alert_active = True

                self.alert_start_time = time.time()

                self.get_logger().warning(
                    "Elevated MQ raw sensor "
                    "signal detected"
                )

                self.trigger_alert()


            # =================================
            # ALERT ACTIVE
            # =================================

            elif self.alert_active:

                alert_elapsed = (
                    time.time()
                    - self.alert_start_time
                )

                self.get_logger().info(
                    f"Alert active | "
                    f"Hold={alert_elapsed:.1f}/"
                    f"{self.alert_hold_seconds:.1f}s"
                )

                # Clear after fixed hold period
                if (
                    alert_elapsed
                    >= self.alert_hold_seconds
                ):

                    self.alert_active = False

                    self.alert_start_time = None

                    self.get_logger().info(
                        "Alert hold period completed"
                    )

                    self.clear_alert()


        except (
            json.JSONDecodeError,
            KeyError,
            ValueError
        ) as error:

            self.get_logger().error(
                f"Invalid gas message: {error}"
            )


    # =====================================
    # ESP32 ALERT ACTIVATION
    # =====================================

    def trigger_alert(self):

        try:

            response = requests.get(
                f"http://{ESP32_IP}/red",
                timeout=2
            )

            response.raise_for_status()

            self.get_logger().warning(
                "ESP32 alert state activated"
            )

        except requests.RequestException as error:

            self.get_logger().error(
                "ESP32 alert command failed: "
                f"{error}"
            )


    # =====================================
    # ESP32 ALERT CLEAR
    # =====================================

    def clear_alert(self):

        try:

            response = requests.get(
                f"http://{ESP32_IP}/off",
                timeout=2
            )

            response.raise_for_status()

            self.get_logger().info(
                "ESP32 alert state cleared"
            )

        except requests.RequestException as error:

            self.get_logger().error(
                "ESP32 clear command failed: "
                f"{error}"
            )


# =====================================
# MAIN
# =====================================

def main(args=None):

    rclpy.init(args=args)

    node = DecisionNode()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        node.get_logger().info(
            "Decision Node shutdown requested"
        )

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":

    main()