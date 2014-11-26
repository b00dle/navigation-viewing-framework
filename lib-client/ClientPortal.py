#!/usr/bin/python

## @file
# Contains class ClientPortal.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed

# import framework libraries
from ConsoleIO import *

# import python libraries
import math

## Class to create, handle and destroy Portal instances on client side.
class ClientPortalManager(avango.script.Script):

  ## @var mf_portal_group_children
  # Children field of the server portal group to be checked for changes.
  mf_portal_group_children = avango.gua.MFNode()

  ## Default constructor.
  def __init__(self):
    self.super(ClientPortalManager).__init__()

    ## @var mf_portal_group_children_connected
    # Boolean indicating if the field connection to mf_portal_group_children was established.
    self.mf_portal_group_children_connected = False

    ## @var portals
    # List of currently active ClientPortal instances.
    self.portals = []

    # set evaluation policy
    self.always_evaluate(True)

  ## Custom constructor.
  # @param SCENEGRAPH Reference to the scenegraph.
  # @param VIEW_LIST List of all View instances in the scene.
  def my_constructor(self, SCENEGRAPH, VIEW_LIST):

    ## @var SCENEGRAPH
    # Reference to the scenegraph.
    self.SCENEGRAPH = SCENEGRAPH

    ## @var VIEW_LIST
    # List of all View instances in the scene.
    self.VIEW_LIST = VIEW_LIST

  ## Tells all view instances that a new portal was added to the scene.
  # @param SERVER_PORTAL_NODE Server portal grouping node.
  def notify_views_on_added_portal(self, SERVER_PORTAL_NODE):

    for _view in self.VIEW_LIST:
      _view.create_portal_preview(SERVER_PORTAL_NODE)

  ## Tells all view instances that a new portal was removed from the scene.
  # @param SERVER_PORTAL_NODE Server portal grouping node.
  def notify_views_on_removed_portal(self, SERVER_PORTAL_NODE):

    for _view in self.VIEW_LIST:
      _view.remove_portal_preview(SERVER_PORTAL_NODE)

  ## Evaluated every frame.
  def evaluate(self):

    try:
      _portal_group_node = self.SCENEGRAPH["/net/virtual_displays"]
    except:
      return

    # connect mf_portal_group_children only once
    if _portal_group_node != None and self.mf_portal_group_children_connected == False:
      self.mf_portal_group_children.connect_from(_portal_group_node.Children)
      self.mf_portal_group_children_connected = True

  ## Called whenever mf_portal_group_children changes.
  @field_has_changed(mf_portal_group_children)
  def mf_portal_group_children_changed(self):

    # boolean list of which Portal instances have already been parsed.
    _instances_matched = [False for i in range(len(self.portals))]

    # iterate over all children of the server portal node
    for _node in self.mf_portal_group_children.value:

      _portal_instance_found = False
      
      # iterate over all Portal instances
      for _i in range(len(self.portals)):

        _portal = self.portals[_i]

        # check for matching instance and break when found
        if _portal.compare_server_portal_node(_node) == True:
          _portal_instance_found = True
          _instances_matched[_i] = True
          break

      # if no matching instance was found, add a new ClientPortal for the node
      if _portal_instance_found == False:
        _portal = ClientPortal(_node)
        self.portals.append(_portal)
        self.notify_views_on_added_portal(_node)

    # check for instances that have not been matched (removed on server side)
    for _i in range(len(_instances_matched)):
      _bool = _instances_matched[_i]

      if _bool == False:

        _portal_to_delete = self.portals[_i]
        self.notify_views_on_removed_portal(_portal_to_delete.SERVER_PORTAL_NODE)

        self.portals.remove(_portal_to_delete)

        # object destruction
        del _portal_to_delete


## Client counterpart for the server Portal class.
class ClientPortal:

  ## Custom constructor.
  # @param SERVER_PORTAL_NODE New portal scenegraph node that was added on server side.
  def __init__(self, SERVER_PORTAL_NODE):

    ## @var SERVER_PORTAL_NODE
    # New portal scenegraph node that was added on server side.
    self.SERVER_PORTAL_NODE = SERVER_PORTAL_NODE

  ## Checks if a given server portal node matches with the server portal node of this instance.
  # @param SERVER_PORTAL_NODE The server portal node to be checked for.
  def compare_server_portal_node(self, SERVER_PORTAL_NODE):
    if self.SERVER_PORTAL_NODE == SERVER_PORTAL_NODE:
      return True

    return False


## A PortalPreView is instantiated for each View for each ClientPortal and displays the correct 
# perspective for the view within the portal.
class PortalPreView(avango.script.Script):

  ## @var sf_screen_width
  # Field containing the current width of the portal screen.
  sf_screen_width = avango.SFFloat()

  ## @var sf_screen_height
  # Field containing the current height of the portal screen.
  sf_screen_height = avango.SFFloat()

  ## @var mf_portal_modes
  # Field containing the GroupNames of the associated portal node. Used for transferring portal mode settings.
  mf_portal_modes = avango.MFString()

  ## Default constructor.
  def __init__(self):
    self.super(PortalPreView).__init__()

  ## Custom constructor.
  # @param SERVER_PORTAL_NODE The portal scenegraph node on server side to be associated with this instance.
  # @param VIEW The View instance to be associated with this instance.
  def my_constructor(self, SERVER_PORTAL_NODE, VIEW):
    
    ## @var SERVER_PORTAL_NODE
    # The portal scenegraph node on server side to be associated with this instance.
    self.SERVER_PORTAL_NODE = SERVER_PORTAL_NODE

    ## @var VIEW
    # The View instance to be associated with this instance.
    self.VIEW = VIEW

    _user_left_eye = VIEW.SCENEGRAPH["/net/w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id) + "/head/eyeL"]

    # if no node is present, this view is not occupied, stop pre view creation
    if _user_left_eye == None:
      print_warning("No user nodes present for " + "w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))
      return
    else:
      print_message("Construct PortalPreView for " + SERVER_PORTAL_NODE.Name.value + " and w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id))

    ## @var transformed_head_node
    # view_transform_node/head of the corresponding UserRepresentation in the portal on server side.
    self.transformed_head_node = VIEW.SCENEGRAPH["/net/virtual_displays/" + SERVER_PORTAL_NODE.Name.value + "/exit/head_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]

    ## @var head_node
    # view_transform_node/head of the corresponding physical user representation
    self.head_node = self.VIEW.SCENEGRAPH["/net/w" + str(self.VIEW.workspace_id) + "_dg" + str(self.VIEW.display_group_id) + "_u" + str(self.VIEW.user_id) + "/head"]

    ## @var left_eye_node
    # Scenegraph node representing the left eye's position in the portal's exit space.
    self.left_eye_node = self.transformed_head_node.Children.value[0]

    ## @var right_eye_node
    # Scenegraph node representing the left eye's position in the portal's exit space.
    self.right_eye_node = self.transformed_head_node.Children.value[1]

    ## @var entry_node
    # Server portal node containing the portal matrix (entry transformation).
    self.entry_node = VIEW.SCENEGRAPH["/net/virtual_displays/" + SERVER_PORTAL_NODE.Name.value + "/entry"]

    ##
    #
    self.texture_offset_nodes = []

    for _entry_child in self.entry_node.Children.value:
      self.texture_offset_nodes.append(_entry_child)


    ## @var exit_node
    # Server portal node containing the scene matrix (exit transformation).
    self.exit_node = VIEW.SCENEGRAPH["/net/virtual_displays/" + SERVER_PORTAL_NODE.Name.value + "/exit"]

    ##
    #
    self.screen_nodes = []

    for _exit_child in self.exit_node.Children.value:
      if _exit_child.Name.value.startswith("screen"):
        self.screen_nodes.append(_exit_child)


    # debug screen visualization TO BE REDONE
    #_loader = avango.gua.nodes.TriMeshLoader()
    #_node = _loader.create_geometry_from_file("screen_visualization", "data/objects/screen.obj", "data/materials/ShadelessBlack.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
    #_node.Transform.value = self.screen_node.Transform.value * \
    #                        avango.gua.make_scale_mat(self.screen_node.Width.value, self.screen_node.Height.value, 1.0)
    #self.scene_matrix_node.Children.value.append(_node)

    ##
    #
    self.cameras = []

    ##
    #
    self.pipelines = []

    ##
    #
    self.textured_quads = []

    ##
    #
    self.back_geometries = []

    ##
    #
    self.border_geometries = []

    for _screen_node in self.screen_nodes:

      # create camera
      _camera = avango.gua.nodes.Camera()
      _camera.SceneGraph.value = VIEW.SCENEGRAPH.Name.value

      _camera.LeftScreen.value = _screen_node.Path.value
      _camera.RightScreen.value = _screen_node.Path.value
      _camera.LeftEye.value = self.left_eye_node.Path.value
      _camera.RightEye.value = self.right_eye_node.Path.value

      _camera.RenderMask.value = "(main_scene | " + self.SERVER_PORTAL_NODE.Name.value + "_" + self.transformed_head_node.Name.value + ") && !do_not_display_group && !portal_invisible_group"
      self.cameras.append(_camera)

      # create pipeline 
      _pipeline = avango.gua.nodes.Pipeline()
      _pipeline.Enabled.value = True
      _pipeline.EnableGlobalClippingPlane.value = True
      _pipeline.Camera.value = _camera

      # init pipline value connections
      #_pipeline.BackgroundMode.connect_from(VIEW.pipeline.BackgroundMode)
      _pipeline.BackgroundTexture.connect_from(VIEW.pipeline.BackgroundTexture)
      _pipeline.FogTexture.connect_from(VIEW.pipeline.FogTexture)
      _pipeline.EnableBloom.connect_from(VIEW.pipeline.EnableBloom)
      _pipeline.BloomIntensity.connect_from(VIEW.pipeline.BloomIntensity)
      _pipeline.BloomThreshold.connect_from(VIEW.pipeline.BloomThreshold)
      _pipeline.BloomRadius.connect_from(VIEW.pipeline.BloomRadius)
      _pipeline.EnableSsao.connect_from(VIEW.pipeline.EnableSsao)
      _pipeline.SsaoRadius.connect_from(VIEW.pipeline.SsaoRadius)
      _pipeline.SsaoIntensity.connect_from(VIEW.pipeline.SsaoIntensity)
      #_pipeline.EnableBackfaceCulling.connect_from(VIEW.pipeline.EnableBackfaceCulling)
      _pipeline.EnableBackfaceCulling.value = False
      _pipeline.EnableFrustumCulling.connect_from(VIEW.pipeline.EnableFrustumCulling)
      _pipeline.EnableFXAA.connect_from(VIEW.pipeline.EnableFXAA)
      _pipeline.AmbientColor.connect_from(VIEW.pipeline.AmbientColor)
      _pipeline.EnableFog.connect_from(VIEW.pipeline.EnableFog)
      _pipeline.FogStart.connect_from(VIEW.pipeline.FogStart)
      _pipeline.FogEnd.connect_from(VIEW.pipeline.FogEnd)

      _pipeline.LeftResolution.value = avango.gua.Vec2ui(1024, 1024)
      _pipeline.RightResolution.value = _pipeline.LeftResolution.value

      if VIEW.is_stereo:  
        _pipeline.EnableStereo.value = True
      else:
        _pipeline.EnableStereo.value = False

      _pipeline.OutputTextureName.value = self.SERVER_PORTAL_NODE.Name.value + "_" + _screen_node.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)
      
      _pipeline.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE
      _pipeline.BackgroundTexture.value = "data/textures/sky.jpg"

      self.VIEW.pipeline.PreRenderPipelines.value.append(_pipeline)

      self.pipelines.append(_pipeline)

      # create textured quad
      _loader = avango.gua.nodes.TriMeshLoader()


      _textured_quad = avango.gua.nodes.TexturedQuadNode(Name = "texture_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id),
                                                         Texture = self.SERVER_PORTAL_NODE.Name.value + "_" + _screen_node.Name.value + "_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id),
                                                         IsStereoTexture = self.VIEW.is_stereo,
                                                         Width = _screen_node.Width.value,
                                                         Height = _screen_node.Height.value
                                                         )
      _textured_quad.GroupNames.value = ["w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
      self.entry_node.Children.value[self.screen_nodes.index(_screen_node)].Children.value.append(_textured_quad)
      self.textured_quads.append(_textured_quad)


      # create back geometry
      _back_geometry = _loader.create_geometry_from_file("back_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id), "data/objects/plane.obj", "data/materials/ShadelessBlue.gmd", avango.gua.LoaderFlags.DEFAULTS)
      _back_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, -0.001) * avango.gua.make_rot_mat(90, 1, 0, 0) * avango.gua.make_scale_mat(_screen_node.Width.value, 1.0, _screen_node.Height.value)
      _back_geometry.GroupNames.value = ["portal_invisible_group", "w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
      self.entry_node.Children.value[self.screen_nodes.index(_screen_node)].Children.value.append(_back_geometry)
      self.back_geometries.append(_back_geometry)

      # create portal border
      _portal_border = _loader.create_geometry_from_file("border_w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id), "data/objects/screen.obj", "data/materials/ShadelessBlue.gmd", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
      _portal_border.ShadowMode.value = avango.gua.ShadowMode.OFF
      _portal_border.GroupNames.value = ["w" + str(VIEW.workspace_id) + "_dg" + str(VIEW.display_group_id) + "_u" + str(VIEW.user_id)]
      _portal_border.Transform.value = avango.gua.make_scale_mat(_screen_node.Width.value, _screen_node.Height.value, 1.0)
      self.entry_node.Children.value[self.screen_nodes.index(_screen_node)].Children.value.append(_portal_border)
      self.border_geometries.append(_portal_border)

    
    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)

    # init field connections
    self.mf_portal_modes.connect_from(VIEW.SCENEGRAPH["/net/virtual_displays/" + SERVER_PORTAL_NODE.Name.value + "/settings"].GroupNames)
    #self.sf_screen_width.connect_from(self.screen_node.Width)
    #self.sf_screen_height.connect_from(self.screen_node.Height)

    # set evaluation policy
    self.always_evaluate(True)

  ## Compares a given portal node with the portal node associated with this instance.
  # @param PORTAL_NODE The portal node to be compared with.
  def compare_portal_node(self, PORTAL_NODE):
    if self.SERVER_PORTAL_NODE == PORTAL_NODE:
      return True

    return False

  ## Updates the size of the portal according to the screen node.
  def update_size(self):
    
    pass
    #try:
    #  self.textured_quad
    #except:
    #  return

    #self.textured_quad.Width.value = self.screen_node.Width.value
    #self.textured_quad.Height.value = self.screen_node.Height.value
    #self.back_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * avango.gua.make_rot_mat(90, 1, 0, 0) * avango.gua.make_scale_mat(self.screen_node.Width.value, 1.0, self.screen_node.Height.value)
    #self.portal_border.Transform.value = avango.gua.make_scale_mat(self.screen_node.Width.value, self.screen_node.Height.value, 1.0)

  ## Removes this portal from the local portal group and destroys all the scenegraph nodes.
  def deactivate(self):

    # disable pipeline and evaluation loop
    self.frame_trigger.Active.value = False
    self.pipeline.Enabled.value = False

    #self.portal_matrix_node.Children.value.remove(self.portal_border)
    #del self.portal_border
    
    #self.portal_matrix_node.Children.value.remove(self.textured_quad)
    #del self.textured_quad
    #del self.back_geometry

    #del self.pipeline
    #del self.camera

  ## Called whenever mf_portal_modes changes.
  @field_has_changed(mf_portal_modes)
  def mf_portal_modes_changed(self):

    # check for deletion
    try:
      self.pipelines
    except:
      return

    #print "change modes to", self.mf_portal_modes.value[0], self.mf_portal_modes.value[1], self.mf_portal_modes.value[2], self.mf_portal_modes.value[3], self.mf_portal_modes.value[4]

    # check for camera mode
    if self.mf_portal_modes.value[1] == "1-ORTHOGRAPHIC":

      for _camera in self.cameras:
        _camera.Mode.value = avango.gua.ProjectionMode.ORTHOGRAPHIC

    else:

      for _camera in self.cameras:
        _camera.Mode.value = avango.gua.ProjectionMode.PERSPECTIVE

    # check for negative parallax
    if self.mf_portal_modes.value[2] == "2-True":

      for _pipeline in self.pipelines:
        _pipeline.EnableGlobalClippingPlane.value = False

    else:

      for _pipeline in self.pipelines:
        _pipeline.EnableGlobalClippingPlane.value = True

    # set correct border material (compare with first border as we assume all other borders to be of identical material)
    if self.border_geometries[0].Material.value != self.mf_portal_modes.value[3].replace("3-", ""):
      
      _material = self.mf_portal_modes.value[3].replace("3-", "")

      if _material != "None":

        for _border in self.border_geometries:
          _border.Material.value = _material

        for _back_geometry in self.back_geometries:
          _back_geometry.Material.value = _material

  ## Evaluated every frame.
  def evaluate(self):

    # trigger frame callback activity
    _server_view_node_name = "w" + str(self.VIEW.workspace_id) + "_dg" + str(self.VIEW.display_group_id) + "_u" + str(self.VIEW.user_id)

    if (len(self.entry_node.GroupNames.value) != 0 and \
       (_server_view_node_name) not in self.entry_node.GroupNames.value) or \
       self.mf_portal_modes.value[4] == "4-False":

      if self.frame_trigger.Active.value == True:
        self.frame_trigger.Active.value = False

        for _pipeline in self.pipelines:
          _pipeline.Enabled.value = False
        
        for _texture in self.textured_quads:
          _textured_quad.GroupNames.value.append("portal_invisible_group")

        for _border in self.border_geometries:
          _border.GroupNames.value.append("portal_invisible_group")
        
        for _back_geometry in self.back_geometries:
          _back_geometry.GroupNames.value.append("portal_invisible_group")
        
      return

    else:

      if self.frame_trigger.Active.value == False:
        self.frame_trigger.Active.value = True

        # fixes display of back geometry when jumping between navigations

        for _back_geometry in self.back_geometries:
          _back_geometry.GroupNames.value.remove("portal_invisible_group")
        
        for _border in self.border_geometries:
          _border.GroupNames.value.remove("portal_invisible_group")


  ## Evaluated every frame when active.
  def frame_callback(self):

    # update global clipping plane when negative parallax is false
    if self.mf_portal_modes.value[2] == "2-False":

      for _pipeline in self.pipelines:

        _index = self.pipelines.index(_pipeline)

        _portal_exit_mat = avango.gua.make_trans_mat(self.screen_nodes[_index].Transform.value.get_translate()) * \
                           self.exit_node.Transform.value * \
                           avango.gua.make_rot_mat(self.screen_nodes[_index].Transform.value.get_rotate())
        _vec = avango.gua.Vec3(0.0, 0.0, -1.0)
        _vec = avango.gua.make_rot_mat(_portal_exit_mat.get_rotate_scale_corrected()) * _vec
        _vec2 = _portal_exit_mat.get_translate()
        _vec2 = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(_portal_exit_mat.get_rotate_scale_corrected())) * _vec2
        _dist = _vec2.z
        
        _pipeline.GlobalClippingPlane.value = avango.gua.Vec4(_vec.x, _vec.y, _vec.z, _dist)


    # determine if outside of viewing range
    if self.head_node != None:

      for _pipeline in self.pipelines:

        _index = self.pipelines.index(_pipeline)

        _view_in_portal_space_mat = avango.gua.make_inverse_mat(self.entry_node.Transform.value * self.screen_nodes[_index].Transform.value) * self.head_node.WorldTransform.value
        _ref_vec = avango.gua.Vec3(0, 0, -1)
        _view_in_portal_space_vec = avango.gua.make_rot_mat(_view_in_portal_space_mat.get_rotate_scale_corrected()) * _ref_vec
        _view_in_portal_space_vec = avango.gua.Vec3(_view_in_portal_space_vec.x, _view_in_portal_space_vec.y, _view_in_portal_space_vec.z)
        _angle = math.acos(_ref_vec.dot(_view_in_portal_space_vec))

        # trigger on/off changes
        if _view_in_portal_space_mat.get_translate().z < 0 or abs(math.degrees(_angle)) > 100.0:

          if _pipeline.Enabled.value == True:
            _pipeline.Enabled.value = False
            
            self.textured_quads[_index].GroupNames.value.append("portal_invisible_group")
            self.back_geometries[_index].GroupNames.value.remove("portal_invisible_group")

        else:

          if _pipeline.Enabled.value == False:
            _pipeline.Enabled.value = True
            
            self.textured_quads[_index].GroupNames.value.remove("portal_invisible_group")
            self.border_geometries[_index].GroupNames.value.remove("portal_invisible_group")
            self.back_geometries[_index].GroupNames.value.append("portal_invisible_group")


  ## Called whenever sf_screen_width changes.
  @field_has_changed(sf_screen_width)
  def sf_screen_width_changed(self):
    self.update_size()

  ## Called whenever sf_screen_height changes.
  @field_has_changed(sf_screen_height)
  def sf_screen_height_changed(self):
    self.update_size()
