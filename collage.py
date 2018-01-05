import bpy
from math import radians

import os
import subprocess


bpy.context.scene.render.resolution_x = 250
bpy.context.scene.render.resolution_y = 250
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.cycles.samples = 1000


orth = {'x': (radians(90), radians(0), radians(90)), 'y': (radians(90), radians(0), radians(180)), 'z': (radians(0), radians(0), radians(180))}

cwd = 'Dropbox/3/mad'
name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]


for ob in bpy.context.scene.objects:
    if ob.type == 'CAMERA':
        bpy.ops.object.delete()

# orth
for i, el in enumerate(orth):
    bpy.ops.object.add(type = 'CAMERA', location = (0, 0, 0))
    
    ob = bpy.context.scene.objects.active
    
    ob.location[i] = 20
    ob.rotation_euler = orth[el]
    
    bpy.context.scene.camera = bpy.context.scene.objects.active

    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render('%s/%s.png' % (cwd, el))

# persp
bpy.ops.object.add(type = 'CAMERA')
    
ob = bpy.context.scene.objects.active

ob.location = (-20, 20, 8.75)
ob.rotation_euler = (radians(77.5), radians(0), radians(225))

bpy.context.scene.camera = bpy.context.scene.objects.active

bpy.ops.render.render()
bpy.data.images['Render Result'].save_render('%s/persp.png' % cwd)


# compile
subprocess.call(['montage', '%s/x.png' % cwd, '%s/y.png' % cwd, '%s/z.png' % cwd, '%s/persp.png' % cwd, '-tile', '2x2', '-geometry', '+0+0', '%s/%s.png' % (cwd, name)])
