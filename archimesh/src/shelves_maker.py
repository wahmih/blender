# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

#----------------------------------------------------------
# File: shelves_maker.py
# Automatic generation of shelves
# Author: Antonio Vazquez (antonioya)
#
#----------------------------------------------------------
import bpy
import copy
from tools import *

#------------------------------------------------------------------
# Define UI class
# Shelves
#------------------------------------------------------------------
class SHELVES(bpy.types.Operator):
    bl_idname = "mesh.archimesh_shelves"
    bl_label = "Shelves"
    bl_description = "Shelves Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
     
    thickness= bpy.props.FloatProperty(name='Side Thickness',min=0.001,max= 5, default= 0.03,precision=3, description='Board thickness')
    sthickness= bpy.props.FloatProperty(name='Shelves Thickness',min=0.001,max= 5, default= 0.03,precision=3, description='Board thickness')
    depth= bpy.props.FloatProperty(name='Depth',min=0.001,max= 50, default= 0.28,precision=3, description='Default unit depth')
    height= bpy.props.FloatProperty(name='Height',min=0.001,max= 50, default= 2,precision=3, description='Default unit height')
    top= bpy.props.FloatProperty(name='Top',min=0,max= 50, default= 0.03,precision=3, description='Default top shelf position')
    bottom= bpy.props.FloatProperty(name='Bottom',min=0,max= 50, default= 0.07,precision=3, description='Default bottom self position')
    stype = bpy.props.EnumProperty(items = (('1',"Full side",""),
                                    ('4',"4 Legs",""),
                                    ('99',"None","")),
                                   name="Sides",
                                   description="Type of side construction")

    fitZ = bpy.props.BoolProperty(name = "Floor origin in Z=0",description="Use Z=0 axis as vertical origin floor position",default = True)

    shelves_num= bpy.props.IntProperty(name='Number of Units',min=1,max= 10, default= 1, description='Number total of shelves units')
    # Cabinet width    
    sX01 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX02 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX03 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX04 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX05 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX06 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX07 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX08 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX09 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
    sX10 = bpy.props.FloatProperty(name='width',min=0.001,max= 10, default= 1,precision=3, description='Furniture width')
        
    wY01 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY02 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY03 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY04 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY05 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY06 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY07 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY08 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY09 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')
    wY10 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify y size')

    wZ01 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ02 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ03 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ04 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ05 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ06 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ07 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ08 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ09 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
    wZ10 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Modify z size')
        
    # Cabinet position shift   
    pX01 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX02 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX03 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX04 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX05 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX06 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX07 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX08 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX09 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')
    pX10 = bpy.props.FloatProperty(name='',min=0,max= 10, default= 0,precision=3, description='Position x shift')

    pY01 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY02 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY03 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY04 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY05 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY06 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY07 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY08 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY09 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')
    pY10 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position y shift')

    pZ01 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ02 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ03 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ04 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ05 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ06 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ07 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ08 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ09 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    pZ10 = bpy.props.FloatProperty(name='',min=-10,max= 10, default= 0,precision=3, description='Position z shift')

    # Shelves
    sNum01 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum02 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum03 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum04 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum05 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum06 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum07 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum08 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum09 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    sNum10 = bpy.props.IntProperty(name='Shelves',min=0,max= 12, default= 6, description='Number total of shelves')
    
    p01Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p01Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p02Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p02Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p03Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p03Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p04Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p04Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p05Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p05Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p06Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p06Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p07Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p07Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p08Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p08Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p09Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p09Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    
    p10Z01 = bpy.props.FloatProperty(name='zS1',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z02 = bpy.props.FloatProperty(name='zS2',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z03 = bpy.props.FloatProperty(name='zS3',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z04 = bpy.props.FloatProperty(name='zS4',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z05 = bpy.props.FloatProperty(name='zS5',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z06 = bpy.props.FloatProperty(name='zS6',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z07 = bpy.props.FloatProperty(name='zS7',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z08 = bpy.props.FloatProperty(name='zS8',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z09 = bpy.props.FloatProperty(name='zS9',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z10 = bpy.props.FloatProperty(name='zS10',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z11 = bpy.props.FloatProperty(name='zS11',min=-10,max= 10, default= 0,precision=3, description='Position z shift')
    p10Z12 = bpy.props.FloatProperty(name='zS12',min=-10,max= 10, default= 0,precision=3, description='Position z shift')

    right01 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right02 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right03 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right04 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right05 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right06 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right07 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right08 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right09 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)
    right10 = bpy.props.BoolProperty(name = "Right",description="Create right side",default = True)

    left01 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left02 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left03 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left04 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left05 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left06 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left07 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left08 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left09 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)
    left10 = bpy.props.BoolProperty(name = "Left",description="Create left side",default = True)



    # Materials        
    crt_mat = bpy.props.BoolProperty(name = "Create default Cycles materials",description="Create default materials for Cycles render.",default = True)

    #-----------------------------------------------------
    # Draw (create UI interface)
    #-----------------------------------------------------
    def draw(self, context):
        layout = self.layout
        space = bpy.context.space_data
        if (not space.local_view):
            # Imperial units warning
            if (bpy.context.scene.unit_settings.system == "IMPERIAL"):
                row=layout.row()
                row.label("Warning: Imperial units not supported", icon='COLOR_RED')
            
            box=layout.box()
            row=box.row()
            row.prop(self,'thickness')
            row.prop(self,'sthickness')
            row=box.row()
            row.prop(self,'depth')
            row.prop(self,'height')
            row=box.row()
            row.prop(self,'top')
            row.prop(self,'bottom')
            row=box.row()
            row.prop(self,'stype')
            row.prop(self,'fitZ')
    
            # Furniture number
            row=layout.row()
            row.prop(self,'shelves_num')
            if (self.shelves_num >= 1): add_shelves(self,'01',self.sNum01)
            if (self.shelves_num >= 2): add_shelves(self,'02',self.sNum02)
            if (self.shelves_num >= 3): add_shelves(self,'03',self.sNum03)
            if (self.shelves_num >= 4): add_shelves(self,'04',self.sNum04)
            if (self.shelves_num >= 5): add_shelves(self,'05',self.sNum05)
            if (self.shelves_num >= 6): add_shelves(self,'06',self.sNum06)
            if (self.shelves_num >= 7): add_shelves(self,'07',self.sNum07)
            if (self.shelves_num >= 8): add_shelves(self,'08',self.sNum08)
            if (self.shelves_num >= 9): add_shelves(self,'09',self.sNum09)
            if (self.shelves_num >= 10): add_shelves(self,'10',self.sNum10)
            
    
            box=layout.box()
            box.prop(self,'crt_mat')
        else:
            row=layout.row()
            row.label("Warning: Operator does not work in local view mode", icon='ERROR')
        
    #-----------------------------------------------------
    # Execute
    #-----------------------------------------------------
    def execute(self, context):
        if (bpy.context.mode == "OBJECT"):
            # Create shelves    
            create_shelves_mesh(self,context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Archimesh: Option only valid in Object mode")
            return {'CANCELLED'}
#-----------------------------------------------------
# Add shelves parameters
#-----------------------------------------------------
def add_shelves(self,num,snum):
    layout = self.layout
    box=layout.box()
    row = box.row()
    row.label("Unit " + str(num))
    row.prop(self,'sX' + num)

    row = box.row()
    row.prop(self,'wY' + num)
    row.prop(self,'wZ' + num)
    if (self.stype != "99"):
        row.prop(self,'left' + num)
        row.prop(self,'right' + num)
    
    row = box.row()
    row.prop(self,'pX' + num)
    row.prop(self,'pY' + num)
    row.prop(self,'pZ' + num)

    row = box.row()
    row.prop(self,'sNum' + num, slider=True)
    
    if (snum >= 1): 
        row = box.row()
        row.prop(self,'p' + num + 'Z01')
    if (snum >= 2): 
        row.prop(self,'p' + num + 'Z02')
    if (snum >= 3): 
        row.prop(self,'p' + num + 'Z03')

    if (snum >= 4): 
        row = box.row()
        row.prop(self,'p' + num + 'Z04')
    if (snum >= 5): 
        row.prop(self,'p' + num + 'Z05')
    if (snum >= 6): 
        row.prop(self,'p' + num + 'Z06')
    
    if (snum >= 7): 
        row = box.row()
        row.prop(self,'p' + num + 'Z07')
    if (snum >= 8): 
        row.prop(self,'p' + num + 'Z08')
    if (snum >= 9): 
        row.prop(self,'p' + num + 'Z09')

    if (snum >= 10): 
        row = box.row()
        row.prop(self,'p' + num + 'Z10')
    if (snum >= 11): 
        row.prop(self,'p' + num + 'Z11')
    if (snum >= 12): 
        row.prop(self,'p' + num + 'Z12')


#------------------------------------------------------------------------------
# Generate mesh data
# All custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def create_shelves_mesh(self,context):
    # deactivate others
    for o in bpy.data.objects:
        if (o.select == True):
            o.select = False
    bpy.ops.object.select_all(False)
    # Create units
    generate_shelves(self,context)
          
    return
#------------------------------------------------------------------------------
# Generate Units
# All custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def generate_shelves(self,context):

    Boxes = []
    location = bpy.context.scene.cursor_location
    myLoc = copy.copy(location) # copy location to keep 3D cursor position
    # Fit to floor
    if (self.fitZ):
        myLoc[2] = 0
    
    # Create units
    lastX = 0
    #------------------------------------------------------------------------------
    # Shelves 01
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 1):
        myData = create_book(self.stype,1,"Shelves01"
                           , self.thickness, self.sthickness
                           , self.sX01, self.depth + self.wY01, self.height + self.wZ01 
                           , myLoc[0] + self.pX01 + lastX, myLoc[1] + self.pY01, myLoc[2] + self.pZ01
                           , self.left01, self.right01
                           , self.sNum01, self.crt_mat
                           ,(self.p01Z01,self.p01Z02,self.p01Z03,self.p01Z04,self.p01Z05
                             ,self.p01Z06,self.p01Z07,self.p01Z08,self.p01Z09,self.p01Z10,self.p01Z11,self.p01Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 02
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 2):
        myData = create_book(self.stype,2,"Shelves02"
                           , self.thickness, self.sthickness
                           , self.sX02, self.depth + self.wY02, self.height + self.wZ02 
                           , self.pX02 + lastX, myLoc[1] + self.pY02, myLoc[2] + self.pZ02
                           , self.left02, self.right02
                           , self.sNum02, self.crt_mat
                           ,(self.p02Z01,self.p02Z02,self.p02Z03,self.p02Z04,self.p02Z05
                             ,self.p02Z06,self.p02Z07,self.p02Z08,self.p02Z09,self.p02Z10,self.p02Z11,self.p02Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 03
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 3):
        myData = create_book(self.stype,3,"Shelves03"
                           , self.thickness, self.sthickness
                           , self.sX03, self.depth + self.wY03, self.height + self.wZ03 
                           , self.pX03 + lastX, myLoc[1] + self.pY03, myLoc[2] + self.pZ03
                           , self.left03, self.right03
                           , self.sNum03, self.crt_mat
                           ,(self.p03Z01,self.p03Z02,self.p03Z03,self.p03Z04,self.p03Z05
                             ,self.p03Z06,self.p03Z07,self.p03Z08,self.p03Z09,self.p03Z10,self.p03Z11,self.p03Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 04
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 4):
        myData = create_book(self.stype,4,"Shelves04"
                           , self.thickness, self.sthickness
                           , self.sX04, self.depth + self.wY04, self.height + self.wZ04 
                           , self.pX04 + lastX, myLoc[1] + self.pY04, myLoc[2] + self.pZ04
                           , self.left04, self.right04
                           , self.sNum04, self.crt_mat
                           ,(self.p04Z01,self.p04Z02,self.p04Z03,self.p04Z04,self.p04Z05
                             ,self.p04Z06,self.p04Z07,self.p04Z08,self.p04Z09,self.p04Z10,self.p04Z11,self.p04Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 05
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 5):
        myData = create_book(self.stype,5,"Shelves05"
                           , self.thickness, self.sthickness
                           , self.sX05, self.depth + self.wY05, self.height + self.wZ05 
                           , self.pX05 + lastX, myLoc[1] + self.pY05, myLoc[2] + self.pZ05
                           , self.left05, self.right05
                           , self.sNum05, self.crt_mat
                           ,(self.p05Z01,self.p05Z02,self.p05Z03,self.p05Z04,self.p05Z05
                             ,self.p05Z06,self.p05Z07,self.p05Z08,self.p05Z09,self.p05Z10,self.p05Z11,self.p05Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 06
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 6):
        myData = create_book(self.stype,6,"Shelves06"
                           , self.thickness, self.sthickness
                           , self.sX06, self.depth + self.wY06, self.height + self.wZ06 
                           , self.pX06 + lastX, myLoc[1] + self.pY06, myLoc[2] + self.pZ06
                           , self.left06, self.right06
                           , self.sNum06, self.crt_mat
                           ,(self.p06Z01,self.p06Z02,self.p06Z03,self.p06Z04,self.p06Z05
                             ,self.p06Z06,self.p06Z07,self.p06Z08,self.p06Z09,self.p06Z10,self.p06Z11,self.p06Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 07
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 7):
        myData = create_book(self.stype,7,"Shelves07"
                           , self.thickness, self.sthickness
                           , self.sX07, self.depth + self.wY07, self.height + self.wZ07 
                           , self.pX07 + lastX, myLoc[1] + self.pY07, myLoc[2] + self.pZ07
                           , self.left07, self.right07
                           , self.sNum07, self.crt_mat
                           ,(self.p07Z01,self.p07Z02,self.p07Z03,self.p07Z04,self.p07Z05
                             ,self.p07Z06,self.p07Z07,self.p07Z08,self.p07Z09,self.p07Z10,self.p07Z11,self.p07Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 08
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 8):
        myData = create_book(self.stype,8,"Shelves08"
                           , self.thickness, self.sthickness
                           , self.sX08, self.depth + self.wY08, self.height + self.wZ08 
                           , self.pX08 + lastX, myLoc[1] + self.pY08, myLoc[2] + self.pZ08
                           , self.left08, self.right08
                           , self.sNum08, self.crt_mat
                           ,(self.p08Z01,self.p08Z02,self.p08Z03,self.p08Z04,self.p08Z05
                             ,self.p08Z06,self.p08Z07,self.p08Z08,self.p08Z09,self.p08Z10,self.p08Z11,self.p08Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 09
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 9):
        myData = create_book(self.stype,9,"Shelves09"
                           , self.thickness, self.sthickness
                           , self.sX09, self.depth + self.wY09, self.height + self.wZ09 
                           , self.pX09 + lastX, myLoc[1] + self.pY09, myLoc[2] + self.pZ09
                           , self.left09, self.right09
                           , self.sNum09, self.crt_mat
                           ,(self.p09Z01,self.p09Z02,self.p09Z03,self.p09Z04,self.p09Z05
                             ,self.p09Z06,self.p09Z07,self.p09Z08,self.p09Z09,self.p09Z10,self.p09Z11,self.p09Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
    #------------------------------------------------------------------------------
    # Shelves 10
    #------------------------------------------------------------------------------
    if (self.shelves_num >= 10):
        myData = create_book(self.stype,10,"Shelves10"
                           , self.thickness, self.sthickness
                           , self.sX10, self.depth + self.wY10, self.height + self.wZ10 
                           , self.pX10 + lastX, myLoc[1] + self.pY10, myLoc[2] + self.pZ10
                           , self.left10, self.right10
                           , self.sNum10, self.crt_mat
                           ,(self.p10Z01,self.p10Z02,self.p10Z03,self.p10Z04,self.p10Z05
                             ,self.p10Z06,self.p10Z07,self.p10Z08,self.p10Z09,self.p10Z10,self.p10Z11,self.p10Z12),self.top,self.bottom)
        Boxes.extend([myData[0]])
        lastX = myData[1]
        
    # refine units
    for box in Boxes:
        remove_doubles(box)
        set_normals(box)
        
    # deactivate others
    for o in bpy.data.objects:
        if (o.select == True):
            o.select = False
    
    Boxes[0].select = True        
    bpy.context.scene.objects.active = Boxes[0]

    # Create materials        
    if (self.crt_mat):
        mat = create_diffuse_material("Shelves_material", False, 0.8, 0.8, 0.8)
        for box in Boxes:
            set_material(box,mat)

  
          
    return
#------------------------------------------------------------------------------
# Create shelves unit
#
# stype: type of sides
# num: Current furniture number
# objName: Name for the new object
# thickness: wood thickness (sides)
# sthickness: wood thickness (shelves)
# sX: Size in X axis
# sY: Size in Y axis
# sZ: Size in Z axis
# pX: position X axis
# pY: position Y axis
# pZ: position Z axis
# right: True-> create right side
# left: True-> create left side
# shelves: Number of shelves
# mat: Flag for creating materials
# zPos: List with z shift for each self
# top: position of top shelf
# bottom: position of bottom shelf
#------------------------------------------------------------------------------
def create_book(stype,num,objName,thickness,sthickness,sX,sY,sZ,pX,pY,pZ,left,right,shelves,mat,zPos,top,bottom):

    myVertex = []
    myFaces = []
    v = 0
    
    # no Sides, then no thickness
    if (stype == "99"):
        thickness = 0
    
    
    #------------------------------
    # Left side 
    #------------------------------
    if (left and stype != "99"):
        # Full side
        if (stype == "1"):
            myVertex.extend([(0,0,0),(0,-sY,0),(0,-sY,sZ),(0,0,sZ)
                             ,(thickness,0,0),(thickness,-sY,0),(thickness,-sY,sZ),(thickness,0,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
        # Four legs
        if (stype == "4"):
            # back
            myVertex.extend([(0,0,0),(0,-thickness,0),(0,-thickness,sZ),(0,0,sZ)
                             ,(thickness,0,0),(thickness,-thickness,0),(thickness,-thickness,sZ),(thickness,0,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
            # Front
            myVertex.extend([(0,-sY + thickness,0),(0,-sY,0),(0,-sY,sZ),(0,-sY + thickness,sZ)
                             ,(thickness,-sY + thickness,0),(thickness,-sY,0),(thickness,-sY,sZ),(thickness,-sY + thickness,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
            
    #-----------------
    # Right side
    #-----------------
    if (right and stype != "99"):
        width = sX - thickness
        # Full side
        if (stype == "1"):
            myVertex.extend([(width,0,0),(width,-sY,0),(width,-sY,sZ),(width,0,sZ)
                             ,(width+thickness,0,0),(width+thickness,-sY,0),(width+thickness,-sY,sZ),(width+thickness,0,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
        # Four legs
        if (stype == "4"):
            # back
            myVertex.extend([(width,0,0),(width,-thickness,0),(width,-thickness,sZ),(width,0,sZ)
                             ,(width+thickness,0,0),(width+thickness,-thickness,0),(width+thickness,-thickness,sZ),(width+thickness,0,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
            # Front
            myVertex.extend([(width,-sY + thickness,0),(width,-sY,0),(width,-sY,sZ),(width,-sY + thickness,sZ)
                             ,(width+thickness,-sY + thickness,0),(width+thickness,-sY,0),(width+thickness,-sY,sZ),(width+thickness,-sY + thickness,sZ)])
            myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
            v = v + 8
    #-----------------
    # shelves
    #-----------------
    posX = 0
    # calculate width
    width = sX - thickness
    posX = posX + thickness
        
    # calculate vertical spaces
    dist = sZ - top - bottom - sthickness
    # if only top/bottom the space is not necessary
    if (shelves > 2):
        space = dist / (shelves - 1)
    else:
        space = 0
             
    posZ1 = bottom

    for x in range(shelves):
        # bottom 
        if (x == 0):
            posZ1 = bottom
        # top 
        if (x == shelves - 1):
            posZ1 = sZ - top - sthickness
        
        posZ2 = posZ1 - sthickness
        myVertex.extend([(posX, 0,posZ1 + zPos[x]),(posX,-sY,posZ1 + zPos[x])
                        ,(posX,-sY,posZ2 + zPos[x]),(posX,0,posZ2 + zPos[x])
                        ,(width, 0,posZ1 + zPos[x]),(width,-sY,posZ1 + zPos[x])
                        ,(width,-sY,posZ2 + zPos[x]),(width,0,posZ2 + zPos[x])])

        myFaces.extend([(v,v+1,v+2,v+3),(v+4,v+5,v+6,v+7),(v,v+4,v+7,v+3),(v,v+1,v+5,v+4),(v+3,v+2,v+6,v+7),(v+1,v+2,v+6,v+5)])
        v = v + 8
        posZ1 = posZ1 + space
        
    
    mymesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mymesh)
    
    myobject.location[0] = pX
    myobject.location[1] = pY
    myobject.location[2] = pZ
    bpy.context.scene.objects.link(myobject)
    
    mymesh.from_pydata(myVertex, [], myFaces)
    mymesh.update(calc_edges=True)
    
    return (myobject,pX + sX -thickness)

#----------------------------------------------
# Code to run alone the script
#----------------------------------------------
if __name__ == "__main__":
    create_mesh(0)
    print("Executed")
