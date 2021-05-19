from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

def changeSize(w, h):
	ratio =  w / h

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glViewport(0, 0, w, h)
	gluPerspective(45, ratio, 0.1, 100)
	glMatrixMode(GL_MODELVIEW)

def drawSnowMan():
	glColor3f(1, 1, 1)

	# Draw Body
	glTranslatef   (0, 0.75, 0)
	glutSolidSphere(0.75, 20, 20)

	# Draw Head
	glTranslatef   (0, 1, 0)
	glutSolidSphere(0.25, 20, 20)

	# Draw Eyes
	glPushMatrix()
	glColor3f      (0, 0, 0)
	glTranslatef   (0.05, 0.1, 0.18)
	glutSolidSphere(0.05, 10, 10)
	glTranslatef   (-0.1, 0, 0)
	glutSolidSphere(0.05, 10, 10)
	glPopMatrix()

	# Draw Nose
	glColor3f    (1, 0.5, 0.5)
	glRotatef    (0, 1, 0, 0)
	glutSolidCone(0.08, 0.5, 10, 2)

def renderScene():
	global y
	
	y         += 0.005
	cx, cy, cz = (x, y, z - 1)
	ax, ay, az = (0, 1, 0)

	glClear(16640)
	glLoadIdentity()
	gluLookAt(x,y,z, cx,cy,cz, ax,ay,az)

	c = 0.9
	glColor3f (c, c, c)
	glBegin   (GL_QUADS)

	d = 100
	glVertex3f(-d, 0, -d)
	glVertex3f(-d, 0,  d)
	glVertex3f( d, 0,  d)
	glVertex3f( d, 0, -d)

	glEnd()

	# Draw 36 SnowMen
	r = range(-3, 3)
	for i in r: 
		for j in r: 
			glPushMatrix()
			glTranslatef(10 * i, 0, 10 * j)
			drawSnowMan()
			glPopMatrix()
			   
	glutSwapBuffers()

x, y, z = 0, 1, 5
w = 320
x1 = 100
glutInit([])
glutInitDisplayMode(18)
glutInitWindowPosition(x1, x1)
glutInitWindowSize(w, w)
glutCreateWindow("")
glutDisplayFunc(renderScene)
glutReshapeFunc(changeSize)
glutIdleFunc(renderScene)
glEnable(GL_DEPTH_TEST)
glutMainLoop()
