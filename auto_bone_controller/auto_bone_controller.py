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
    "name": "Auto Bone Controller",
    "author": "Antonio Vazquez (antonioya)",
    "version": (1, 0, 12),
    "blender": (2, 7, 8),
    "location": "View3D > Properties",
    "description": "Add controllers for bendy bones automatically",
    "category": "3D View"}

# noinspection PyUnresolvedReferences
import bpy
# noinspection PyUnresolvedReferences
from mathutils import Vector


# ------------------------------------------------------
# Load combox objects
# ------------------------------------------------------
# noinspection PyUnusedLocal
def combobox_object_callback(scene, context):
    items = []
    i = 0
    i += 1
    items.append(("*NONE", "", "No custom shape", "OBJECT", i))
    for obj in context.scene.objects:
        if obj.type in ('MESH', 'EMPTY'):
            i += 1
            items.append((obj.name, obj.name, "Select this object", "OBJECT", i))

    return items


# --------------------------------------------------------------------
# Parent armature (keep positions)
# --------------------------------------------------------------------
def parent_armature(armature, parentobj, childobj):
    for mybone in armature.edit_bones:
        mybone.select = False

    parent = armature.edit_bones[parentobj]
    child = armature.edit_bones[childobj]
    armature.edit_bones.active = parent

    parent.select = True
    child.select = True
    bpy.ops.armature.parent_set(type='OFFSET')


# ------------------------------------------------------
# Action class
# ------------------------------------------------------
class RunAction(bpy.types.Operator):
    bl_idname = "bone.add_controller"
    bl_label = "Add"
    bl_description = "Create bone controllers"

    @classmethod
    def poll(cls, context):
        if context.active_bone is None:
            return False

        return True

    # ------------------------------
    # Create bone groups (POSE mode)
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def create_bone_groups(self, amt):
        bpy.ops.object.mode_set(mode='POSE')
        if 'Grp_In' in bpy.data.objects[amt.name].pose.bone_groups:
            grp_in = bpy.data.objects[amt.name].pose.bone_groups['Grp_In']
        else:
            grp_in = bpy.data.objects[amt.name].pose.bone_groups.new("Grp_In")
            grp_in.color_set = 'THEME03'  # Green

        if 'Grp_Out' in bpy.data.objects[amt.name].pose.bone_groups:
            grp_out = bpy.data.objects[amt.name].pose.bone_groups['Grp_Out']
        else:
            grp_out = bpy.data.objects[amt.name].pose.bone_groups.new("Grp_Out")
            grp_out.color_set = 'THEME01'  # Red

        bpy.ops.object.mode_set(mode='EDIT')

        return grp_in, grp_out

    # ------------------------------
    # Set bone groups
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_bone_group(self, amt, bone_name, grp):
        bpy.data.objects[amt.name].pose.bones[bone_name].bone_group = grp

    # ------------------------------
    # Create bone controllers
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def create_controllers(self, amt, main_bone, txt_a, txt_b, size_a, size_b, bx, bz, roll):
        main_name = main_bone.name
        tail = main_bone.tail
        head = main_bone.head

        v1 = Vector((head[0] - tail[0], head[1] - tail[1], head[2] - tail[2],))
        v1.normalize()

        # create controller A
        bone_a = amt.edit_bones.new(main_name + txt_a)
        bone_a.tail = head
        bone_a.head = (head[0] + (v1[0] * size_a), head[1] + (v1[1] * size_a), head[2] + (v1[2] * size_a))
        bone_a.bbone_x = bx * 1.15
        bone_a.bbone_z = bz * 1.15
        bone_a.roll = roll

        # create controller B
        bone_b = amt.edit_bones.new(main_name + txt_b)
        bone_b.head = tail
        bone_b.tail = (tail[0] + (v1[0] * -size_b), tail[1] + (v1[1] * -size_b), tail[2] + (v1[2] * -size_b))
        bone_b.bbone_x = bx * 1.20
        bone_b.bbone_z = bz * 1.20
        bone_b.roll = roll

    # ------------------------------
    # Set custom shapes and segments
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_custom_shapes(self, context, ob, main_bone, main_name, txt_a, txt_b):
        scene = context.scene
        # increase segments and set properties
        if type(main_bone).__name__ != "EditBone":
            bpy.ops.object.mode_set(mode='EDIT')

        bpy.data.objects[ob.name].data.edit_bones[main_bone.name].bbone_segments = scene.auto_bone_subdivisions

        # need set as object mode
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        b = ob.pose.bones[main_name]
        b.use_bbone_custom_handles = True
        b.bbone_custom_handle_start = bpy.data.objects[ob.name].pose.bones[main_name + txt_a]
        b.bbone_custom_handle_end = bpy.data.objects[ob.name].pose.bones[main_name + txt_b]

    # ------------------------------
    # Set lock and deform
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_lock_and_deform(self, context, main_name, ob, txt_a, txt_b):
        scene = context.scene
        bpy.ops.object.mode_set(mode='POSE')
        ma = bpy.data.objects[ob.name].pose.bones[main_name]
        # lock rot and scale
        ma.lock_rotation[0] = True
        ma.lock_rotation[1] = True
        ma.lock_rotation[2] = True
        if ma.rotation_mode == 'QUATERNION':
            ma.lock_rotation_w = True

        ma.lock_location[0] = True
        ma.lock_location[1] = True
        ma.lock_location[2] = True

        ba = bpy.data.objects[ob.name].pose.bones[main_name + txt_a]
        bb = bpy.data.objects[ob.name].pose.bones[main_name + txt_b]
        # disable deform
        ob.data.bones[main_name + txt_a].use_deform = False
        ob.data.bones[main_name + txt_b].use_deform = False

        if scene.auto_bone_list_a != "*NONE":
            ba.custom_shape = bpy.data.objects[scene.auto_bone_list_a]
            ba.custom_shape_scale = scene.auto_bone_scale_a

        if scene.auto_bone_list_b != "*NONE":
            bb.custom_shape = bpy.data.objects[scene.auto_bone_list_b]
            bb.custom_shape_scale = scene.auto_bone_scale_b

    # ------------------------------
    # Set constraintlock and deform
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_constraint(self, context, main_name, ob, txt_b):
        # flush modes to force recalc
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='POSE')
        bpy.data.objects[ob.name].data.bones.active = bpy.data.objects[ob.name].pose.bones[main_name].bone
        # constraint
        bpy.ops.pose.constraint_add(type='STRETCH_TO')
        bpy.data.objects[ob.name].pose.bones[main_name].constraints[0].target = ob  # "Stretch To"
        context.object.pose.bones[main_name].constraints[0].subtarget = main_name + txt_b

    # ------------------------------
    # Set bone controllers
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def set_bone(self, context, ob, amt, main_bone, size_a, txt_a, size_b, txt_b):
        scene = context.scene
        oldmode = ob.mode

        if oldmode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        main_name = main_bone.name
        # save main bone parent
        if bpy.data.armatures[amt.name].edit_bones[main_name].parent is not None:
            main_parent = bpy.data.armatures[amt.name].edit_bones[main_name].parent.name
        else:
            main_parent = ""
        # get roll
        roll = bpy.data.armatures[amt.name].edit_bones[main_name].roll

        # get scale
        bx = bpy.data.armatures[amt.name].edit_bones[main_name].bbone_x
        bz = bpy.data.armatures[amt.name].edit_bones[main_name].bbone_z
        # create groups
        if scene.auto_bone_color is True:
            grp_in, grp_out = self.create_bone_groups(amt)

        # create controllers
        self.create_controllers(amt, main_bone, txt_a, txt_b, size_a, size_b, bx, bz, roll)

        # increase segments and set properties
        self.set_custom_shapes(context, ob, main_bone, main_name, txt_a, txt_b)

        # set lock and deform
        self.set_lock_and_deform(context, main_name, ob, txt_a, txt_b)

        # set constraint
        self.set_constraint(context, main_name, ob, txt_b)

        # back to edit mode (need a flush)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        # parent bone with controller A
        parent_armature(amt, main_name + txt_a, main_name)

        # if original bone was parented, parent controllers
        if main_parent != "":
            parent_armature(amt, main_parent, main_name + txt_a)
            parent_armature(amt, main_parent, main_name + txt_b)

        # set bone groups
        if scene.auto_bone_color is True:
            # noinspection PyUnboundLocalVariable
            self.set_bone_group(amt, main_name + txt_a, grp_in)
            # noinspection PyUnboundLocalVariable
            self.set_bone_group(amt, main_name + txt_b, grp_out)

        # back to original mode
        bpy.ops.object.mode_set(mode=oldmode)

        return {'FINISHED'}

    # ------------------------------
    # Execute
    # ------------------------------
    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        scene = context.scene
        size_a = scene.auto_bone_size_a
        txt_a = scene.auto_bone_txt_a
        size_b = scene.auto_bone_size_b
        txt_b = scene.auto_bone_txt_b

        ob = context.object
        # retry armature
        amt = ob.data
        # save the list of selected bones because the selection is missing when parent
        selbones = []
        if context.mode == "EDIT_ARMATURE":
            for bone in context.selected_bones:
                selbones.extend([bone])

        if context.mode == 'POSE':
            for bone in context.selected_pose_bones:
                selbones.extend([bone])

        # Loop
        for main_bone in selbones:
            self.set_bone(context, ob, amt, main_bone, size_a, txt_a, size_b, txt_b)

        return {'FINISHED'}


# ------------------------------------------------------
# UI Class
# ------------------------------------------------------
class PanelUI(bpy.types.Panel):
    bl_label = "Auto Bone Controller"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        o = context.object
        if o:
            if o.mode == "EDIT":
                if o.type == "ARMATURE":
                    return True

        return False

    # ------------------------------
    # Draw UI
    # ------------------------------
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        o = context.object
        row = layout.row(align=False)
        row.operator("bone.add_controller", icon='GROUP_BONE')
        row = layout.row(align=False)
        row.prop(scene, "auto_bone_subdivisions", text="Bone Segments")

        row = layout.row()
        box = row.box()
        box.label("Controller A")
        box.prop(scene, "auto_bone_txt_a", text="Subfix")
        box.prop(scene, "auto_bone_size_a", text="Size")
        box.prop(scene, "auto_bone_list_a", text="Shape")
        box.prop(scene, "auto_bone_scale_a", text="Scale")

        row = layout.row()
        box = row.box()
        box.label("Controller B")
        box.prop(scene, "auto_bone_txt_b", text="Subfix")
        box.prop(scene, "auto_bone_size_b", text="Size")
        box.prop(scene, "auto_bone_list_b", text="Shape")
        box.prop(scene, "auto_bone_scale_b", text="Scale")

        row = layout.row(align=False)
        row.prop(scene, "auto_bone_color", text="Use color for controllers")

        amt = context.object.data
        if o.mode == "EDIT":
            active_bone = amt.edit_bones.active
        elif o.mode == "POSE":
            active_bone = context.active_bone
        else:
            active_bone = None

        if active_bone:
            row = layout.row(align=False)
            row.label("Active Bone: " + active_bone.name)

            if active_bone.name.endswith("_In") or active_bone.name.endswith("_Out"):
                row = layout.row(align=False)
                row.label("Selected bone looks a bone controller", icon="ERROR")


# ------------------------------------------------------
# Registration
# ------------------------------------------------------
def register():
    bpy.utils.register_class(RunAction)
    bpy.utils.register_class(PanelUI)
    # Define properties
    bpy.types.Scene.auto_bone_subdivisions = bpy.props.IntProperty(name='Div', min=1, max=25,
                                                                   default=10,
                                                                   description='Number total of subdivisions')

    bpy.types.Scene.auto_bone_txt_a = bpy.props.StringProperty(name="Subfix", maxlen=48,
                                                               description="Subfix added to first controler bone",
                                                               default="_In")
    bpy.types.Scene.auto_bone_txt_b = bpy.props.StringProperty(name="Subfix", maxlen=48,
                                                               description="Subfix added to second controler bone",
                                                               default="_Out")

    bpy.types.Scene.auto_bone_size_a = bpy.props.FloatProperty(name='Size', min=0, max=100, default=0.2,
                                                               precision=3,
                                                               description="Controller size factor")
    bpy.types.Scene.auto_bone_size_b = bpy.props.FloatProperty(name='Size', min=0, max=100, default=0.5,
                                                               precision=3,
                                                               description="Controller size factor")

    bpy.types.Scene.auto_bone_list_a = bpy.props.EnumProperty(items=combobox_object_callback,
                                                              name="Object",
                                                              description="List of available objects")

    bpy.types.Scene.auto_bone_list_b = bpy.props.EnumProperty(items=combobox_object_callback,
                                                              name="Object",
                                                              description="List of available objects")
    bpy.types.Scene.auto_bone_scale_a = bpy.props.FloatProperty(name='Scale', min=0.1, max=25, default=1.0,
                                                                precision=3,
                                                                description="Custom shape scale")
    bpy.types.Scene.auto_bone_scale_b = bpy.props.FloatProperty(name='Scale', min=0.1, max=25, default=1.0,
                                                                precision=3,
                                                                description="Custom shape scale")
    bpy.types.Scene.auto_bone_color = bpy.props.BoolProperty(name="Color",
                                                             description="Use color groups for controllers",
                                                             default=True)


def unregister():
    bpy.utils.unregister_class(RunAction)
    bpy.utils.unregister_class(PanelUI)

    del bpy.types.Scene.auto_bone_subdivisions
    del bpy.types.Scene.auto_bone_txt_a
    del bpy.types.Scene.auto_bone_size_a
    del bpy.types.Scene.auto_bone_list_a
    del bpy.types.Scene.auto_bone_scale_a

    del bpy.types.Scene.auto_bone_txt_b
    del bpy.types.Scene.auto_bone_size_b
    del bpy.types.Scene.auto_bone_list_b
    del bpy.types.Scene.auto_bone_scale_b

    del bpy.types.Scene.auto_bone_color

if __name__ == "__main__":
    register()
