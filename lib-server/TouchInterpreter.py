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

        self.finger_geometries      = []
        self.hand_geometries        = []
        self.ray_geometries         = []

        self.hand_widgets           = {}

        self.always_evaluate(True)

    def my_constructor(self, graph):
        self.touch_device           = TouchDevice()
        
        self.scene_graph            = graph
        
        self.screen_transform_node  = avango.gua.nodes.TransformNode(Name = "screen_transform")
        self.screen_transform_node.Transform.connect_from(self.scene_graph["/net/w0_dg0_u0/screen_0"].Transform)
        self.scene_graph["/net"].Children.value.append(self.screen_transform_node)
        self.inv_screen_mat = avango.gua.make_inverse_mat(self.screen_transform_node.Transform.value)

        self.cut_sphere_node = avango.gua.nodes.TransformNode(Name = "cut_sphere")
        self.scene_graph["/net"].Children.value.append(self.cut_sphere_node)

        self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0)

        self.touch_device = TouchDevice()
        for hand in self.touch_device.hands.value:
            self.hand_widgets[hand.HandID.value] = None

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
        set_cut = True
        for handID in self.touch_device.active_hands:
            fingerPositions = []
            for touchPoint in self.touch_device.active_hands[handID]:
                unmappedPos = avango.gua.Vec3(touchPoint.PosX.value, touchPoint.PosY.value, 0)
                fingerPositions.append(self.mapInputPosition(unmappedPos))
            
            if self.hand_widgets[handID] != None and len(fingerPositions) > 0: #HandWidget exists and is updated
                inactiveWidgets.remove(handID)
                self.hand_widgets[handID].computeMatrices(fingerPositions)
            
            elif len(fingerPositions) > 0: # HandWidget does not exist and is created
                inactiveWidgets.remove(handID)
                fingerGeometries = []
                for i in range(0, 5):
                    fingerGeometries.append(self.finger_geometries[5*handID + i])
                self.hand_widgets[handID] = HandWidget()
                self.hand_widgets[handID].my_constructor(handID,
                                                        fingerPositions,
                                                        self.hand_geometries[handID],
                                                        self.ray_geometries[handID],
                                                        fingerGeometries,
                                                        self.inv_screen_mat)

            if set_cut and self.hand_widgets[handID] != None:
                handPos = self.hand_widgets[handID].hand_mat.get_translate()
                self.setCutSphereUniforms(self.hand_widgets[handID].hand_mat.get_translate(), 0.5*self.hand_widgets[handID].length_finger_span)
                set_cut = False

        if set_cut:
            self.setCutSphereUniforms(avango.gua.Vec3(0,0,0), 0.0)
            set_cut = False

        # remove inactive HandWidgets
        for handID in inactiveWidgets:
            if self.hand_widgets[handID] != None:
                self.hand_widgets[handID].kill()
                self.hand_widgets[handID] = None

    def mapInputPosition(self, POS):
        displaySize = avango.gua.Vec2(1.115,0.758)

        """ map points from interval [0, 1] to [-0.5, 0.5] """
        mappedPosX = POS[0] * 1 - 0.5
        mappedPosY = POS[1] * 1 - 0.5

        """ map point to display intervall ([-1/2*display-size] -> [+1/2*display-size]) """
        #mappedPos = avango.gua.Vec3(mappedPosX * displaySize.x, -1 * (mappedPosY * displaySize.y), 0.0)   
        mappedPos = avango.gua.Vec3(mappedPosX * displaySize.x, 0.0, mappedPosY * displaySize.y)   

        return mappedPos

    def setupTouchGeometries(self, FINGEROBJPATH, HANDOBJPATH, RAYOBJPATH):
        _loader = avango.gua.nodes.TriMeshLoader()

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

    def setCutSphereUniforms(self, SPHERECENTER, SPHERERADIUS):
        _mat = avango.gua.make_identity_mat()
        
        _mat.set_element(0, 0, SPHERECENTER.x)
        _mat.set_element(1, 0, SPHERECENTER.y)
        _mat.set_element(2, 0, SPHERECENTER.z)
        
        _mat.set_element(0, 1, SPHERERADIUS)
        
        self.cut_sphere_node.Transform.value = _mat


