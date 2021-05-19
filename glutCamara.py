#from OpenGL.GLUT import glutInit,glutInitDisplayMode,\
#GLUT_DEPTH,GLUT_DOUBLE,GLUT_RGBA,glutInitWindowPosition
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

# angle of rotation for the camera direction
angle = 0

# actual vector representing the cameras direction
lx, lz = 0, -1

# XZ position of the camera
x, z = 0, 5

# the key states. These variables will be zero
# when no key is being presses
deltaAngle = 0
deltaMove = 0
xOrigin = -1

def changeSize(w, h):
	# Prevent a divide by zero, when window is too short
	# (you cant make a window of zero width).
	if h == 0:
		h = 1

	ratio =  w / h

	# Use the Projection Matrix
	glMatrixMode(GL_PROJECTION)

	# Reset Matrix
	glLoadIdentity()

	# Set the viewport to be the entire window
	glViewport(0, 0, w, h)

	# Set the correct perspective.
	gluPerspective(45, ratio, 0.1, 100)

	# Get Back to the Modelview
	glMatrixMode(GL_MODELVIEW)

def drawSnowMan():
	glColor3f(1, 1, 1)

	# Draw Body
	glTranslatef(0, 0.75, 0)
	glutSolidSphere(0.75, 20, 20)

	# Draw Head
	glTranslatef(0, 1, 0)
	glutSolidSphere(0.25, 20, 20)

	# Draw Eyes
	glPushMatrix()
	glColor3f(0, 0, 0)
	glTranslatef(0.05, 0.1, 0.18)
	glutSolidSphere(0.05, 10, 10)
	glTranslatef(-0.1, 0, 0)
	glutSolidSphere(0.05, 10, 10)
	glPopMatrix();

	# Draw Nose
	glColor3f(1, 0.5, 0.5)
	glRotatef(0, 1, 0, 0)
	glutSolidCone(0.08, 0.5, 10, 2)

def computePos(deltaMove):
	global x, z
	x += deltaMove * lx / 10
	z += deltaMove * lz / 10

def renderScene():
	'''aqui si'''
	global deltaMove
	deltaMove += 0.0005

	if deltaMove:
		computePos(deltaMove)
		#print(deltaMove)

	# Clear Color and Depth Buffers
	glClear(GL_COLOR_BUFFER_BIT + GL_DEPTH_BUFFER_BIT)

	# Reset transformations
	glLoadIdentity()
	
	# Set the camera
	gluLookAt(x,      1, z,
			  x + lx, 1, z + lz,
			  0,      1, 0)

	#print("gluLookAt(x = "+str(x)+")")

	# Draw ground
	glColor3f(0.9, 0.9, 0.9)
	glBegin(GL_QUADS)
	glVertex3f(-100, 0, -100)
	glVertex3f(-100, 0,  100)
	glVertex3f( 100, 0,  100)
	glVertex3f( 100, 0, -100)
	glEnd()

	# Draw 36 SnowMen
	for i in range(-3, 3): 
		for j in range(-3, 3): 
			glPushMatrix()
			glTranslatef(i * 10, 0, j * 10)
			drawSnowMan()
			glPopMatrix()
			   
	glutSwapBuffers()
 
def processNormalKeys(key, x, y):	
	if (key == 27):
		exit(0)

def pressKey(key, x, y):
	global deltaMove
	#if key == GLUT_KEY_UP: 
	deltaMove += 0.5 

	#elif key == GLUT_KEY_DOWN: 
	#	deltaMove = -0.5 
	
def releaseKey(key, x, y): 	
	#if key == GLUT_KEY_DOWN: 
	#deltaMove = 0
	pass
		
from math import sin,cos

def mouseMove(x, y): 	
	global deltaAngle, lx, lz
	# this will only be true when the left button is down
	#if (xOrigin >= 0):
	# update deltaAngle
	deltaAngle = x - xOrigin # / 1000

	# update camera's direction
	lx =  sin(angle + deltaAngle)
	lz = -cos(angle + deltaAngle) # ly?

	#print("deltaAngle = " + str(deltaAngle) + \
	#	", lx = " + str(lx) + ", lz = " + str(lz))

def mouseButton(button, state, x, y):
	global angle
	# only start motion if the left button is pressed
	#if button == GLUT_LEFT_BUTTON:
	# when the button is released
	#if state == GLUT_LEFT_BUTTON: #GLUT_UP:
	angle += deltaAngle
	xOrigin = -1
		
	#else:  # state = GLUT_DOWN
	#	xOrigin = x
		


# init GLUT and create window
#glutInit(&argc, argv)
glutInit([])
glutInitDisplayMode(GLUT_DEPTH + GLUT_DOUBLE + GLUT_RGBA)
glutInitWindowPosition(100, 100)
glutInitWindowSize(320, 320)
glutCreateWindow("")

# register callbacks
glutDisplayFunc(renderScene)
glutReshapeFunc(changeSize)
glutIdleFunc(renderScene)

glutIgnoreKeyRepeat(1)
glutKeyboardFunc(processNormalKeys)
glutSpecialFunc(pressKey)
glutSpecialUpFunc(releaseKey)

# here are the two new functions
#glutMouseFunc(mouseButton)
#glutMotionFunc(mouseMove)

# OpenGL init
glEnable(GL_DEPTH_TEST)

# enter GLUT event processing cycle
glutMainLoop()
