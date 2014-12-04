#!/usr/bin/python

import avango
import avango.gua
import avango.script
import avango.daemon
from avango.script import field_has_changed

class TUIOCursor(avango.script.Script):
    PosX                = avango.SFFloat()
    PosY                = avango.SFFloat()
    SpeedX              = avango.SFFloat()
    SpeedY              = avango.SFFloat()
    MotionSpeed         = avango.SFFloat()
    MotionAcceleration  = avango.SFFloat()
    IsMoving            = avango.SFBool()
    State               = avango.SFFloat()
    SessionID           = avango.SFFloat()
    CursorID            = avango.SFInt()
    IsTouched           = avango.SFBool()
    MovementVector      = avango.gua.SFVec2()

    def __init__(self):
        self.super(TUIOCursor).__init__()

        # initialize fields
        self.PosX.value           = -1.0
        self.PosY.value           = -1.0
        self.State.value          =  4.0
        self.SessionID.value      = -1.0
        self.MovementVector.value = avango.gua.Vec2(0, 0)

        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.PosX.connect_from(self.device_sensor.Value0)
        self.PosY.connect_from(self.device_sensor.Value1)
        self.SpeedX.connect_from(self.device_sensor.Value2)
        self.SpeedY.connect_from(self.device_sensor.Value3)
        self.MotionSpeed.connect_from(self.device_sensor.Value4)
        self.MotionAcceleration.connect_from(self.device_sensor.Value5)
        self.IsMoving.connect_from(self.device_sensor.Value6)
        self.State.connect_from(self.device_sensor.Value7)
        self.SessionID.connect_from(self.device_sensor.Value8)
        

    def updateTouched(self):
        """
        Call whenever some touch input data has changed. This method will update self.IsTouched accordingly.
        """
        self.IsTouched.value = (self.PosX.value != -1.0 and self.PosY.value != -1.0)

    @field_has_changed(CursorID)
    def set_station(self):
        """
        Set station name.
        """
        self.device_sensor.Station.value = "gua-finger{}#cursor".format(self.CursorID.value)

    @field_has_changed(PosX)
    def updatePosX(self):
        self.updateTouched()

    @field_has_changed(PosY)
    def updatePosY(self):
        self.updateTouched()


class TUIOHand(avango.script.Script):
    HandClass  = avango.SFFloat()
    Finger1SID = avango.SFFloat()
    Finger2SID = avango.SFFloat()
    Finger3SID = avango.SFFloat()
    Finger4SID = avango.SFFloat()
    Finger5SID = avango.SFFloat()
    FingerSIDs = avango.MFFloat()
    SessionID  = avango.SFFloat()
    HandID     = avango.SFInt()

    CLASS_UNKNOWN = 0
    CLASS_LEFT    = 1
    CLASS_RIGHT   = 2

    def __init__(self):
        self.super(TUIOHand).__init__()

        self.FingerSIDs.value = [-1.0, -1.0, -1.0, -1.0, 1.0]
        self.SessionID.value  = -1.0
        self.Finger1SID.value = -1.0
        self.Finger2SID.value = -1.0
        self.Finger3SID.value = -1.0
        self.Finger4SID.value = -1.0
        self.Finger5SID.value = -1.0

        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.HandClass.connect_from(self.device_sensor.Value0)
        self.Finger1SID.connect_from(self.device_sensor.Value1)
        self.Finger2SID.connect_from(self.device_sensor.Value2)
        self.Finger3SID.connect_from(self.device_sensor.Value3)
        self.Finger4SID.connect_from(self.device_sensor.Value4)
        self.Finger5SID.connect_from(self.device_sensor.Value5)
        self.SessionID.connect_from(self.device_sensor.Value6)

    @field_has_changed(HandID)
    def set_station(self):
        """
        Set station name.
        """
        self.device_sensor.Station.value = "gua-finger{}#hand".format(self.HandID.value)

    @field_has_changed(Finger1SID)
    def updateFinger1InField(self):
        self.FingerSIDs.value[0] = self.Finger1SID.value

    @field_has_changed(Finger2SID)
    def updateFinger2InField(self):
        self.FingerSIDs.value[1] = self.Finger2SID.value

    @field_has_changed(Finger3SID)
    def updateFinger3InField(self):
        self.FingerSIDs.value[2] = self.Finger3SID.value

    @field_has_changed(Finger4SID)
    def updateFinger4InField(self):
        self.FingerSIDs.value[3] = self.Finger4SID.value

    @field_has_changed(Finger5SID)
    def updateFinger5InField(self):
        self.FingerSIDs.value[4] = self.Finger5SID.value