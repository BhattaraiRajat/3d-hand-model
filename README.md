## 3d-hand-model

##Description
A simple project that draws a “3D hand” using the very
basic tools of computer graphics in python.

Only the inbuilt function for plotting a pixel from pygame package has been used in the entire project.

Bresenham line drawing algorithm has been used to draw lines, scan line for filling the polygons and
Barycentric Algorithm for triangles. To give the
object a more realistic feel, shading and illumination models have been applied (flat shading).
Camera has also been added so that viewing angle can be moved by changing coordinates.
Likewise, hidden surface removal algorithm (z-buffers) has also been applied in addition to the various
other algorithms. 
Finally, various transformation functions have been added like translation, rotation, scaling and so on 
that work on various keyboard inputs.

##Screenshots
![hand_wireframe](https://cloud.githubusercontent.com/assets/20043960/16203544/c3c767a6-36e8-11e6-9842-c7d6fb0ac254.PNG)

To fill hand wireframe with color, uncomment the commented part in wireframeDisplay.py file that gives following output.

![filled_hand](https://cloud.githubusercontent.com/assets/20043960/16203576/e87d15e6-36e8-11e6-818a-671bb3a3b2dd.PNG)
