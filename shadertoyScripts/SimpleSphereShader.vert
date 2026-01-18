
vec3 ro = vec3(0.0,0.0,0.0);
vec3 rd = vec3(0.0);
vec3 p = vec3(0.0);
vec2 object = vec2(0.0);
vec2 hit = vec2(0.0);
vec3 colour = vec3(0.0,0.0,0.0);
vec3 n = vec3(0.0);
vec3 l = vec3(10.0,80.0,-20.0);
vec3 diff = vec3(0.0);
float aspect = 1.0;
vec2 mouse = vec2(0.0);
float PI = 3.14153;


mat2 rot(float a){
    float c = cos(a);
    float s = sin(a);
    return mat2(c,s,-s,c);
}

vec3 rotx(vec3 p,float a){
    return vec3(p.x,p.yz*rot(a));
}

vec3 rotz(vec3 p,float a){
    return vec3(p.xy*rot(a),p.z);
}

vec3 roty(vec3 p,float a){
    vec2 r = p.xz*rot(a);
    return vec3(r.x,p.y,r.y);
}

vec3 rot3(vec3 p, float x, float y , float z){
    p = rotx(p,x);
    p = roty(p,y);
    return rotz(p,z);
}

vec3 getMaterial(float id){
    if(id == 1.0){
        return vec3(0.0,1.0,0.0);
    }
    if(id == 2.0){
        return vec3(1.0);
    }
    if(id == 3.0){
        return vec3(0.0);
    }
}

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

vec2 sdfPlane(vec3 p){
    float d = p.y+5.0;
    float id = 2.0;
    if(int(mod(p.x,2.0)) == int(mod(p.z,2.0))){
        id = 3.0;
    }
    return vec2(d,id);
}

vec2 sdfSphere(vec3 p){
    return vec2(length(p-vec3(0.0,-4.0,8.0)) - 1.0,1.0);
}

vec2 map(vec3 p){
    vec2 d = sdfSphere(p);
    d = min2(d,sdfPlane(p));
    return d;
}

vec3 normal(vec3 p){
    vec2 e = vec2(0.01,0.0);
    return vec3(map(p+e.xyy).x-map(p-e.xyy).x,
           map(p+e.yxy).x-map(p-e.yxy).x,
           map(p+e.yyx).x-map(p-e.yyx).x
           );
}

vec3 cw(vec3 p){
    float x = -2.0*PI*mouse.y;
    float y = -2.0*PI*mouse.x;
    float z = 0.0;
    p.x/=aspect;
    p = rot3(p,x,y,z);
    p.x*=aspect;
    //p += rot3(normalize(vec3(0.0,0.0,1.0)),x,y,z)*iTime;
    return p;
}

void rayMarching(){
    for(int i=0;i<64;i++){
        p = cw(ro + rd*object.x);
        hit = map(p);
        object.y = hit.y;
        object.x += hit.x;
        if(hit.x < 0.001 && object.x > 100.0){
            break;
        }
    }
    if(object.x < 100.0){
        p = cw(ro + rd*object.x);
        n = normal(p);
        diff = getMaterial(object.y)*clamp(dot(n,l),0.0,1.0);
        colour+= diff;
    }
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/iResolution.xy;
    uv = uv*2.0 - 1.0;
    aspect = iResolution.x/iResolution.y;
    uv.x *= aspect;
    
    //mouse = (iMouse.xy)/iResolution.xy;
    //mouse.x *= aspect;
    
    rd = normalize(vec3(uv,1.0));
    rayMarching();
    vec3 col = colour;
    // Output to screen
    fragColor = vec4(col,1.0);
}
