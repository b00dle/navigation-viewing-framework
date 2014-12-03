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

## Proxy geometry for virutal displays. Used for ray intersection within virtual displays.
class VirtualDisplayProxy(avango.script.Script):

  ## @var sf_entry_transform
  # Transformation matrix field of the virtual display group's entry matrix.
  sf_entry_transform = avango.gua.SFMatrix4()
  sf_entry_transform.value = avango.gua.make_identity_mat()

  ## @var sf_screen_transform
  # Transformation matrix field of the virtual display's screen in the virtual display group.
  sf_screen_transform = avango.gua.SFMatrix4()
  sf_screen_transform.value = avango.gua.make_identity_mat()

  ## @var sf_width
  # Width of the virtual display's screen.
  sf_width = avango.SFFloat()

  ## @var sf_height
  # Height of the virtual display's screen.
  sf_height = avango.SFFloat()

  ## @var sf_geometry_matrix
  # Output matrix field that is written to the geometry node of the proxy geometry.
  sf_geometry_matrix = avango.gua.SFMatrix4()
  sf_geometry_matrix.value = avango.gua.make_identity_mat()

  ## Default constructor.
  def __init__(self):
    self.super(VirtualDisplayProxy).__init__()

  ## Custom constructor.
  # @param NAME Name of this virtual display proxy geometry.
  # @param PARENT_NODE Parent scenegraph node to which the proxy geometry subtree is to be added.
  # @param VIRTUAL_DISPLAY_GROUP Instance of VirtualDisplayGroup to which this proxy is belonging to.
  # @param SCREEN_NODE Screen node for which the proxy geometry is created.
  def my_constructor(self, NAME, PARENT_NODE, VIRTUAL_DISPLAY_GROUP, SCREEN_NODE):

    # init field connections
    self.sf_entry_transform.connect_from(VIRTUAL_DISPLAY_GROUP.entry_node.Transform)
    self.sf_screen_transform.connect_from(SCREEN_NODE.Transform)
    self.sf_width.connect_from(SCREEN_NODE.Width)
    self.sf_height.connect_from(SCREEN_NODE.Height)

    ## @var entry_transform_node
    # First node of the proxy geometry's subtree storing the virtual display group's entry transformation.
    self.entry_transform_node = avango.gua.nodes.TransformNode(Name = NAME)
    self.entry_transform_node.Transform.connect_from(self.sf_entry_transform)
    PARENT_NODE.Children.value.append(self.entry_transform_node)

    ## @var screen_transform_node
    # Second node of the proxy geometry's subtree storing the transformation of the respective screen node.
    self.screen_transform_node = avango.gua.nodes.TransformNode(Name = "screen_transform")
    self.screen_transform_node.Transform.connect_from(self.sf_screen_transform)
    self.entry_transform_node.Children.value.append(self.screen_transform_node)

    _loader = avango.gua.nodes.TriMeshLoader()

    ## @var geometry_node
    # Third node of the proxy geometry's subtree (the geometry itself).
    self.geometry_node = _loader.create_geometry_from_file("geometry"
                                                         , "data/objects/plane.obj"
                                                         , "data/materials/White.gmd"
                                                         , avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
    self.geometry_node.Transform.connect_from(self.sf_geometry_matrix)
    self.geometry_node.GroupNames.value = ["man_pick_group", "virtual_proxy"]
    self.geometry_node.ShadowMode.value = avango.gua.ShadowMode.OFF
    self.screen_transform_node.Children.value.append(self.geometry_node)


  ## Evaluated when an input field changes.
  def evaluate(self):

    self.sf_geometry_matrix.value = avango.gua.make_rot_mat(90, 1, 0 ,0) * \
                                    avango.gua.make_scale_mat(self.sf_width.value, 1.0, self.sf_height.value)
