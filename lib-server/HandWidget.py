#!/bin/python

import avango
import avango.gua
import avango.daemon
import avango.script

from Intersection import *

import math

class HandWidget(avango.script.Script):

    sf_pick_mat = avango.gua.SFMatrix4()

    def __init__(self):
        self.super(HandWidget).__init__()

        self.hand_id                = 0

        self.hand_mat               = avango.gua.make_identity_mat()
        self.last_hand_mat          = avango.gua.make_identity_mat()
        self.finger_mat_list        = []
        self.length_finger_span     = 0.0

        self.scene_graph             = None
        self.hand_geometry          = None
        self.ray_geometry           = None
        self.finger_geometries      = []

        self.intersection           = None

        self.is_hidden              = False

        self.geometry_offset_mat    = avango.gua.make_identity_mat()
        self.rot_mat                = avango.gua.make_identity_mat()

        self.always_evaluate(True)

    def my_constructor(self, HANDID, FINGERPOSITIONS, GRAPH, HANDGEOMETRY, RAYGEOMETRY, FINGERGEOMETRIES, GEOMETRYOFFSETMAT, ROTATIONMAT):
        self.hand_id                = HANDID
        
        # compute hand and finger matrices
        self.computeMatrices(FINGERPOSITIONS)

        # ensure that hand mat and last hand mat are equal upon construction to avoid unwanted interaction
        self.last_hand_mat          = self.hand_mat

        self.scene_graph            = GRAPH
        self.hand_geometry          = HANDGEOMETRY
        self.ray_geometry           = RAYGEOMETRY
        self.finger_geometries      = FINGERGEOMETRIES

        self.geometry_offset_mat    = GEOMETRYOFFSETMAT
        self.rot_mat                = ROTATIONMAT

    def evaluate(self):
        if len(self.finger_mat_list) == 5:
            if self.intersection == None:
                self.sf_pick_mat.value = avango.gua.make_trans_mat(0,0.05,0) * self.hand_mat * self.rot_mat
                self.intersection = Intersection()
                self.intersection.my_constructor(self.scene_graph, self.sf_pick_mat, 10.0)
                self.intersection.picking_options = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                                               | avango.gua.PickingOptions.PICK_ONLY_FIRST_FACE \
                                               | avango.gua.PickingOptions.GET_POSITIONS \
                                               | avango.gua.PickingOptions.GET_WORLD_POSITIONS \
                                               | avango.gua.PickingOptions.GET_WORLD_NORMALS
            else:
                print("pick results of touch_widget_", self.hand_id, ":")
                for result in self.intersection.mf_pick_result.value:
                    print(result.Object.value.Name.value)
        else:
            if self.intersection != None:
                del(self.intersection)
                self.intersection = None

        self.visualize()

    def kill(self):
        self.hide()
        if self.intersection != None:
            del(self.intersection)
            self.intersection = None
        for i in range(0, len(self.finger_mat_list)):
            del(self.finger_mat_list[len(self.finger_mat_list)-1])

    def computeMatrices(self, FINGERPOSITIONS):
        for i in range(0, len(self.finger_mat_list)):
            del(self.finger_mat_list[len(self.finger_mat_list)-1])

        self.finger_mat_list = []
        for fingerPos in FINGERPOSITIONS:
            self.finger_mat_list.append(avango.gua.make_trans_mat(fingerPos))

        self.computeHandCenter()

    def visualize(self):
        if not self.is_hidden:
            i = 0
            for geometry in self.finger_geometries:
                if i < len(self.finger_mat_list):
                    geometry.GroupNames.value = []
                    geometry.Transform.value = self.geometry_offset_mat *\
                                                self.finger_mat_list[i] *\
                                                avango.gua.make_scale_mat(0.025, 0.0025, 0.025)
                else:
                    geometry.GroupNames.value = ["do_not_display_group"]
                i += 1

            if len(self.finger_mat_list) == 5:
                pos = self.hand_mat.get_translate()
                self.hand_geometry.Transform.value = self.geometry_offset_mat *\
                                                    self.hand_mat *\
                                                    avango.gua.make_scale_mat(0.5*self.length_finger_span, 0.5*self.length_finger_span, 0.5*self.length_finger_span)
                self.hand_geometry.GroupNames.value = []

                rayLength = 1
                rayTranslate = self.hand_mat.get_translate()
                rayTranslate.y = -0.5 * rayLength
                self.ray_geometry.Transform.value = self.geometry_offset_mat *\
                                                    avango.gua.make_trans_mat(rayTranslate) *\
                                                    avango.gua.make_scale_mat(0.01, rayLength, 0.01)
                self.ray_geometry.GroupNames.value = []
                
            else:
                self.hand_geometry.GroupNames.value = ["do_not_display_group"]
                self.ray_geometry.GroupNames.value = ["do_not_display_group"]

    def hide(self):
        self.is_hidden = True

        for geometry in self.finger_geometries:
            geometry.GroupNames.value = ["do_not_display_group"]

        self.hand_geometry.GroupNames.value = ["do_not_display_group"]
        self.ray_geometry.GroupNames.value = ["do_not_display_group"]

    def show(self):
        self.is_hidden = False
        #self.visualize()

    def computeHandCenter(self):
        if len(self.finger_mat_list) == 1:
            self.hand_mat = self.finger_mat_list[0]
            self.length_finger_span = 0.07
        
        else:
            xMin = 100000.0
            yMin = 100000.0
            zMin = 100000.0
            xMax = -100000.0
            yMax = -100000.0
            zMax = -100000.0

            for fingerMat in self.finger_mat_list:
                fingerPos = fingerMat.get_translate()
                xMin = min(xMin, fingerPos.x)
                xMax = max(xMax, fingerPos.x)
                yMin = min(yMin, fingerPos.y)
                yMax = max(yMax, fingerPos.y)
                zMin = min(zMin, fingerPos.z)
                zMax = max(zMax, fingerPos.z)

            vecMinMax = avango.gua.Vec3((xMax-xMin), (yMax-yMin), (zMax-zMin))
            centerPos = avango.gua.Vec3(xMin, yMin, zMin) + avango.gua.Vec3(0.5*vecMinMax.x, 0.5*vecMinMax.y, 0.5*vecMinMax.z)
            self.last_hand_mat = self.hand_mat
            self.hand_mat = avango.gua.make_trans_mat(centerPos)
            self.length_finger_span = math.sqrt(math.pow(vecMinMax.x,2) + math.pow(vecMinMax.y,2) + math.pow(vecMinMax.z,2))

