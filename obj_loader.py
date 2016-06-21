__author__ = 'rajat123'

class OBJ:
    def __init__(self, filename):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        #self.normals = []
        #self.texcoords = []
        self.faces = []

        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                self.vertices.append(v)

            elif values[0] == 'f':
                face = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                self.faces.append(face)
	
