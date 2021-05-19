from pygame.display import set_mode
from pygame.locals import DOUBLEBUF,OPENGL
from pygame.mouse import set_pos
from pygame.event import get
from pygame.key import get_pressed
from pygame.time import wait
from pygame.display import flip
from pygame import quit,init,QUIT,KEYDOWN,K_ESCAPE,K_RETURN,\
     K_PAUSE,K_p,MOUSEMOTION,K_w,K_s,K_d,K_a

from OpenGL.GL import glEnable,GL_DEPTH_TEST,GL_LIGHTING,\
     glShadeModel,GL_SMOOTH,GL_COLOR_MATERIAL,glColorMaterial,\
     GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,GL_LIGHT0,\
     glLightfv,GL_AMBIENT,GL_DIFFUSE,glMatrixMode,\
     GL_PROJECTION,GL_MODELVIEW,glGetFloatv,GL_MODELVIEW_MATRIX,\
     glLoadIdentity,glRotatef,glPushMatrix,glMultMatrixf,\
     glPopMatrix,GL_POSITION,glClear,GL_COLOR_BUFFER_BIT,\
     GL_DEPTH_BUFFER_BIT,glColor4f,glBegin,GL_QUADS,glVertex3f,\
     glEnd,glTranslatef

from OpenGL.GLU import gluNewQuadric,gluPerspective,gluLookAt,\
     gluSphere

init()
display = (400, 300)
screen = set_mode(display, DOUBLEBUF + OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable (GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

sphere = gluNewQuadric() 

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# init mouse movement and center mouse on screen
#for i in range(2):
#    print(screen.get_size()[i]==display[i])
displayCenter = [display[i] // 2 for i in range(2)]
mouseMove = [0, 0]
set_pos(displayCenter)

up_down_angle = 0
paused = False

run = True
while run:
    for event in get():
        if event.type == QUIT:
            run = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_RETURN:
                run = False

            if event.key == K_PAUSE or event.key == K_p:
                paused = not paused
                set_pos(displayCenter) 

        if not paused: 
            if event.type == MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] \
                             for i in range(2)]

            set_pos(displayCenter)    

    if not paused:
        # get keys
        keypress = get_pressed()
        #mouseMove = pygame.mouse.get_rel()
    
        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        up_down_angle += mouseMove[1] / 10
        glRotatef(up_down_angle, 1, 0, 0)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movement 
        if keypress[K_w]:
            glTranslatef(0, 0, 0.1)

        if keypress[K_s]:
            glTranslatef(0, 0, -0.1)

        if keypress[K_d]:
            glTranslatef(-0.1, 0, 0)

        if keypress[K_a]:
            glTranslatef(0.1, 0, 0)

        # apply the left and right rotation
        glRotatef(mouseMove[0] / 10, 0, 1, 0)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix 
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glVertex3f(-10, -10, -2)
        glVertex3f( 10, -10, -2)
        glVertex3f( 10,  10, -2)
        glVertex3f(-10,  10, -2)
        glEnd()

        glTranslatef(-1.5, 0, 0)
        glColor4f(0.5, 0.2, 0.2, 1)
        gluSphere(sphere, 1, 32, 16) 

        glTranslatef(3, 0, 0)
        glColor4f(0.2, 0.2, 0.5, 1)
        gluSphere(sphere, 1, 32, 16) 

        glPopMatrix()

        flip()
        wait(10)

quit()
