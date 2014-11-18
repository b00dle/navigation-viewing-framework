#!/bin/python

from SceneManager import SceneManager 
from Intersection import *
from TrackingReader import *
import Tools

import avango
import avango.gua
import avango.daemon
import avango.script
from avango.script import field_has_changed

import subprocess
import math
import avango.utils
import time

class MultiTouchDevice(avango.script.Script):
    """
    Base class for multi touch devices.

    rayOrientation: orientation matrix (start position + direction) of ray 
    fingerCenterPos: the center of finger position in interval from -display-size to +display-size
    """
    _rayOrientation = avango.gua.SFMatrix4()
    _fingerCenterPos = avango.gua.SFVec3()

    sf_key2 = avango.SFBool()
    sf_key3 = avango.SFBool()
    
    def __init__(self):
        self.super(MultiTouchDevice).__init__()
        self._sceneGraph = None
        self._display    = None
        self._worldMat   = avango.gua.make_identity_mat()
        self._transMat   = avango.gua.make_identity_mat()
        self._rotMat     = avango.gua.make_identity_mat()
        self._scaleMat   = avango.gua.make_identity_mat()
        
        """ Scene transform matrix """
        self._globalMatrix = avango.gua.make_identity_mat()

        """ last cursor position """
        self._lastPos = None

        """ params to evaluate object / navigation mode """
        self._sceneName = None
        self._objectName = None
        self._objectMode = False

        self._headPosition1 = avango.gua.Vec3(0,0,0)

        """ params to evaluate intersection """
        self._intersection = Intersection() # ray intersection for target identification
        self._intersectionFound = False
        self._intersectionPoint = avango.gua.Vec3(0,0,0)
        self._intersectionObject = None
        self._lastIntersectionCounter = 0

        """ ray representation"""
        self.ray_length = 10
        self.ray_thickness = 0.0075
        self.intersection_sphere_size = 0.025
        self.highlighted_object = None
        self.hierarchy_selection_level = -1

        self.always_evaluate(True)


    #def my_constructor(self, graph, display, NET_TRANS_NODE, SCENE_MANAGER, APPLICATION_MANAGER):
    def my_constructor(self, graph, display, NET_TRANS_NODE, APPLICATION_MANAGER):
        """
        Initialize multi-touch device.

        @param graph: the scene graph on which to operate
        @param display: the physical display
        """

        self._sceneGraph = graph
        self._display    = display

        """ original matrix of the scene """
        self._origMat    = graph.Root.value.Transform.value

        """  """
        self._applicationManager = APPLICATION_MANAGER

        self._intersection.my_constructor(self._sceneGraph, self._rayOrientation, self.ray_length, "") # parameters: SCENEGRAPH, SF_PICK_MATRIX, PICK_LENGTH, PICKMASK

        """ parent node of ray node """
        _parent_node = self._sceneGraph["/net/platform_0/scale"]
        
        """
        # init scenegraph node
        ## @var ray_transform
        # Transformation node of the pointer's ray.
        """
        self.ray_transform = avango.gua.nodes.TransformNode(Name = "ray_transform")
        _parent_node.Children.value.append(self.ray_transform)

        _loader = avango.gua.nodes.TriMeshLoader()
        
        """
        ## @var ray_geometry
        # Geometry node representing the ray graphically.
        """
        self.ray_geometry = _loader.create_geometry_from_file("ray_geometry", "data/objects/cylinder.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.ray_transform.Children.value.append(self.ray_geometry)
        self.ray_geometry.GroupNames.value = ["do_not_display_group"]

        self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0,0,0) * \
                                            avango.gua.make_rot_mat(0,0,0,0) * \
                                            avango.gua.make_scale_mat(0,0,0)
        
        """
        @var intersection_point_geometry
        Geometry node representing the intersection point of the ray with an object in the scene.
        """
        self.intersection_point_geometry = _loader.create_geometry_from_file("intersection_point_geometry", "data/objects/sphere.obj", "data/materials/White.gmd", avango.gua.LoaderFlags.DEFAULTS)
        _parent_node.Children.value.append(self.intersection_point_geometry)
        #NET_TRANS_NODE.Children.value.append(self.intersection_point_geometry)
        self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] # set geometry invisible

        self.ray_transform.Transform.connect_from(self._rayOrientation)

        """ representation of fingercenterpos """
        self.fingercenterpos_geometry = _loader.create_geometry_from_file("fingercenterpos", "data/objects/sphere.obj", "data/materials/Red.gmd", avango.gua.LoaderFlags.DEFAULTS)
        _parent_node.Children.value.append(self.fingercenterpos_geometry)
        #NET_TRANS_NODE.Children.value.append(self.fingercenterpos_geometry)
        self.fingercenterpos_geometry.GroupNames.value = ["do_not_display_group"]

        #######
        """ representation of touchpoints """
        self.touch1_geometry = _loader.create_geometry_from_file("touch1", "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.touch1_geometry.GroupNames.value = ["do_not_display_group"]
        _parent_node.Children.value.append(self.touch1_geometry)
        #NET_TRANS_NODE.Children.value.append(self.touch1_geometry)
        
        self.touch2_geometry = _loader.create_geometry_from_file("touch2", "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.touch2_geometry.GroupNames.value = ["do_not_display_group"]
        _parent_node.Children.value.append(self.touch2_geometry)
        #NET_TRANS_NODE.Children.value.append(self.touch2_geometry)
        
        self.touch3_geometry = _loader.create_geometry_from_file("touch3", "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.touch3_geometry.GroupNames.value = ["do_not_display_group"]
        _parent_node.Children.value.append(self.touch3_geometry)
        #NET_TRANS_NODE.Children.value.append(self.touch3_geometry)
        
        self.touch4_geometry = _loader.create_geometry_from_file("touch4", "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.touch4_geometry.GroupNames.value = ["do_not_display_group"]
        _parent_node.Children.value.append(self.touch4_geometry)
        #NET_TRANS_NODE.Children.value.append(self.touch4_geometry)
        
        self.touch5_geometry = _loader.create_geometry_from_file("touch5", "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
        self.touch5_geometry.GroupNames.value = ["do_not_display_group"]
        _parent_node.Children.value.append(self.touch5_geometry)
        #NET_TRANS_NODE.Children.value.append(self.touch5_geometry)
                

        # parameters for visualizeFingers function
        self.transNode = avango.gua.nodes.TransformNode(Name = "transNode")
        _parent_node.Children.value.append(self.transNode)
        #NET_TRANS_NODE.Children.value.append(self.transNode)
        self.fingerPos_geometries = []

        """ hand tracking """
        self.hand_tracking = TrackingTargetReader()
        self.hand_tracking.my_constructor("tracking-dlp-hand")
        self.hand_tracking.set_transmitter_offset(self._applicationManager.user_list[0].transmitter_offset)
        self.hand_tracking.set_receiver_offset(avango.gua.make_identity_mat())

        self.hand_tracking_trans = avango.gua.nodes.TransformNode(Name = "hand_tracking_node")
        self.hand_tracking_trans.Transform.connect_from(self.hand_tracking.sf_tracking_mat)
        self._applicationManager.navigation_list[0].platform.platform_scale_transform_node.Children.value.append(self.hand_tracking_trans)

        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.keyboard_sensor.Station.value = "device-keyboard0"
        
        self.sf_key2.connect_from(self.keyboard_sensor.Button11) # key 2
        self.sf_key3.connect_from(self.keyboard_sensor.Button12) # key 3
        #######

        """ hand representation """
        self.handPos_geometry = _loader.create_geometry_from_file("handpos", "data/objects/ring.obj", "data/materials/Red.gmd", avango.gua.LoaderFlags.DEFAULTS)
        _parent_node.Children.value.append(self.handPos_geometry)
        #NET_TRANS_NODE.Children.value.append(self.handPos_geometry)
        self.handPos_geometry.GroupNames.value = ["do_not_display_group"]


        """ define Input display size """
        #111,5cm x 75,8
        self._inputDisplaySize = avango.gua.Vec2(1.115,0.758)


    def getDisplay(self):
        return self._display
    

    def getSceneGraph(self):
        return self._sceneGraph


    def mapInputPosition(self, Pos):
        """
        Map input position to display size
        """

        point = Pos

        #TODO: correct finger center position
        """ map points from interval [0, 1] to [-0.5, 0.5] """
        mappedPosX = point[0] * 1 - 0.5
        mappedPosY = point[1] * 1 - 0.5

        """ map point to display intervall ([-1/2*display-size] -> [+1/2*display-size]) """
        mappedPos = avango.gua.Vec3(mappedPosX * self._inputDisplaySize.x, 0.0, mappedPosY * self._inputDisplaySize.y)   

        return mappedPos        

    def setFingerCenterPos(self, fingerPos):
        self._fingerCenterPos.value = fingerPos

        """ update fingercenterpos representation """
        self.fingercenterpos_geometry.GroupNames.value = []
        self.fingercenterpos_geometry.Transform.value = avango.gua.make_trans_mat(self._fingerCenterPos.value) * \
                                                        avango.gua.make_scale_mat( 0.025, 0.025 , 0.025 )

    def visualizeTouchPos(self, touchPos, index):
        #touchPos.x += 0.016
        #touchPos.z += 0.010
        """ update fingerpos representation """
        if index == 0:
            self.touch1_geometry.GroupNames.value = []
            self.touch1_geometry.Transform.value = avango.gua.make_trans_mat(touchPos) * \
                                                    avango.gua.make_scale_mat(0.025, 0.0025, 0.025)
        elif index == 1:
            self.touch2_geometry.GroupNames.value = []
            self.touch2_geometry.Transform.value = avango.gua.make_trans_mat(touchPos) * \
                                                    avango.gua.make_scale_mat(0.025, 0.0025, 0.025)
        elif index == 2:
            self.touch3_geometry.GroupNames.value = []
            self.touch3_geometry.Transform.value = avango.gua.make_trans_mat(touchPos) * \
                                                    avango.gua.make_scale_mat(0.025, 0.0025, 0.025)
        elif index == 3:
            self.touch4_geometry.GroupNames.value = []
            self.touch4_geometry.Transform.value = avango.gua.make_trans_mat(touchPos) * \
                                                    avango.gua.make_scale_mat(0.025, 0.0025, 0.025)
        elif index == 4: 
            self.touch5_geometry.GroupNames.value = []
            self.touch5_geometry.Transform.value = avango.gua.make_trans_mat(touchPos) * \
                                                    avango.gua.make_scale_mat(0.025, 0.0025, 0.025)

    def visualizePointingRay(self, touchPos):
        #touchPos.x += 0.016
        #touchPos.z += 0.010

        handPos = self.hand_tracking.sf_abs_vec.value
        
        handPos.z += 0.025

        directionVector = touchPos - handPos
            
        """ calculate rotation matrix """
        vec1 = avango.gua.Vec3(0.0,0.0,-1.0)
        directionVector.normalize()
        rotationMatrix = Tools.get_rotation_between_vectors( vec1, directionVector)
        
        """ start position and rotation matrix """
        self._rayOrientation.value = avango.gua.make_trans_mat(handPos) * rotationMatrix

        self.ray_geometry.GroupNames.value = []

        """update ray"""
        self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 20 * -0.5) * \
                                            avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                            avango.gua.make_scale_mat(self.ray_thickness, 20, self.ray_thickness)

    def visualizeFingers(self, fingerPositions):
        loader = avango.gua.nodes.TriMeshLoader()

        for i in range(0, len(self.fingerPos_geometries)):
            self.transNode.Children.value.remove(self.fingerPos_geometries[i])
        
        self.fingerPos_geometries = []

        i = 0
        for fingerPos in fingerPositions:
            finger_geo = loader.create_geometry_from_file("fingerpos_" + str(i), "data/objects/cube.obj", "data/materials/Blue.gmd", avango.gua.LoaderFlags.DEFAULTS)
            finger_geo.Transform.value = avango.gua.make_trans_mat(fingerPos)
            self.fingerPos_geometries.append(finger_geo)
            self.transNode.Children.value.append(self.fingerPos_geometries[i])
            i += 1

        print(len(self.transNode.Children.value))

    def visualisizeHandPosition(self, handPos):
        """ update hand representation """
        self.handPos_geometry.GroupNames.value = []
        self.handPos_geometry.Transform.value = avango.gua.make_trans_mat(handPos) * \
                                                avango.gua.make_scale_mat( 0.08, 0.08 , 0.08 )


    def setObjectMode(self, active):
        """
        Evaluate object mode.
        object mode activated only if an intersection was found

        @param active: toggle active state of object mode 
        """
        if active and self._intersectionFound:
            self._objectMode = True
            self._objectName = self._intersectionObject.Parent.value.Name.value
            return True
        else: 
            self._objectMode = False
            self._objectName = None
            return False


    def addLocalTranslation(self, transMat):
        """
        Add local translation.

        @param transMat: the (relative) translation matrix
        """
        self._transMat *= transMat


    def addLocalRotation(self, rotMat):
        """
        Add local rotation.

        @param rotMat: the (relative) rotation matrix
        """
        self._rotMat *= rotMat


    def addLocalScaling(self, scaleMat):
        """
        Add local scaling.

        @param scaleMat: the (relative) scaling matrix
        """
        self._scaleMat *= scaleMat

    def intersectSceneWithFingerPos(self):
        """
        Intersect Scene with ray from head to finger position. works only for first user.

        @param transMat: the (relative) translation matrix
        """

        #TODO: decide between displays with tracking and not
        #for no tracking use this: #self._rayOrientation.value = avango.gua.make_trans_mat(self._fingerCenterPos.value.x , 0.5 , self._fingerCenterPos.value.z) * avango.gua.make_rot_mat(-90,1,0,0)

        #do this only once per gesture
        if (1 < (self._frameCounter - self._lastIntersectionCounter)):
            """ head position of first user """
            self._headPosition1 = self._applicationManager.user_list[0].headtracking_reader.sf_abs_vec.value

            """ direction Vector between head and finger position """
            _directionVector = self._fingerCenterPos.value - self._headPosition1
            
            """ ray shouldn't start in the head of the user (for the representation) """  
            _startPosition = self._headPosition1 + _directionVector * 0.8
            
            """ calculate rotation matrix """
            _vec1 = avango.gua.Vec3(0.0,0.0,-1.0)
            _directionVector.normalize()
            _rotationMatrix = Tools.get_rotation_between_vectors( _vec1, _directionVector)
            
            """ start position and rotation matrix """
            self._rayOrientation.value = avango.gua.make_trans_mat(_startPosition) * _rotationMatrix
                    
            """intersection found"""
            if len(self._intersection.mf_pick_result.value) > 0:
                self._intersectionFound = True

                """first intersected object"""
                _pick_result = self._intersection.mf_pick_result.value[0]

                self._intersectionPoint = _pick_result.Position.value 
                self._intersectionObject = _pick_result.Object.value
                
                """update intersectionObject until you insert object Mode"""
                if not self._objectMode:
                    self._lastIntersectionObject = self._intersectionObject
                
                """ transform point into world coordinates """
                self._intersectionPoint = self._intersectionObject.WorldTransform.value * self._intersectionPoint 
                
                """make Vec3 from Vec4"""
                self._intersectionPoint = avango.gua.Vec3(self._intersectionPoint.x,self._intersectionPoint.y,self._intersectionPoint.z) 
                
                if (self._objectMode and not self._objectName == self._intersectionObject.Parent.value.Name.value):
                    #print "same object"
                    self._intersectionPoint = avango.gua.Vec3(0,0,0)

                """ VISUALISATION """
                """update intersection sphere"""
                self.intersection_point_geometry.Transform.value = avango.gua.make_trans_mat(self._intersectionPoint) * \
                                                                   avango.gua.make_scale_mat(self.intersection_sphere_size, self.intersection_sphere_size, self.intersection_sphere_size)
                """set sphere and ray visible"""                                           
                #self.intersection_point_geometry.GroupNames.value = [] 
                self.ray_geometry.GroupNames.value = []

                """update ray"""
                _distance = (self._intersectionPoint - self.ray_transform.WorldTransform.value.get_translate()).length()

                self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, _distance * -0.5) * \
                                                    avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                                    avango.gua.make_scale_mat(self.ray_thickness, _distance, self.ray_thickness)

            else:
                """set geometry invisible"""
                self.intersection_point_geometry.GroupNames.value = ["do_not_display_group"] 
                self.ray_geometry.GroupNames.value = ["do_not_display_group"]

                """set to default ray length"""
                self.ray_geometry.Transform.value = avango.gua.make_trans_mat(0.0,0.0,self.ray_length * -0.5) * \
                                                    avango.gua.make_rot_mat(-90.0,1,0,0) * \
                                                    avango.gua.make_scale_mat(self.ray_thickness, self.ray_length, self.ray_thickness)
                self._intersectionFound = False
                self._intersectionPoint = avango.gua.Vec3(0,0,0)
        
        self._lastIntersectionCounter = self._frameCounter




    def update_object_highlight(self):
        """highlight active object:"""
        if self._objectMode:
            _node = self._lastIntersectionObject

            if _node.has_field("InteractiveObject") == True:
                _object = _node.InteractiveObject.value
              
                if self.hierarchy_selection_level >= 0:          
                    _object = _object.get_higher_hierarchical_object(self.hierarchy_selection_level)
              
                if _object == None:
                    """ evtl. disable highlight of prior object"""
                    if self.highlighted_object != None:
                        self.highlighted_object.enable_highlight(False)

                else:
                    if _object != self.highlighted_object: # new object hit
                    
                        """evtl. disable highlight of prior object"""
                        if self.highlighted_object != None:
                            self.highlighted_object.enable_highlight(False)

                        self.highlighted_object = _object
                        
                        """enable highlight of new object"""
                        self.highlighted_object.enable_highlight(True)

        else:
            """evtl. disable highlight of prior object"""
            if self.highlighted_object != None:
                self.highlighted_object.enable_highlight(False)
                self.highlighted_object = None


    def applyTransformations(self):
        """
        Apply calculated world matrix to scene graph.
        Requires the scene graph to have a transform node as root node.
        """

        """ Reguires the scnene Name of actually scene to change dynamically """
        self._sceneName = SceneManager.active_scene_name

        """ to avoid errors until the scenen Name is set """
        if (None != self._sceneName):
            sceneNode = "/net/" + self._sceneName
            self._globalMatrix = self._sceneGraph[sceneNode].Transform.value
            
            """ object Mode """
            if self._objectMode:
                objectNode = "/net/" + self._sceneName + "/" + self._objectName
                scenePos = self._sceneGraph[objectNode].Transform.value.get_translate()
                TransformMatrix = self._sceneGraph[objectNode].Transform.value
            
            else: 
                scenePos = self._sceneGraph[sceneNode].Transform.value.get_translate()
                TransformMatrix = self._sceneGraph[sceneNode].Transform.value
            
            """ distance between finger position and scene position (object position) """
            translateDistance = self._fingerCenterPos.value - scenePos

            """transform world-space to object-space"""
            translateDistance = avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * translateDistance
            translateDistance = avango.gua.Vec3(translateDistance.x, translateDistance.y, translateDistance.z)

            #todo: 
            #   warum verschiebt sich manchmal das scenen koordinatensystem?
            #   alles in einer transformmatrix berechnung 

            """ TransfotmMatrix: first translate and rotate to origin, second calculate new position, third translate and rotate back """

            """ object mode """
            if self._objectMode:
                TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(self._globalMatrix.get_rotate_scale_corrected())) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * \
                                  self._rotMat * \
                                  self._scaleMat * \
                                  self._transMat * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_rot_mat(self._globalMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_scale_mat(TransformMatrix.get_scale())

            else:
                TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) *\
                                  avango.gua.make_trans_mat(translateDistance * 1.0) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * -1.0 , 0)) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * \
                                  self._rotMat * \
                                  self._scaleMat * \
                                  self._transMat * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * 1.0 , 0)) * \
                                  avango.gua.make_trans_mat(translateDistance * -1.0) * \
                                  avango.gua.make_scale_mat(TransformMatrix.get_scale())
            """
            TransformMatrix = avango.gua.make_trans_mat(TransformMatrix.get_translate()) * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) *\
                                  avango.gua.make_trans_mat(translateDistance * 1.0) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * -1.0 , 0)) * \
                                  avango.gua.make_inverse_mat(avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected())) * \
                                  self._rotMat * \
                                  self._scaleMat * \
                                  self._transMat * \
                                  avango.gua.make_rot_mat(TransformMatrix.get_rotate_scale_corrected()) * \
                                  avango.gua.make_trans_mat(avango.gua.Vec3(0, self._intersectionPoint.y * 1.0 , 0)) * \
                                  avango.gua.make_trans_mat(translateDistance * -1.0) * \
                                  avango.gua.make_scale_mat(TransformMatrix.get_scale())
            """

            """ object mode """
            if self._objectMode:
                self._sceneGraph[objectNode].Transform.value = TransformMatrix
            
            else:
                self._sceneGraph[sceneNode].Transform.value = TransformMatrix


        """ reset all data """ 
        self._transMat   = avango.gua.make_identity_mat()
        self._rotMat     = avango.gua.make_identity_mat()
        self._scaleMat   = avango.gua.make_identity_mat()
        self._globalMatrix = avango.gua.make_identity_mat()

    ## Called whenever sf_key2 changes.
    @field_has_changed(sf_key2)
    def sf_key2_changed(self):

        if self.sf_key2.value == True: # key pressed
            _parent_node = self._sceneGraph["/net/platform_0/scale"]
            _parent_node.Transform.value = avango.gua.make_trans_mat(0.0,0.1,0.0) * _parent_node.Transform.value
  
    ##Called whenever sf_key3 changes.
    @field_has_changed(sf_key3)
    def sf_key3_changed(self):

        if self.sf_key3.value == True: # key pressed
            _parent_node = self._sceneGraph["/net/platform_0/scale"]
            _parent_node.Transform.value = avango.gua.make_trans_mat(0.0,-0.1,0.0) * _parent_node.Transform.value
