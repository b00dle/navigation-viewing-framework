#!/usr/bin/python

## @file
# Contains display configuration classes and a list of Display instances to be used by the framework.

# import guacamole libraries
import avango
import avango.gua

# import framework libraries
from Display import Display

## Display configuration for the large powerwall in the VR lab.
class LargePowerwall(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "kerberos"
                    , name = "large_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0", ":0.1", ":0.2", ":0.3"]
                    , size = (4.16, 2.6)
                    , transformation = avango.gua.make_trans_mat(0, 1.57, 0)
                    #, shutter_timings = [ [(0,2400), (100,2500)],
                    #                      [(3000,4600),(3100,4700)],
                    #                      [(5700,8175), (5800,8275)],
                    #                      [(8200,10700), (8300,10800)],
                    #                      [(11400,12900), (11500,13000)],
                    #                      [(14000,15800), (14100,15900)]
                    #                    ]
                    , shutter_timings = [ [(0,8175), (100,8275)],
                                          [(8200,10700), (8300,10800)],
                                          [(11400,12900), (11500,13000)],
                                          [(14000,15800), (14100,15900)]
                                        ]
                    #, shutter_values = [  [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)]
                    #                   ]
                    , shutter_values = [  [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)]
                                       ]
                    , max_viewing_distance = 5.0
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 4:
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


class LargePowerwall2(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "kerberos"
                    , name = "large_powerwall2"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.0"]
                    , size = (4.16, 2.6)
                    , transformation = avango.gua.make_trans_mat(0, 1.57, 0)
                    #, shutter_timings = [ [(0,2400), (100,2500)], 
                    #                      [(3000,4600),(3100,4700)],
                    #                      [(5700,8175), (5800,8275)],
                    #                      [(8200,10700), (8300,10800)],
                    #                      [(11400,12900), (11500,13000)],
                    #                      [(14000,15800), (14100,15900)]
                    #                    ]
                    , shutter_timings = [ [(0,8175), (100,8275)],
                                          [(8200,10700), (8300,10800)],
                                          [(11400,12900), (11500,13000)],
                                          [(14000,15800), (14100,15900)]
                                        ]
                    #, shutter_values = [  [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)],
                    #                      [(22,44), (88,11)]
                    #                   ]
                    , shutter_values = [  [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)],
                                          [(22,44), (88,11)]
                                       ]
                    , max_viewing_distance = 5.0
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 4:
      warpmatrices = [
          "/opt/dlp-warpmatrices/dlp_6_warp_P4.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P5.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P6.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P1.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P2.warp"
        , "/opt/dlp-warpmatrices/dlp_6_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


## Display configuration for the small powerwall in the VR lab.
class SmallPowerwall(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "pandora"
                    , name = "small_powerwall"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.1", ":0.0"]
                    , size = (3.0, 1.98)
                    , transformation = avango.gua.make_trans_mat(0, 1.42, 0)
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]
                                        ]
                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]                    

                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 2:
      warpmatrices = [
          "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)

        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


class SmallPowerwall2(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "pandora"
                    , name = "small_powerwall2"
                    , resolution = (1920, 1200)
                    , displaystrings = [":0.1"]
                    , size = (3.0, 1.98)
                    , transformation = avango.gua.make_trans_mat(0, 1.42, 0)
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]                                          
                                        ]
                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]                    
                    )

  ## Registers a new view at this display and returns the display string
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 2:
      warpmatrices = [
          "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 2)

        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
        , "/opt/lcd-warpmatrices/lcd_4_warp_P{0}.warp".format(2 * view_num + 1)
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


## Display configuration for the 3D multiuser touch table in the VR lab.
class TouchTable3D(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "medusa.medien.uni-weimar.de"
                    , name = "touch_table_3D"
                    , resolution = (1400, 1050)
                    , displaystrings = [":0.0", ":0.1", ":0.2"] 
                    , shutter_timings = [  [(100, 200, 2900, 3000), (8400, 8500, 11400, 11500)],
                                           [(2600, 2700, 5700, 5800), (11000, 11100, 14600, 14700)],
                                           [(6000, 6100, 8200, 8300), (14300, 14400, 15900, 16000)]                                          
                                        ]

                    , shutter_values =  [  [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)],
                                           [(20, 80, 40, 10), (2, 8, 4, 1)]
                                        ]
                    , size = (1.27, 0.93)
                    , transformation = #avango.gua.make_trans_mat(-1.56, 0.953, 2.28) * \
                                       #avango.gua.make_rot_mat(90, 0, 1, 0) * \
                                       avango.gua.make_rot_mat(90.0, -1,0, 0)
                    , max_viewing_distance = 1.0
                    , stereo = True
                    , stereomode = "SIDE_BY_SIDE"                    
                    )

  def get_touch_protocols(self):
    return [ "TUIO" ]


  ## Registers a new view at this display and returns the display string 
  # and the warp matrices assigned to the new view.
  def register_view(self):
    view_num = self.num_views
    if view_num < 3:
      warpmatrices = [
          "/opt/3D43-warpmatrices/3D43_warp_P4.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P5.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P6.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P1.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P2.warp"
        , "/opt/3D43-warpmatrices/3D43_warp_P3.warp"
      ]
      self.num_views += 1
      return (self.displaystrings[view_num], warpmatrices)
    else:
      return None


class SamsungStereoTV(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "apollo"
                    , name = "samsung_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.235, 0.695)
                    , transformation = avango.gua.make_trans_mat(0.0,1.6,0.0) * avango.gua.make_rot_mat(-40.0,1,0,0)
                    , stereo = True
                    , stereomode = "CHECKERBOARD"
                    )


class MitsubishiStereoTV(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__(self):
    Display.__init__( self
                    , hostname = "demeter"
                    , name = "mitsubishi_tv"
                    , resolution = (1920, 1080)
                    , displaystrings = [":0.0"]
                    , size = (1.44, 0.81)
                    , transformation = avango.gua.make_trans_mat(0.0,1.3,0.0)
                    , stereo = True
                    , stereomode = "CHECKERBOARD"
                    )

class OculusRift(Display):

  ## Custom constructor.
  # @param hostname The hostname to which this display is connected to.
  # @param name A name to be associated to that display. Will be used in XML configuration file.
  # @param resolution The display's resolution to be used.
  # @param displaystrings A list of strings on which the windows for each user will pop up.
  # @param size Physical size of the display medium in meters.
  # @param transformation A matrix specifying the display's transformation with respect to the platform coordinate system.
  def __init__( self
              , hostname = "atalante"
              , name = "oculus_rift_atalante"
              , resolution = (1280,  800)
              , displaystrings = [":0.0"]
              , size = (0.16, 0.1)
              , stereo = True
              , stereomode = "HMD"
              ):
    Display.__init__( self
                    , hostname = hostname
                    , name = name
                    , resolution = resolution
                    , displaystrings = displaystrings
                    , size = size
                    , stereo = stereo
                    , stereomode = stereomode
                    )

  ## Creates the screen node of this display to be appended to the Platform transformation node.
  # @param name The name of the screen scenegraph node.
  def create_screen_node(self, name = "screen_node"):

    # For a HMD, the screens must be appended to the slot node, not to the platform.
    return None

class PerseusTouchTable(Display):
    def __init__(self):
        Display.__init__(self
                        , hostname = "perseus"
                        , name = "perseus_touch_table"
                        , resolution = (1920 * 2, 1080 * 2)
                        , displaystrings = [":0.0"]
                        , size = (1.25, .71)
                        , transformation = avango.gua.make_trans_mat(0.0,1.2,0.0) * avango.gua.make_rot_mat(-90.0, 1.0, .0, .0)
                        )

    def get_touch_protocols(self):
        return [ "TUIO" ]

class NohraTouchTable(Display):
    def __init__(self):
        Display.__init__(self
                        , hostname = "nohra"
                        , name = "nohra_touch_table"
                        , resolution = (1920 * 2, 2160)
                        , displaystrings = [":0.0"]
                        , size = (1.25, .71)
                        , transformation = avango.gua.make_trans_mat(0.0,0,0.0) * avango.gua.make_rot_mat(-90.0, 1.0, .0, .0)
                        )

    def get_touch_protocols(self):
        return [ "TUIO" ]


##################################################
# STORE ALL DISPLAYS TO BE USED IN THIS LIST
##################################################
## @var displays A list of Display instances to be used in the framework.

displays = [
  #LargePowerwall() ,
  #LargePowerwall2() ,  
  #SmallPowerwall() ,
  #SmallPowerwall2() ,  
  #OculusRift() ,
  TouchTable3D() ,
  #Display(hostname = "daedalos", stereo = False) ,

  PerseusTouchTable(), 
  NohraTouchTable(),

  Display(hostname = "apollo"
      , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0) * avango.gua.make_rot_mat(-90.0, 1.0, .0, .0)
  )
  #,
  #Display(hostname = "atalante"
  #    , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0) * avango.gua.make_rot_mat(-90.0, 1.0, .0, .0)
  #)
  #,
  #Display(hostname = "agenor"
  #    , transformation = avango.gua.make_trans_mat(0.0, 1.2, 0.0) * avango.gua.make_rot_mat(-90.0, 1.0, .0, .0)
  #)
]

## @var INTELLIGENT_SHUTTER_SWITCHING
# If true, free display slots will be assigned to users, vip and active flags
# of users are considered and the users' shutter timings are updated.
INTELLIGENT_SHUTTER_SWITCHING = False
