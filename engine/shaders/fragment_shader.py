fragment_shader = """

#version 330

in vec3 out_color;
in vec3 out_pos;
in vec3 sun_min;
in vec3 sun_max;
//will not work as we are using x/z, y/z instead of 3D

vec3 new_color;

out vec4 f_color;

void main(){
        new_color = out_color;
        //float x = (in_sun[1]-out_pos[1])/(in_sun[0]-out_pos[0]) + (-out_pos[1]/(out_pos[0]));
        //float y = (in_sun[2]-out_pos[2])/(in_sun[1]-out_pos[1]) + (-out_pos[2]/(out_pos[1]));
        //float z = (in_sun[2]-out_pos[0])/(in_sun[2]-out_pos[0]) + (-out_pos[2]/(out_pos[0]));
        //if((x < 0.01 && x > -0.01) || (y<0.01 && y>-0.01) || (z<0.01 && z>-0.01)){
          //  new_color[0] = 1.0;
           // new_color[1] = 1.0;
           // new_color[2] = 1.0;
        //}
        vec3 reflection = vec3(out_pos[0],-out_pos[1],out_pos[2]);
        float z1 = out_pos[2]*(0.1)*(0.1)/(out_pos[0]*out_pos[1]);
        float z2 = out_pos[2]*(0.1)*(1.0)/(out_pos[0]*out_pos[1]);
        if((z1 < 0.1 && z1 > -0.1) || (z2 < 0.1 && z2 > -0.1)){
            new_color[0] = 1.0;
            new_color[1] = 1.0;
            new_color[2] = 1.0;
        }
        f_color = vec4(new_color,1.0);
}


"""
