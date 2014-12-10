#!/usr/bin/python

### import avango-guacamole libraries
import avango
import avango.gua
import avango.script

import math

from Navigation import *

class TouchNavigation(Navigation):

  def __init__(self):
    self.super(TouchNavigation).__init__()

  def my_constructor(self, STARTING_MATRIX, STARTING_SCALE, TRACE_VISIBILITY_LIST, REACTS_ON_PORTAL_TRANSIT):

    self.list_constructor(TRACE_VISIBILITY_LIST)
    self.bc_init_movement_traces(str(self), 100, 50.0)

    self.start_matrix = STARTING_MATRIX

    self.start_scale  = STARTING_SCALE

    self.bc_set_nav_mat(self.start_matrix)

    self.bc_set_nav_scale(self.start_scale)    

    self.reacts_on_portal_transit = REACTS_ON_PORTAL_TRANSIT

  def setupProxyPlane(self, SCREENNODE):
       
    _loader = avango.gua.nodes.TriMeshLoader()

    inv_screen_mat = avango.gua.make_inverse_mat(SCREENNODE.Transform.value)

    # touch navigation proxy plane
    self.proxy_plane = _loader.create_geometry_from_file("touch_proxy_plane",
                                                            "data/objects/cube.obj",
                                                            "data/materials/White.gmd",
                                                            avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    
    self.proxy_plane.Transform.value = inv_screen_mat *\
                                            avango.gua.make_trans_mat(0, -0.0030, 0) *\
                                            avango.gua.make_scale_mat(1.115, 0.0025, 0.758)

    self.proxy_plane.add_and_init_field(avango.script.SFObject(), "TouchNavigation", self) # rework ??
    self.proxy_plane.TouchNavigation.dont_distribute(True)

    SCREENNODE.Children.value.append(self.proxy_plane)

  def addContact(self):
    print("hello from TouchNavigation!")
    #_mat = self.bc_get_nav_mat()
    #self.bc_set_nav_mat(avango.gua.make_trans_mat(0.01,0,0) * _mat)

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
      _trans_vec *= math.pow(min(_trans_input, 1.0), 3) * self.bc_get_nav_scale()
      _trans_vec = self.transform_vector_with_matrix(_trans_vec, _ref_rot_mat) # transform into reference orientation (e.g. input device orientation)

    if _rot_input != 0.0: # transfer function for rotation
      _rot_vec.normalize()
      _rot_vec *= math.pow(min(_rot_input, 1.0), 3)


    # map input
    _nav_mat = avango.gua.make_trans_mat(_trans_vec) * \
               _nav_mat * \
               avango.gua.make_trans_mat(_rot_center) * \
               avango.gua.make_rot_mat(_rot_vec.y, 0, 1, 0) * \
               avango.gua.make_rot_mat(_rot_vec.x, 1, 0, 0) * \
               avango.gua.make_rot_mat(_rot_vec.z, 0, 0, 1) * \
               avango.gua.make_trans_mat(_rot_center * -1)

    self.bc_set_nav_mat(_nav_mat)

  ## Resets the navigation's matrix to the initial value.
  def reset(self):
   
    self.bc_set_nav_mat(self.start_matrix)
    self.bc_set_nav_scale(self.start_scale)

    self.bc_clear_movement_traces() # evtl. reset movement traces

  def get_reference_center(self):
  
    _center = self.sf_reference_mat.value.get_translate() * self.bc_get_nav_scale()
    return _center

  def transform_vector_with_matrix(self, VECTOR, MATRIX):

    _vec = MATRIX * VECTOR
    return avango.gua.Vec3(_vec.x, _vec.y, _vec.z)