# Elsabot Jeep Sim

Node used to help simulate certain driver control modes implemented by the base driver of the Jeep (on the Teensy 4.1). This is used during for Gazebo simulation.  For example, when the driver control mode is 'PedalEnablesMovement', the driver must press the acelerator pedal to enable movement when the Jeep is in autonomous control.  

Currently this node emulates PedalEnablesMovement vs. Full control driver control modes.

* If PedalEnablesMovement (2) is published to /driver_control_mode, then True must be published to topic /accel_pedal_pressed
to enable movement.
* If Full (0) is published to /driver_control_mode, then movement is enabled regardless of topic /accel_pedal_pressed.


