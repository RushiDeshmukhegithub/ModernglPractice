import pygame
import moderngl
import numpy as np
import math

pygame.init()
width = 800
height = 600
pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
pygame.display.set_caption("Simplicity")

ctx = moderngl.create_context()
ctx.enable(moderngl.PROGRAM_POINT_SIZE)

vertex_shader="""
#version 330
in vec3 in_pos;
in vec3 in_color;
in float in_point_size;
out vec3 v_color;
void main(){
        gl_Position = vec4(in_pos,1.0);
        gl_PointSize = in_point_size;
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

prog = ctx.program(vertex_shader,fragment_shader);

def load_vao(vc,prog):
    vertices = np.array(vc,dtype='f4')
    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.vertex_array(prog,[(vbo,'3f 3f 1f','in_pos','in_color','in_point_size')])
    #vbo.release()
    return vbo,vao


def transform_2D(p,angle,camera):
    cos = math.cos(angle)
    sin = math.sin(angle)
    x = p[0]*cos + p[2]*sin
    z = -p[0]*sin + p[2]*cos
    z = z + camera
    x = x/z
    y = p[1]/z
    #camera = 0.0
    return [x,y,1.0]

angle = 0
camera = 3.0
def update_vertices(vc):
    global angle,camera
    angle+=0.01
    camera += 0.001 
    vertices = []
    for i in range(len(vc)):
        vertices.extend(transform_2D(vc[i],angle,camera))
        vertices.extend(vc[i][3:])
    #print(vertices)
    return vertices,vc


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

vc = [
    [ 0.5, 0.5, 0.5,  1.0,0.0,0.0,  10.0],
    [-0.5, 0.5, 0.5,  0.5,0.5,0.0,  10.0],
    [-0.5,-0.5, 0.5,  0.0,1.0,0.0,  10.0],
    [ 0.5,-0.5, 0.5,  0.0,0.0,1.0,  10.0],
    
    [ 0.5, 0.5, -0.5,  1.0,0.0,0.0,  10.0],
    [-0.5, 0.5, -0.5,  0.5,0.5,0.0,  10.0],
    [-0.5,-0.5, -0.5,  0.0,1.0,0.0,  10.0],
    [ 0.5,-0.5, -0.5,  0.0,0.0,1.0,  10.0],
    ]

vc = attach_tetrahedron([vc])
vertices = []
vertices,vc = update_vertices(vc)
vbo,vao = load_vao(vertices,prog)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            point = event.pos
            print(pos)
    ctx.clear(0.0,0.0,0.0)
    vbo.release()
    vao.release()
    vertices,vc = update_vertices(vc)
    vbo,vao = load_vao(vertices,prog)
    #vao.render(mode=moderngl.POINTS)
    vao.render(mode=moderngl.LINES)
    #vao.release()
    pygame.display.flip()
    clock.tick(60)

vao.release()
vbo.release()
ctx.release()
pygame.quit()

