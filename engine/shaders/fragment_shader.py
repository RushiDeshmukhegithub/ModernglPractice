fragment_shader = """

#version 330

in vec3 v_color;

out vec4 f_color;

vec3 rayMarchScene(vec3 rayOrigin, vec3 rayDirection){
        float t = 0.0;
        for(int i=0;i<64;i++){
            //vec3 p = ro + rd*i;
        }
        return vec3(0.0,0.0,0.0);
}

void main(){
        //vec2 uv = gl_FragCoord.xy/vec2(800,600)*2.0-1.0;
        //uv.x *= (800.0/600.0);
        //vec3 ro = camera_pos;
        //vec3 rd = normalize(vec3(uv,1.0));

        //f_color = vec4(rayMarchScene(ro,rd),1.0);
        f_color = vec4(v_color,1.0);
}


"""
