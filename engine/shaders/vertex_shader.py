vertex_shader = """

#version 330

in vec3 in_pos;
in vec3 in_color;
in float in_point_size;

uniform vec3 camera_pos;

out vec3 v_color;
out vec3 out_pos;
out float v_dist;
// Problem is we need to block the distance if ray travels through obj
void main(){
       gl_Position = vec4(in_pos,1.0);
       gl_PointSize = in_point_size;
       vec3 ro = vec3(10.0,10.0,10.0);
       ro[0] += 0.001*camera_pos[1];
       float b = 1.0 - distance(ro,in_pos)/100.0;
       v_color = in_color*b;
       out_pos = in_pos;
}

"""
