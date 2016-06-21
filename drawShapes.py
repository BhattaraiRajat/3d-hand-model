__author__ = 'rajat123'
import wireframe
def my_swap(x,y):
    temp = x
    x = y
    y = temp
    return(x,y)

#bresenham line
def draw_line(screen, c1, c2, color):
    x0 = c1[0]
    y0 = c1[1]
    x1 = c2[0]
    y1 = c2[1]

    if( x0 == x1 ):
        if( y0 < y1):
            for y in range(y0,y1):
                x = x0
                screen.set_at((x, y), color)
        else:
            for y in range(y1,y0+1):
                x = x0
                screen.set_at((x, y), color)
    elif( y0 == y1 ):
        if(x0 < x1):
            for x in range(x0,x1+1):
                y = y0;
                screen.set_at((x, y), color)
        else:
            for x in range(x1,x0):
                y = y0
                screen.set_at((x, y), color)
    else:
        if (abs(y1 - y0) > abs(x1 - x0)):
            steep = 1
        else:
            steep = 0
        if(steep):
            (x0,y0) = my_swap(x0,y0)
            (x1,y1) = my_swap(x1,y1)
        if(x0 >x1):
            (x0,x1) = my_swap(x0,x1)
            (y0,y1) = my_swap(y0,y1)

        dErr = abs(y1 - y0)
        if (y0 > y1):
            ystep = -1
        else:
            ystep = 1
        dx = x1 - x0

        err = dx *2
        y = y0

        for x in range(int(x0),int(x1+1)):
            if(steep):
                screen.set_at( (int(x), int(y)), color)
            else:
                screen.set_at((int(x), int(y)), color)
            err -= dErr
            if(err < 0):
                y += ystep
                err += dx


#mid point circle algorithm
'''def draw_circle(screen, p1, r, color):
    xc, yc = int(p1.x), int(p1.y)
    x = 0
    y = r
    p = 1 - r

    def circle_plot(xc, yc, x, y):
        screen.set_at((xc + x, yc + y), color)
        screen.set_at((xc - x, yc + y), color)
        screen.set_at((xc + x, yc - y), color)
        screen.set_at((xc - x, yc - y), color)
        screen.set_at((xc + y, yc + x), color)
        screen.set_at((xc - y, yc + x), color)
        screen.set_at((xc + y, yc - x), color)
        screen.set_at((xc - y, yc - x), color)

    circle_plot(xc, yc, x, y)

    while(x < y):
        x += 1
        if (p <0):
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        circle_plot(xc, yc, x, y)'''



def crossZ((x1,y1),(x2,y2)):
    return x1*y2-y1*x2

def crossProduct(a,b):
    return wireframe.Node((a.y*b.z-a.z*b.y  ,b.x*a.z-a.x*b.z , a.x*b.y-a.y*b.x))
def normalise(v1):
    m = (v1.x**2+v1.y**2+v1.z**2 )**0.5
    return wireframe.Node((v1.x/m,v1.y/m,v1.z/m))

def fillTriangle(screen,n1,n2,n3,color,z,light_pos):
    #finding the smallest bounding rectangle that bounds the triangle with vertices x1 y1 x2 y2 x3 y3
    #barycentric method
    xmax=max(n1.x,max(n2.x,n3.x))
    xmin=min(n1.x,min(n2.x,n3.x))
    ymax=max(n1.y,max(n2.y,n3.y))
    ymin=min(n1.y,min(n2.y,n3.y))

    #zbuffer
    v1 =wireframe.Node((n2.x - n1.x, n2.y - n1.y, n2.z-n1.z))
    v2 =wireframe.Node((n3.x - n2.x, n3.y - n2.y, n3.z-n2.z))
    tn = crossProduct(v1,v2)
    if(tn.z == 0):
        return 0
    n = normalise(tn)
    light_pos = normalise(light_pos)

    P = n.x * light_pos.x + n.y * light_pos.y + n.z * light_pos.z
    costheta = P/((n.x**2+n.y**2+n.z**2 )**0.5*(light_pos.x**2+light_pos.y**2+light_pos.z**2 )**0.5)
    an = tn.x
    bn = tn.y
    cn = tn.z
    d = -an*n1.x-bn*n1.y-cn*n1.z

    #lighting
    ka,Ia,kd,Id = 0.6,0.6,0.6,0.9
    I = ka * Ia + kd * Id * costheta
    col_list = list(color)
    for i in range(3):
        col_list[i] *= abs(I)
    color = tuple(col_list)


    for x in range(int(xmin),int(xmax+1),1):
        for y in range(int(ymin), int(ymax),1):
            i=crossZ((x-n1.x,y-n1.y),(n2.x-n1.x,n2.y-n1.y))
            j=crossZ((x-n2.x,y-n2.y),(n3.x-n2.x,n3.y-n2.y))
            k=crossZ((x-n3.x,y-n3.y),(n1.x-n3.x,n1.y-n3.y))
            depth = (-d-an*x-bn*y)/cn
            if((i >= 0 and j >=0 and k >= 0)or (i<0 and j<0 and k<0)):
                if (x > 0 and x < 800 and y >0 and y < 600):
                    if(depth  < z[x][y]):
                        z[x][y] = depth
                        screen.set_at((x,y), color)




