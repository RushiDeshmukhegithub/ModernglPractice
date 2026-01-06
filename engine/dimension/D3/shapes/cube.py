import numpy as np
from pysdf import SDF

class Cube:
    def __init__(self):
        self.vertices_list = [
             0.5, 0.5, 0.5,
            -0.5, 0.5, 0.5,
            -0.5,-0.5, 0.5,
             0.5,-0.5, 0.5,
             
             0.5, 0.5,-0.5,
            -0.5, 0.5,-0.5,
            -0.5,-0.5,-0.5,
             0.5,-0.5,-0.5,
            ]

        self.triangles = [
                [0,1,2],
                [0,1,5],
                [0,3,2],
                [0,3,7],
                [0,4,5],
                [0,4,7],
                [6,2,1],
                [6,2,3],
                [6,5,1],
                [6,5,4],
                [6,7,3],
                [6,7,4],
        ]

        self.color = [0.0,1.0,0.0]
        self.pointSize = 10.0
        self.sdf_function = SDF(np.array([self.vertices_list[i:i+3] for i in range(0,len(self.vertices_list),3)],dtype='f4'),
                                np.array(self.triangles,dtype='f4'))

    def get_shape(self,vertices,triangles):
        res = []
        for triangle in triangles:
            res.extend(vertices[triangle[0]*3:triangle[0]*3+3])
            res.extend(vertices[triangle[1]*3:triangle[1]*3+3])
            res.extend(vertices[triangle[2]*3:triangle[2]*3+3])
        return res

    def get_vertices(self):
        shape = self.get_shape(self.vertices_list,self.triangles)
        extra = self.color.copy()
        extra.extend([self.pointSize])
        arr = np.array(shape,dtype='f4').reshape(-1,3)
        #vertices = [[shape[i]+0.001,shape[i+1]+0.001,shape[i+2]+0.001] for i in range(0,len(shape),3)]
        #distances = self.sdf_function(np.array(vertices,dtype='f4'))
        #distances = distances.reshape(-1,1)
        #print("dis : ",distances)
        arr = np.hstack((arr , np.tile(extra,(len(arr),1))))
        #arr = np.hstack((arr , distances))
        print("arr",arr)
        return arr.flatten().astype('f4')

    def set_vertices(self,vertices):
        self.vertices_list = vertices

    def scale(self,sc):
        for i in range(0,len(self.vertices_list),3):
            self.vertices_list[i]*=sc[0]
            self.vertices_list[i+1]*=sc[1]
            self.vertices_list[i+2]*=sc[2]
