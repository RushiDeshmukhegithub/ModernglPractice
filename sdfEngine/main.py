import pygame
import moderngl
import numpy as np
import math


pygame.init()
WIDTH , HEIGHT = 1000,800
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
uniform float r;
uniform vec3 cc;
uniform bool setHashb;
vec3 colour
//;
=vec3(0.1,0.1,0.1);

out vec4 f_color;

//Global Variables
vec3 ro = camera_pos;
vec3 rd = vec3(0.0,0.0,0.0);


vec2 min2(vec2 a, vec2 b){
        if(a.x < b.x){
            return a;
        }
        return b;
}

vec2 max2(vec2 a, vec2 b){
        if(a.x > b.x){
            return a;
        }
        return b;
}

vec2 returnMin(vec2 dis[100],int size){
        vec2 mindis = dis[0];
        for(int i=1;i<size;i++){
            mindis = min2(mindis,dis[i]);
        }
        return mindis;
}

vec2 oc(vec3 p,vec3 center){
        p = p - center;
        float d1 = length(p-vec3(min(abs(p.x),3.0),0.0,0.0)) - 0.05;
        float d2 = length(p-vec3(0.0,min(abs(p.y),3.0),0.0)) - 0.05;
        float d3 = length(p-vec3(0.0,0.0,min(abs(p.z),3.0))) - 0.05;
        vec2 arr[100];
        arr[0] = vec2(d1,2.0);
        arr[1] = vec2(d2,1.0);
        arr[2] = vec2(d3,3.0);
        return returnMin(arr,3);
}

vec2 sdfBeam(vec3 p,float d,vec2 mindist){
        vec3 p2 = camera_pos + rd*d;
        //vec3 p2 = p - camera_pos;
        //float res = (length(p-ro) + length(p-p2))/(2*d)-0.8;
        float res = length(p-vec3(p2.x,p2.y,min(abs(p.z),d))) - 1.0;
        //return max2(mindist,vec2(-res,mindist.y));
        return min2(mindist,vec2(res,8.0));
}

vec2 sdfPlane(vec3 p, float z){
        float d = p.z-z;
        float id = 6.0;
        if(mod(int(p.x),2)== mod(int(p.y),2)){
            id=7.0;
        }
        return vec2(d,id);
}

vec2 sdSphere(vec3 p, float radius, vec3 center,vec3 camera_pos){
        float x = min(abs(p.x),2);
        x = 0.0;
        vec2 d1 = vec2(length(p-vec3(x,0.0,0.0)-center-camera_pos) - radius,4.0);
        vec2 d2 = oc(p,center);
        return min2(d1,d2);
        //return d1;
}

vec2 fBox(vec3 p,vec3 b,vec3 center){
        vec3 z = abs(p-center) - abs(b);
        vec2 d1 = vec2(max(max(z[0],z[1]),z[2]),5.0);
        vec2 d2 = oc(p,center);
        return min2(d1,d2);
}


vec2 map(vec3 p){
        vec2 d1 = sdSphere(p,r,cc,vec3(0.0,0.0,0.0));
        vec2 d2 = fBox(p,vec3(1.0,2.0,0.5),vec3(0.0));
        vec2 d3 = sdfPlane(p,0.0);
        vec2 arr[100];
        int n = 3;
        //vec2 d = max(-d1,d2);
        arr[0] = d1;
        arr[1] = d2;
        arr[2] = d3;
        //for(int i=0;i<n;i++){
          //  arr[i] = sdSphere(p,1.0+r*(i)*0.1,cc*vec3((100-i)*0.1,i*0.5-0.2,1.0+i*0.9),vec3(0.0));
        //}
        vec2 d = returnMin(arr,n);
        d = sdfBeam(p,30.0,d);
        return d;
}

vec3 getMaterial(vec2 object){
    if(object.y == 1.0){
        return vec3(1.0,0.1,0.1);
    }
    if(object.y == 2.0){
        return vec3(0.0,1.0,0.0);
    }
    if(object.y == 3.0){
        return vec3(0.0,0.0,1.0);
    }
    if(object.y == 4.0){
        return vec3(0.9,0.9,0.0);
    }
    if(object.y == 5.0){
        return vec3(0.0,0.5,0.5);
    }            
    if(object.y == 6.0){
        return vec3(1.0);
    }            
    if(object.y == 7.0){
        return vec3(0.0);
    }            
    if(object.y == 8.0){
        return vec3(1.0,0.0,0.0);
    }            
}

vec3 getNormal(vec3 p){
        vec2 e = vec2(0.1,0.0);
        return normalize(vec3(
            map(p+e.xyy).x - map(p-e.xyy).x,
            map(p+e.yxy).x - map(p-e.yxy).x,
            map(p+e.yyx).x - map(p-e.yyx).x
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

vec3 changeWorld(vec3 p){
        p = p*rotate_x(angles.x);
        p = p*rotate_y(angles.y);
        return p; 
}

void main(){
        vec2 uv = gl_FragCoord.xy / u_resolution;
        uv = uv*2.0 - 1.0;
        uv.x *= u_resolution.x/u_resolution.y; 
        vec3 center = vec3(0.0,0.0,5.0);
        vec3 normal = normalize(vec3(uv,-1.0));
        rd = vec3(uv,1.0);
        //rd = rd*rotate_x(angles.x);
        //rd = rd*rotate_y(angles.y);
        //ro = ro*rotate_x(angles.x);
        //ro = ro*rotate_y(angles.y);
        vec2 object;
        object.x = 0.0;
        object.y = 0;
        vec3 p = ro;
        float d = 0.0;
        vec2 hit;
        for(int i=0;i<64;i++){
            vec3 p = ro + rd*object.x;
            p = changeWorld(p);
            hit = map(p);
            object.x += hit.x;
            object.y = hit.y;
            if(hit.x<0.001){
                break;
            }
            if(object.x>100.0){
                break;
            }
        }
        vec3 col
        //;
        =vec3(0.1,0.1,0.1);
        if(object.x < 100.0){
            p = ro+rd*object.x;
            colour = getMaterial(object);
            vec3 l = normalize(light_source - p);
            vec3 n = getNormal(p);
            vec3 v = normalize(ro-p);
            vec3 h = normalize(l+v);
            //vec3 diffusion = colour*clamp(dot(n,l),0.0,1.0);
            //col += diffusion;
            float diff = max(0.0,dot(n,l));
            float sss = pow(max(0.0,dot(rd,-l)),4.0)*5.0;
            float spec = pow(max(0.0,dot(n,h)),64.0);
            col = colour * (diff*0.6+0.4);
            //col += vec3(0.8,1.0,0.9)*sss;
            col += vec3(1.0)*spec;
        }
        else{
            col = vec3(0.8);
        }
        if(abs(uv.x)<0.005){
            col = vec3(0.0,0.0,1.0);
        }
        if(abs(uv.y)<0.005){
            col = vec3(1.0,0.0,0.0);
        }
        f_color = vec4(col,1.0);
}

"""

program = ctx.program(vertex_shader,fragment_shader)

def setProgramVariables():
    global program,r,cc,camera_pos,light_source,u_resolution,angles
    program['r'] = r
    program['cc'] = cc
    program['camera_pos'] = camera_pos
    program['light_source'] = light_source
    program['u_resolution'] = u_resolution
    program['angles'] = angles


r = 1.0
cc = [1.0,0.0,0.0]
program['r'] = r
program['cc'] = cc
camera_pos = [0.0,0.0,-10.0]
#program['camera_pos'].value = camera_pos
light_source = [0.0,50.0,-10.0];
#program['light_source'].value = light_source
u_resolution = (WIDTH,HEIGHT)
angles = [0.0,0.0,0.0]
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
dragging = False
drag_start_pos = [0.0,0.0]
drag_end_pos = [0.0,0.0]
dr = r
toggle = False
while running:
    m_x,m_y = pygame.mouse.get_pos()
    mouse_pos = [m_x,m_y]
    mouse_pos[1] = -((mouse_pos[1]*2)/600 -1)
    mouse_pos[0] = (mouse_pos[0]*2)/800 - 1
    print(mouse_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not dragging:
                drag_start_pos = mouse_pos.copy()
            dragging = True
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                pass
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
    if dragging:
        r = dr+(mouse_pos[0]-drag_start_pos[0])
    else:
        dr = r
        angles[1]=mouse_pos[0]*math.pi
        angles[0]=mouse_pos[1]*math.pi
    if(toggle and cc[0] < 2.0):
        cc[0] += 0.01
    else:
        toggle = False
    if(cc[0] > -2.0 and not toggle):
        cc[0]-=0.01
    else:
        toggle = True 
    setProgramVariables()
    ctx.clear(0.0,0.0,0.0)
    vao.render()
    pygame.display.flip()

vbo.release()
vao.release()
pygame.quit()

