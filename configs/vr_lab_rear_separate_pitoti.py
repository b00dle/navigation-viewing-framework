#!/usr/bin/python

## @file
# Contains workspace, display, navigation, display group and user configuration classes to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from DisplayGroup import *
from PhysicalDisplay import *
from VirtualDisplay import *
from Workspace import Workspace
from SteeringNavigation import SteeringNavigation
from StaticNavigation import StaticNavigation

## Create Workspaces first ##
vr_lab_rear = Workspace('VR-Lab-Rear', avango.gua.make_trans_mat(0.0, 0.043, 0.0))

video_visibility_table = {
                            "dlp_wall"  : {"table" : False, "portal" : False}
                          , "table" : {"dlp_wall" : True, "portal" : False}
                          , "portal" : {"dlp_wall" : True, "table" : False}
                         }

#vr_lab_rear.associate_video_3D("/opt/kinect-resources/kinect_surface_K_23_24_25.ks"
#                             , avango.gua.make_trans_mat(0.0, 0.043, 1.6)
#                             , video_visibility_table)

workspaces = [vr_lab_rear]

## Create Navigation instances ##
trace_visibility_list_dlp_wall_nav = {  "dlp_wall"  : False
                                      , "table" : True 
                                      , "portal" : False
                                     }

trace_visibility_list_table_nav = {  "dlp_wall"  : False
                                   , "table" : False 
                                   , "portal" : False
                                  }
                                  

spheron_navigation = SteeringNavigation()
spheron_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(388.50, 56.9, -53.6)
                                 , STARTING_SCALE = 1.0
                                 , INPUT_DEVICE_TYPE = 'NewSpheron'
                                 , INPUT_DEVICE_NAME = 'device-new-spheron'
                                 , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.75, 1.6)
                                 , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                 , INVERT = False
                                 , TRACE_VISIBILITY_LIST = trace_visibility_list_dlp_wall_nav
                                 , DEVICE_TRACKING_NAME = 'tracking-new-spheron'
                                 , REACTS_ON_PORTAL_TRANSIT = True)

spacemouse_navigation = SteeringNavigation()
spacemouse_navigation.my_constructor( STARTING_MATRIX = avango.gua.make_trans_mat(66.0, 37.0, -240.0)
                                    , STARTING_SCALE = 550.0
                                    , INPUT_DEVICE_TYPE = 'Spacemouse'
                                    , INPUT_DEVICE_NAME = 'device-spacemouse'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , GROUND_FOLLOWING_SETTINGS = [False, 0.75]
                                    , INVERT = True
                                    , TRACE_VISIBILITY_LIST = trace_visibility_list_table_nav
                                    , DEVICE_TRACKING_NAME = None
                                    , REACTS_ON_PORTAL_TRANSIT = False)


xbox_navigation = SteeringNavigation()
xbox_navigation.my_constructor(       STARTING_MATRIX = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
                                    , STARTING_SCALE = 1.0
                                    , INPUT_DEVICE_TYPE = 'XBoxController'
                                    , INPUT_DEVICE_NAME = 'device-xbox-1'
                                    , NO_TRACKING_MAT = avango.gua.make_trans_mat(0.0, 1.2, 0.6)
                                    , GROUND_FOLLOWING_SETTINGS = [True, 0.75]
                                    , INVERT = False
                                    , TRACE_VISIBILITY_LIST = trace_visibility_list_dlp_wall_nav
                                    , DEVICE_TRACKING_NAME = 'tracking-xbox-1'
                                    , IS_REQUESTABLE = True
                                    , REQUEST_BUTTON_NUM = 3
                                    , REACTS_ON_PORTAL_TRANSIT = True)


## Create Display instances. ##
large_powerwall = LargePowerwall()
touch_table_3D = TouchTable3D()

displays = [large_powerwall, touch_table_3D]

## Create display groups ##
vr_lab_rear.create_display_group( DISPLAY_LIST = [large_powerwall]
                                , NAVIGATION_LIST = [spheron_navigation, xbox_navigation]
                                , VISIBILITY_TAG = "dlp_wall"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0, 0, 1.6) )

vr_lab_rear.create_display_group( DISPLAY_LIST = [touch_table_3D]
                                , NAVIGATION_LIST = [spacemouse_navigation]
                                , VISIBILITY_TAG = "table"
                                , OFFSET_TO_WORKSPACE = avango.gua.make_trans_mat(0.6975, -0.96, 1.9825) * \
                                                        avango.gua.make_rot_mat(-90, 0, 1, 0) )


## Create users ##
avatar_visibility_table = {
                            "dlp_wall"  : {"table" : False, "portal" : False}
                          , "table" : {"dlp_wall" : True, "portal" : False}
                          , "portal" : {"dlp_wall" : True, "table" : False}
                          }

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-6'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-4'
                       , EYE_DISTANCE = 0.065)

vr_lab_rear.create_user( VIP = False
                       , AVATAR_VISIBILITY_TABLE = avatar_visibility_table
                       , HEADTRACKING_TARGET_NAME = 'tracking-dlp-glasses-3'
                       , EYE_DISTANCE = 0.065)

## Create tools ##

# visibility table
# format: A : { B : bool}
# interpretation: does display with tag A see representation of tool in displays with tag B?
tool_visibility_table = {
                          "dlp_wall"  : {"table" : False, "portal" : False}
                        , "table" : {"dlp_wall" : True, "portal" : False}  
                        , "portal" : {"dlp_wall" : True, "table" : False}
                       }

vr_lab_rear.create_ray_pointer( POINTER_TRACKING_STATION = 'tracking-dlp-pointer1' 
                              , POINTER_DEVICE_STATION = 'device-pointer1'
                              , VISIBILITY_TABLE = tool_visibility_table)

#vr_lab_rear.create_portal_cam(  CAMERA_TRACKING_STATION = 'tracking-portal-camera-32'
#                             ,  CAMERA_DEVICE_STATION = 'device-portal-camera-32'
#                             ,  VISIBILITY_TABLE = tool_visibility_table)

virtual_display_groups = []
