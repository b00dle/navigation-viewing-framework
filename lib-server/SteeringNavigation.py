#!/usr/bin/python

## @file
# Contains class SteeringNavigation.

### import avango-guacamole libraries
import avango
import avango.gua
import avango.script

### import framework libraries
from Device           import *
#from GroundFollowing  import *
#from InputMapping     import *
from Intersection       import *
from Navigation       import *
import Utilities
from scene_config import scenegraphs

### import python libraries
import math


## Representation of a steering navigation controlled by a 6-DOF device. Creates the device,
# an InputMapping instance and a GroundFollowing instance.
#
# Furthermore, this class reacts on the device's button inputs and toggles the 3-DOF (realistic) / 6-DOF (unrealistic) 
# navigation mode. When switching from unrealistic to realistic mode, an animation is triggered in which the matrix
# is rotated back in an upright position (removal of pitch and roll angle).
class SteeringNavigation(Navigation):

  ### additional fields ###

  ## input fields
  
  ## @var mf_rel_input_values
  # The relative input values of the device.
  mf_rel_input_values = avango.MFFloat()
  
  ## @var sf_reset_trigger
  # Boolean field to indicate if the navigation is to be reset.
  sf_reset_trigger = avango.SFBool()

  ## @var sf_coupling_trigger
  # Boolean field to indicate if the coupling mechanism is to be triggered.
  sf_coupling_trigger = avango.SFBool()

  ## @var sf_nav_mode_toggle_trigger
  # Boolean field to indicate if the change of the dof mode is to be triggered.
  sf_nav_mode_toggle_trigger = avango.SFBool()

  ## internal fields

  sf_gf_start_mat = avango.gua.SFMatrix4()
  sf_gf_start_mat.value = avango.gua.make_identity_mat()

  ## @var mf_ground_pick_result
  # Intersections of the ground following ray with the objects in the scene.
  mf_ground_pick_result = avango.gua.MFPickResult()

  '''
  ## @var sf_request_trigger
  # Boolean field to indicate if the request mechanism is to be triggered.
  sf_request_trigger = avango.SFBool()
  '''

  ## Default constructor.
  def __init__(self):
    self.super(SteeringNavigation).__init__()

  ## Custom constructor.
  # @param STARTING_MATRIX Initial position matrix of the navigation to be created.
  # @param STARTING_SCALE Start scaling of the navigation.
  # @param INPUT_DEVICE_TYPE String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
  # @param INPUT_DEVICE_NAME Name of the input device sensor as chosen in daemon.
  # @param NO_TRACKING_MAT Matrix which should be applied if no tracking is available.
  # @param GROUND_FOLLOWING_SETTINGS Setting list for the GroundFollowing instance: [activated, ray_start_height]
  # @param INVERT Boolean indicating if the input values should be inverted.
  # @param TRACE_VISIBILITY_LIST A list containing visibility rules according to the DisplayGroups' visibility tags. 
  # @param DEVICE_TRACKING_NAME Name of the device's tracking target name as chosen in daemon.
  # @param IS_REQUESTABLE Boolean saying if this Navigation is a requestable one. Requestable navigations can be switched to using a special button on the device.
  # @param REQUEST_BUTTON_NUM Button number of the device's sensor which should be used for the request mechanism.
  # @param REACTS_ON_PORTAL_TRANSIT Boolean saying if this navigation is allowed to be reset by portal transitions.
  def my_constructor(
      self
    , STARTING_MATRIX
    , STARTING_SCALE
    , INPUT_DEVICE_TYPE
    , INPUT_DEVICE_NAME
    , NO_TRACKING_MAT
    , GROUND_FOLLOWING_SETTINGS
    , INVERT
    , TRACE_VISIBILITY_LIST
    , DEVICE_TRACKING_NAME = None
    , IS_REQUESTABLE = False
    , REQUEST_BUTTON_NUM = None
    , REACTS_ON_PORTAL_TRANSIT = False
    ):

    self.list_constructor(TRACE_VISIBILITY_LIST)

    ### attributes ###

    ## @var reacts_on_portal_transit
    # Boolean saying if this navigation is allowed to be reset by portal transitions.
    self.reacts_on_portal_transit = REACTS_ON_PORTAL_TRANSIT

    ## @var nav_mode
    # value to indicate if the user is navigation mode: 0 = ground-based movement (incl GF); 1 = 6DoF navigation.
    self.nav_mode = 0 

    # factors for input amplifying
    ## @var input_trans_factor
    # Factor to modify the translation input.
    self.input_trans_factor = 1.0

    ## @var input_rot_factor
    # Factor to modify the rotation input.
    self.input_rot_factor = 1.0

    ## @var min_scale
    # The minimum scaling factor that can be applied.
    self.min_scale = 0.0001

    ## @var max_scale
    # The maximum scaling factor that can be applied.
    self.max_scale = 10000.0
    
    ## @var scale_stop_duration
    # Time how long a scaling process is stopped at a fixed step in seconds.
    self.scale_stop_duration = 1.0

    ## @var invert
    # Boolean indicating if the input values should be inverted.
    self.invert = INVERT
    

    ### variables ###

    ## @var input_device_type
    # String indicating the type of input device to be created, e.g. "XBoxController" or "OldSpheron"
    self.input_device_type = INPUT_DEVICE_TYPE

    ## @var input_device_name
    # Name of the input device sensor as chosen in daemon.
    self.input_device_name = INPUT_DEVICE_NAME

    ## @var start_matrix
    # Initial position matrix of the navigation.
    self.start_matrix = STARTING_MATRIX

    ## @var start_scale
    # Initial scaling factor of the navigation.
    self.start_scale = STARTING_SCALE

    ## @var in_dofchange_animation
    # Boolean variable to indicate if a movement animation for a DOF change (realistic/unrealistic) is in progress.
    self.in_dofchange_animation = False

    ## @var blocked
    # Boolean variable indicating if the device input is blocked (e.g. when in coupling animation)
    self.blocked = False

    ## @var scale_stop_time
    # Time at which a scaling process stopped at a fixed step.
    self.scale_stop_time = None
    

    ### subclasses ###
        
    # create device
    ## @var device
    # Device instance handling relative inputs of physical device.
    if self.input_device_type == "OldSpheron":
      self.device = OldSpheronDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "NewSpheron":
      self.device = NewSpheronDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "XBoxController":
      self.device = XBoxDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "KeyboardMouse":
      self.device = KeyboardMouseDevice()
      self.device.my_constructor(NO_TRACKING_MAT)
    elif self.input_device_type == "Spacemouse":
      self.device = SpacemouseDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, DEVICE_TRACKING_NAME, NO_TRACKING_MAT)
    elif self.input_device_type == "Globefish":
      self.device = GlobefishDevice()
      self.device.my_constructor(INPUT_DEVICE_NAME, NO_TRACKING_MAT)
        

    '''
    ## @var timer
    # Instance of TimeSensor to handle the duration of animations.
    self.timer = avango.nodes.TimeSensor()
    '''

    self.input_trans_factor = self.device.translation_factor
    self.input_rot_factor = self.device.rotation_factor
    
    
    self.bc_init_movement_traces(str(self), 100, 50.0)
    
    if self.input_device_type == "Spacemouse":
      self.set_nav_mode(1) # set to 6DoF navigation

    else:
      self.init_groundfollowing(float(GROUND_FOLLOWING_SETTINGS[1]))

    '''
    ## @var is_requestable
    # Boolean saying if this Navigation is a requestable one. Requestable navigations
    # can be switched to using a special button on the device.
    self.is_requestable = IS_REQUESTABLE

    # connect request button
    if self.is_requestable:
      exec("self.sf_request_trigger.connect_from(self.device.device_sensor.Button" + str(REQUEST_BUTTON_NUM) + ")")
    '''
    

    ### field connections ###
    
    self.sf_reset_trigger.connect_from(self.device.sf_reset_trigger)
    self.sf_coupling_trigger.connect_from(self.device.sf_coupling_trigger)
    self.sf_nav_mode_toggle_trigger.connect_from(self.device.sf_dof_trigger)
    self.mf_rel_input_values.connect_from(self.device.mf_dof)
    self.sf_reference_mat.connect_from(self.device.sf_station_mat)

    self.reset() # set to start parameters


  ### functions ###

  def init_groundfollowing(self, RAY_START_HEIGHT):

    # further variables
  
    ## @var falling
    # A boolean indicating if the user is currently falling. Used for fall speed computations.
    self.falling = False

    ## @var initial_fall_velocity
    # The starting velocity when the user is falling in meters per frame. Is increased the longer the falling process goes on.
    self.initial_fall_velocity = 0.05

    ## @var height_modification_factor
    # Scaling factor used for the modification of up and down vectors.
    self.height_modification_factor = 0.15

    # fall velocity in meter per frame
    ## @var fall_velocity
    # Speed when the user is falling in meters per frame.
    self.fall_velocity = self.initial_fall_velocity

    # pick length in meter
    ## @var ground_pick_length
    # Length of the ground following ray.
    self.ground_pick_length = 100.0

    ## @var ground_pick_direction_mat
    # Direction of the ground following ray.
    self.ground_pick_direction_mat = avango.gua.make_identity_mat()

    ## @var ray_start_height
    # Starting height of the ground following ray.
    self.ray_start_height = RAY_START_HEIGHT


    ## @var groundfollowing_trigger
    # Triggers framewise evaluation of respective callback method
    self.groundfollowing_trigger = avango.script.nodes.Update(Callback = self.groundfollowing_callback, Active = False)
       
    self.set_pick_direction(avango.gua.Vec3(0.0, -1.0, 0.0))
    
    _scenegraph = scenegraphs[0]
    _pick_mask = "gf_pick_group"

    self.ground_intersection = Intersection()
    self.ground_intersection.my_constructor(_scenegraph, self.sf_gf_start_mat, self.ground_pick_length, _pick_mask)
    self.mf_ground_pick_result.connect_from(self.ground_intersection.mf_pick_result)
    
    

  ## Resets the navigation's matrix to the initial value.
  def reset(self):
   
    self.bc_set_nav_mat(self.start_matrix)
    self.bc_set_nav_scale(self.start_scale)

    self.bc_clear_movement_traces() # evtl. reset movement traces


  def set_nav_mode(self, MODE):
  
    self.nav_mode = MODE
    
    if self.nav_mode == 0: # ground-based movement

      if self.groundfollowing_trigger != None:
        self.groundfollowing_trigger.Active.value = True
    
    elif self.nav_mode == 1: # 6DoF navigation

      if self.groundfollowing_trigger != None:
        self.groundfollowing_trigger.Active.value = False


  ## Sets the pick_direction attribute.
  # @param PICK_DIRECTION New pick direction.
  def set_pick_direction(self, PICK_DIRECTION):

    PICK_DIRECTION.normalize()
    
    _ref = avango.gua.Vec3(0.0,0.0,-1.0)
    _angle = math.degrees(math.acos(_ref.dot(PICK_DIRECTION)))
    _axis = _ref.cross(PICK_DIRECTION)

    self.ground_pick_direction_mat = avango.gua.make_rot_mat(_angle, _axis)


  def groundfollowing_callback(self):
  
    _nav_mat = self.bc_get_nav_mat()
    _nav_scale = self.bc_get_nav_scale()
  
    # prepare ground following matrix
    _gf_start_pos = self.sf_reference_mat.value.get_translate()
    _gf_start_pos.y = self.ray_start_height
    _gf_start_pos = self.sf_platform_mat.value * _gf_start_pos
    self.sf_gf_start_mat.value = avango.gua.make_trans_mat(_gf_start_pos.x, _gf_start_pos.y, _gf_start_pos.z) * self.ground_pick_direction_mat

    if len(self.mf_ground_pick_result.value) > 0: # an intersection with the ground was found
  
      # get first intersection target
      _pick_result = self.mf_ground_pick_result.value[0]             
      #print(_pick_result.Object.value, _pick_result.Object.value.Name.value)

      # compare distance to ground and ray_start_height
      _distance_to_ground = _pick_result.Distance.value * self.ground_pick_length
      _difference = _distance_to_ground - (self.ray_start_height * _nav_scale)
      _difference = round(_difference, 3)

      if _difference < 0: # climb up

        # end falling when necessary
        if self.falling == True:
          self.falling = False
          self.fall_velocity = self.initial_fall_velocity 

        # move player up
        _up_vec = avango.gua.Vec3(0.0, _difference * -1.0 * self.height_modification_factor, 0.0)
        _nav_mat = avango.gua.make_trans_mat(_up_vec) * _nav_mat

        self.bc_set_nav_mat(_nav_mat)


      elif _difference > 0:
        
        if _difference > (self.ray_start_height * _nav_scale): # falling

          # make player fall down faster every time
          self.falling = True
          _fall_vec = avango.gua.Vec3(0.0, -self.fall_velocity, 0.0)
          _nav_mat = avango.gua.make_trans_mat(_fall_vec) * _nav_mat

          self.bc_set_nav_mat(_nav_mat)

          self.fall_velocity += 0.005

        else: # climb down
          
          # end falling when necessary
          if self.falling:
            self.falling = False
            self.fall_velocity = self.initial_fall_velocity 

          # move platform downwards
          _down_vec = avango.gua.Vec3(0.0, _difference * -1.0 * self.height_modification_factor, 0.0)
          _nav_mat = avango.gua.make_trans_mat(_down_vec) * _nav_mat
          
          self.bc_set_nav_mat(_nav_mat)


  '''
  ## Activates 3-DOF (realistic) navigation mode.
  def activate_realistic_mode(self):

    # remove pitch and roll from current orientation
    _current_mat = self.sf_abs_mat.value
    _current_trans = _current_mat.get_translate()
    _current_yaw = Utilities.get_yaw(_current_mat)

    ## @var start_rot
    # Quaternion representing the start rotation of the animation
    self.start_rot = self.sf_abs_mat.value.get_rotate()

    ## @var target_rot
    # Quaternion representing the target rotation of the animation
    self.target_rot = avango.gua.make_rot_mat(math.degrees(_current_yaw), 0, 1, 0).get_rotate()

    ## @var animation_time
    # Time of the rotation animation in relation to the rotation distance.
    self.animation_time = 2 * math.sqrt(math.pow(self.start_rot.x - self.target_rot.x, 2) \
      + math.pow(self.start_rot.y - self.target_rot.y, 2) \
      + math.pow(self.start_rot.z - self.target_rot.z, 2) \
      + math.pow(self.start_rot.w - self.target_rot.w, 2))
   
    # if no animation is needed, set animation time to a minimum value to avoid division by zero
    if self.animation_time == 0.0:
      self.animation_time = 0.01

    ## @var start_trans
    # Starting translation vector of the animation.
    self.start_trans = _current_trans

    ## @var animation_start_time
    # Point in time where the animation started.
    self.animation_start_time = self.timer.Time.value
 
    self.in_dofchange_animation = True                       

  ## Activates 6-DOF (unrealistic) navigation mode.
  def deactivate_realistic_mode(self):
    self.inputmapping.deactivate_realistic_mode()
  '''
  
  '''
  ## Animates the removal of pitch and roll angles when switching from 6-DOF (unrealistic) to 3-DOF (realistic) navigation mode.
  def animate_dofchange(self):

    _current_time = self.timer.Time.value
    _slerp_ratio = (_current_time - self.animation_start_time) / self.animation_time

    # when end of animation is reached
    if _slerp_ratio > 1:
      _slerp_ratio = 1
      self.in_dofchange_animation = False
      self.inputmapping.activate_realistic_mode()

    # compute slerp position and set it on the player's inputmapping
    _transformed_quat = self.start_rot.slerp_to(self.target_rot, _slerp_ratio)

    _position_yaw_mat = avango.gua.make_trans_mat(self.start_trans.x, self.start_trans.y, self.start_trans.z) * \
                        avango.gua.make_rot_mat(_transformed_quat)

    self.inputmapping.set_abs_mat(_position_yaw_mat)
  '''

  '''
  ## Switches from realistic to unrealistic or from unrealistic to realistic mode on this
  # and all other coupled instances.
  def trigger_dofchange(self):

    # if in realistic mode, switch to unrealistic mode
    if self.inputmapping.realistic == True:
      #print("GF off")
      self.deactivate_realistic_mode()
    
    # if in unrealistic mode, switch to realistic mode
    else:
      #print("GF on")
      self.activate_realistic_mode()
  '''

  ## Applies a new scaling to this input mapping.
  # @param SCALE The new scaling factor to be applied.
  def map_scale_input(self, SCALE_INPUT):
  
    if SCALE_INPUT == 0.0:
      return
  
    _old_scale = self.bc_get_nav_scale()
    _new_scale = _old_scale * (1.0 + SCALE_INPUT * 0.015)
    _new_scale = max(min(_new_scale, self.max_scale), self.min_scale)


    if self.scale_stop_duration == 0.0:
      self.bc_set_nav_scale(_new_scale) # directly apply new scale
   
      return
     
    if self.scale_stop_time != None: # in stop time intervall
    
      if (time.time() - self.scale_stop_time) > self.scale_stop_duration:
        self.scale_stop_time = None
    
      return
      
    _old_scale = round(_old_scale,6)      
    _new_scale = round(_new_scale,6)
            
    # auto pause at specific scale levels
    if (_old_scale < 1000.0 and _new_scale > 1000.0) or (_new_scale < 1000.0 and _old_scale > 1000.0):
      #print("snap 1000:1")
      _new_scale = 1000.0
      self.scale_stop_time = time.time()
      
    elif (_old_scale < 100.0 and _new_scale > 100.0) or (_new_scale < 100.0 and _old_scale > 100.0):
      #print("snap 100:1")
      _new_scale = 100.0
      self.scale_stop_time = time.time()
            
    elif (_old_scale < 10.0 and _new_scale > 10.0) or (_new_scale < 10.0 and _old_scale > 10.0):
      #print("snap 10:1")
      _new_scale = 10.0
      self.scale_stop_time = time.time()
    
    elif (_old_scale < 1.0 and _new_scale > 1.0) or (_new_scale < 1.0 and _old_scale > 1.0):
      #print("snap 1:1")
      _new_scale = 1.0
      self.scale_stop_time = time.time()

    elif (_old_scale < 0.1 and _new_scale > 0.1) or (_new_scale < 0.1 and _old_scale > 0.1):
      #print("snap 1:10")
      _new_scale = 0.1
      self.scale_stop_time = time.time()

    elif (_old_scale < 0.01 and _new_scale > 0.01) or (_new_scale < 0.01 and _old_scale > 0.01):
      #print("snap 1:100")
      _new_scale = 0.01
      self.scale_stop_time = time.time()

    elif (_old_scale < 0.001 and _new_scale > 0.001) or (_new_scale < 0.001 and _old_scale > 0.001):
      #print("snap 1:1000")
      _new_scale = 0.001
      self.scale_stop_time = time.time()

    
    #'''
    # scale relative to a reference point
    _scale_center_offset = self.sf_reference_mat.value.get_translate() 

    if _scale_center_offset.length() > 0: # scale/rotation center defined
      _pos1 = _scale_center_offset * _old_scale
      _pos2 = _scale_center_offset * _new_scale

      _vec = _pos1 - _pos2

      _new_mat = self.bc_get_nav_mat() * avango.gua.make_trans_mat(_vec)
    
      self.bc_set_nav_mat(_new_mat)
    #'''

    self.bc_set_nav_scale(_new_scale) # apply new scale

 
  def map_movement_input(self, X, Y, Z, RX, RY, RZ):

    _trans_vec = avango.gua.Vec3(X, Y, Z)
    _trans_input = _trans_vec.length()

    _rot_vec = avango.gua.Vec3(RX, RY, RZ)
    _rot_input = _rot_vec.length()
    
    if _trans_input == 0.0 and _rot_input == 0.0:
      return

    _rot_center = self.get_reference_center()
    _nav_mat = self.bc_get_nav_mat()    
    
    if _trans_input != 0.0: # transfer function for translation      
      _ref_rot_mat = avango.gua.make_rot_mat(_nav_mat.get_rotate())
      _ref_rot_mat = _ref_rot_mat * avango.gua.make_rot_mat(self.sf_reference_mat.value.get_rotate())
      
      _trans_vec.normalize()
      _trans_vec *= math.pow(min(_trans_input, 1.0), 3) * self.input_trans_factor * self.bc_get_nav_scale()
      _trans_vec = self.transform_vector_with_matrix(_trans_vec, _ref_rot_mat) # transform into reference orientation (e.g. input device orientation)

    if _rot_input != 0.0: # transfer function for rotation
      _rot_vec.normalize()
      _rot_vec *= math.pow(min(_rot_input, 1.0), 3) * self.input_rot_factor


    # map input
    _nav_mat = avango.gua.make_trans_mat(_trans_vec) * \
               _nav_mat * \
               avango.gua.make_trans_mat(_rot_center) * \
               avango.gua.make_rot_mat(_rot_vec.y, 0, 1, 0) * \
               avango.gua.make_rot_mat(_rot_vec.x, 1, 0, 0) * \
               avango.gua.make_rot_mat(_rot_vec.z, 0, 0, 1) * \
               avango.gua.make_trans_mat(_rot_center * -1)

    self.bc_set_nav_mat(_nav_mat)


  ## Transforms a vector using a transformation matrix.
  # @param VECTOR The vector to be transformed.
  # @param MATRIX The matrix to be applied for transformation.
  def transform_vector_with_matrix(self, VECTOR, MATRIX):

    _vec = MATRIX * VECTOR
    return avango.gua.Vec3(_vec.x, _vec.y, _vec.z)

  
  def get_reference_center(self):
  
    _center = self.sf_reference_mat.value.get_translate() * self.bc_get_nav_scale()
    return _center

  
  ### callbacks ###

  ## Evaluated when device input values change.
  @field_has_changed(mf_rel_input_values)
  def mf_rel_input_values_changed(self):
    
    if self.blocked == True:
      return

    # get input values
    _s = self.mf_rel_input_values.value[6]
    
    _x = self.mf_rel_input_values.value[0]
    _y = self.mf_rel_input_values.value[1]
    _z = self.mf_rel_input_values.value[2]

    _rx = self.mf_rel_input_values.value[3]
    _ry = self.mf_rel_input_values.value[4]
    _rz = self.mf_rel_input_values.value[5]


    # invert movement if activated
    if self.invert == True:
      _x = -_x
      _y = -_y
      _z = -_z
      _rx = -_rx
      _ry = -_ry
      _rz = -_rz

    # ground-based movement --> ignore hight input and roll/pitch input
    if self.nav_mode == 0: 
      _y = 0.0
      _rx = 0.0
      _rz = 0.0
    
    # map inputs    
    self.map_scale_input(_s)
    self.map_movement_input(_x, _y, _z, _rx, _ry, _rz)


    '''
    # get translation values from input device
    _trans_vec = avango.gua.Vec3(_x,_y,_z)
    _trans_input = _trans_vec.length()

    # get rotation values from input device
    _rot_vec = avango.gua.Vec3(_rx,_ry,_rz) * self.input_rot_factor
    _rot_input = _rot_vec.length()

    # only accumulate inputs on absolute matrix when the device values change
    if _trans_input != 0.0 or _rot_input != 0.0:

      # transfer function for translation
      if _trans_input != 0.0:
        _trans_vec.normalize()
        _trans_vec *= math.pow(min(_trans_input,1.0), 3) * self.input_trans_factor * self.sf_scale.value

      # global platform rotation in the world
      _platform_quat = self.sf_abs_mat.value.get_rotate()

      # Fix if quaternion angle is nan
      _quat_angle = _platform_quat.get_angle()

      if math.isnan(_quat_angle) == False:
        _platform_rot_mat = avango.gua.make_rot_mat(_quat_angle, _platform_quat.get_axis())
        self.lf_quat_angle = _quat_angle
      else:
        _platform_rot_mat = avango.gua.make_rot_mat(self.lf_quat_angle, _platform_quat.get_axis())

      # global rotation of the device in the world
      _device_forward_yaw = Utilities.get_yaw(self.sf_station_mat.value)
      _device_rot_mat = avango.gua.make_rot_mat(math.degrees(_device_forward_yaw), 0, 1, 0)

      # combined platform and device rotation
      _combined_rot_mat = _platform_rot_mat * _device_rot_mat
 
      # rotation center of the device
      _rot_center = self.sf_station_mat.value.get_translate() * self.sf_scale.value

      # transformed translation, rotation and rotation center
      _transformed_trans_vec = self.transform_vector_with_matrix(_trans_vec, _combined_rot_mat)

      _transformed_rot_vec = self.transform_vector_with_matrix(_rot_vec, _combined_rot_mat)
      _transformed_rot_center = self.transform_vector_with_matrix(_rot_center, _platform_rot_mat)
      
      # create new transformation matrix
      _new_mat = avango.gua.make_trans_mat(_transformed_trans_vec) * \
                 self.sf_abs_mat.value * \
                 avango.gua.make_trans_mat(_rot_center) * \
                 avango.gua.make_rot_mat( _rot_vec.y, 0, 1, 0) * \
                 avango.gua.make_rot_mat( _rot_vec.x, 1, 0, 0) * \
                 avango.gua.make_rot_mat( _rot_vec.z, 0, 0, 1) * \
                 avango.gua.make_trans_mat(_rot_center * -1)

      ## # update matrix on coupled navigations
      ##_global_rot_center = self.sf_abs_mat.value * _rot_center
      ##_global_rot_center = avango.gua.Vec3(_global_rot_center.x, _global_rot_center.y, _global_rot_center.z)
      ##
      ##for _navigation in self.NAVIGATION.coupled_navigations:
      ##  _navigation.inputmapping.modify_abs_uncorrected_mat(_transformed_trans_vec, _transformed_rot_vec, _global_rot_center)

    else:
      # the device values are all equal to zero
      _new_mat = self.sf_abs_mat.value

    # save the computed new matrix
    self.sf_abs_uncorrected_mat.value = _new_mat   
    '''
  
  '''
  ## Evaluated every frame.
  def evaluate(self):

    # handle dofchange animation
    if self.in_dofchange_animation:
      self.animate_dofchange()

    # draw the traces if enabled
    if len(self.active_user_representations) > 0:
      _device_pos = self.device.sf_station_mat.value.get_translate()
      self.trace.update(self.sf_abs_mat.value * avango.gua.make_trans_mat(_device_pos.x, 0, _device_pos.z))

    # update sf_nav_mat
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)
  '''


  ## Evaluated when value changes.
  @field_has_changed(sf_reset_trigger)
  def sf_reset_trigger_changed(self):
  
    if self.sf_reset_trigger.value == True: # button pressed
      #print("RESET")
      self.reset()       
          

  ## Evaluated when value changes.
  @field_has_changed(sf_nav_mode_toggle_trigger)
  def sf_nav_mode_toggle_trigger_changed(self):
  
    if self.sf_nav_mode_toggle_trigger.value == True: # button pressed

      #if self.in_dofchange_animation == False:
      #   self.trigger_dofchange()
      
      if self.in_dofchange_animation == False:
      
        if self.nav_mode == 0: # ground-based movement
          self.set_nav_mode(1) # set to 6DoF navigation mode
          
        elif self.nav_mode == 1: # 6DoF navigation
          self.set_nav_mode(0) # set to ground-based mode
