import pygame
import moderngl
import numpy as np
import math
import random

#n = int(input("Enter : "))

def translation(pos):
    return np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [pos[0],pos[1],pos[2],1],
        ],dtype='f4')

def scaling(pos):
    return np.array([
        [pos[0],0,0,0],
        [0,pos[1],0,0],
        [0,0,pos[2],0],
        [0,0,0,1],
        ],dtype='f4')

def rotation_y(angle):
    return np.array([
        [math.cos(angle) , 0, math.sin(angle), 0],
        [0               , 1, 0,               0],
        [-math.sin(angle), 0, math.cos(angle), 0],
        [0               , 0, 0,               1],
        ],dtype='f4')

def rotation_x(angle):
    return np.array([
        [1 , 0, 0, 0                            ],
        [0, math.cos(angle) ,  math.sin(angle),0],
        [0,-math.sin(angle) , math.cos(angle), 0],
        [0               , 0, 0,               1],
        ],dtype='f4')


def rotation_z(angle):
    return np.array([
        [math.cos(angle) , math.sin(angle),0, 0],
        [-math.sin(angle), math.cos(angle),0, 0],
        [0               , 0,              1, 0],
        [0               , 0, 0,              1],
        ],dtype='f4')


def perspective(fov,aspect,znear,zfar):
    f = 1.0 / math.tan(fov/2.0)
    v00 = f/aspect
    v11 = f
    v22 = (zfar+znear)/(znear-zfar)
    v32 = (2*zfar*znear)/(znear-zfar)
    return np.array([
        [v00, 0, 0, 0],
        [0, v11, 0, 0],
        [0, 0, v22,-1],
        [0, 0, v32, 0],
        ],dtype='f4')


def rand_vertex():
    return [
            random.uniform(-1.0,1.0),
            random.uniform(-1.0,1.0),
            random.uniform(-1.0,1.0),
            random.uniform(0.0,1.0),
            random.uniform(0.0,1.0),
            random.uniform(0.0,1.0)]

def random_shape(n):
    res = []
    for i in range(n):
        res.append(rand_vertex())
    return res

pygame.init()
width,height = 800,600
pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.OPENGL )
pygame.display.set_caption("P3")


ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

vertex_shader="""
#version 330
in vec3 in_pos;
in vec3 in_color;

uniform mat4 mvp; 

out vec3 v_color;
void main(){
        gl_Position = mvp *  vec4(in_pos,1.0);
        v_color = in_color;
}
"""

fragment_shader="""
#version 330
in vec3 v_color;
out vec4 f_color;
void main(){
        f_color = vec4(v_color,1.0);
}
"""
for name in dir(moderngl):
    print(f"Attempting to access attribute: {name}")

prog = ctx.program(vertex_shader=vertex_shader,fragment_shader=fragment_shader)
mvp_uniform = prog["mvp"]


e = [0.0, 0.0, 0.0,    1.0,0.0,0.0]
f = [0.8, 0.0, 0.0,    0.0,1.0,0.0]
g = [0.0, 0.8, 0.0,  0.0,0.0,1.0]

def merge(arr):
    res = []
    for a in arr:
        res.extend(a)
    return res

def give_all_tri(arr):
    res = []
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            for k in range(j+1,len(arr)):
                res.extend([arr[i],arr[j],arr[k]])
    return res

def attach_tetrahedron(arr):
    res = []
    for a in arr:
        res.extend(give_all_tri(a))
    return res

def give_all_tri2(arr):
    res = []
    for i in range(len(arr)-2):
        res.extend([arr[i],arr[i+1],arr[i+2]])
    return res

def render(rotations,view,proj,mvp_uniform,vao,move=[0,0,0],scale=[1,1,1]):
    translated = translation(move)
    scaled = scaling(scale)
    rotation = rotations[2] @ rotations[1] @ rotations[0]
    model = translated @ scaled @ rotation
    model = model @ rotation_z(0.3) @ rotation_y(0.0) @rotation_x(-4)
    #view = view @ rotation_z(0.0) @ rotation_y(0.0) @rotation_x(0.0)
    #proj = proj @ rotation_z(0.0) @ rotation_y(0.0) @rotation_x(0.0)
    mvp = model @ view @ proj
    mvp_uniform.write(mvp.tobytes())
    vao.render(moderngl.TRIANGLES,vertices=3,first=0)


obj_tri = []
tri = [e,f,g]
for i in range(1):
    obj_tri.append(tri)
obj = attach_tetrahedron(obj_tri)
vertices = np.array(obj,dtype='f4')

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(prog,[(vbo,'3f 3f','in_pos','in_color')])

clock = pygame.time.Clock()
running = True
iden_mat = np.eye(4,dtype='f4')
model = iden_mat
rotate = False
diff1 = 0
diff2 = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            rotate = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            rotate = False
    ctx.clear(0.1,0.1,0.1)
    time = pygame.time.get_ticks() / 1000.0
    proj = perspective(math.radians(60),width/height,0.1,10.0)
    view = np.eye(4,dtype='f4')
    mat4 = np.eye(4,dtype='f4')
    view[3][2] = -3.0
    #view[3][1] = -0.5
    #view[3][3] = 3.0
    angle = max(-time,math.radians(-180))
    Rx = rotation_x(angle)
    Ry = rotation_x(angle)
    Rz = rotation_x(angle)
    rotations = [mat4,mat4,mat4]
    render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    rotations[0] = Rx
    render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    if -time < math.radians(-180):
        rotations[0] = mat4
        if diff1 == 0:
            diff1 = time
        nRy = rotation_y(max(diff1-time,math.radians(-180)))
        rotations[1] = nRy
        render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    if -time < math.radians(-360):
        rotations[1] = mat4
        if diff2 == 0:
            diff2 = time
        nRx = rotation_x(max(diff2-time,math.radians(-180)))
        nRy = rotation_y(max(diff2-time,math.radians(-180)))
        rotations[0] = nRx
        rotations[1] = nRy
        render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    if -time < math.radians(-540):
        rotations[1] = mat4
        if diff2 == 0:
            diff2 = time
        nRx = rotation_x(max(diff2-time,math.radians(-180)))
        nRy = rotation_y(max(diff2-time,math.radians(-180)))
        rotations[0] = nRx
        rotations[1] = nRy
        render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    #rotations[0] = mat4
    #render(rotations,view,proj,mvp_uniform,vao,[0.0,0.0,0.0],[1.0,1.0,1.0])
    #Do it so that one after another model with develop and it will pick next ones to ratate
    pygame.display.flip()
    clock.tick(60)

vao.release()
vbo.release()
ctx.release()
pygame.quit()
