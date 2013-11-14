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

bl_info = {
    "name": "Turnaround camera around object",
    "author": "Antonio Vazquez (antonioya)",
    "version": (0, 2, 1),
    "blender": (2, 68, 0),
    "location": "View3D > Toolshelf > Turnaround camera",
    "description": "Add a camera rotation around selected object.",
    "category": "3D View"}


import bpy
import math
#------------------------------------------------------
# Action class
#------------------------------------------------------
class RunAction(bpy.types.Operator):
    bl_idname = "object.rotate_around"
    bl_label = "Turnaround"
    bl_description = "Create camera rotation around selected object"

    #------------------------------
    # Execute
    #------------------------------
    def execute(self, context):
        #----------------------
        # Save old data       
        #----------------------
        scene = context.scene
        selectObject = context.active_object
        camera = bpy.data.objects[bpy.context.scene.camera.name]
        savedCursor = bpy.context.scene.cursor_location.copy() # cursor position
        savedFrame = scene.frame_current
        if (scene.use_cursor == False):
            bpy.ops.view3d.snap_cursor_to_selected()
        
        #-------------------------
        # Create empty and parent
        #-------------------------
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        myEmpty = bpy.data.objects[bpy.context.active_object.name]

        myEmpty.location = selectObject.location
        savedState = myEmpty.matrix_world
        myEmpty.parent = selectObject
        myEmpty.name = 'MCH_Rotation_target'
        myEmpty.matrix_world = savedState

        #-------------------------
        # Parent camera to empty
        #-------------------------
        savedState = camera.matrix_world
        camera.parent = myEmpty
        camera.matrix_world = savedState
        
        #-------------------------
        # Now add revolutions 
        # (make empty active object)
        #-------------------------
        bpy.ops.object.select_all(False)
        myEmpty.select = True
        bpy.context.scene.objects.active = myEmpty
        # save current configuration     
        savedInterpolation = context.user_preferences.edit.keyframe_new_interpolation_type
        # change interpolation mode
        context.user_preferences.edit.keyframe_new_interpolation_type ='LINEAR'
        # create first frame
        myEmpty.rotation_euler = (0,0,0)
        myEmpty.empty_draw_size = 0.1
        bpy.context.scene.frame_set(scene.frame_start)
        myEmpty.keyframe_insert(data_path='rotation_euler', frame=(scene.frame_start))
        # Dolly zoom
        if (scene.dolly_zoom  != "0"):
            bpy.data.cameras[camera.name].lens=scene.camera_from_lens
            bpy.data.cameras[camera.name].keyframe_insert('lens',frame=(scene.frame_start))
        
        
        # Calculate rotation XYZ
        if (scene.inverse_x):
            iX = -1
        else:
            iX = 1    

        if (scene.inverse_y):
            iY = -1
        else:
            iY = 1    

        if (scene.inverse_z):
            iZ = -1
        else:
            iZ = 1    
        
        xRot = (math.pi * 2) * scene.camera_revol_x * iX
        yRot = (math.pi * 2) * scene.camera_revol_y * iY
        zRot = (math.pi * 2) * scene.camera_revol_z * iZ

        # create middle frame
        if (scene.back_forw == True):
            myEmpty.rotation_euler = (xRot,yRot,zRot)
            myEmpty.keyframe_insert(data_path='rotation_euler', frame=((scene.frame_end - scene.frame_start) / 2))
            # reverse
            xRot = xRot * -1
            yRot = yRot * -1
            zRot = 0
            
        # Dolly zoom
        if (scene.dolly_zoom  == "2"):
            bpy.data.cameras[camera.name].lens=scene.camera_to_lens
            bpy.data.cameras[camera.name].keyframe_insert('lens',frame=((scene.frame_end - scene.frame_start) / 2))
            
        
        # create last frame
        myEmpty.rotation_euler = (xRot,yRot,zRot)
        myEmpty.keyframe_insert(data_path='rotation_euler', frame=(scene.frame_end))
        # Dolly zoom
        if (scene.dolly_zoom  != "0"):
            if (scene.dolly_zoom  == "1"):
                bpy.data.cameras[camera.name].lens=scene.camera_to_lens # final
            else:
                bpy.data.cameras[camera.name].lens=scene.camera_from_lens # back to init
                
            bpy.data.cameras[camera.name].keyframe_insert('lens',frame=scene.frame_end)
        bpy.context.scene.objects.active = camera
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints[-1].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints[-1].up_axis = 'UP_Y'
        bpy.context.object.constraints[-1].target = bpy.data.objects[myEmpty.name]


        
        # back previous configuration
        context.user_preferences.edit.keyframe_new_interpolation_type = savedInterpolation    
        bpy.context.scene.cursor_location = savedCursor      
        
        #-------------------------
        # Back to old selection
        #-------------------------
        bpy.ops.object.select_all(False)
        selectObject.select = True
        bpy.context.scene.objects.active = selectObject
        bpy.context.scene.frame_set(savedFrame)
        
        return {'FINISHED'}
#------------------------------------------------------
# UI Class
#------------------------------------------------------
class PanelUI(bpy.types.Panel):
    bl_label = "Turnaround Camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #------------------------------
    # Draw UI
    #------------------------------
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        if (context.active_object is not None):
            if (context.active_object.type != 'CAMERA'):
                buf = context.active_object.name
                row = layout.row(align=False)
                row.operator("object.rotate_around", icon='OUTLINER_DATA_CAMERA')
                row.label(buf, icon='MESH_DATA')
                row = layout.row()
                row.prop(scene,"use_cursor")
                row = layout.row(align=False)
                row.prop(scene, "camera")
                row = layout.row()
                row.prop(scene, "frame_start")
                row.prop(scene, "frame_end")
                row = layout.row()
                row.prop(scene,"camera_revol_x")
                row.prop(scene,"camera_revol_y")
                row.prop(scene,"camera_revol_z")
                row = layout.row()
                row.prop(scene,"inverse_x")
                row.prop(scene,"inverse_y")
                row.prop(scene,"inverse_z")
                row = layout.row()
                row.prop(scene,"back_forw")
                row = layout.row()
                row.prop(scene,"dolly_zoom")
                if (scene.dolly_zoom != "0"):
                    row = layout.row()
                    row.prop(scene,"camera_from_lens")
                    row.prop(scene,"camera_to_lens")
                    
            else:
                buf = "No valid object selected"
                layout.label(buf, icon='MESH_DATA')
                
        
#------------------------------------------------------
# Registration
#------------------------------------------------------
def register():
    bpy.utils.register_class(RunAction)
    bpy.utils.register_class(PanelUI)
    # Define properties
    bpy.types.Scene.camera_revol_x = bpy.props.FloatProperty(name='X',min=0,max= 25
                                                  ,default= 0,precision=2
                                                  ,description='Number total of revolutions in X axis')
    bpy.types.Scene.camera_revol_y = bpy.props.FloatProperty(name='Y',min=0,max= 25
                                                  ,default= 0,precision=2
                                                  ,description='Number total of revolutions in Y axis')
    bpy.types.Scene.camera_revol_z = bpy.props.FloatProperty(name='Z',min=0,max= 25
                                                  ,default= 1,precision=2
                                                  ,description='Number total of revolutions in Z axis')
    
    bpy.types.Scene.inverse_x = bpy.props.BoolProperty(name = "-X",description="Inverse rotation",default = False)
    bpy.types.Scene.inverse_y = bpy.props.BoolProperty(name = "-Y",description="Inverse rotation",default = False)
    bpy.types.Scene.inverse_z = bpy.props.BoolProperty(name = "-Z",description="Inverse rotation",default = False)
    bpy.types.Scene.use_cursor = bpy.props.BoolProperty(name = "Use cursor position",description="Use cursor position instead of object origin",default = False)
    bpy.types.Scene.back_forw = bpy.props.BoolProperty(name = "Back and forward",description="Create back and forward animation",default = False)

    bpy.types.Scene.dolly_zoom = bpy.props.EnumProperty(items = (('0',"None",""),('1',"Dolly zoom",""),('2',"Dolly zoom B/F","")),
                                name="Lens Effects",description="Create a camera lens movement")


    
    bpy.types.Scene.camera_from_lens = bpy.props.FloatProperty(name='From',min=1,max= 500,default= 35,precision=3
                                                  ,description='Start lens value')
    bpy.types.Scene.camera_to_lens = bpy.props.FloatProperty(name='To',min=1,max= 500,default= 35,precision=3
                                                  ,description='End lens value')
    

def unregister():
    bpy.utils.unregister_class(RunAction)
    bpy.utils.unregister_class(PanelUI)

    del bpy.types.Scene.camera_revol_x
    del bpy.types.Scene.camera_revol_y
    del bpy.types.Scene.camera_revol_z
    del bpy.types.Scene.inverse_x
    del bpy.types.Scene.inverse_y
    del bpy.types.Scene.inverse_z
    del bpy.types.Scene.use_cursor
    del bpy.types.Scene.back_forw
    del bpy.types.Scene.dolly_zoom
    del bpy.types.Scene.camera_from_lens
    del bpy.types.Scene.camera_to_lens

if __name__ == "__main__":
    register()
