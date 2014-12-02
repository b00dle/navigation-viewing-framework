#!/usr/bin/python

## @file
# Contains class VirtualDisplay.

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


## A VirtualDisplay is a display medium of another location in the scene in the form of a texture.
class VirtualDisplay(Display):

  ## @var num_instances_created
  # Static intance counter to assign proper IDs to the portals.
  num_instances_created = 0

  ## Custom constructor.
  # @param ENTRY_MATRIX Matrix where the virtual display is located in the scene (entry).
  # @param WIDTH Width of the virtual display in meters.
  # @param HEIGHT Height of the virtual display in meters.
  def __init__(self
             , ENTRY_MATRIX
             , WIDTH
             , HEIGHT):

    _stereo = True
    self.base_constructor("portal_" + str(VirtualDisplay.num_instances_created), (1000, 1000), (WIDTH, HEIGHT), _stereo)

    ## @var id
    # The ID assigned to the virtual display.
    self.id = VirtualDisplay.num_instances_created
    VirtualDisplay.num_instances_created += 1

    ## @var entry_matrix
    # Matrix where the virtual display is located in the scene (entry).
    self.entry_matrix = ENTRY_MATRIX

  ## Returns a boolean value saying if this display is virtual.
  def is_virtual(self):
    return True