import pygame
import moderngl
import numpy as np
import math


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
uniform vec3 angles;
vec3 colour
//;
=vec3(0.1,0.1,0.1);

out vec4 f_color;

float sdCircle(vec2 uv,float r,vec3 center){
        return length(uv-center.xy)-r;
}

float sdSphere(vec3 p, float radius, vec3 center,vec3 camera_pos){
        return length(p-center-camera_pos) - radius;
}

float fBox(vec3 p,vec3 b,vec3 center){
        vec3 z = abs(p) - abs(b);
        return max(max(z[0],z[1]),z[2]);
}


float map(vec3 p){
        float d1 = sdSphere(p,1.0,vec3(0.0,1.0,0.0),vec3(0.0,0.0,0.0));
        float d2 = fBox(p,vec3(20.0,0.01,20.0),vec3(0));
        if(d1 < d2){
            colour = vec3(0.9,0.9,0.0);
            return d1;
        }
        colour = vec3(0.0,0.5,0.5);
        return d2;
}

vec3 getNormal(vec3 p){
        vec2 e = vec2(0.1,0.0);
        return normalize(vec3(
            map(p+e.xyy) - map(p-e.xyy),
            map(p+e.yxy) - map(p-e.yxy),
            map(p+e.yyx) - map(p-e.yyx)
            ));
}

mat3 rotate_x(float angle){
        float c = cos(angle);
        float s = sin(angle);
        return mat3(
            1,0,0,
            0,c,s,
            0,-s,c
            );
}

mat3 rotate_y(float angle){
        float c = cos(angle);
        float s = sin(angle);
        return mat3(
            c,0,s,
            0,1,0,
            -s,0,c
            );
}

void main(){
        vec2 uv = gl_FragCoord.xy / u_resolution;
        uv = uv*2.0 - 1.0;
        uv.x *= u_resolution.x/u_resolution.y; 
        vec3 center = vec3(0.0,0.0,5.0);
        vec3 ro = camera_pos;
        vec3 normal = normalize(vec3(uv,-1.0));
        vec3 rd = vec3(uv,1.0);
        rd = rd*rotate_x(angles.x);
        rd = rd*rotate_y(angles.y);
        //rd *= angle;
        float t = 0.0;
        vec3 p = ro;
        for(int i=0;i<256;i++){
            vec3 p = ro + rd*t;
            //float d = sdSphere(p,1.0,center,vec3(0.0,0.0,0.0));
            //float d = fBox(p,vec3(0.1,0.3,0.8),vec3(0.0,0.0,0.0));
            float d = map(p);
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
            vec3 diffusion = colour*clamp(dot(getNormal(p),normalize(light_source-p)),0.0,1.0);
            col += diffusion;
        }
        else{
            col = vec3(0);
        }
        if(abs(uv.x)<0.005){
            col = vec3(0.0,0.0,1.0);
        }
        if(abs(uv.y)<0.005){
            col = vec3(1.0,0.0,0.0);
        }
        //col = pow(col,vec3(0.4545));
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
rotation_angles = [0.0,0.0,0.0]
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
                light_source[2] += 10.0
            if event.key == pygame.K_j:
                light_source[2] -= 10.0
            if event.key == pygame.K_h:
                light_source[0] -= 10.0
            if event.key == pygame.K_k:
                light_source[0] += 10.0
            if event.key == pygame.K_t:
                light_source[1] += 10.0
            if event.key == pygame.K_g:
                light_source[1] -= 10.0

    program['camera_pos'].value = camera_pos
    program['light_source'].value = light_source
    m_x,m_y = pygame.mouse.get_pos()
    mouse_pos = [m_x,m_y]
    print(mouse_pos)
    mouse_pos[1] = -((mouse_pos[1]*2)/600 -1)
    mouse_pos[0] = (mouse_pos[0]*2)/800 - 1
    print(mouse_pos)
    rotation_angles[1]=mouse_pos[0]*math.pi
    rotation_angles[0]=mouse_pos[1]*math.pi
    print(rotation_angles)
    program['angles'].value = rotation_angles
    ctx.clear(0.0,0.0,0.0)
    vao.render()
    pygame.display.flip()

vbo.release()
vao.release()
pygame.quit()

