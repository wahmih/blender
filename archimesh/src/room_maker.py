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
# File: room_maker.py
# Automatic generation of rooms
# Author: Antonio Vazquez (antonioya)
#
#----------------------------------------------------------
import bpy
import math
from tools import *

#------------------------------------------------------------------
# Reset room default values
# Rooms
#------------------------------------------------------------------
def reset_room(self):
    self.room_height=2.4
    self.wall_width=0.0
    self.inverse = False
    self.crt_mat = True
    self.wall_num=1
    self.baseboard = True
    self.base_width=0.015
    self.base_height=0.12
    self.ceiling = False
    self.floor = False
    self.merge = False
   
    self.w01=1
    self.w02=1
    self.w03=1
    self.w04=1
    self.w05=1
    self.w06=1
    self.w07=1
    self.w08=1
    self.w09=1
    self.w10=1
    self.w11=1
    self.w12=1
    self.w13=1
    self.w14=1
    self.w15=1
    self.w16=1
    self.w17=1
    self.w18=1
    self.w19=1
    self.w20=1
    self.w11=1
    self.w12=1
    self.w23=1
    self.w24=1
    self.w25=1
    
    self.a01= False
    self.a02= False
    self.a03= False
    self.a04= False
    self.a05= False
    self.a06= False
    self.a07= False
    self.a08= False
    self.a09= False
    self.a10= False
    self.a11= False
    self.a12= False
    self.a13= False
    self.a14= False
    self.a15= False
    self.a16= False
    self.a17= False
    self.a18= False
    self.a19= False
    self.a20= False
    self.a21= False
    self.a22= False
    self.a23= False
    self.a24= False
    self.a25= False
   
    self.m01= 0
    self.m02= 0
    self.m03= 0
    self.m04= 0
    self.m05= 0
    self.m06= 0
    self.m07= 0
    self.m08= 0
    self.m09= 0
    self.m10= 0
    self.m11= 0
    self.m12= 0
    self.m13= 0
    self.m14= 0
    self.m15= 0
    self.m16= 0
    self.m17= 0
    self.m18= 0
    self.m19= 0
    self.m20= 0
    self.m21= 0
    self.m22= 0
    self.m23= 0
    self.m24= 0
    self.m25= 0
       
    self.f01= 0
    self.f02= 0
    self.f03= 0
    self.f04= 0
    self.f05= 0
    self.f06= 0
    self.f07= 0
    self.f08= 0
    self.f09= 0
    self.f10= 0
    self.f11= 0
    self.f12= 0
    self.f13= 0
    self.f14= 0
    self.f15= 0
    self.f16= 0
    self.f17= 0
    self.f18= 0
    self.f19= 0
    self.f20= 0
    self.f21= 0
    self.f22= 0
    self.f23= 0
    self.f24= 0
    self.f25= 0
       
    self.r01= 0
    self.r02= 90
    self.r03= 0
    self.r04= 90
    self.r05= 0
    self.r06= 90
    self.r07= 0
    self.r08= 90
    self.r09= 0
    self.r10= 90
    self.r11= 0
    self.r12= 90
    self.r13= 0
    self.r14= 90
    self.r15= 0
    self.r16= 90
    self.r17= 0
    self.r18= 90
    self.r19= 0
    self.r20= 90
    self.r21= 0
    self.r22= 90
    self.r23= 0
    self.r24= 90
    self.r25= 0
    
    self.h01 = '0'
    self.h02 = '0'
    self.h03 = '0'
    self.h04 = '0'
    self.h05 = '0'
    self.h06 = '0'
    self.h07 = '0'
    self.h08 = '0'
    self.h09 = '0'
    self.h10 = '0'
    self.h11 = '0'
    self.h12 = '0'
    self.h13 = '0'
    self.h14 = '0'
    self.h15 = '0'
    self.h16 = '0'
    self.h17 = '0'
    self.h18 = '0'
    self.h19 = '0'
    self.h20 = '0'
    self.h21 = '0'
    self.h22 = '0'
    self.h23 = '0'
    self.h24 = '0'
    self.h25 = '0'
       
    self.reset = '0';
#------------------------------------------------------------------
# Define UI class
# Rooms
#------------------------------------------------------------------
class ROOM(bpy.types.Operator):
    bl_idname = "mesh.archimesh_room"
    bl_label = "Room"
    bl_description = "Room Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    # reset function
    reset=bpy.props.EnumProperty(items = (('0',"Keep last values",""),('1',"Reset to Default","")),
                                name="",description="Reset all values to default parameters")

    # Define properties
    room_height= bpy.props.FloatProperty(name='Height',min=0.001,max= 50, default= 2.4,precision=3, description='Room height')
    wall_width= bpy.props.FloatProperty(name='Thickness',min=0.000,max= 10, default= 0.0,precision=3, description='Thickness of the walls')
    inverse = bpy.props.BoolProperty(name = "Inverse",description="Inverse normals to outside.",default = False)
    crt_mat = bpy.props.BoolProperty(name = "Create default Cycles materials",description="Create default materials for Cycles render.",default = True)

    wall_num= bpy.props.IntProperty(name='Number of Walls',min=1,max= 25, default= 1, description='Number total of walls in the room')
    
    baseboard = bpy.props.BoolProperty(name = "Create baseboard",description="Create a baseboard automatically.",default = True)
    base_width= bpy.props.FloatProperty(name='Width',min=0.001,max= 10, default= 0.015,precision=3, description='Baseboard width')
    base_height= bpy.props.FloatProperty(name='Height',min=0.05,max= 20, default= 0.12,precision=3, description='Baseboard height')
    
    ceiling = bpy.props.BoolProperty(name = "Ceiling",description="Create a ceiling.",default = False)
    floor = bpy.props.BoolProperty(name = "Floor",description="Create a floor automatically.",default = False)

    merge = bpy.props.BoolProperty(name = "Close walls",description="Close walls to create a full closed room.",default = False)
   
    w01= bpy.props.FloatProperty(name='Wall01 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w02= bpy.props.FloatProperty(name='Wall02 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w03= bpy.props.FloatProperty(name='Wall03 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w04= bpy.props.FloatProperty(name='Wall04 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w05= bpy.props.FloatProperty(name='Wall05 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w06= bpy.props.FloatProperty(name='Wall06 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w07= bpy.props.FloatProperty(name='Wall07 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w08= bpy.props.FloatProperty(name='Wall08 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w09= bpy.props.FloatProperty(name='Wall09 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w10= bpy.props.FloatProperty(name='Wall10 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w11= bpy.props.FloatProperty(name='Wall11 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w12= bpy.props.FloatProperty(name='Wall12 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w13= bpy.props.FloatProperty(name='Wall13 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w14= bpy.props.FloatProperty(name='Wall14 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w15= bpy.props.FloatProperty(name='Wall15 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w16= bpy.props.FloatProperty(name='Wall16 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w17= bpy.props.FloatProperty(name='Wall17 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w18= bpy.props.FloatProperty(name='Wall18 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w19= bpy.props.FloatProperty(name='Wall19 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w20= bpy.props.FloatProperty(name='Wall20 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w21= bpy.props.FloatProperty(name='Wall21 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w22= bpy.props.FloatProperty(name='Wall22 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w23= bpy.props.FloatProperty(name='Wall23 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w24= bpy.props.FloatProperty(name='Wall24 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    w25= bpy.props.FloatProperty(name='Wall25 size',min=-150,max= 150, default= 1,precision=3, description='Length of the wall (negative to reverse direction)')
    
    a01 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m01= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f01= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r01= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a02 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m02= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f02= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r02= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a03 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m03= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f03= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r03= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a04 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m04= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f04= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r04= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a05 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m05= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f05= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r05= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a06 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m06= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f06= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r06= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a07 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m07= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f07= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r07= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a08 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m08= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f08= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r08= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a09 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m09= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f09= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r09= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a10 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m10= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f10= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r10= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a11 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m11= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f11= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r11= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a12 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m12= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f12= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r12= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a13 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m13= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f13= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r13= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a14 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m14= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f14= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r14= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a15 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m15= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f15= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r15= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a16 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m16= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f16= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r16= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a17 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m17= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f17= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r17= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a18 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m18= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f18= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r18= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a19 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m19= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f19= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r19= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a20 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m20= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f20= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r20= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a21 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m21= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f21= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r21= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a22 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m22= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f22= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r22= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a23 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m23= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f23= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r23= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')
    
    a24 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m24= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f24= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r24= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 90,precision=1, description='Wall Angle (-180 to +180)')
    
    a25 = bpy.props.BoolProperty(name = "Advanced",description="Advance options.",default = False)
    m25= bpy.props.FloatProperty(name='',min=0,max= 50, default= 0,precision=3, description='Middle height variation')
    f25= bpy.props.FloatProperty(name='',min=-1,max= 1, default= 0,precision=3, description='Middle displacement')
    r25= bpy.props.FloatProperty(name='',min=-180,max= 180, default= 0,precision=1, description='Wall Angle (-180 to +180)')

    h01=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h02=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h03=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h04=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h05=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h06=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h07=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h08=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h09=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h10=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h11=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h12=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h13=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h14=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h15=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h16=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h17=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h18=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h19=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h20=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h21=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h22=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h23=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h24=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")
    h25=bpy.props.EnumProperty(items = (('0',"Visible",""),('1',"Baseboard",""),('2',"Wall",""),('3',"Hidden","")),
                                name="",description="Wall visibility")



    #-----------------------------------------------------
    # Draw (create UI interface)
    #-----------------------------------------------------
    def draw(self, context):
        layout = self.layout
        space = bpy.context.space_data
        if (not space.local_view):
            row=layout.row()
            row.prop(self,"reset")
            row=layout.row()
            row.prop(self,'room_height')
            row.prop(self,'wall_width')
            row.prop(self,'inverse')
        
            row=layout.row()
            row.prop(self,'ceiling')
            row.prop(self,'floor')
            row.prop(self,'merge')
                    
            box=layout.box()
            # Wall number
            box.prop(self,'wall_num')
            if (self.wall_num >= 1): add_wall(self,context,box,self.a01,'01')
            if (self.wall_num >= 2): add_wall(self,context,box,self.a02,'02')
            if (self.wall_num >= 3): add_wall(self,context,box,self.a03,'03')
            if (self.wall_num >= 4): add_wall(self,context,box,self.a04,'04')
            if (self.wall_num >= 5): add_wall(self,context,box,self.a05,'05')
            if (self.wall_num >= 6): add_wall(self,context,box,self.a06,'06')
            if (self.wall_num >= 7): add_wall(self,context,box,self.a07,'07')
            if (self.wall_num >= 8): add_wall(self,context,box,self.a08,'08')
            if (self.wall_num >= 9): add_wall(self,context,box,self.a09,'09')
            if (self.wall_num >= 10): add_wall(self,context,box,self.a10,'10')
            if (self.wall_num >= 11): add_wall(self,context,box,self.a11,'11')
            if (self.wall_num >= 12): add_wall(self,context,box,self.a12,'12')
            if (self.wall_num >= 13): add_wall(self,context,box,self.a13,'13')
            if (self.wall_num >= 14): add_wall(self,context,box,self.a14,'14')
            if (self.wall_num >= 15): add_wall(self,context,box,self.a15,'15')
            if (self.wall_num >= 16): add_wall(self,context,box,self.a16,'16')
            if (self.wall_num >= 17): add_wall(self,context,box,self.a17,'17')
            if (self.wall_num >= 18): add_wall(self,context,box,self.a18,'18')
            if (self.wall_num >= 19): add_wall(self,context,box,self.a19,'19')
            if (self.wall_num >= 20): add_wall(self,context,box,self.a20,'20')
            if (self.wall_num >= 21): add_wall(self,context,box,self.a21,'21')
            if (self.wall_num >= 22): add_wall(self,context,box,self.a22,'22')
            if (self.wall_num >= 23): add_wall(self,context,box,self.a23,'23')
            if (self.wall_num >= 24): add_wall(self,context,box,self.a24,'24')
            if (self.wall_num >= 25): add_wall(self,context,box,self.a25,'25')
            
            
            box=layout.box()
            box.prop(self,'baseboard')
            if (self.baseboard==True):
                row = box.row()
                row.prop(self,'base_width')
                row.prop(self,'base_height')
    
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
            if (self.reset == '1'):
                reset_room(self)
            
            
            create_room_mesh(self,context)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Archimesh: Option only valid in Object mode")
            return {'CANCELLED'}

#-----------------------------------------------------
# Add wall parameters
#-----------------------------------------------------
def add_wall(self,context,box,var,num):
    row = box.row()
    row.prop(self,'w' + num)
    row.prop(self,'a' + num)
    if (var == True):
        srow = row.row()
        srow.prop(self,'r' + num)
        srow.prop(self,'h' + num)
        srow.prop(self,'m' + num)
        srow.prop(self,'f' + num)
 


#------------------------------------------------------------------------------
# Generate mesh data
# All custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def create_room_mesh(self,context):
    # deactivate others
    for o in bpy.data.objects:
        if (o.select == True):
            o.select = False
    bpy.ops.object.select_all(False)
    # Create room
    myRoom = create_room(self,context,"Room",get_BlendUnits(self.room_height))
    myRoom.select = True
    bpy.context.scene.objects.active = myRoom
    # Mark Seams
    select_vertices(myRoom,[0,1])   
    mark_seam(myRoom) 
    # Unwrap
    unwrap_mesh(myRoom)
    
    remove_doubles(myRoom)
    set_normals(myRoom,not self.inverse) # inside/outside

    if (self.wall_width > 0.0):
        set_modifier_solidify(myRoom,get_BlendUnits(self.wall_width))
        
    # Create baseboard
    if (self.baseboard):
        myBase = create_room(self,context,"Baseboard",get_BlendUnits(self.base_height),True)
        set_normals(myBase,self.inverse) # inside/outside room
        if (self.base_width > 0.0):
            set_modifier_solidify(myBase,get_BlendUnits(self.base_width))
        myBase.parent = myRoom    
        # Mark Seams
        select_vertices(myBase,[0,1])   
        mark_seam(myBase) 
        # Unwrap
        unwrap_mesh(myBase)
        
    # Create floor
    if (self.floor):
        myFloor = create_floor(self,context,"Floor",myRoom)
        myFloor.parent = myRoom    
        # Unwrap
        unwrap_mesh(myFloor)

    # Create ceiling
    if (self.ceiling):
        myCeiling = create_floor(self,context,"Ceiling",myRoom)
        myCeiling.parent = myRoom    
        # Unwrap
        unwrap_mesh(myCeiling)

    # Create materials        
    if (self.crt_mat):
        # Wall material (two faces)
        mat = create_diffuse_material("Wall_material",False,0.765, 0.650, 0.588,0.8,0.621,0.570,0.1,True)
        set_material(myRoom,mat)
        # Baseboard material
        if (self.baseboard):
            mat = create_diffuse_material("Baseboard_material",False,0.8, 0.8, 0.8)
            set_material(myBase,mat)
        
        # Ceiling material
        if (self.ceiling):
            mat = create_diffuse_material("Ceiling_material",False,0.95, 0.95, 0.95)
            set_material(myCeiling,mat)
            
        # Floor material    
        if (self.floor):
            mat = create_brick_material("Floor_material",False,0.711, 0.668, 0.668,0.8,0.636,0.315)
            set_material(myFloor,mat)
          
    bpy.ops.object.select_all(False)    
    myRoom.select = True
    bpy.context.scene.objects.active = myRoom
            
    return
#------------------------------------------------------------------------------
# Verify visibility of walls
#------------------------------------------------------------------------------
def check_visibility(h,base):
    # Visible
    if (h == '0'):
        return True
    # Wall
    if (h == '2'):
        if (base == True):
            return False
        else:
            return True
    # Baseboard
    if (h == '1'):
        if (base == True):
            return True
        else:
            return False
    # Hidden
    if (h == '3'):
        return False

#------------------------------------------------------------------------------
# Create Room/baseboard
# Some custom values are passed using self container (self.myvariable)
#------------------------------------------------------------------------------
def create_room(self,context,objName,height,baseboard = False):

    myVertex = []
    myFaces = []
    lastFace = 0
    #---------------------------------
    # Horizontal (First)
    #---------------------------------
    if (self.wall_num >= 1):
        # Calculate size using angle
        sizeX = math.cos(math.radians(self.r01)) * get_BlendUnits(self.w01)
        sizeY = math.sin(math.radians(self.r01)) * get_BlendUnits(self.w01)

        if (self.a01 == False or baseboard == True):
            myVertex.extend([(0.0,0.0,0.0),(0.0,0.0,height)
                             ,(sizeX,sizeY,height)
                             ,(sizeX,sizeY,0.0)])
            if (check_visibility(self.h01,baseboard)):
                myFaces.extend([(0,1,2,3)])
            lastFace = 2
            lastX = sizeX
            lastY = sizeY
        else:
            mid = get_BlendUnits(self.w01 / 2 + ((self.w01 / 2) * self.f01))
            midX = math.cos(math.radians(self.r01)) * mid
            midY = math.sin(math.radians(self.r01)) * mid
            
            # first
            myVertex.extend([(0.0,0.0,0.0)
                             ,(0.0,0.0,height)
                             ,(midX,midY,height + get_BlendUnits(self.m01))
                             ,(midX,midY,0.0)])
            if (math.fabs(self.f01) != 1):
                if (check_visibility(self.h01,baseboard)):
                    myFaces.extend([(0,1,2,3)])  
            # second
            myVertex.extend([(sizeX,sizeY,0.0),(sizeX,sizeY,height)])
            if (check_visibility(self.h01,baseboard)):
                if (math.fabs(self.f01) != 1): 
                    myFaces.extend([(2,3,4,5)])
                else:    
                    myFaces.extend([(0,1,5,4),(1,2,5)])
            
            lastFace = 4
                
            lastX = sizeX
            lastY = sizeY
        
    #---------------------------------
    # Vertical
    #---------------------------------
    if (self.wall_num >= 2):
        myDat = make_wall(self.a01,
                              self.a02,self.w02,self.m02,self.f02
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r02,self.h02)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Horizontal
    if (self.wall_num >= 3):
        myDat = make_wall(self.a02,
                              self.a03,self.w03,self.m03,self.f03
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r03,self.h03)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 4):
        myDat = make_wall(self.a03,
                              self.a04,self.w04,self.m04,self.f04
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r04,self.h04)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Horizontal
    if (self.wall_num >= 5):
        myDat = make_wall(self.a04,
                              self.a05,self.w05,self.m05,self.f05
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r05,self.h05)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 6):
        myDat = make_wall(self.a05,
                              self.a06,self.w06,self.m06,self.f06
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r06,self.h06)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 7):
        myDat = make_wall(self.a06,
                              self.a07,self.w07,self.m07,self.f07
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r07,self.h07)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 8):
        myDat = make_wall(self.a07,
                              self.a08,self.w08,self.m08,self.f08
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r08,self.h08)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 9):
        myDat = make_wall(self.a08,
                              self.a09,self.w09,self.m09,self.f09
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r09,self.h09)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 10):
        myDat = make_wall(self.a09,
                              self.a10,self.w10,self.m10,self.f10
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r10,self.h10)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 11):
        myDat = make_wall(self.a10,
                              self.a11,self.w11,self.m11,self.f11
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r11,self.h11)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 12):
        myDat = make_wall(self.a11,
                              self.a12,self.w12,self.m12,self.f12
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r12,self.h12)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 13):
        myDat = make_wall(self.a12,
                              self.a13,self.w13,self.m13,self.f13
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r13,self.h13)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 14):
        myDat = make_wall(self.a13,
                              self.a14,self.w14,self.m14,self.f14
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r14,self.h14)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 15):
        myDat = make_wall(self.a14,
                              self.a15,self.w15,self.m15,self.f15
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r15,self.h15)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 16):
        myDat = make_wall(self.a15,
                              self.a16,self.w16,self.m16,self.f16
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r16,self.h16)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 17):
        myDat = make_wall(self.a16,
                              self.a17,self.w17,self.m17,self.f17
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r17,self.h17)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Vertical
    if (self.wall_num >= 18):
        myDat = make_wall(self.a17,
                              self.a18,self.w18,self.m18,self.f18
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r18,self.h18)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 19):
        myDat = make_wall(self.a18,
                              self.a19,self.w19,self.m19,self.f19
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r19,self.h19)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Vertical
    if (self.wall_num >= 20):
        myDat = make_wall(self.a19,
                              self.a20,self.w20,self.m20,self.f20
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r20,self.h20)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 21):
        myDat = make_wall(self.a20,
                              self.a21,self.w21,self.m21,self.f21
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r21,self.h21)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Vertical
    if (self.wall_num >= 22):
        myDat = make_wall(self.a21,
                              self.a22,self.w22,self.m22,self.f22
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r22,self.h22)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 23):
        myDat = make_wall(self.a22,
                              self.a23,self.w23,self.m23,self.f23
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r23,self.h23)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Vertical
    if (self.wall_num >= 24):
        myDat = make_wall(self.a23,
                              self.a24,self.w24,self.m24,self.f24
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r24,self.h24)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]

    # Horizontal
    if (self.wall_num >= 25):
        myDat = make_wall(self.a24,
                              self.a25,self.w25,self.m25,self.f25
                              ,baseboard,lastFace
                              ,lastX,lastY,height,myVertex,myFaces,self.r25,self.h25)
        lastX = myDat[0]
        lastY = myDat[1]
        lastFace = myDat[2]
        
    # Close room
    if (self.merge == True):
        if (baseboard == False):     
            if ((self.wall_num == 1 and self.a01 == True)
            or (self.wall_num == 2 and self.a02 == True)
            or (self.wall_num == 3 and self.a03 == True)
            or (self.wall_num == 4 and self.a04 == True)
            or (self.wall_num == 5 and self.a05 == True)
            or (self.wall_num == 6 and self.a06 == True)
            or (self.wall_num == 7 and self.a07 == True)
            or (self.wall_num == 8 and self.a08 == True)
            or (self.wall_num == 9 and self.a09 == True)
            or (self.wall_num == 10 and self.a10 == True)
            or (self.wall_num == 11 and self.a11 == True)
            or (self.wall_num == 12 and self.a12 == True)
            or (self.wall_num == 13 and self.a13 == True)
            or (self.wall_num == 14 and self.a14 == True)
            or (self.wall_num == 15 and self.a15 == True)
            or (self.wall_num == 16 and self.a16 == True)
            or (self.wall_num == 17 and self.a17 == True)
            or (self.wall_num == 18 and self.a18 == True)
            or (self.wall_num == 19 and self.a19 == True)
            or (self.wall_num == 20 and self.a20 == True)
            or (self.wall_num == 21 and self.a21 == True)
            or (self.wall_num == 22 and self.a22 == True)
            or (self.wall_num == 23 and self.a23 == True)
            or (self.wall_num == 24 and self.a24 == True)
            or (self.wall_num == 25 and self.a25 == True)):
                myFaces.extend([(0,1,lastFace + 1, lastFace)])
            else:   
                myFaces.extend([(0,1,lastFace, lastFace + 1)])
        else:
            myFaces.extend([(0,1,self.wall_num * 2, self.wall_num * 2 + 1)])   
        
        
    mymesh = bpy.data.meshes.new(objName)
    myobject = bpy.data.objects.new(objName, mymesh)
    
    if (baseboard == False):
        myobject.location = bpy.context.scene.cursor_location
    else:
        myobject.location = (0,0,0)
        
    bpy.context.scene.objects.link(myobject)
    
    mymesh.from_pydata(myVertex, [], myFaces)
    mymesh.update(calc_edges=True)
    
    return myobject
#------------------------------------------------------------------------------
# Make a Wall
#------------------------------------------------------------------------------
def make_wall(prv,advance,size,over,factor,baseboard,lastFace,lastX,lastY,height,myVertex,myFaces,angle,hide):
    
    # if angle negative, calculate real
    # use add because the angle is negative 
    if (angle < 0):
        angle = 360 + angle
    # Verify Units    
    size = get_BlendUnits(size)
    over = get_BlendUnits(over)
    
    # Calculate size using angle
    sizeX = math.cos(math.radians(angle)) * size
    sizeY = math.sin(math.radians(angle)) * size
    
    # Create faces
    if (advance == False or baseboard == True):
        myVertex.extend([(lastX + sizeX,lastY + sizeY,height)
                         ,(lastX + sizeX,lastY + sizeY,0.0)])
        if (check_visibility(hide,baseboard)):
            if (prv == False or baseboard == True):
                myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
            else:
                myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
            
        lastFace = lastFace + 2
    else:
        mid = size / 2 + ((size / 2) * factor)
        midX = math.cos(math.radians(angle)) * mid
        midY = math.sin(math.radians(angle)) * mid
        # first
        myVertex.extend([(lastX + midX,lastY + midY,height + over)
                         ,(lastX + midX,lastY + midY,0.0)])
        if (check_visibility(hide,baseboard)):
            if (math.fabs(factor) != 1):
                if (prv == False):
                    myFaces.extend([(lastFace,lastFace + 2,lastFace + 3,lastFace + 1)]) # no advance
                else:
                    myFaces.extend([(lastFace,lastFace + 1,lastFace + 2,lastFace + 3)]) # advance
        # second
        myVertex.extend([(lastX + sizeX,lastY + sizeY,0.0)
                         ,(lastX + sizeX,lastY + sizeY,height)])
        if (check_visibility(hide,baseboard)):
            if (math.fabs(factor) != 1): 
                myFaces.extend([(lastFace + 2,lastFace + 3,lastFace + 4,lastFace+ 5)])
            else:   
                if (prv == False):
                    myFaces.extend([(lastFace, lastFace + 5, lastFace + 4, lastFace + 1)
                                   ,(lastFace, lastFace + 2, lastFace + 5)])
                else:
                    myFaces.extend([(lastFace, lastFace + 4, lastFace + 5, lastFace + 1)
                               ,(lastFace + 1, lastFace + 2, lastFace + 5)])
            
        lastFace = lastFace + 4
        
    lastX = lastX + sizeX
    lastY = lastY + sizeY
    
        
    return (lastX,lastY,lastFace)

#------------------------------------------------------------------------------
# Create Floor or Ceiling
#------------------------------------------------------------------------------
def create_floor(self,context,typ,myRoom):
    bpy.context.scene.objects.active = myRoom

    myVertex = []
    myFaces = []
    verts = []
    
    obverts = bpy.context.active_object.data.vertices
    for vertex in obverts:
        verts.append(tuple(vertex.co))
    # Loop only selected
    i = 0 
    for e in verts:
        if (typ == "Floor"):
            if(e[2] == 0.0):
                myVertex.extend([(e[0],e[1],e[2])])
                i = i + 1    
        else: # ceiling
            if(round(e[2],5) == round(get_BlendUnits(self.room_height),5)):
                myVertex.extend([(e[0],e[1],e[2])])    
                i = i + 1
    
    # Create faces
    fa = []
    for f in range(0,i):
        fa.extend([f])
                        
    myFaces.extend([fa])
        
        
    mymesh = bpy.data.meshes.new(typ)
    myobject = bpy.data.objects.new(typ, mymesh)
    
    myobject.location = (0,0,0)
    bpy.context.scene.objects.link(myobject)
    
    mymesh.from_pydata(myVertex, [], myFaces)
    mymesh.update(calc_edges=True)
    
    return myobject

#----------------------------------------------
# Code to run alone the script
#----------------------------------------------
if __name__ == "__main__":
    create_mesh(0)
    print("Executed")
