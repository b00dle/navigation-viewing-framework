#!/usr/bin/python

## @file
# Client application for the distributed Navigation and Viewing Framework.

# import avango-guacamole libraries
import avango
import avango.script
import avango.gua
import avango.oculus

# import framework libraries
from ClientMaterialUpdaters import *
from View import *
from ClientPortal import *
from examples_common.GuaVE import GuaVE

# import python libraries
import sys


def prepare_volume():

  _loader = avango.gua.nodes.VolumeLoader()
  _node = _loader.load("volume_test", "/mnt/data_internal/volume_data/general/backpack16_w512_h512_d373_c1_b16.raw", avango.gua.VolumeLoaderFlags.DEFAULTS)


def prepare_medieval():

  timer = avango.nodes.TimeSensor()
  
  water_updater = ClientMaterialUpdaters.TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)


def prepare_pitoti():

  _loader = avango.gua.nodes.PLODLoader()
  _loader.UploadBudget.value = 512
  _loader.RenderBudget.value = 4*1024
  _loader.OutOfCoreBudget.value = 32*1024

  # Valcamonica
  #_path = "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/01_SFM-Befliegung_Seradina_PointCloud/" # opt path
  #_path = "/media/SSD_500GB/CONVERTED_Seradina_Parts/" # ssd path
  
  #_path = "/mnt/pitoti/Seradina_FULL_SCAN/Parts/"
  #_path = "/mnt/pitoti/Seradina_FULL_SCAN/sera_fixed/"
  _path = "/mnt/ssd_pitoti/pitoti/valley/seradina_flyover/" # ssd path

  _node = _loader.create_geometry_from_file("valley1", _path + "sera_part_01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley2", _path + "sera_part_02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley3", _path + "sera_part_03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley4", _path + "sera_part_04.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley5", _path + "sera_part_05.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley6", _path + "sera_part_06.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley7", _path + "sera_part_07.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley8", _path + "sera_part_08.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley9", _path + "sera_part_09.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley10", _path + "sera_part_10.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley11", _path + "sera_part_11.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley12", _path + "sera_part_12.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley13", _path + "sera_part_13.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley14", _path + "sera_part_14.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley15", _path + "sera_part_15.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley16", _path + "sera_part_16.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  
  #_path = "/mnt/ssd_pitoti/pitoti/valley/nadro_flyover/" # ssd path
  #_node = _loader.create_geometry_from_file("valley17", _path + "foppe_di_nadro_const.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _path = "/mnt/ssd_pitoti/pitoti/valley/nadro_flyover/new/" # ssd path
  #_node = _loader.create_geometry_from_file("valley17", _path + "foppe_050713__3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley18", _path + "foppe_050713__4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley19", _path + "foppe_050713__7.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley20", _path + "foppe_050713__8.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley21", _path + "foppe_050713__9.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("valley22", _path + "foppe_050713__10.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)        

  # seradina 12c rock
  _path = "/mnt/ssd_pitoti/pitoti/seradina_12c/rock/" # pitoti ssd path
  _node = _loader.create_geometry_from_file("seradina_12c_rock", _path + "TLS_Seradina_Rock-12C.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  # seradina 12c motives
  _path = "/mnt/ssd_pitoti/pitoti/seradina_12c/motives/" # pitoti ssd path
  _node = _loader.create_geometry_from_file("seradina_motive1", _path + "Area-1_Warrior-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive2", _path + "Area-1_Warrior-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive3", _path + "Area-1_Warrior-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive4", _path + "Area-1_Warrior-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive5", _path + "Area-1_Warrior-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive6", _path + "Area-1_Warrior-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive7", _path + "Area-1_Warrior-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive8", _path + "Area-1_Warrior-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive9", _path + "Area-1_Warrior-scene_P03-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive10", _path + "Area-1_Warrior-scene_P03-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive11", _path + "Area-1_Warrior-scene_P03-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive12", _path + "Area-1_Warrior-scene_P03-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("seradina_motive13", _path + "Area-2_Plowing-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive14", _path + "Area-2_Plowing-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("seradina_motive15", _path + "Area-2_Plowing-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("seradina_motive16", _path + "Area-2_Plowing-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive17", _path + "Area-2_Plowing-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive18", _path + "Area-2_Plowing-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("seradina_motive19", _path + "Area-2_Plowing-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("seradina_motive20", _path + "Area-2_Plowing-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
    
  _node = _loader.create_geometry_from_file("seradina_motive21", _path + "Area-10_Hunting_Scene_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive22", _path + "Area-10_Hunting_Scene_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive23", _path + "Area-10_Hunting_Scene_P03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    

  _node = _loader.create_geometry_from_file("seradina_motive24", _path + "Area-6_house_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive25", _path + "Area-6_house_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  

  _node = _loader.create_geometry_from_file("seradina_motive26", _path + "Area-3_Archers_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina_motive27", _path + "Area-3_Archers_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    
  
  _node = _loader.create_geometry_from_file("seradina_motive28", _path + "Area_4_hunter_with_bow.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("seradina_motive29", _path + "Area-5_hunter_with_speer_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)              
  _node = _loader.create_geometry_from_file("seradina_motive30", _path + "Area-5_hunter_with_speer_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)        

  # nadro 24 rock
  _path = "/mnt/ssd_pitoti/pitoti/nadro_24/rock/" # pitoti ssd path
  _node = _loader.create_geometry_from_file("nadro_24_rock", _path + "TLS_Foppe-di-Nadro_Rock-24.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _path = "/mnt/ssd_pitoti/pitoti/nadro_24/motives/" # pitoti ssd path
  _loader.create_geometry_from_file("nadro_24_motive1", _path + "Area-7_Rosa-Camuna.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _loader.create_geometry_from_file("nadro_24_motive2", _path + "Area-7_Warrior.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)


# Command line parameters:
# main.py SERVER_IP WORKSPACE_CONFIG_FILE WORKSPACE_ID DISPLAY_GROUP_ID SCREEN_ID DISPLAY_NAME

class Test:

  ## Default constructor.
  def __init__(self, GRAPH):

    self.graph = GRAPH

    ## @var frame_trigger
    # Triggers framewise evaluation of frame_callback method.
    self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)    

    
  ## Evaluated every frame.
  def frame_callback(self):

    #print("in function frame_callback")
   
    _node1 = self.graph["/net/cut_sphere1"]
    _node2 = self.graph["/net/cut_sphere2"]
    _node3 = self.graph["/net/cut_sphere3"]
    _node4 = self.graph["/net/cut_sphere4"]
    _node5 = self.graph["/net/cut_sphere5"]
    
    #print(_node != None)
    if _node1 != None and _node2 != None and _node3 != None and _node4 != None and _node5 != None:
      #print("inside", self.frame_trigger.Active.value)
      self.cut_sphere_updater1 = TimedCutSphereUpdate()
      self.cut_sphere_updater1.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"
      self.cut_sphere_updater1.UniformMat.connect_from(_node1.Transform)

      self.cut_sphere_updater2 = TimedCutSphereUpdate()
      self.cut_sphere_updater2.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"
      self.cut_sphere_updater2.UniformMat.connect_from(_node2.Transform)

      self.cut_sphere_updater3 = TimedCutSphereUpdate()
      self.cut_sphere_updater3.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"
      self.cut_sphere_updater3.UniformMat.connect_from(_node3.Transform)

      self.cut_sphere_updater4 = TimedCutSphereUpdate()
      self.cut_sphere_updater4.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"
      self.cut_sphere_updater4.UniformMat.connect_from(_node4.Transform)

      self.cut_sphere_updater5 = TimedCutSphereUpdate()
      self.cut_sphere_updater5.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"
      self.cut_sphere_updater5.UniformMat.connect_from(_node5.Transform)

      self.frame_trigger.Active.value = False # disable frame callback
    
## Main method for the client application.
def start():

  # disable logger warningss
  logger = avango.gua.nodes.Logger(EnableWarning = False)

  # get the server ip
  server_ip = str(sys.argv[1])

  # get the workspace config file #
  workspace_config_file = str(sys.argv[2])
  exec('from ' + workspace_config_file.replace("/", ".").replace(".py", "") + ' import displays', globals())

  # get the workspace id
  workspace_id = int(sys.argv[3])

  # get the display group id
  display_group_id = int(sys.argv[4])

  # get the screen id
  screen_id = int(sys.argv[5])

  # get the display name
  display_name = str(sys.argv[6])

  # get own hostname
  hostname = open('/etc/hostname', 'r').readline()
  hostname = hostname.strip(" \n")

  print("This client is running on", hostname, "and listens to server", server_ip)
  print("It is responsible for workspace", workspace_id, ", display group", display_group_id, "and screen", screen_id)

  # preload materials and shading models
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")
  
  # create distribution node
  nettrans = avango.gua.nodes.NetTransform(
                Name = "net",
                # specify role, ip, and port
                Groupname = "AVCLIENT|{0}|7432".format(server_ip)
                )

  # create a dummy scenegraph to be extended by distribution
  graph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
  graph.Root.value.Children.value = [nettrans]
  
  # create material updaters as this cannot be distributed
  avango.gua.load_shading_models_from("data/materials")
  avango.gua.load_materials_from("data/materials")
  
  timer = avango.nodes.TimeSensor()
  
  water_updater = TimedMaterialUniformUpdate()
  water_updater.MaterialName.value = "data/materials/Water.gmd"
  water_updater.UniformName.value = "time"
  water_updater.TimeIn.connect_from(timer.Time)

  '''
  avango.gua.set_material_uniform("data/materials/SimplePhongWhiteCut.gmd",
                                    "sphere_center",
                                    avango.gua.Vec3(0,0,0))
    
  avango.gua.set_material_uniform("data/materials/SimplePhongWhiteCut.gmd",
                                    "sphere_radius",
                                    0.01)
  '''
  #cut_sphere_updater = TimedCutSphereUpdate()
  #cut_sphere_updater.MaterialName.value = "data/materials/SimplePhongWhiteCut.gmd"

  test = Test(graph)

  #i = 0
  #for i == 0:
  #  if graph["/net/cut_sphere"] != None:
  #    cut_sphere_updater.UniformMat.connect_from(graph["/net/cut_sphere"].Transform)
  #    break

  '''
  # PLOD Stuff
  _loader = avango.gua.nodes.PLODLoader()
  _loader.UploadBudget.value = 256
  _loader.RenderBudget.value = 4*1024
  _loader.OutOfCoreBudget.value = 24*1024

  
  # Valcamonica
  _path = "/mnt/pitoti/KDN_LOD/PITOTI_KDN_LOD/01_SFM-Befliegung_Seradina_PointCloud/" # opt path
  #_path = "/media/SSD_500GB/CONVERTED_Seradina_Parts/" # ssd path 

  _node = _loader.create_geometry_from_file("seradina1_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina2_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina3_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("seradina4_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_04.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    
  _node = _loader.create_geometry_from_file("seradina5_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_05.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina6_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_06.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina7_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_07.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina8_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_08.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina9_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_09.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina10_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_10.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina11_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_11.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina12_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_12.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina13_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_13.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina14_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_14.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina15_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_15.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  _node = _loader.create_geometry_from_file("seradina16_", "/mnt/pitoti/Seradina_FULL_SCAN/Parts/sera_part_16.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)            
  
  # seradina rock
  _path = "/mnt/pitoti/XYZ_ALL/new_pitoti_sampling/" # opt path
  #_path = "/media/SSD_500GB/Pitoti_Resampled/" # ssd path
  _node = _loader.create_geometry_from_file("rock", _path + "TLS_Seradina_Rock-12C.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  
  # seradina pitoti
  _node = _loader.create_geometry_from_file("pitoti1", _path + "Area-1_Warrior-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti2", _path + "Area-1_Warrior-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti3", _path + "Area-1_Warrior-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti4", _path + "Area-1_Warrior-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti5", _path + "Area-1_Warrior-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti6", _path + "Area-1_Warrior-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti7", _path + "Area-1_Warrior-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti8", _path + "Area-1_Warrior-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti9", _path + "Area-1_Warrior-scene_P03-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti10", _path + "Area-1_Warrior-scene_P03-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti11", _path + "Area-1_Warrior-scene_P03-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti12", _path + "Area-1_Warrior-scene_P03-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)

  _node = _loader.create_geometry_from_file("pitoti13", _path + "Area-2_Plowing-scene_P01-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti14", _path + "Area-2_Plowing-scene_P01-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti15", _path + "Area-2_Plowing-scene_P01-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti16", _path + "Area-2_Plowing-scene_P01-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti17", _path + "Area-2_Plowing-scene_P02-1.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti18", _path + "Area-2_Plowing-scene_P02-2.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti19", _path + "Area-2_Plowing-scene_P02-3.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  
  _node = _loader.create_geometry_from_file("pitoti20", _path + "Area-2_Plowing-scene_P02-4.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
    
  _node = _loader.create_geometry_from_file("pitoti21", _path + "Area-10_Hunting_Scene_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti22", _path + "Area-10_Hunting_Scene_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti23", _path + "Area-10_Hunting_Scene_P03.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    

  _node = _loader.create_geometry_from_file("pitoti24", _path + "Area-6_house_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti25", _path + "Area-6_house_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)  

  _node = _loader.create_geometry_from_file("pitoti26", _path + "Area-3_Archers_P01.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)
  _node = _loader.create_geometry_from_file("pitoti27", _path + "Area-3_Archers_P02.kdn", avango.gua.PLODLoaderFlags.DEFAULTS)    

  
  #prepare_volume()
  prepare_medieval()
  #prepare_pitoti()
  '''

  # get the display instance
  for _display in displays:
    if _display.name == display_name:
      handled_display_instance = _display

  # create a viewer
  viewer = avango.gua.nodes.Viewer()

  # Create a view for each displaystring (= slot)
  _string_num = 0
  views = []

  for _displaystring in handled_display_instance.displaystrings:

    _view = View()
    _view.my_constructor(graph, 
                         viewer,
                         handled_display_instance, 
                         workspace_id,
                         display_group_id,
                         screen_id,
                         _string_num)
    views.append(_view)
    _string_num += 1

  viewer.SceneGraphs.value = [graph]

  # create client portal manager
  portal_manager = ClientPortalManager()
  portal_manager.my_constructor(graph, views)

  shell_client = GuaVE()
  shell_client.start(locals(), globals())

  # start rendering process
  viewer.run()

if __name__ == '__main__':
  print("client_main", sys.argv)
  start()
