#!/usr/bin/python

## @file
# Contains class PortalCameraNavigation.

# import avango-guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed

# import framework libraries
from Navigation import *
from PortalCamera import *

# import python libraries
import time


## Special type of Navigation associated to a PortalCamera.
# Allows moving and rotating by moving the device when a button is pressed and
# changes scalings by button presses.
class PortalCameraNavigation(Navigation):

  ## @var sf_navigation_flag
  # Boolean field to check if the clutch trigger button was pressed.
  sf_navigation_flag = avango.SFBool()

  ## Default constructor.
  def __init__(self):
    self.super(PortalCameraNavigation).__init__()

  ## Custom constructor.
  # @param PORTAL_CAMERA_INSTANCE Instance of PortalCamera which is the input device of this Navigation.
  def my_constructor(self, PORTAL_CAMERA_INSTANCE):

    ### references ###    
    
    ## @var portal_cam
    # Instance of PortalCamera which is the input device of this Navigation.
    self.PORTAL_CAMERA_INSTANCE = PORTAL_CAMERA_INSTANCE


    ### attributes ###

    ## @var min_scale
    # The minimum scaling factor that can be applied.
    self.min_scale = 0.0001

    ## @var max_scale
    # The maximum scaling factor that can be applied.
    self.max_scale = 10000.0

    ## @var scale_stop_duration
    # Time how long a scaling process is stopped at a fixed step in seconds.
    self.scale_stop_duration = 1.0


    ### variables ###

    ## @var drag_last_frame_camera_mat
    # Matrix containing the value of the tracking target of the last frame when in drag mode.
    self.drag_last_frame_camera_mat = None

    ## @var scale_stop_time
    # Time at which a scaling process stopped at a fixed step.
    self.scale_stop_time = None


    ### trigger callbacks ###
    
    ## @var scale_up_trigger
    # Triggers framewise evaluation of respective callback method
    self.scale_up_trigger = avango.script.nodes.Update(Callback = self.scale_up_callback, Active = False)

    ## @var scale_down_trigger
    # Triggers framewise evaluation of respective callback method
    self.scale_down_trigger = avango.script.nodes.Update(Callback = self.scale_down_callback, Active = False)

    ## @var scale_up_trigger
    # Triggers framewise evaluation of respective callback method
    self.navigation_trigger = avango.script.nodes.Update(Callback = self.navigation_callback, Active = False)


    ### field connections ###
    
    self.scale_up_trigger.Active.connect_from(self.PORTAL_CAMERA_INSTANCE.sf_scale_up_button)
    self.scale_down_trigger.Active.connect_from(self.PORTAL_CAMERA_INSTANCE.sf_scale_down_button)
    self.sf_navigation_flag.connect_from(self.PORTAL_CAMERA_INSTANCE.sf_focus_button)



  ### callbacks ###
  
  def scale_up_callback(self):

    if self.PORTAL_CAMERA_INSTANCE.current_shot != None:    
      _scale = self.PORTAL_CAMERA_INSTANCE.get_scale() # old scale
      _scale *= 0.985 # new scale
    
      self.set_scale(_scale)

    # update nav mat
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)


  def scale_down_callback(self):

    if self.PORTAL_CAMERA_INSTANCE.current_shot != None:
      _scale = self.PORTAL_CAMERA_INSTANCE.get_scale() # old scale
      _scale *= 1.015 # new scale
    
      self.set_scale(_scale)
      
    # update nav mat
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)


  def navigation_callback(self):
  
    _camera_mat = self.PORTAL_CAMERA_INSTANCE.get_local_portal_mat()
    
    _drag_input_mat = avango.gua.make_inverse_mat(self.drag_last_frame_camera_mat) * _current_camera_mat
    _drag_input_mat.set_translate(_drag_input_mat.get_translate() * self.sf_scale.value) # adjust input to scaling factor of viewing setup
    self.sf_abs_mat.value = self.sf_abs_mat.value * _drag_input_mat
      
    # update nav mat
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)

    self.drag_last_frame_camera_mat = _current_camera_mat


  ## Called whenever sf_navigation_flag changes
  @field_has_changed(sf_navigation_flag)
  def sf_navigation_flag_changed(self):
    
    # initiate dragging
    if self.sf_navigation_flag.value == True and self.PORTAL_CAMERA_INSTANCE.current_shot != None:

      self.drag_last_frame_camera_mat = self.PORTAL_CAMERA_INSTANCE.get_local_portal_mat()

      self.navigation_trigger.Active.value = True

    # stop dragging
    elif self.sf_navigation_flag.value == False:
      self.navigation_trigger.Active.value = False


  ### functions ###

  def set_scale(self, SCALE):
    
    if self.scale_stop_time == None:

      _old_scale = self.PORTAL_CAMERA_INSTANCE.get_scale()
      _old_scale = round(_old_scale,6)
      
      _new_scale = max(min(SCALE, self.max_scale), self.min_scale)
      _new_scale = round(_new_scale,6)
            
      # auto pause at dedicated scale levels
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

      self.PORTAL_CAMERA_INSTANCE.set_scale(_new_scale) # apply new scale
      #self.virtual_nav.set_navigation_values(self.virtual_nav.sf_abs_mat.value, _new_scale)

    else:

      if (time.time() - self.scale_stop_time) > self.scale_stop_duration:
        self.scale_stop_time = None



  ## Sets sf_abs_mat and sf_scale.
  # @param STATIC_ABS_MAT The new sf_abs_mat to be set.
  # @param STATIC_SCALE The new sf_scale to be set.
  def set_navigation_values(self, STATIC_ABS_MAT, STATIC_SCALE):
    self.sf_abs_mat.value = STATIC_ABS_MAT
    self.sf_scale.value = STATIC_SCALE
    self.sf_nav_mat.value = self.sf_abs_mat.value * avango.gua.make_scale_mat(self.sf_scale.value)

  

