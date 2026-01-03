import pygame
import moderngl
import numpy as np
from shaders.vertex_shader import vertex_shader
from shaders.fragment_shader import fragment_shader
from dimension.D3.shapes.cube import Cube

pygame.init()
width , height = 800,800
pygame.display.set_mode((width,height),pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
pygame.display.set_caption("MIGHTY ENGINE")

ctx = moderngl.create_context()
ctx.enable(moderngl.PROGRAM_POINT_SIZE)
program = ctx.program(vertex_shader,fragment_shader)
vertices = np.array([
    0,0,0,  1,1,1, 5.0
    ],dtype='f4')
vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(program,[(vbo,'3f 3f 1f','in_pos','in_color','in_point_size')])
running = True
clock = pygame.time.Clock()
universe = []
camera = [0.0,0.0,0.0]

def load_vertices():
    global vertices
    new_vertices = np.array([],dtype='f4')
    for obj in universe:
        new_vertices = np.concatenate((new_vertices,obj.get_vertices()),axis=0)
    if len(universe) < 1:
        vertices = np.array([
        0.4,0.4, 0.5,    1,0,0,  10.0,
        -0.4,0.4,0.5,  0,1,0,  10.0,
        -0.4,-0.4, 0.5,  0,0,1,  10.0,
        ],dtype='f4')
    else:
        vertices = new_vertices

def load_camera():
    global vertices,universe,camera
    vertices = vertices.reshape(-1,7)
    vertices[:,:1]-=camera[0]
    vertices[:,1:2]-=camera[1]
    vertices[:,2:3]-=camera[2]
    #vertices[:,:1]/=vertices[:,2:3]
    #vertices[:,1:2]/=vertices[:,2:3]
    #vertices[:,2:3]=1.0
    print("vertices",vertices)
    vertices = vertices.flatten()

def load_vbo_vao():
    global vertices,program,vbo,vao
    vbo.release()
    vao.release()
    vbo = ctx.buffer(vertices.tobytes())
    vao = ctx.vertex_array(program,[(vbo,'3f 3f 1f','in_pos','in_color','in_point_size')])


def readEvents():
    global running,universe
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                universe.append(Cube())
            if event.key == pygame.K_w:
                camera[2]+=1.0
            if event.key == pygame.K_a:
                camera[0]+=1.0
            if event.key == pygame.K_d:
                camera[0]-=1.0
            if event.key == pygame.K_s:
                camera[2]-=1.0
            if event.key == pygame.K_UP:
                camera[1]-=1.0
            if event.key == pygame.K_DOWN:
                camera[1]+=1.0

def render():
    global vao
    load_vertices()
    load_camera()
    load_vbo_vao()
    vao.render(mode=moderngl.POINTS)
    #vao.render(mode=moderngl.LINES)
    vao.render(mode=moderngl.TRIANGLES)

while running:
    readEvents()
    ctx.clear(0.1,0.1,0.1)
    render()
    pygame.display.flip()
    clock.tick(60)

vbo.release()
vao.release()
ctx.release()
pygame.quit()


