import pygame
import moderngl
import numpy as np

pygame.init()
WIDTH , HEIGHT = 800,800
dim = (WIDTH, HEIGHT)
pygame.display.set_mode(dim,pygame.DOUBLEBUF | pygame.OPENGL )
pygame.display.set_caption("SDF Engine")

ctx = moderngl.create_context()

vertex_shader = """

#version 330

layout (location = 0) in vec3 in_pos;
in vec3 in_color;

void main(){
        gl_Position = vec4(in_pos,1.0);
}

"""

fragment_shader = """

#version 330

uniform vec2 u_resolution;

out vec4 f_color;

int circle(vec2 uv){
        if(uv.x*uv.x + uv.y*uv.y < 0.25){
            return 0;
        }
        return 1;
}

void main(){
        vec2 uv = gl_FragCoord.xy / u_resolution;
        uv = uv*2.0 - 1.0;
        uv.x *= u_resolution.x/u_resolution.y; 
        if(circle(uv) == 0){
            f_color = vec4(1.0,1.0,1.0,1.0);
        }
        else{
            f_color = vec4(0.0,1.0,0.0,1.0);
        }
}

"""

program = ctx.program(vertex_shader,fragment_shader)
u_resolution = program['u_resolution']
u_resolution.value = (WIDTH,HEIGHT)

vertices = np.array([
    -1.0, 1.0,1.0,
     1.0, 1.0,1.0,
     1.0,-1.0,1.0,
    
     1.0,-1.0,1.0,
    -1.0,-1.0,1.0,
    -1.0, 1.0,1.0, 
    ],dtype='f4')

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(program,[(vbo,'3f','in_pos')])

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    ctx.clear(0.0,0.0,0.0)
    vao.render(mode=moderngl.TRIANGLES)
    pygame.display.flip()

vbo.release()
vao.release()
pygame.quit()

