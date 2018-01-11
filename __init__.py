bl_info = {
        'name': 'Render Collage',
        'author': 'JackHasaKeyboard',
        'version': (1, 0),
        'blender': (2, 76, 0),
        'location': 'Dynamic Context Menu',
        'description': 'Render a scene with all angles orthographically and a perspective shot',
        'category': 'Render'
        }


import bpy
from math import radians

import os
import subprocess


class RenderCollage(bpy.types.Operator):
    '''Render a scene with all angles orthographically and a perspective shot'''
    bl_idname = 'render.collage'
    bl_label = 'Render Collage'
    bl_options = {'REGISTER'}


    def execute(self, context):
        scn = context.scene

        orth = {'x': (90, 0, 90), 'y': (90, 0, 180), 'z': (0, 0, 180)}

        cwd = os.path.expanduser('~')
        name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]


        for ob in scn.objects:
            if ob.type == 'CAMERA':
                bpy.ops.object.delete()


        for i, el in enumerate(orth):
            bpy.ops.object.add(type = 'CAMERA', location = (0, 0, 0))

            ob = scn.objects.active

            ob.location[i] = 20
            ob.rotation_euler = (radians(orth[el][0]), radians(orth[el][1]), radians(orth[el][2]))

            scn.camera = context.scene.objects.active

            bpy.ops.render.render()
            bpy.data.images['Render Result'].save_render('%s/%s.png' % (cwd, el))


        # compile
        subprocess.call(['montage', '%s/x.png' % cwd, '%s/y.png' % cwd, '%s/z.png' % cwd, '%s/persp.png' % cwd, '-tile', '2x2', '-geometry', '+0+0', '%s/%s.png' % (cwd, name)])
        subprocess.call(['rm', '%s/x.png' % cwd, '%s/y.png' % cwd, '%s/z.png' % cwd, '%s/persp.png' % cwd])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RenderCollage)


def unregister():
    bpy.utils.unregister_class(RenderCollage)


if __name__ == '__main__':
    register()
