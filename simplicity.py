import pygame
import moderngl
import numpy as np
import math

pygame.init()
width = 800
height = 800
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

def rotate(p,xangle,yangle,zangle):
    xcos = math.cos(xangle)
    xsin = math.sin(xangle)
    ycos = math.cos(yangle)
    ysin = math.sin(yangle)
    zcos = math.cos(zangle)
    zsin = math.sin(zangle)
    x1 = p[0]*ycos + p[2]*ysin
    z1 = -p[0]*ysin + p[2]*ycos
    x2 = x1*zcos + p[1]*zsin
    y1 = -x1*zsin + p[1]*zcos
    y2 = y1*xcos + z1*xsin
    z2 = -y1*xsin + z1*xcos
    return [x2,y2,z2]

def transform_2D(p,angle,camera):
    x,y,z = rotate(p,math.pi*0.4,angle,0)
    z = z + camera
    x = x/z
    y = y/z
    #camera = 0.0
    return [x,y,1.0]

angle = 0
camera = 5.0
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

def draw_circle(p,r,segment,completion,recur,rotation):
    color = [0.5,1.0,0.5]
    size = [5.0]
    res = []
    #p[1]+=r
    for i in range(0,segment):
        angle = completion*2*math.pi*i/segment
        new_p = rotate(p,rotation[0]*angle,rotation[1]*angle,rotation[2]*angle)
        new_p.extend(color)
        new_p.extend(size)
        res.append(new_p)
        #continue
        if recur:
            res.extend(draw_circle(new_p,r,segment,1.0,False,[0,1,0]))
    return res

def draw_cylinder(p,r,segment,completion,recur,rotation,dir):
    color = [0.5,1.0,0.5]
    size = [5.0]
    res = []
    for i in range(0,segment):
        new_p = p.copy()
        tmp = i/segment
        new_p = [new_p[0]+dir[0]*tmp,new_p[1]+dir[1]*tmp,new_p[2]+dir[2]*tmp]
        new_p.extend(color)
        new_p.extend(size)
        res.append(new_p)
        if recur:
            res.extend(draw_circle(new_p,r,segment,1.0,False,[1,0,0]))
    return res

def circle(center,radius,color,size,segment,rotation):
    p = [0,radius,1.0]
    completion = 1.0
    res = []
    for i in range(0, segment):
        angle = completion*2*math.pi*i/segment
        new_p = rotate(p,rotation[0]*angle,rotation[1]*angle,rotation[2]*angle)
        new_p = [new_p[0] + center[0],new_p[1]+center[1],new_p[2]+center[2]]
        new_p.extend(color)
        new_p.extend(size)
        res.append(new_p)
    return res

def donut(center,radius,color,size,segment,rotation):
    res = []
    vc = circle(center,radius,color,size,segment,rotation)
    for i in range(len(vc)):
        res.extend(circle(vc[i],radius-1,color,size,segment,[0,1,0]))
    return res

vc = [
    [ 0.5, 0.5, 0.5,  1.0,0.0,0.0,  10.0],
    [-0.5, 0.5, 0.5,  1.0,0.0,0.0,  10.0],
    [-0.5,-0.5, 0.5,  1.0,0.0,0.0,  10.0],
    [ 0.5,-0.5, 0.5,  1.0,0.0,0.0,  10.0],
    
    [ 0.5, 0.5, -0.5,  1.0,0.0,0.0,  10.0],
    [-0.5, 0.5, -0.5,  1.0,0.0,0.0,  10.0],
    [-0.5,-0.5, -0.5,  1.0,0.0,0.0,  10.0],
    [ 0.5,-0.5, -0.5,  1.0,0.0,0.0,  10.0],
    ]

#vc = attach_tetrahedron([vc])
#vc = draw_circle([0.0,1.0,0],0.8,50,0.5,True,[0,0,1])
#vc = draw_cylinder([0.0,1.0,0],0.8,50,0.5,True,[0,0,1],[1,0,0])
vc = circle([0.0,0.0,1.0],0.8,[0,0,1],[10.0],30,[0,0,1])
vc = donut([0.0,0.0,3.0],0.8,[0,0,1],[5.0],30,[0,0,1])
print(vc)
#vertices = []
vertices,vc = update_vertices(vc)
vertices = vc
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
    vao.render(mode=moderngl.POINTS)
    vao.render(mode=moderngl.LINES)
    #vao.render(mode=moderngl.TRIANGLES)
    #vao.release()
    pygame.display.flip()
    clock.tick(60)

vao.release()
vbo.release()
ctx.release()
pygame.quit()

