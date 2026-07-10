import json
import time
import requests

import rclpy

from rclpy.node import Node

from std_msgs.msg import String

from ai_engine.config import ESP32_IP


class SensorBridgeNode(Node):

    def __init__(self):

        super().__init__(
            "classmind_sensor_bridge"
        )

        self.publisher = self.create_publisher(
            String,
            "/classmind/gas",
            10
        )

        self.timer = self.create_timer(
            2.0,
            self.read_sensor
        )

        self.get_logger().info(
            "ClassMind MQ sensor bridge started"
        )

    def read_sensor(self):

        try:

            response = requests.get(
                f"http://{ESP32_IP}/gas",
                timeout=2
            )

            response.raise_for_status()

            sensor_data = response.json()

            # RDK-side timestamp
            sensor_data["rdk_timestamp"] = time.time()

            message = String()

            message.data = json.dumps(
                sensor_data
            )

            self.publisher.publish(
                message
            )

            self.get_logger().info(
                f"Gas sensor published: "
                f"ADC={sensor_data['raw_adc']}"
            )

        except requests.RequestException as error:

            self.get_logger().error(
                f"ESP32 sensor communication failed: {error}"
            )

        except (
            ValueError,
            KeyError
        ) as error:

            self.get_logger().error(
                f"Invalid sensor data: {error}"
            )


def main(args=None):

    rclpy.init(
        args=args
    )

    node = SensorBridgeNode()

    try:

        rclpy.spin(
            node
        )

    except KeyboardInterrupt:

        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":

    main()