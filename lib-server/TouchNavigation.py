#!/usr/bin/python

### import avango-guacamole libraries
import avango
import avango.gua
import avango.script

import math
import time

from Navigation import *

class TouchNavigation(Navigation):

  def __init__(self):
    self.super(TouchNavigation).__init__()

    #self.always_evaluate(True)

  def my_constructor(self, STARTING_MATRIX, STARTING_SCALE, TRACE_VISIBILITY_LIST, REACTS_ON_PORTAL_TRANSIT):

    self.list_constructor(TRACE_VISIBILITY_LIST)
    self.bc_init_movement_traces(str(self), 100, 50.0)

    self.start_matrix               = STARTING_MATRIX
    self.start_scale                = STARTING_SCALE

    self.bc_set_nav_mat(self.start_matrix)
    self.bc_set_nav_scale(self.start_scale)    

    self.reacts_on_portal_transit   = REACTS_ON_PORTAL_TRANSIT

    self.receiving_input            = False

    self.active_contact             = -1

    self.lastInput                  = avango.gua.make_identity_mat()

    self.touch_contacts             = []

    self.multi_touch_center         = avango.gua.Vec3(0,0,0)
    self.last_multi_touch_center    = avango.gua.Vec3(0,0,0)
    self.multi_touch_distance       = 0.0

    self.addedSecondContact         = True

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

    self.proxy_plane.GroupNames.value = ["do_not_display_group"]

    SCREENNODE.Children.value.append(self.proxy_plane)

  def addContact(self, HANDMAT, ID):
    kill_contacts = []
    for contact in self.touch_contacts:
      if time.clock() - contact.last_update_timer > 0.1:
        kill_contacts.append(contact.input_id)
    for input_id in kill_contacts:
      self.removeContact(input_id)

    if len(self.touch_contacts) == 0:
      newContact = TouchContact(ID, HANDMAT, time.clock())
      self.touch_contacts.append(newContact)
      return True

    elif len(self.touch_contacts) == 1:
      if self.touch_contacts[0].input_id == ID:
        self.touch_contacts[0].update(HANDMAT)
        self.evaluateContacts()
        return True
      else:
        newContact = TouchContact(ID, HANDMAT, time.clock()) 
        self.touch_contacts.append(newContact)
        self.addedSecondContact = True
        return True

    else:
      for contact in self.touch_contacts:
        if contact.input_id == ID:
          contact.update(HANDMAT)
          self.evaluateContacts()
          return True

    return False

  def computeMultiTouchCenter(self):
    if len(self.touch_contacts) > 1:
      pos1 = self.touch_contacts[0].input_mat.get_translate()
      pos2 = self.touch_contacts[1].input_mat.get_translate()
      pos1ToPos2 = pos2 - pos1
      self.last_multi_touch_center = self.multi_touch_center
      self.multi_touch_center = pos1 + avango.gua.Vec3(0.5*pos1ToPos2.x, 0.5*pos1ToPos2.y, 0.5*pos1ToPos2.z)

  def computeMultiTouchDistance(self):
    if len(self.touch_contacts) > 1:
      pos1 = self.touch_contacts[0].input_mat.get_translate()
      pos2 = self.touch_contacts[1].input_mat.get_translate()
      pos1ToPos2 = pos2 - pos1
      self.multi_touch_distance = pos1ToPos2.length()
      
  def evaluateContacts(self):
    
    if len(self.touch_contacts) == 1:
      self.translate()

    elif len(self.touch_contacts) == 2:
      self.computeMultiTouchCenter()
      self.sf_reference_mat.value = avango.gua.make_trans_mat(self.multi_touch_center)
      if self.addedSecondContact:
        self.computeMultiTouchDistance()
        self.addedSecondContact = False
      else:
        self.translate()
        self.rotate()
        self.scale()
      
  def translate(self):
    relativeInput = avango.gua.Vec3(0,0,0)
    
    if len(self.touch_contacts) == 1:
      relativeInput = self.touch_contacts[0].getRelativeInput()
    else:
      relativeInput = self.multi_touch_center - self.last_multi_touch_center

    self.map_movement_input(-relativeInput.x, -relativeInput.y, -relativeInput.z, 0, 0, 0)
    
  def rotate(self):
    pos1 = self.touch_contacts[0].last_input_mat.get_translate()
    pos2 = self.touch_contacts[1].last_input_mat.get_translate()
    lastVec = pos2 - pos1
    
    pos1 = self.touch_contacts[0].input_mat.get_translate()
    pos2 = self.touch_contacts[1].input_mat.get_translate()
    newVec = pos2 - pos1
    
    newVec.normalize()
    lastVec.normalize()

    cross = lastVec.cross(newVec)
    
    alpha = 0
    if lastVec != newVec:
      cosAlpha = max(min(lastVec.dot(newVec), 1.0), -1.0)
      alpha = math.acos(cosAlpha)

    alphaDeg = math.degrees(alpha) * 0.5
    
    if cross.y < 0.0:
      self.map_movement_input(0,0,0,0,alphaDeg,0)
    else:
      self.map_movement_input(0,0,0,0,-alphaDeg,0)

  def scale(self):
    if self.addedSecondContact:
      pos1 = self.touch_contacts[0].input_mat.get_translate()
      pos2 = self.touch_contacts[1].input_mat.get_translate()
      pos1ToPos2 = pos2 - pos1
      self.multi_touch_distance = pos1ToPos2.length()
    else:
      pos1 = self.touch_contacts[0].input_mat.get_translate()
      pos2 = self.touch_contacts[1].input_mat.get_translate()
      pos1ToPos2 = pos2 - pos1
      self.map_scale_input(self.multi_touch_distance / max(pos1ToPos2.length(), 0.000000001))

  def removeContact(self, ID):
    kill_contact = None

    i = 0
    for contact in self.touch_contacts:
      if contact.input_id == ID:
        kill_contact = contact
        break
      i += 1

    if kill_contact != None:
      #self.touch_contacts.remove(kill_contact)
      del(self.touch_contacts[i])

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
      
      #_trans_vec.normalize()
      _trans_vec *= self.bc_get_nav_scale()
      _trans_vec = self.transform_vector_with_matrix(_trans_vec, _ref_rot_mat) # transform into reference orientation (e.g. input device orientation)

    #if _rot_input != 0.0: # transfer function for rotation
    #  _rot_vec.normalize()
    #  _rot_vec *= math.pow(min(_rot_input, 1.0), 3)

    # map input
    _nav_mat = avango.gua.make_trans_mat(_trans_vec) * \
               _nav_mat * \
               avango.gua.make_trans_mat(_rot_center) * \
               avango.gua.make_rot_mat(_rot_vec.y, 0, 1, 0) * \
               avango.gua.make_rot_mat(_rot_vec.x, 1, 0, 0) * \
               avango.gua.make_rot_mat(_rot_vec.z, 0, 0, 1) * \
               avango.gua.make_trans_mat(_rot_center * -1)

    self.bc_set_nav_mat(_nav_mat)

  def map_scale_input(self, SCALE_INPUT):
  
    if SCALE_INPUT == 0.0:
      return
  
    _old_scale = self.bc_get_nav_scale()
    _new_scale = SCALE_INPUT
        
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

class TouchContact:

  def __init__(self, INPUTID, STARTMAT, STARTTIME):
    self.input_id           = INPUTID
    
    self.input_mat          = STARTMAT

    self.last_input_mat     = STARTMAT

    self.last_update_timer  = STARTTIME

  def update(self, NEWMAT):
    self.last_input_mat    = self.input_mat

    self.input_mat         = NEWMAT

    if self.input_mat.get_translate() != self.last_input_mat.get_translate():
      self.last_update_timer = time.clock()
    
  def getRelativeInput(self):
    return self.input_mat.get_translate() - self.last_input_mat.get_translate() 
