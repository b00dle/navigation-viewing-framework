#!/usr/bin/python

## @file
# Contains base class Navigation.

# import avango-guacamole libraries
import avango
import avango.gua
from avango.script import field_has_changed

# import framework libraries
from ApplicationManager import *
from VisibilityHandler import *
from TraceLines import *

## Base class. Not to be instantiated.
class Navigation(VisibilityHandler1D):

  ### fields ###

  ## output fields
  
  ## @var sf_platform_mat
  # Combined matrix of translation, rotation and scaling of the viewing platform
  sf_platform_mat = avango.gua.SFMatrix4()
  sf_platform_mat.value = avango.gua.make_identity_mat()

  ## @var sf_reference_mat
  # The reference matrix for defining a rotation/scaling center offset.
  sf_reference_mat = avango.gua.SFMatrix4()
  sf_reference_mat.value = avango.gua.make_identity_mat()

  ### static class variables ###
  
  ## @var trace_materials
  # List of material pretexts to choose from when a trace is created. All avatars on this
  # navigation will have this material.
  trace_materials = ['AvatarBlue', 'AvatarGreen', 'AvatarRed', 'AvatarYellow', 'AvatarMagenta', 
                     'AvatarOrange', 'AvatarWhite', 'AvatarGrey', 'AvatarDarkGreen']

  ## @var number_of_instances
  # Number of SteeringNavigation instances already created. Used for trace material assignment.
  number_of_instances = 0


  ## Base constructor.
  def __init__(self):
    self.super(Navigation).__init__()

    exec('from ApplicationManager import *', globals())

    ### variables ###

    ## @var nav_mat
    # Matrix representing the current translation and rotation of the navigation in the scene.
    self.nav_mat = avango.gua.make_identity_mat()

    ## @var nav_scale
    # The current scaling factor of this navigation platform.
    self.nav_scale = 1.0

    ## @var trace
    # The trace class that handles the line segment updating.
    self.trace = None
    
    self.groundfollowing_trigger = None
    
    ## @var active_user_representations
    # List of UserRepresentation instances which are currently connecting with this navigations matrix.
    self.active_user_representations = []

    # get the selected material 
    ## @var trace_material
    # The material to be used for the movement traces.
    self.trace_material = self.trace_materials[self.number_of_instances]
    self.number_of_instances += 1
    self.number_of_instances = self.number_of_instances % len(self.trace_materials)


  ### functions ###

  def bc_get_nav_mat(self):
    return self.nav_mat

  def bc_get_nav_scale(self):
    return self.nav_scale

  def bc_set_nav_mat(self, MATRIX):
    self.nav_mat = MATRIX

    # update viewing platform
    self.sf_platform_mat.value = self.nav_mat * avango.gua.make_scale_mat(self.nav_scale)

  def bc_set_nav_scale(self, SCALE):
    self.nav_scale = SCALE

    # update viewing platform
    self.sf_platform_mat.value = self.nav_mat * avango.gua.make_scale_mat(self.nav_scale)


  def bc_init_movement_traces(self, IDENTIFIER, NUM_LINES, LINE_DISTANCE):
  
    ## @var trace
    # Instance of Trace class to handle trace drawing of this navigation's movements.
    self.trace = Trace(IDENTIFIER, NUM_LINES, LINE_DISTANCE, self.trace_material + 'Shadeless')


  def bc_update_movement_traces(self):
  
    if self.trace != None and len(self.active_user_representations) > 0:
  
      _reference_pos = self.sf_reference_mat.value.get_translate()
      _reference_pos.y = 0.0
      
      _mat = self.sf_platform_mat.value * avango.gua.make_trans_mat(_reference_pos)
      
      self.trace.update(_mat)

  def bc_clear_movement_traces(self):
    
    if self.trace != None:

      _reference_pos = self.sf_reference_mat.value.get_translate()
      _reference_pos.y = 0.0
      
      _mat = self.sf_platform_mat.value * avango.gua.make_trans_mat(_reference_pos)
      
      self.trace.clear(_mat)




  ## Adds a UserRepresentation to this navigation.
  # @param USER_REPRESENTATION The UserRepresentation instance to be added.
  def add_user_representation(self, USER_REPRESENTATION):

    # set navigation color plane
    for _screen in USER_REPRESENTATION.screens:

      try:
        _screen.Children.value[0].Material.value = 'data/materials/' + self.trace_material + 'Shadeless.gmd'
      except:
        pass

    #if len(self.active_user_representations) == 0:
    #  self.bc_clear_movement_traces()

    self.active_user_representations.append(USER_REPRESENTATION)
  
  ## Removes a UserRepresentation from this navigation.
  # @param USER_REPRESENTATION The UserRepresentation instance to be removed.
  def remove_user_representation(self, USER_REPRESENTATION):

    if USER_REPRESENTATION in self.active_user_representations:
      self.active_user_representations.remove(USER_REPRESENTATION)

      if len(self.active_user_representations) == 0:
        self.bc_clear_movement_traces()


  ## Triggers the correct GroupNames for the different DisplayGroups.
  def handle_correct_visibility_groups(self):

    _trace_visible_for = []

    for _user_repr in ApplicationManager.all_user_representations:

      if self.visibility_list[_user_repr.DISPLAY_GROUP.visibility_tag]:
        _trace_visible_for.append(_user_repr.view_transform_node.Name.value)

    if len(_trace_visible_for) == 0:
      self.trace.append_to_group_names("do_not_display_group")
    
    else:  
      for _string in _trace_visible_for:
        self.trace.append_to_group_names(_string)

  
  ### callbacks ###

  ## Evaluated when value changes.
  @field_has_changed(sf_platform_mat)
  def sf_platform_mat_changed(self):
  
    self.bc_update_movement_traces() # evtl. update movement traces
    

