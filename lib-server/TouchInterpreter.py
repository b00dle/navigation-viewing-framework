#!/bin/python

from SceneManager import SceneManager
from TouchDevice import *
from HandWidget import *
import Utilities

import avango
import avango.gua
import avango.daemon
import avango.script
from avango.script import field_has_changed
import subprocess

class TouchInterpreter(avango.script.Script):

    def __init__(self):
        self.super(TouchInterpreter).__init__()

        self.scene_graph            = None
        self.screen_transform_node  = None
        self.net_transform_node     = None
        self.touch_device           = None

        self.nav_proxy_plane        = None
        self.finger_geometries      = []
        self.hand_geometries        = []
        self.ray_geometries         = []

        self.hand_widgets           = {}

        self.id_iterator            = 0

        self.always_evaluate(True)

    def my_constructor(self, graph):
        self.scene_graph            = graph

        # setup screen transform node to append touch geometry        
        self.screen_transform_node  = avango.gua.nodes.TransformNode(Name = "screen_transform")
        self.screen_transform_node.Transform.connect_from(self.scene_graph["/net/w0_dg0_u0/screen_0"].WorldTransform)
        self.scene_graph["/net"].Children.value.append(self.screen_transform_node)
        
        # get inverse screen mat for HandWidget geometry positioning
        self.inv_screen_mat = avango.gua.make_inverse_mat(self.screen_transform_node.Transform.value)
        
        # get screen totation matrix for HandWidget pick ray orientation
        self.screen_rot_mat = avango.gua.make_rot_mat(self.screen_transform_node.Transform.value.get_rotate())

        # setup cut sphere uniform carriers for clientside material update
        self.cut_sphere_node1 = avango.gua.nodes.TransformNode(Name = "cut_sphere1")
        self.cut_sphere_node2 = avango.gua.nodes.TransformNode(Name = "cut_sphere2")
        self.cut_sphere_node3 = avango.gua.nodes.TransformNode(Name = "cut_sphere3")
        self.cut_sphere_node4 = avango.gua.nodes.TransformNode(Name = "cut_sphere4")
        self.cut_sphere_node5 = avango.gua.nodes.TransformNode(Name = "cut_sphere5")

        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node1)
        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node2)
        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node3)
        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node4)
        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node5)

        # fill cut sphere nodes with default values
        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0, 1)
        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0, 2)
        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0, 3)
        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0, 4)
        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0, 5)

        # get TouchDevice instance for reading input data
        self.touch_device = TouchDevice()

        # reserve space for the maximum count of HandWidgets
        for hand in self.touch_device.hands.value:
            self.hand_widgets[hand.HandID.value] = None

        # create touch geometries to be handed to HandWidgets upon creation
        self.setupTouchGeometries("data/objects/cube.obj","data/objects/ring.obj","data/objects/cylinder.obj")

    def evaluate(self):
        if self.touch_device != None:
            if self.touch_device.input_changed:
                self.touch_device.input_changed = False
                self.processChange()

    def processChange(self):
        inactiveWidgets = [] 
        for handID in self.hand_widgets:
            inactiveWidgets.append(handID)

        # create/update active HandWidgets
        for handID in self.touch_device.active_hands:
            
            # get world space mapped finger positions from input
            fingerPositions = []
            for touchPoint in self.touch_device.active_hands[handID]:
                unmappedPos = avango.gua.Vec3(touchPoint.PosX.value, touchPoint.PosY.value, 0)
                fingerPositions.append(self.mapToScreen(unmappedPos))
            
            # HandWidget exists and is updated
            if len(fingerPositions) > 0 and self.hand_widgets[handID] != None:
                inactiveWidgets.remove(handID)
                self.hand_widgets[handID].computeMatrices(fingerPositions)
            
            # HandWidget does not exist and is created
            elif len(fingerPositions) > 0:
                inactiveWidgets.remove(handID)
                fingerGeometries = []
                for i in range(0, 5):
                    fingerGeometries.append(self.finger_geometries[5*handID + i])
                self.hand_widgets[handID] = HandWidget()
                self.hand_widgets[handID].my_constructor(self.id_iterator,
                                                        fingerPositions,
                                                        self.scene_graph,
                                                        self.hand_geometries[handID],
                                                        self.ray_geometries[handID],
                                                        fingerGeometries,
                                                        self.inv_screen_mat,
                                                        self.screen_rot_mat)
                self.hand_widgets[handID].sf_world_mat.connect_from(self.screen_transform_node.Transform)
                self.id_iterator += 1

            # set cut sphere uniforms only for first widget (only one cut supported) 
            if self.hand_widgets[handID] != None:
                handPos = (self.inv_screen_mat * self.hand_widgets[handID].hand_mat).get_translate()
                worldFingerSpan = 0.5*self.hand_widgets[handID].length_finger_span
                worldFingerSpan = worldFingerSpan * self.screen_transform_node.Transform.value.get_scale().x 
                self.setCutSphereUniforms(self.mapToWorld(handPos), worldFingerSpan, handID+1)

        # remove inactive HandWidgets
        for handID in inactiveWidgets:
            if self.hand_widgets[handID] != None:
                self.hand_widgets[handID].sf_world_mat.disconnect_from(self.screen_transform_node.Transform)
                self.hand_widgets[handID].kill()
                del(self.hand_widgets[handID])
                self.hand_widgets[handID] = None
                self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0, handID+1)

        i = 0
        for handID in self.hand_widgets:
            if self.hand_widgets[handID] != None:
                i += 1

    def mapToScreen(self, POS):
        displaySize = avango.gua.Vec2(1.115,0.758)

        """ map points from interval [0, 1] to [-0.5, 0.5] """
        mappedPosX = POS[0] * 1 - 0.5
        mappedPosY = POS[1] * 1 - 0.5

        """ map point to display intervall ([-1/2*display-size] -> [+1/2*display-size]) """
        #mappedPos = avango.gua.Vec3(mappedPosX * displaySize.x, -1 * (mappedPosY * displaySize.y), 0.0)   
        mappedPos = avango.gua.Vec3(mappedPosX * displaySize.x, 0.0, mappedPosY * displaySize.y)   

        return mappedPos

    def mapToWorld(self, POS):
        return self.transform_vector_with_matrix(POS, self.screen_transform_node.Transform.value)

    def transform_vector_with_matrix(self, VECTOR, MATRIX):
        _vec = MATRIX * VECTOR
        return avango.gua.Vec3(_vec.x, _vec.y, _vec.z)

    def setupTouchGeometries(self, FINGEROBJPATH, HANDOBJPATH, RAYOBJPATH):
        _loader = avango.gua.nodes.TriMeshLoader()

        # touch navigation proxy plane
        '''
        self.nav_proxy_plane = _loader.create_geometry_from_file("touch_proxy_plane",
                                                                "data/objects/cube.obj",
                                                                "data/materials/White.gmd",
                                                                avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.nav_proxy_plane.Transform.value = self.inv_screen_mat *\
                                                avango.gua.make_trans_mat(0, -0.0030, 0) *\
                                                avango.gua.make_scale_mat(1.115, 0.0025, 0.758)
        self.screen_transform_node.Children.value.append(self.nav_proxy_plane)
        '''

        for i in range(0, len(self.touch_device.cursors.value)):
            self.finger_geometries.append(_loader.create_geometry_from_file("touch_finger_" + str(i),
                                                                            FINGEROBJPATH,
                                                                            "data/materials/Blue.gmd",
                                                                            avango.gua.LoaderFlags.DEFAULTS))
            self.finger_geometries[i].GroupNames.value = ["do_not_display_group"]
            self.screen_transform_node.Children.value.append(self.finger_geometries[i])

        for i in range(0, len(self.touch_device.hands.value)):
            # setup hand geometry
            self.hand_geometries.append(_loader.create_geometry_from_file("touch_hand_" + str(i),
                                                                            HANDOBJPATH,
                                                                            "data/materials/Red.gmd",
                                                                            avango.gua.LoaderFlags.DEFAULTS))
            self.hand_geometries[i].GroupNames.value = ["do_not_display_group"]
            self.screen_transform_node.Children.value.append(self.hand_geometries[i])

            #setup ray geometry
            self.ray_geometries.append(_loader.create_geometry_from_file("touch_ray_" + str(i),
                                                                            RAYOBJPATH,
                                                                            "data/materials/White.gmd",
                                                                            avango.gua.LoaderFlags.DEFAULTS))
            self.ray_geometries[i].GroupNames.value = ["do_not_display_group"]
            self.screen_transform_node.Children.value.append(self.ray_geometries[i])

    def setCutSphereUniforms(self, SPHERECENTER, SPHERERADIUS, SPHEREINDEX):
        _mat = avango.gua.make_identity_mat()
        
        _mat.set_element(0, 0, SPHERECENTER.x)
        _mat.set_element(1, 0, SPHERECENTER.y)
        _mat.set_element(2, 0, SPHERECENTER.z)
        
        _mat.set_element(0, 1, SPHERERADIUS)
        _mat.set_element(0, 2, SPHEREINDEX)
        
        if SPHEREINDEX == 1:
            self.cut_sphere_node1.Transform.value = _mat
        elif SPHEREINDEX == 2:
            self.cut_sphere_node2.Transform.value = _mat
        elif SPHEREINDEX == 3:
            self.cut_sphere_node3.Transform.value = _mat
        elif SPHEREINDEX == 4:
            self.cut_sphere_node4.Transform.value = _mat
        elif SPHEREINDEX == 5:
            self.cut_sphere_node5.Transform.value = _mat


