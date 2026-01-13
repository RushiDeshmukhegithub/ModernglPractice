import pygame
import moderngl
import numpy as np

pygame.init()
WIDTH , HEIGHT = 800,600
dim = (WIDTH, HEIGHT)
pygame.display.set_mode(dim,pygame.DOUBLEBUF | pygame.OPENGL )
pygame.display.set_caption("SDF Engine")

ctx = moderngl.create_context()

vertex_shader = """

#version 330

layout (location = 0) in vec3 in_pos;

void main(){
        gl_Position = vec4(in_pos,1.0);
}

"""

fragment_shader = """

#version 330

uniform vec2 u_resolution;
uniform vec3 camera_pos;
uniform vec3 light_source;

out vec4 f_color;

float sdCircle(vec2 uv,float r,vec3 center){
        return length(uv-center.xy)-r;
}

float sdSphere(vec3 p, float radius, vec3 center,vec3 camera_pos){
        return length(p-center-camera_pos) - radius;
}

float map(vec3 p){
        return sdSphere(p,1.0,vec3(0.0,0.0,5.0),vec3(0.0,0.0,0.0));
}

vec3 getNormal(vec3 p){
        vec2 e = vec2(0.1,0.0);
        return normalize(vec3(
            map(p+e.xyy) - map(p-e.xyy),
            map(p+e.yxy) - map(p-e.yxy),
            map(p+e.yyx) - map(p-e.yyx)
            ));
}

void main(){
        vec2 uv = gl_FragCoord.xy / u_resolution;
        uv = uv*2.0 - 1.0;
        uv.x *= u_resolution.x/u_resolution.y; 
        vec3 center = vec3(0.0,0.0,5.0);
        vec3 ro = camera_pos;
        vec3 normal = normalize(vec3(uv,-1.0));
        vec3 rd = vec3(uv,1.0);
        //ro *= angle;
        //rd *= angle;
        float t = 0.0;
        vec3 p = ro;
        for(int i=0;i<256;i++){
            vec3 p = ro + rd*t;
            float d = sdSphere(p,1.0,center,vec3(0.0,0.0,0.0));
            t+=d;
            if(abs(d)<0.001){
                break;
            }
            if(t>500.0){
                break;
            }
        }
        vec3 light_ray = light_source - p;
        vec3 col
        //;
        =vec3(0.1,0.1,0.1);
        if(t < 500.0){
            p = ro+rd*t;
            vec3 diffusion = vec3(1)*clamp(dot(getNormal(p),normalize(light_source-p)),0.0,1.0);
            col += diffusion;
        }
        f_color = vec4(col,1.0);
}

"""

program = ctx.program(vertex_shader,fragment_shader)
camera_pos = [0.0,0.0,0.0]
program['camera_pos'].value = camera_pos
light_source = [20.0,40.0,-30.0];
program['light_source'].value = light_source
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
            if event.key == pygame.K_w:
                camera_pos[2] += 1.0
            if event.key == pygame.K_s:
                camera_pos[2] -= 1.0
            if event.key == pygame.K_a:
                camera_pos[0] -= 0.1
            if event.key == pygame.K_d:
                camera_pos[0] += 0.1
            if event.key == pygame.K_UP:
                camera_pos[1] += 0.1
            if event.key == pygame.K_DOWN:
                camera_pos[1] -= 0.1
            if event.key == pygame.K_u:
                light_source[2] += 0.1
            if event.key == pygame.K_j:
                light_source[2] -= 0.1
            if event.key == pygame.K_h:
                light_source[0] -= 0.1
            if event.key == pygame.K_k:
                light_source[0] += 0.1
            if event.key == pygame.K_t:
                light_source[1] += 0.1
            if event.key == pygame.K_g:
                light_source[1] -= 0.1

    ctx.clear(0.0,0.0,0.0)
    program['camera_pos'].value = camera_pos
    program['light_source'].value = light_source
    vao.render()
    pygame.display.flip()

vbo.release()
vao.release()
pygame.quit()

