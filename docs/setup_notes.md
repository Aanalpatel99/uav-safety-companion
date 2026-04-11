## ROS 2 Verification
- `ros2 pkg list` returned installed packages successfully
- ROS 2 environment sourced through `/opt/ros/jazzy/setup.bash`
- `ros2 --version` is not a valid verification command

## Next Step
- Clone PX4 into `external/PX4-Autopilot`
- Run `Tools/setup/ubuntu.sh`
- Attempt first SITL launch

## PX4 SITL Verification
- Command used: `make px4_sitl gz_x500`
- Result: [success / error]
- Gazebo launched: [yes / no]
- Drone visible: [yes / no]
- Notes: