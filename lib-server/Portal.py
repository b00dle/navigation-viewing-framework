#!/usr/bin/python

## @file
# Contains classes Portal.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ApplicationManager import *
from Display import *
from ConsoleIO import *
from scene_config import scenegraphs
import Utilities

# import python libraries
import time
import math


## A Portal is the display of another location on a virtual display.
class Portal(Display):

  ## @var num_instances_created
  # Static intance counter to assign proper IDs to the portals.
  num_instances_created = 0

  ## Custom constructor.
  # @param PORTAL_MATRIX Matrix where the portal display is located (entry).
  # @param WIDTH Width of the portal in meters.
  # @param HEIGHT Height of the portal in meters.
  # @param VIEWING_MODE Viewing mode of the portal, can be either "2D" or "3D".
  # @param CAMERA_MODE Projection mode of the portal camera, can be either "PERSPECTIVE" or "ORTHOGRAPHIC".
  # @param NEGATIVE_PARALLAX Indicating if negative parallax is allowed in the portal, can be either "True" or "False".
  # @param BORDER_MATERIAL The material string to be used for the portal's border.
  # @param TRANSITABLE Boolean saying if teleportation for this portal is enabled.
  def __init__(self
             , PORTAL_MATRIX
             , WIDTH
             , HEIGHT):


    _stereo = True
    self.base_constructor("portal_" + str(Portal.num_instances_created), (1000, 1000), (WIDTH, HEIGHT), _stereo)

    ## @var id
    # The portal ID assigned to the portal.
    self.id = Portal.num_instances_created
    Portal.num_instances_created += 1

    ## @var portal_matrix
    # Matrix where the portal display is located (entry).
    self.portal_matrix = PORTAL_MATRIX

  ## Returns a boolean value saying if this display is virtual.
  def is_virtual(self):
    return True