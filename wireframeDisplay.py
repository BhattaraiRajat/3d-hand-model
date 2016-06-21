__author__ = 'rajat123'

import wireframe
import pygame
from obj_loader import *
from drawShapes import *
from pygame.locals import *

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1))}


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('3D Hand Model')
        self.background = (0,0,0)

        self.wireframes = {}
        self.displayEdges = True
        self.edgeColour = (200,0,0)
        self.z = [[0 for x in range(height)] for y in range(width)]
        self.light_pos = wireframe.Node((400,300,400))


    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe


    def run(self):
        """ Create a pygame screen until it is closed. """
        clock = pygame.time.Clock()
        rx, ry = (0,0)
        tx, ty = (0,0)
        rotate = move = False

        running = True
        while running:
            clock.tick(30)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key in key_to_function:
                        key_to_function[e.key](self)
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 3: rotate = True
                    elif e.button == 1: move = True
                elif e.type == MOUSEBUTTONUP:
                    if e.button ==3: rotate = False
                    elif e.button == 1: move = False
                elif e.type == MOUSEMOTION:
                    i, j = e.rel
                    if rotate:
                        rx += i
                        ry += j
                    if move:
                        tx -= i
                        ty += j


            hand.translate('x',-tx/15)
            hand.translate('y',ty/15)
            hand.rotateX(hand.findCentre(),ry)
            hand.rotateY(hand.findCentre(),rx)

            self.display(hand)

            pygame.display.flip()

    def clear_z(self):
        for i in range(self.width):
            for j in range(self.height):
                self.z[i][j]=99999999.0
                self.screen.set_at((i,j), self.background)

    def display(self,hand):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        for f in hand.faces:
            if (len(f) == 3):
                pygame.draw.line(self.screen, self.edgeColour, (hand.nodes[f[0]-1].x, hand.nodes[f[0]-1].y), (hand.nodes[f[1]-1].x, hand.nodes[f[1]-1].y))
                pygame.draw.line(self.screen,self.edgeColour, (hand.nodes[f[1]-1].x, hand.nodes[f[1]-1].y), (hand.nodes[f[2]-1].x, hand.nodes[f[2]-1].y))
                pygame.draw.line(self.screen,self.edgeColour, (hand.nodes[f[2]-1].x, hand.nodes[f[2]-1].y), (hand.nodes[f[0]-1].x, hand.nodes[f[0]-1].y))
	"""uncomment these sections to fill the wireframes with colors
                draw_line(self.screen, (hand.nodes[f[0]-1].x, hand.nodes[f[0]-1].y), (hand.nodes[f[1]-1].x, hand.nodes[f[1]-1].y), self.edgeColour)
                draw_line(self.screen, (hand.nodes[f[1]-1].x, hand.nodes[f[1]-1].y), (hand.nodes[f[2]-1].x, hand.nodes[f[2]-1].y),self.edgeColour)
                draw_line(self.screen, (hand.nodes[f[2]-1].x, hand.nodes[f[2]-1].y), (hand.nodes[f[0]-1].x, hand.nodes[f[0]-1].y),self.edgeColour)



        self.clear_z()
        for f in hand.faces:
            fillTriangle(self.screen,hand.nodes[f[0]-1],hand.nodes[f[1]-1],hand.nodes[f[2]-1],(194,151,120),self.z,self.light_pos)"""




    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.itervalues():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.itervalues():
            wireframe.scale((centre_x, centre_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.itervalues():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)




if __name__ == '__main__':
    pv = ProjectionViewer(800, 600)
    obj = OBJ('hand_3.obj')
    hand = wireframe.Wireframe()
    hand.addNodes(obj.vertices)
    hand.faces = obj.faces
    pv.addWireframe('Hand', hand)

    #isometric projection
    hand.rotateX((0,0,0),0.785)
    hand.rotateY((0,0,0),1.8)
    hand.rotateZ((0,0,0),1.5)
    hand.translate('x',400)
    hand.translate('y',300)
    hand.scale((400,300),650)

    hand.camera_view(0,-3.14/2,0)
    pv.run()
