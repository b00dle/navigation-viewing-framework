#!/usr/bin/python

## @file
# Contains classes DisplayGroup and VirtualDisplayGroup.

# import avango-guacamole libraries
import avango
import avango.gua

# import framework libraries
from ApplicationManager import *
from scene_config import scenegraphs


## Collection of displays that are semantically one navigational unit, although users
# might have individual navigations assigned.
class DisplayGroup:

  ## Custom constructor.
  # @param ID Identification number of this DisplayGroup within the workspace.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assigned to the display group.
  # @param VISIBILITY_TAG Tag used by the Tools' visibility matrices to define if they are visible for this display group.
  # @param OFFSET_TO_WORKSPACE Offset describing the origin of this display group with respect to the origin of the workspace.
  # @param WORKSPACE_TRANSMITTER_OFFSET Transmitter offset applied in the workspace.
  def __init__(self
             , ID
             , DISPLAY_LIST
             , NAVIGATION_LIST
             , VISIBILITY_TAG
             , OFFSET_TO_WORKSPACE
             , WORKSPACE_TRANSMITTER_OFFSET):

    ## @var id
    # Identification number of this DisplayGroup within the workspace.
    self.id = ID

    ## @var displays
    # List of Display instances assigned to this display group.
    self.displays = DISPLAY_LIST

    ## @var navigations
    # List of (Steering-)Navigation instances assigned to the display group.
    self.navigations = NAVIGATION_LIST

    ## @var visibility_tag
    # Tag used by the Tools' visibility matrices to define if they are visible for this display group.
    self.visibility_tag = VISIBILITY_TAG

    ## @var offset_to_workspace
    # Offset describing the origin of this display group with respect to the origin of the workspace.
    self.offset_to_workspace = OFFSET_TO_WORKSPACE

    # update device tracking transmitter offset
    for _navigation in self.navigations:
      
      try:
        _navigation.device.tracking_reader.set_transmitter_offset(self.offset_to_workspace * WORKSPACE_TRANSMITTER_OFFSET)
      except:
        pass


## Collection of virtual displays that are semantically one navigational unit, although users
# might have individual navigations assigned.
class VirtualDisplayGroup(DisplayGroup):

  ## @var num_instances_created
  # Static intance counter to assign proper IDs to the portals.
  num_instances_created = 0

  ## @var portal_group_node
  # Scenegraph node on server side to which all portal relevant nodes are appended to.
  portal_group_node = avango.gua.nodes.TransformNode(Name = "virtual_displays")

  ## Custom constructor.
  # @param DISPLAY_LIST List of Display instances to be assigned to the new display group.
  # @param NAVIGATION_LIST List of (Steering-)Navigation instances to be assigned to the display group.
  # @param VISIBILITY_TAG Tag used by the Tools' visibility matrices to define if they are visible for this display group.
  # @param VIEWING_MODE Viewing mode of the virtual displays in the group, can be either "2D" or "3D".
  # @param CAMERA_MODE Projection mode of the virtual displays in the group, can be either "PERSPECTIVE" or "ORTHOGRAPHIC".
  # @param NEGATIVE_PARALLAX Indicating if negative parallax is allowed in the the virtual displays of the group, can be either "True" or "False".
  # @param BORDER_MATERIAL The material string to be used for the the virtual displays' border.
  # @param TRANSITABLE Boolean saying if teleportation for the virtual displays in the group is enabled.
  # @param PORTAL_NODE_NAME_ATTACHMENT Additional string information passed in the name of portal_node.
  def __init__(self
             , DISPLAY_LIST
             , NAVIGATION_LIST
             , VISIBILITY_TAG
             , VIEWING_MODE
             , CAMERA_MODE
             , NEGATIVE_PARALLAX
             , BORDER_MATERIAL
             , TRANSITABLE
             , PORTAL_NODE_NAME_ATTACHMENT = "wa_dga"):


    # call base class constructor
    DisplayGroup.__init__(self
                        , None # id is set properly when nodes are attached to the scenegraph
                        , DISPLAY_LIST
                        , NAVIGATION_LIST
                        , VISIBILITY_TAG
                        , avango.gua.make_identity_mat()
                        , avango.gua.make_identity_mat())

    ## @var NET_TRANS_NODE
    # Reference to the nettrans node of the scenegraph for portal_group_node to attach.
    self.NET_TRANS_NODE = scenegraphs[0]["/net"]

    ## @var portal_node_name_attachment
    # Additional string information passed in the name of the virtual display group node.
    self.portal_node_name_attachment = PORTAL_NODE_NAME_ATTACHMENT

    ## @var viewing_mode
    # Viewing mode of the virtual displays in the group, can be either "2D" or "3D".
    self.viewing_mode = VIEWING_MODE

    ## @var camera_mode
    # Projection mode of the virtual displays in the group, can be either "PERSPECTIVE" or "ORTHOGRAPHIC".
    self.camera_mode = CAMERA_MODE

    ## @var negative_parallax
    # Indicating if negative parallax is allowed in the the virtual displays of the group, can be either "True" or "False".
    self.negative_parallax = NEGATIVE_PARALLAX

    ## @var border_material
    # The material string to be used for the the virtual displays' border.
    self.border_material = BORDER_MATERIAL

    ## @var visible
    # Boolean string variable indicating if the portal is currently visible.
    self.visible = "True"

    ## @var transitable
    # Boolean saying if teleportation for the virtual displays in the group is enabled.
    self.transitable = TRANSITABLE


  ## Appends the necessary virtual display group nodes to the scenegraph.
  def add_virtual_display_nodes(self):

    self.id = VirtualDisplayGroup.num_instances_created
    VirtualDisplayGroup.num_instances_created += 1

    # determine offsets for all virtual displays

    _offsets = []

    for _display in self.displays:

      if self.displays.index(_display) == 0:
        _offsets.append(avango.gua.make_identity_mat())
      else:
        _offsets.append(avango.gua.make_inverse_mat(self.displays[0].entry_matrix) * \
                        _display.entry_matrix)


    # append the viewing setup for this display group to the scenegraph

    _nettrans_node = scenegraphs[0]["/net"]

    if self.id == 0:
      self.NET_TRANS_NODE.Children.value.append(VirtualDisplayGroup.portal_group_node)
      self.NET_TRANS_NODE.distribute_object(VirtualDisplayGroup.portal_group_node)

    ## @var portal_node
    # Grouping node for this virtual display group below the group node for all virtual displays.
    self.portal_node = avango.gua.nodes.TransformNode(Name = "vir_dg" + str(self.id) + "_" + self.portal_node_name_attachment)
    VirtualDisplayGroup.portal_group_node.Children.value.append(self.portal_node)
    self.NET_TRANS_NODE.distribute_object(self.portal_node)

    ## @var settings_node
    # Node whose group names store information about the virtual display group settings, such as viewing mode, etc.
    self.settings_node = avango.gua.nodes.TransformNode(Name = "settings")
    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]
    self.portal_node.Children.value.append(self.settings_node)
    self.NET_TRANS_NODE.distribute_object(self.settings_node)

    ## @var entry_node
    # Node storing the matrix of the virtual display group's primary display's entry.
    self.entry_node = avango.gua.nodes.TransformNode(Name = "entry")
    self.entry_node.Transform.value = self.displays[0].entry_matrix
    self.portal_node.Children.value.append(self.entry_node)
    self.NET_TRANS_NODE.distribute_object(self.entry_node)

    ## @var exit_node
    # Node storing the matrix of the virtual display group's exit.
    self.exit_node = avango.gua.nodes.TransformNode(Name = "exit")
    self.exit_node.Transform.value = avango.gua.make_identity_mat()
    self.portal_node.Children.value.append(self.exit_node)
    self.NET_TRANS_NODE.distribute_object(self.exit_node)


    # add texture offset nodes and screen nodes
    
    ## @var texture_offset_nodes
    # Scenegraph nodes below entry that offset the textures by the virtual screen transformations.
    self.texture_offset_nodes = []
    
    ## @var screen_nodes
    # List of screen nodes belonging to this virtual display group.
    self.screen_nodes = []

    for _offset in _offsets:

      _index = _offsets.index(_offset)
      
      _offset_node = avango.gua.nodes.TransformNode(Name = "offset_tex_" + str(_index))
      _offset_node.Transform.value = _offset
      self.entry_node.Children.value.append(_offset_node)
      self.NET_TRANS_NODE.distribute_object(_offset_node)
      self.texture_offset_nodes.append(_offset_node)

      _screen_node = avango.gua.nodes.ScreenNode(Name = "screen_" + str(_index))
      _screen_node.Width.value = self.displays[_index].size[0]
      _screen_node.Height.value = self.displays[_index].size[1]
      _screen_node.Transform.value = _offset
      self.exit_node.Children.value.append(_screen_node)
      self.NET_TRANS_NODE.distribute_object(_screen_node)
      self.screen_nodes.append(_screen_node)


  ## Switches viewing_mode to the other state.
  def switch_viewing_mode(self):
    if self.viewing_mode == "2D":
      self.viewing_mode = "3D"
    else:
      self.viewing_mode = "2D"

    for _user_repr in ApplicationManager.all_user_representations:
      if _user_repr.DISPLAY_GROUP == self:

        if self.viewing_mode == "2D":
          _user_repr.make_default_viewing_setup()
        else:
          _user_repr.make_complex_viewing_setup()

    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]

  ## Switches camera_mode to the other state.
  def switch_camera_mode(self):
    if self.camera_mode == "PERSPECTIVE":
      self.camera_mode = "ORTHOGRAPHIC"
    else:
      self.camera_mode = "PERSPECTIVE"

    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]

  ## Switches negative_parallax to the other state.
  def switch_negative_parallax(self):
    if self.negative_parallax == "True":
      self.negative_parallax = "False"
    else:
      self.negative_parallax = "True"

    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]


  ## Connects the virtual display group's primary entry matrix to a given field.
  # @param SF_MATRIX The matrix field to be connected.
  def connect_entry_matrix(self, SF_MATRIX):

    self.entry_node.Transform.disconnect()
    
    if SF_MATRIX != None:
      self.entry_node.Transform.connect_from(SF_MATRIX)

  ## Sets the border material to be used for the portal.
  # @param BORDER_MATERIAL The material string to be set.
  def set_border_material(self, BORDER_MATERIAL):
    self.border_material = BORDER_MATERIAL
    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]

  ## Sets the visiblity of this portal.
  # @param VISIBLE Boolean describing the visibility to be set.
  def set_visibility(self, VISIBLE):
    if VISIBLE:
      self.visible = "True"
    else:
      self.visible = "False"

    self.settings_node.GroupNames.value = ["0-" + self.viewing_mode, "1-" + self.camera_mode, "2-" + self.negative_parallax, "3-" + self.border_material, "4-" + self.visible]

    for _workspace in ApplicationManager.all_workspaces:
      for _tool in _workspace.tools:
        _tool.handle_correct_visibility_groups_for(self)

  ## Sets the size of a screen node of this virtual display group.
  # @param INDEX Index of the screen node to set a new size for.
  # @param WIDTH The new width in meters to be set.
  # @param HEIGHT The new height in meters to be set.
  def set_size(self, INDEX, WIDTH, HEIGHT):
    self.size = (WIDTH, HEIGHT)
    self.screen_nodes[INDEX].Width.value = WIDTH
    self.screen_nodes[INDEX].Height.value = HEIGHT

  ## Deletes the scenegraph representation of this virtual display group.
  def delete(self):

    VirtualDisplayGroup.portal_group_node.Children.value.remove(self.portal_node)

    for _user_repr in ApplicationManager.all_user_representations:
      if _user_repr.DISPLAY_GROUP == self:
        ApplicationManager.all_user_representations.remove(_user_repr)
        del _user_repr

    self.delete_downwards_from(self.portal_node)
    del self.portal_node

  ## Deletes all nodes below a given node.
  # @param NODE The node to start deleting from.
  def delete_downwards_from(self, NODE):

    for _child in NODE.Children.value:
      self.delete_downwards_from(_child)
      del _child