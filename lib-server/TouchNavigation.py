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

    self.multi_touch_center         = avango.gua.make_identity_mat()

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

  def addContact(self, HANDMAT, ID):
    if len(self.touch_contacts) == 0:
      newContact = TouchContact(ID, HANDMAT)
      self.touch_contacts.append(newContact)
      return True

    elif len(self.touch_contacts) == 1:
      if self.touch_contacts[0].input_id == ID:
        self.touch_contacts[0].update(HANDMAT)
        self.evaluateContacts()
        return True
      else:
        newContact = TouchContact(ID, HANDMAT) 
        self.touch_contacts.append(newContact)
        self.computeMultiTouchCenter()
        self.sf_reference_mat.value = avango.gua.make_trans_mat(self.multi_touch_center)
        return True

    else:
      for contact in self.touch_contacts:
        if contact.input_id == ID:
          contact.update(HANDMAT)
          self.evaluateContacts()
          return True

    return False

  def computeMultiTouchCenter(self):
    if len(self.touch_contacts):
      pos1 = self.touch_contacts[0].input_mat.get_translate()
      pos2 = self.touch_contacts[1].input_mat.get_translate()
      pos1ToPos2 = pos2 - pos1
      self.multi_touch_center = pos1 + avango.gua.Vec3(0.5*pos1ToPos2.x, 0.5*pos1ToPos2.y, 0.5*pos1ToPos2.z)
      print(self.multi_touch_center)

  def evaluateContacts(self):
    
    if len(self.touch_contacts) == 1:
      self.translate()

    elif len(self.touch_contacts) == 2:
      self.rotate()

  def translate(self):
    relativeInput = self.touch_contacts[0].getRelativeInput()

    self.map_movement_input(-relativeInput.x, -relativeInput.y, -relativeInput.z, 0, 0, 0)
    #mat = self.bc_get_nav_mat()
    #transVec = avango.gua.Vec3(-1.0 * relativeInput.x, -1.0 * relativeInput.y, -1.0 * relativeInput.z)

    #self.bc_set_nav_mat(avango.gua.make_trans_mat(transVec) * mat)

  def rotate(self):
    #pass
    #relativeInput = self.touch_contacts[0].getRelativeInput()
    pos1 = self.touch_contacts[0].last_input_mat.get_translate()
    pos2 = self.touch_contacts[1].last_input_mat.get_translate()
    lastVec = pos2 - pos1
    lastVec.normalize()
    
    pos1 = self.touch_contacts[0].input_mat.get_translate()
    pos2 = self.touch_contacts[1].input_mat.get_translate()
    newVec = pos2 - pos1
    newVec.normalize()

    print("lastVec: " , lastVec)
    print("newVec: " , newVec)
    
    alpha = 0
    if lastVec != newVec:
      cosAlpha = max(min(lastVec.dot(newVec), 1.0), -1.0)
      print("cosAlpha: ", cosAlpha)
      alpha = math.acos(cosAlpha)

    alphaDeg = alpha * 180 / math.pi
    print("alpha: ", alpha)
    print("alphaDeg: ", alphaDeg)
    self.map_movement_input(0,0,0,0,-alphaDeg,0)

  def removeContact(self, ID):
    kill_contact = None

    for contact in self.touch_contacts:
      if contact.input_id == ID:
        kill_contact = contact
        break

    if kill_contact != None:
      self.touch_contacts.remove(kill_contact)

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

  def __init__(self, INPUTID, STARTMAT):
    self.input_id       = INPUTID
    
    self.input_mat      = STARTMAT

    self.last_input_mat = STARTMAT

  def update(self, NEWMAT):
    self.last_input_mat = self.input_mat

    self.input_mat      = NEWMAT
    
  def getRelativeInput(self):
    return self.input_mat.get_translate() - self.last_input_mat.get_translate() 
