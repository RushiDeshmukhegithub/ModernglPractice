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




void main(){
        vec2 uv = gl_FragCoord.xy / u_resolution;
        uv = uv*2.0 - 1.0;
        uv.x *= u_resolution.x/u_resolution.y; 
        vec3 center = vec3(0.0,0.0,1.0);
        vec3 ro = vec3(0.0,0.0,3.0);
        vec3 normal = normalize(vec3(uv,-1.0));
        vec3 rd = vec3(uv,-1.0);
        float t = 0.0;
        vec3 p = ro;
        for(int i=0;i<64;i++){
            vec3 p = ro + rd*t;
            float d = sdSphere(p,0.5,center,camera_pos);
            if(d<0.001){
                break;
            }
            t+=d;
            if(d>10.0){
                break;
            }
        }
        vec3 light_ray = p - light_source;
        vec3 view_ray = p - camera_pos;
        vec3 normal_ray = p - center;
        float diff = max(dot(light_ray,normal_ray),0.0)/(length(light_ray)*length(normal_ray))  + 
                     max(dot(view_ray,normal_ray),0.0)/(length(view_ray)*length(normal_ray));
        if(t < 10.0){
            //f_color = vec4(0.5,1.0*((10.1-t)/10.0),0.0,1.0);
            f_color = vec4(0.0,1.0*(1.0-min(abs(diff),0.9)),0.0,1.0);
        }
        else{
            f_color = vec4(0.0,0.0,0.0,1.0);
        }
        if(abs(uv.x) < 0.005){
            f_color = vec4(1.0,0.0,0.0,1.0); 
        }
        if(abs(uv.y) < 0.005){
            f_color = vec4(0.0,0.0,1.0,1.0); 
        }
}

"""

program = ctx.program(vertex_shader,fragment_shader)
camera_pos = [0.0,0.0,0.0]
program['camera_pos'].value = camera_pos
light_source = [0.0,0.0,0.0];
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
                camera_pos[2] += 0.1
            if event.key == pygame.K_s:
                camera_pos[2] -= 0.1
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
    vao.render(mode=moderngl.TRIANGLES)
    pygame.display.flip()

vbo.release()
vao.release()
pygame.quit()

