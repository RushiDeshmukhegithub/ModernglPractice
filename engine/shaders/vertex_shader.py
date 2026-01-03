vertex_shader = """

#version 330

in vec3 in_pos;
in vec3 in_color;
in float in_point_size;

out vec3 out_color;
out vec3 out_pos;

void main(){
       gl_Position = vec4(in_pos,1.0);
       gl_PointSize = in_point_size;
       out_color = in_color;
       out_pos = in_pos;
}

"""
