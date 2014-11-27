#!/usr/bin/python

## @file
# Contains classes SceneManager, TimedMaterialUniformUpdate and TimedRotationUpdate.

# import avango-guacamole libraries
import avango

# import framework libraries
from Objects import *

# import python libraries
# ...


class Passat(SceneObject):

  # dummy testing scene with just the passat object

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Passat", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    _mat = avango.gua.make_trans_mat(-1.99, 0.0, -3) * \
           avango.gua.make_rot_mat(-90.0,1,0,0) * \
           avango.gua.make_rot_mat(90.0,0,0,1) * \
           avango.gua.make_scale_mat(0.04)
    self.init_geometry("passat", "data/objects/passat/passat.obj", _mat, None, True, True, self.scene_root) 

    self.background_texture = "data/textures/skymap.png"


class SceneMedievalTown(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "MedievalTown", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # navigation parameters
    # nice navigation starting mat is avango.gua.make_trans_mat(0.0, 0.0, 22.0)

    # geometry
    _mat = avango.gua.make_scale_mat(7.5)
    self.init_geometry("town", "data/objects/demo_models/medieval_harbour/town.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    
    _mat = avango.gua.make_trans_mat(0, -3.15, 0) * avango.gua.make_scale_mat(1000.0)
    self.init_geometry("water", "data/objects/plane.obj", _mat, 'data/materials/Water.gmd', True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG,
  
    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 20.0)
    #self.init_kinect("kinect1", "/opt/kinect-resources/shot_steppo_animation_distributed_daedalos.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE    
    #self.init_kinect("kinect1", "/opt/kinect-resources/kinect_surface_K_23_24_25.ks", _mat, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, PARENT_NODE
     
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5,0.5,0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
    
    #_mat = avango.gua.make_trans_mat(0.0, 35.0, 30.0) * avango.gua.make_rot_mat(-55.0,1,0,0)
    #self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 1.0, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, RENDER_GROUP = "main_scene", ENABLE_SHADOW = True, LIGHT_DIMENSIONS = avango.gua.Vec3(300.0,300.0,150.0) ) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = False
    self.enable_fxaa = True

class SceneVianden(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "SceneVianden", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # nice navigation starting mat is avango.gua.make_trans_mat(72.730, -5.571, -51.930)  

    # geometry
    _mat = avango.gua.make_rot_mat(90.0,-1,0,0)
    #self.init_geometry("vianden_out", "data/objects/demo_models/Arctron/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    #self.init_geometry("vianden_in", "data/objects/demo_models/Arctron/Vianden/Innen_gesamt/Innenraeume_Gesamt.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("vianden_out", "/mnt/ssd_pitoti/Vianden/Aussen_gesamt/VIANDEN.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_geometry("vianden_in", "/mnt/ssd_pitoti/Vianden/Innen_gesamt/Innenraeume_Gesamt.obj", _mat, None, True, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

          
    # lights
    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.75, 0.75, 0.75), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False, SHADOW_MAP_SIZE = 256, ENABLE_GODRAYS = False) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(50.0, 100.0, -50.0) * \
           avango.gua.make_rot_mat(-90.0, 1.0, 0.0, 0.0)

    self.init_light(TYPE = 2, 
                    NAME = "spot_light",
                    COLOR = avango.gua.Color(1.0, 1.0, 1.0), 
                    MATRIX = _mat, 
                    PARENT_NODE = self.scene_root,
                    RENDER_GROUP = "main_scene", 
                    MANIPULATION_PICK_FLAG = True, 
                    ENABLE_SHADOW = True, 
                    LIGHT_DIMENSIONS = avango.gua.Vec3(900.0,900.0,300.0),
                    SHADOW_MAP_SIZE = 2048)


    # render pipeline parameters
    self.enable_backface_culling = False
    self.enable_frustum_culling = True
    self.enable_ssao = True
    self.enable_fxaa = True
    self.enable_fog = False
    self.ambient_color = avango.gua.Color(0.25, 0.25, 0.25)
    #self.background_texture = "/opt/guacamole/resources/skymaps/DH221SN.png"
    self.background_texture = "/opt/guacamole/resources/skymaps/cycles_island2.jpg"

 
class SceneMonkey(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Monkey", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # nice navigation starting mat is avango.gua.make_trans_mat(0.0, 0.0, 1.0)

    _mat = avango.gua.make_identity_mat()
    self.init_group("group", _mat, False, True, self.scene_root, "main_scene")

    _parent_object = self.get_object("group")

    _mat = avango.gua.make_trans_mat(0.0,1.2,0.0) * avango.gua.make_scale_mat(0.1)
    self.init_geometry("monkey1", "data/objects/monkey.obj", _mat, "data/materials/SimplePhongWhite.gmd", False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE, RENDER_GROUP

    _mat = avango.gua.make_trans_mat(-0.25,1.2,0.0) * avango.gua.make_scale_mat(0.05)
    self.init_geometry("monkey2", "data/objects/monkey.obj", _mat, "data/materials/AvatarBlue.gmd", False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.25,1.2,0.0) * avango.gua.make_scale_mat(0.05)
    self.init_geometry("monkey3", "data/objects/monkey.obj", _mat, "data/materials/AvatarBlue.gmd", False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0, 1.0, 0.0) * avango.gua.make_scale_mat(2.0)
    self.init_geometry("plane", "data/objects/plane.obj", _mat, 'data/materials/ComplexPhongTiles.gmd', False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
  
    
    # lights
    _mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(-0.3, 1.4, 0.0)
    self.init_light(TYPE = 1, NAME = "point_light", COLOR = avango.gua.Color(0.0, 1.0, 0.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    _mat = avango.gua.make_trans_mat(0.0, 1.55, 0.0) * avango.gua.make_rot_mat(90.0,-1,0,0)
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.25, 0.25), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = True, LIGHT_DIMENSIONS = avango.gua.Vec3(2.0,2.0,1.0), RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE



class SceneValcamonica(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Valcamonica", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    #self.starting_matrix = avango.gua.make_identity_mat()
    #self.starting_scale = 1.0


    # rotate whole scene upright
    _rot_mat = avango.gua.make_identity_mat()
    _rot_mat.set_element(0,0, 0.088)
    _rot_mat.set_element(1,0, 0.016)
    _rot_mat.set_element(2,0, 0.996)
    _rot_mat.set_element(0,1, 0.996)
    _rot_mat.set_element(1,1, 0.005)
    _rot_mat.set_element(2,1, -0.088)
    _rot_mat.set_element(0,2, -0.007)
    _rot_mat.set_element(1,2, 1.0)
    _rot_mat.set_element(2,2, -0.016)

    self.scene_root.Transform.value = _rot_mat
    
    ### valley
    _offset_mat = avango.gua.make_trans_mat(-604050.0, -5098490.0, -400.0)

    # seradina flyover
    _scale = 31.261682663898622
   
    _rot_mat = avango.gua.make_identity_mat()
    _rot_mat.set_element(0,0, -0.57732352)
    _rot_mat.set_element(1,0, 0.816437476)
    _rot_mat.set_element(2,0, 0.0112872)
    _rot_mat.set_element(0,1, 0.040792)
    _rot_mat.set_element(1,1, 0.042645956)
    _rot_mat.set_element(2,1, -0.998257147)
    _rot_mat.set_element(0,2, -0.8154959)
    _rot_mat.set_element(1,2, -0.5758569)
    _rot_mat.set_element(2,2, -0.057924671)
   
    _pos = avango.gua.Vec3(603956.727956973, 5098223.502562742, 819.626837676)
    
    _mat = avango.gua.make_trans_mat(_pos) * _rot_mat * avango.gua.make_scale_mat(_scale)
    _mat = _offset_mat * _mat
       
    #_path = "/mnt/pitoti/Seradina_FULL_SCAN/sera_fixed/"
    _path = "/mnt/ssd_pitoti/pitoti/valley/seradina_flyover/" # pitoti ssd path
    
    self.init_plod("valley1", _path + "sera_part_01.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("valley2", _path + "sera_part_02.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley3", _path + "sera_part_03.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley4", _path + "sera_part_04.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley5", _path + "sera_part_05.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley6", _path + "sera_part_06.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley7", _path + "sera_part_07.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley8", _path + "sera_part_08.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley9", _path + "sera_part_09.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley10", _path + "sera_part_10.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley11", _path + "sera_part_11.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley12", _path + "sera_part_12.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley13", _path + "sera_part_13.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley14", _path + "sera_part_14.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley15", _path + "sera_part_15.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley16", _path + "sera_part_16.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
 
    # foppe di nadro flyover
    #_path = "/mnt/ssd_pitoti/pitoti/valley/nadro_flyover/" # pitoti ssd path
    _path = "/mnt/ssd_pitoti/pitoti/valley/nadro_flyover/new/" # pitoti ssd path        

    _scale = 36.14874291170112
  
    _rot_mat = avango.gua.make_identity_mat()
    _rot_mat.set_element(0,0, -0.230820615)
    _rot_mat.set_element(1,0, -0.972716931)
    _rot_mat.set_element(2,0, -0.0233156)
    _rot_mat.set_element(0,1, -0.4758191)
    _rot_mat.set_element(1,1, 0.0919426)
    _rot_mat.set_element(2,1, 0.8747244)
    _rot_mat.set_element(0,2, -0.848715517)
    _rot_mat.set_element(1,2, 0.212998422)
    _rot_mat.set_element(2,2, -0.484059545)
  
    _pos = avango.gua.Vec3(605535.577, 5097551.573, 1468.071)
    
    _mat = avango.gua.make_trans_mat(_pos) * _rot_mat * avango.gua.make_scale_mat(_scale)
    _mat = _offset_mat * _mat
 
    #self.init_plod("valley17", _path + "foppe_di_nadro_const.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    #self.init_plod("valley17", _path + "foppe_050713__3.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley18", _path + "foppe_050713__4.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley19", _path + "foppe_050713__7.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley20", _path + "foppe_050713__8.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley21", _path + "foppe_050713__9.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("valley22", _path + "foppe_050713__10.kdn", _mat, False, True, self.scene_root, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE


    ### rocks
    
    # seradina 12c
    _mat = avango.gua.make_trans_mat(604050.0, 5098490.0, 400.0)
    _mat = _offset_mat * _mat
    
    self.init_group("seradina_12c_group", _mat, False, True, self.scene_root, "main_scene")

    _parent_object = self.get_interactive_object("seradina_12c_group")
    _mat = avango.gua.make_identity_mat()
        
    _path = "/mnt/ssd_pitoti/pitoti/seradina_12c/rock/" # pitoti ssd path

    self.init_plod("seradina_12c_rock", _path + "TLS_Seradina_Rock-12C.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    


    # seradina motives
    _path = "/mnt/ssd_pitoti/pitoti/seradina_12c/motives/" # pitoti ssd path

    self.init_plod("seradina_motive1", _path + "Area-1_Warrior-scene_P01-1.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive2", _path + "Area-1_Warrior-scene_P01-2.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive3", _path + "Area-1_Warrior-scene_P01-3.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive4", _path + "Area-1_Warrior-scene_P01-4.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive5", _path + "Area-1_Warrior-scene_P02-1.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive6", _path + "Area-1_Warrior-scene_P02-2.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive7", _path + "Area-1_Warrior-scene_P02-3.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive8", _path + "Area-1_Warrior-scene_P02-4.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive9", _path + "Area-1_Warrior-scene_P03-1.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive10", _path + "Area-1_Warrior-scene_P03-2.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive11", _path + "Area-1_Warrior-scene_P03-3.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive12", _path + "Area-1_Warrior-scene_P03-4.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    

    self.init_plod("seradina_motive13", _path + "Area-2_Plowing-scene_P01-1.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("seradina_motive14", _path + "Area-2_Plowing-scene_P01-2.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive15", _path + "Area-2_Plowing-scene_P01-3.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive16", _path + "Area-2_Plowing-scene_P01-4.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("seradina_motive17", _path + "Area-2_Plowing-scene_P02-1.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("seradina_motive18", _path + "Area-2_Plowing-scene_P02-2.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive19", _path + "Area-2_Plowing-scene_P02-3.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive20", _path + "Area-2_Plowing-scene_P02-4.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_plod("seradina_motive21", _path + "Area-10_Hunting_Scene_P01.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive22", _path + "Area-10_Hunting_Scene_P02.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE    
    self.init_plod("seradina_motive23", _path + "Area-10_Hunting_Scene_P03.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE

    self.init_plod("seradina_motive24", _path + "Area-6_house_P01.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("seradina_motive25", _path + "Area-6_house_P02.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE                            

    self.init_plod("seradina_motive26", _path + "Area-3_Archers_P01.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE            
    self.init_plod("seradina_motive27", _path + "Area-3_Archers_P02.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE            

    self.init_plod("seradina_motive28", _path + "Area_4_hunter_with_bow.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE            

    self.init_plod("seradina_motive29", _path + "Area-5_hunter_with_speer_P01.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE            
    self.init_plod("seradina_motive30", _path + "Area-5_hunter_with_speer_P02.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE       


    # nadro 24
    _mat = avango.gua.make_trans_mat(604050.0, 5098490.0, 400.0)
    _mat = _offset_mat * _mat

    self.init_group("nadro_24_group", _mat, False, True, self.scene_root, "main_scene")

    _parent_object = self.get_interactive_object("nadro_24_group")
    _mat = avango.gua.make_identity_mat()
    
    _path = "/mnt/ssd_pitoti/pitoti/nadro_24/rock/" # pitoti ssd path

    self.init_plod("nadro_24_rock", _path + "TLS_Foppe-di-Nadro_Rock-24.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE        

    # nadro 24 motives    
    _path = "/mnt/ssd_pitoti/pitoti/nadro_24/motives/" # pitoti ssd path
           
    self.init_plod("nadro_24_motive1", _path + "Area-7_Rosa-Camuna.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE
    self.init_plod("nadro_24_motive2", _path + "Area-7_Warrior.kdn", _mat, False, True, _parent_object, "main_scene") # parameters: NAME, FILENAME, MATRIX, MATERIAL, GROUNDFOLLOWING_PICK_FLAG, MANIPULATION_PICK_FLAG, PARENT_NODE            


    #_mat = avango.gua.make_trans_mat(0.0, 0.0, 0.0)
    #self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 0.0, 0.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, RENDER_GROUP = "main_scene", ENABLE_SHADOW = False, LIGHT_DIMENSIONS = avango.gua.Vec3(10.0,10.0,10.0) ) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    #_mat = avango.gua.make_trans_mat(0.0, 2.0, 0.0)
    #self.init_light(TYPE = 1, NAME = "point_light", COLOR = avango.gua.Color(1.0, 1.0, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, RENDER_GROUP = "main_scene", LIGHT_DIMENSIONS = avango.gua.Vec3(50.0,50.0,50.0)) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(1.0, 0.0, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = False, RENDER_GROUP = "main_scene") # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE

    # render pipeline parameters
    self.background_texture = "/opt/guacamole/resources/skymaps/DayLight_08.jpg"
    self.near_clip = 0.15
    self.far_clip = 10000.0
    self.enable_backface_culling = True
    self.enable_frustum_culling = True
      
'''
class SceneWeimar(SceneObject):

  # constructor
  def __init__(self, SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE):
    SceneObject.__init__(self, "Weimar", SCENE_MANAGER, SCENEGRAPH, NET_TRANS_NODE) # call base class constructor

    # nice navigation starting mat is avango.gua.make_trans_mat(42.0, 0.1, -5.8)
    
    self.enable_ssao = True
    self.ssao_radius = 2.0
    self.ssao_intensity = 2.0
    self.enable_fog = False
    self.ambient_color.value = avango.gua.Color(0.0, 0.0, 0.0)
    #self.ambient_color.value = avango.gua.Color(1.0, 0.0, 0.0)
    self.far_clip = 2000.0

    self.background_texture = "data/textures/bright_sky.jpg"

    _mat = avango.gua.make_scale_mat(0.5)
    #self.init_geometry("weimar", "data/objects/demo_models/weimar_stadtmodell_29.08.12/weimar_stadtmodell_final.obj", _mat, "data/materials/SimplePhongWhite.gmd", True, False, self.scene_root, "main_scene")
    self.init_geometry("weimar", "data/objects/demo_models/weimar_stadtmodell_29.08.12/weimar_stadtmodell_final.obj", _mat, None, True, False, self.scene_root, "main_scene")

    _mat = avango.gua.make_trans_mat(0.0, 200.0, 60.0) * \
           avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0)
    self.init_light(TYPE = 2, NAME = "spot_light", COLOR = avango.gua.Color(1.0, 1.0, 1.0), MATRIX = _mat, PARENT_NODE = self.scene_root, MANIPULATION_PICK_FLAG = True, ENABLE_SHADOW = False, LIGHT_DIMENSIONS = avango.gua.Vec3(1000.0,1000.0,300.0), FALLOFF = 0.009, SOFTNESS = 0.003, SHADOW_MAP_SIZE = 2048, ENABLE_SPECULAR_SHADING = True)

    #_mat = avango.gua.make_rot_mat(72.0, -1.0, 0, 0) * avango.gua.make_rot_mat(-30.0, 0, 1, 0)
    #self.init_light(TYPE = 0, NAME = "sun_light", COLOR = avango.gua.Color(0.5, 0.5, 0.5), MATRIX = _mat, PARENT_NODE = self.scene_root, ENABLE_SHADOW = True, SHADOW_MAP_SIZE = 2048) # parameters TYPE (0 = sun light), NAME, COLOR, MATRIX, PARENT_NODE
'''