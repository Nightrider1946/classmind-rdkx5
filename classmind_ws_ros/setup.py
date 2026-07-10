from setuptools import find_packages, setup
from glob import glob
import os


package_name = "classmind_ros"


setup(
    name=package_name,
    version="0.0.0",

    packages=find_packages(
        exclude=["test"]
    ),

    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name]
        ),
        (
            "share/" + package_name,
            ["package.xml"]
        ),
        (
            os.path.join(
                "share",
                package_name,
                "launch"
            ),
            glob("launch/*.launch.py")
        ),
    ],

    install_requires=[
        "setuptools"
    ],

    zip_safe=True,

    maintainer="Narendra Andhale",

    maintainer_email="andhalenarendra2@gmail.com",

    description=(
        "ClassMind ROS 2 sensor bridge "
        "and classroom decision system"
    ),

    license="MIT",

    tests_require=[
        "pytest"
    ],

    entry_points={
        "console_scripts": [
            "sensor_bridge = classmind_ros.sensor_bridge_node:main",
            "decision = classmind_ros.decision:main"
        ],
    },
)