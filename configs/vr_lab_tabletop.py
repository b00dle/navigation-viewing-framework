#!/usr/bin/python

## @file
# Contains workspace, display, navigation, display group and user configuration classes to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from DisplayGroup import *
from PhysicalDisplay import *
from Portal import *
from Workspace import Workspace
from SteeringNavigation import SteeringNavigation
from StaticNavigation import StaticNavigation

## Create Workspaces first ##
vr_lab_tabletop = Workspace('VR-Lab-Tabletop', avango.gua.make_trans_mat(0.0, 0.043, 0.0))

video_visibility_table = {
                            "table" : {"portal" : False}
                          , "portal" : {"table" : False}
                         }

#vr_lab_rear.associate_video_3D("/opt/kinect-resources/kinect_surface_K_23_24_25.ks"
#                             , avango.gua.make_trans_mat(0.0, 0.043, 1.6)
#                             , video_visibility_table)

workspaces = [vr_lab_tabletop]

## Create Navigation instances ##
trace_visibility_list_table_nav = { 
                                     "table" : False 
                                   , "portal" : False
                                  }

spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , STARTING_SCALE = 100.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , GROUND_FOLLOWING_SETTINGS = [False, 0.75]
                                    , INVERT = True
                                    , TRACE_VISIBILITY_LIST = trace_visibility_list_table_nav
                                    , DEVICE_TRACKING_NAME = None
                                    , REACTS_ON_PORTAL_TRANSIT = False)


## Create Display instances. ##
touch_table_3D = TouchTable3D()

displays = [touch_table_3D]

## Create display groups ##
vr_lab_tabletop.create_display_group( DISPLAY_LIST = [touch_table_3D]
                                , NAVIGATION_LIST = [spacemouse_navigation]
                                , VISIBILITY_TAG = "table"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0.6975, -0.96, 1.9825) * \
                                                        avango.gua.make_rot_mat(-90, 0, 1, 0) )


## Create users ##
avatar_visibility_table = {
                            "table" : {"portal" : False}
                          , "portal" : {"table" : False}
                          }

vr_lab_tabletop.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-6'
                       , EYE_DISTANCE = 0.065)

vr_lab_tabletop.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-4'
                       , EYE_DISTANCE = 0.065)

vr_lab_tabletop.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-3'
                       , EYE_DISTANCE = 0.065)

## Create tools ##

# visibility table
# format: A : { B : bool}
# interpretation: does display with tag A see representation of tool in displays with tag B?
tool_visibility_table = {
                          "table" : {"portal" : False}  
                        , "portal" : {"table" : False}
                       }

vr_lab_tabletop.create_ray_pointer( POINTER_TRACKING_STATION = 'tracking-dlp-pointer1' 
                              , POINTER_DEVICE_STATION = 'device-pointer1'
                              , VISIBILITY_TABLE = tool_visibility_table)

#vr_lab_tabletop.create_portal_cam(  CAMERA_TRACKING_STATION = 'tracking-portal-camera-32'
#                             ,  CAMERA_DEVICE_STATION = 'device-portal-camera-32'
#                             ,  VISIBILITY_TABLE = tool_visibility_table)

portal_display_groups = []
