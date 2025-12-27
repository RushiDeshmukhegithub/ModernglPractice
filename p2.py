import pygame
from pygame.locals import DOUBLEBUF, OPENGL, RESIZABLE
import moderngl
import numpy as np

pygame.init()
width,height = 800,600
pygame.display.set_mode((width,height),DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("practice")

ctx = moderngl.create_context()

vertex_shader="""
#version 330
in vec3 in_pos;
in vec3 in_color;
out vec3 v_color;
void main(){
        gl_Position = vec4(in_pos,1.0);
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

prog = ctx.program(vertex_shader,fragment_shader)

vertices = np.array([
     0.0, 0.6, 0.0,  1.0,0.0,0.0,
    -0.6, 0.0, 0.0,  0.5,0.5,0.0,
    -0.6,-0.6, 0.0,  0.0,1.0,0.0,
     0.6,-0.6, 0.0,  0.0,0.0,1.0,
    ],dtype='f4')

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(prog,[(vbo,'3f 3f','in_pos','in_color')])

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            running = False
    ctx.clear(0.08,0.08,0.08)
    vao.render(mode=moderngl.TRIANGLES)
    pygame.display.flip()
    clock.tick(60)

vao.release()
vbo.release()
ctx.release()
pygame.quit()




