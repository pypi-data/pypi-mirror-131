from setuptools import setup

package_name = 'fishrotate'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools','transforms3d'],
    zip_safe=True,
    maintainer='fishros',
    maintainer_email='fishros@foxmail.com',
    description='基于ROS2旋转可视化工具',
    license='OSI Approved :: BSD License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
             'fishrotate = fishrotate.fishrotate:main',
        ],
    },
)
