#!/usr/bin/python

## @file
# Contains classes TrackingReader, TrackingTargetReader and TrackingDefaultReader.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
import avango.daemon
from avango.script import field_has_changed

# import framework libraries
# ...

# import python libraries
# ...


## Reads tracking values of a device registered in daemon.
class TrackingTargetReader(avango.script.Script):

  # output fields
  ## @var sf_mat 
  # The absolute matrix read from the tracking system.
  sf_mat = avango.gua.SFMatrix4()
  sf_mat.value = avango.gua.make_identity_mat()

  ## @var sf_abs_vec
  # Just the translation vector read from the tracking system.
  sf_abs_vec = avango.gua.SFVec3()
  sf_abs_vec.value = avango.gua.Vec3(0.0, 0.0, 0.0)

  ## @var sf_global_mat
  # Tracking matrix without the consideration of the transmitter offset.
  #sf_global_mat = avango.gua.SFMatrix4()
  #sf_global_mat.value = avango.gua.make_identity_mat()


  ## Default constructor.
  def __init__(self):
    self.super(TrackingTargetReader).__init__()

  ## Custom constructor
  # @param TARGET_NAME The target name of the tracked object as chosen in daemon.
  def my_constructor(self, TARGET_NAME):
    
    ## @var sensor
    # A device sensor to capture the tracking values.
    self.sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
    self.sensor.Station.value = TARGET_NAME
    self.sensor.TransmitterOffset.value = avango.gua.make_identity_mat()
    self.sensor.ReceiverOffset.value = avango.gua.make_identity_mat()

    # init field connection
    self.sf_mat.connect_from(self.sensor.Matrix)

  ## Called whenever sf_mat changes.
  @field_has_changed(sf_mat)
  def sf_mat_changed(self):  
    #self.sf_global_mat.value = avango.gua.make_inverse_mat(self.sensor.TransmitterOffset.value) * self.sensor.Matrix.value
    self.sf_abs_vec.value = self.sf_mat.value.get_translate()

  ## Sets the transmitter offset for this tracking reader.
  # @param TRANSMITTER_OFFSET The transmitter offset to be set.
  def set_transmitter_offset(self, TRANSMITTER_OFFSET):
    self.sensor.TransmitterOffset.value = TRANSMITTER_OFFSET

  ## Sets the receiver offset for this tracking reader.
  # @param RECEIVER_OFFSET The receiver offset to be set.
  def set_receiver_offset(self, RECEIVER_OFFSET):
    self.sensor.ReceiverOffset.value = RECEIVER_OFFSET


## Supplies constant tracking values if no real tracking is available.
class TrackingDefaultReader(avango.script.Script):

  # output fields
  ## @var sf_mat 
  # The absolute matrix read from the tracking system.
  sf_mat = avango.gua.SFMatrix4()
  sf_mat.value = avango.gua.make_identity_mat()

  ## @var sf_abs_vec
  # Just the translation vector read from the tracking system.
  sf_abs_vec = avango.gua.SFVec3()
  sf_abs_vec.value = avango.gua.Vec3(0.0, 0.0, 0.0)

  ## @var sf_global_mat
  # Tracking matrix without the consideration of the transmitter offset.
  #sf_global_mat = avango.gua.SFMatrix4()
  #sf_global_mat.value = avango.gua.make_identity_mat()

  ## Default constructor
  def __init__(self):
    self.super(TrackingDefaultReader).__init__()

  ## Sets the transmitter offset for this tracking reader.
  # @param TRANSMITTER_OFFSET The transmitter offset to be set.
  def set_transmitter_offset(self, TRANSMITTER_OFFSET):
    pass

  ## Sets the receiver offset for this tracking reader.
  # @param RECEIVER_OFFSET The receiver offset to be set.
  def set_receiver_offset(self, RECEIVER_OFFSET):
    pass

  ## Sets the constant data to be supplied by this tracking "reader"
  # @param MATRIX The constant matrix to be supplied as tracking values.
  def set_no_tracking_matrix(self, MATRIX):
    self.sf_mat.value = MATRIX
    #self.sf_global_mat.value = MATRIX
    self.sf_abs_vec.value = MATRIX.get_translate()
    
