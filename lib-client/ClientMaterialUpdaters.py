#!/usr/bin/python

## @file
# Contains classes for material updates on client side.

# import avango-guacamole libraries
import avango
import avango.gua
import avango.script
from   avango.script import field_has_changed

## Helper class to update material values with respect to the current time.
class TimedMaterialUniformUpdate(avango.script.Script):

  ## @var TimeIn
  # Field containing the current time in milliseconds.
  TimeIn = avango.SFFloat()

  ## @var MaterialName
  # Field containing the name of the material to be updated
  MaterialName = avango.SFString()

  ## @var UniformName
  # Field containing the name of the uniform value to be updated
  UniformName = avango.SFString()

  ## Called whenever TimeIn changes.
  @field_has_changed(TimeIn)
  def update(self):
    avango.gua.set_material_uniform(self.MaterialName.value,
                                    self.UniformName.value,
                                    self.TimeIn.value)

class TimedCutSphereUpdate(avango.script.Script):
  UniformMat = avango.gua.SFMatrix4()

  MaterialName = avango.SFString()

  def __init__(self):
    self.super(TimedCutSphereUpdate).__init__()

    #self.UniformMat.value = avango.gua.make_identity_mat()
    #self.MaterialName.value = ""


  @field_has_changed(UniformMat)
  def update(self):

    sphere_radius = self.UniformMat.value.get_element(0,1)
    
    sphere_center = avango.gua.Vec3(self.UniformMat.value.get_element(0,0),
                                    self.UniformMat.value.get_element(1,0),
                                    self.UniformMat.value.get_element(2,0))
    



    avango.gua.set_material_uniform(self.MaterialName.value,
                                    "sphere_center",
                                    sphere_center)

    avango.gua.set_material_uniform(self.MaterialName.value,
                                    "sphere_radius",
                                    sphere_radius)
    #print("field")
    