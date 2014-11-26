#!/usr/bin/python

## @file
# Contains classes VirtualDisplay.

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


## A VirtualDisplay is the display of another location in the scene on a texture.
class VirtualDisplay(Display):

  ## @var num_instances_created
  # Static intance counter to assign proper IDs to the portals.
  num_instances_created = 0

  ## Custom constructor.
  # @param ENTRY_MATRIX Matrix where the portal display is located (entry).
  # @param WIDTH Width of the portal in meters.
  # @param HEIGHT Height of the portal in meters.
  def __init__(self
             , ENTRY_MATRIX
             , WIDTH
             , HEIGHT):

    _stereo = True
    self.base_constructor("portal_" + str(VirtualDisplay.num_instances_created), (1000, 1000), (WIDTH, HEIGHT), _stereo)

    ## @var id
    # The portal ID assigned to the portal.
    self.id = VirtualDisplay.num_instances_created
    VirtualDisplay.num_instances_created += 1

    ## @var entry_matrix
    # Matrix where the portal display is located (entry).
    self.entry_matrix = ENTRY_MATRIX

  ## Returns a boolean value saying if this display is virtual.
  def is_virtual(self):
    return True