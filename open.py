#!/usr/bin/python
# -*- coding: utf-8 -*-


from OpenGL.GL import *  # car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
from sys import argv as sysargv
import numpy as np


###############################################################
# variables globales
quadric = gluNewQuadric()
# caméra
eye_x, eye_y, eye_z = 0.0, 0.0, 5.0  # placement de la caméra
view_x, view_y, view_z = 0.0, 0.0, 0.0  # point de bracage
up_x, up_y, up_z = 0.0, 1.0, 0.0  # vecteur pointant vers le haut
matrice_cout = None
dimension_grille = 30
height = 700  # hauteur
width = 1000  # longueur
dim_carre = height // dimension_grille


###############################################################


def filtre_median(mat):
    """applique le filtre de Tukey à la matrice mat"""
    l = np.empty(shape=mat.shape, dtype=int)
    for coords in np.ndindex(l.shape):
        l[coords] = np.median(
            np.take(
                mat,
                mat[
                    coords[0] - 1 if coords[0] > 0 else 0 : coords[0] + 2,
                    coords[1] - 1 if coords[1] > 0 else 0 : coords[1] + 2,
                ],
                mode="clip",
            )
        )
    return l


def gen_matrice(l, c):
    """Fonction qui genere une matrice aleatoire et lui applique un filtre
    median"""
    data = np.random.randint(1, 10, size=(l, c))
    dataf = filtre_median(data)
    return dataf


def init_matrices():
    mat_cout = gen_matrice(30, 30)
    return mat_cout


def display_terrain(matrice):

    coutmax = 10
    i = 0
    coord = []
    for i in range(dimension_grille):
        liste = []
        for j in range(dimension_grille):
            le_cout = matrice[i][j]
            color = le_cout * 30 // coutmax
            # print(color)
            ### BORDURE
            if (
                i == 0
                or j == 0
                or i == dimension_grille - 1
                or j == dimension_grille - 1
            ):
                glColor4f(0.0, 0.0, 1.0, 1.0)  # bleu

                glBegin(GL_QUADS)
                glVertex3f(2 * i, 2 * j, 0.0)
                glVertex3f(2 * i + 1, 2 * j, 0.0)
                glVertex3f(2 * i + 1, 2 * j + 1, 0.0)
                glVertex3f(2 * i, 2 * j + 1, 0.0)
                glEnd()
            ### interieur terrain
            glColor4f(1.0, 0.0, 0.0, 0.0)  # rouge
            glBegin(GL_QUADS)
            cube = [
                [2 * i, 2 * j, 0.0] * dim_carre,
                [2 * i + 1, 2 * j, 0.0] * dim_carre,
                [2 * i + 1, 2 * j + 1, 0.0] * dim_carre,
                [2 * i, 2 * j + 1, 0.0] * dim_carre,
            ]
            glVertex3f(cube[0][0], cube[0][1], cube[0][2])
            glVertex3f(cube[1][0], cube[1][1], cube[1][2])
            glVertex3f(cube[2][0], cube[2][1], cube[2][2])
            glVertex3f(cube[3][0], cube[3][1], cube[3][2])
            glEnd()

    return None


###############################################################


def init():
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    # global quadric
    glClearColor(0.0, 0.0, 0.0, 0.0)  # couleur de fond

    glEnable(GL_DEPTH_TEST)  # profondeur
    glEnable(GL_DITHER)  # impression couleur
    glEnable(GL_COLOR_MATERIAL)

    diffuse = [0.7, 0.7, 0.7, 1.0]
    pos = [1, 0, 0, 0]  # pos de la lumiere
    specular = [0.001, 0.001, 0.001, 1.0]
    white = [1.0, 1.0, 1.0, 1.0]
    red = [1, 0, 0, 0]

    glEnable(GL_LIGHTING)  # prise en compte des calculs associes aux sources lumineuses
    glEnable(GL_LIGHT0)
    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, white)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, white)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 9.0)

    glLightfv(GL_LIGHT0, GL_POSITION, pos)  # position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)  # intensité
    # glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

    glShadeModel(GL_SMOOTH)  # definit l'ombre


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, view_x, view_y, view_z, up_x, up_y, up_z)

    glPushMatrix()
    glTranslatef(-15, -25.0, -6.0)
    display_terrain(matrice)
    glPopMatrix()

    glutSwapBuffers()


def reshape(width, height):
    """Projection dans le repère OPENGL"""
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(150.0, width / height, 1.0, 20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, view_x, view_y, view_z, up_x, up_y, up_z)


def keyboard(key, x, y):

    global day, year, eye_y, eye_z
    dz = 1 if eye_z >= 1.11 else 0
    ndz = 1 if eye_z < 15.0 else 0
    dy = 1 if eye_y > 0.01 else 0
    ndy = 1 if eye_y < 15.0 else 0

    if key == b"z":
        eye_z -= dz
    elif key == b"s":
        eye_z += ndz
        #print(eye_z)
    elif key == b"q":
        eye_y -= dy
    elif key == b"d":
        eye_y += ndy
    # print(eye_y)

    elif key == b"\033":
        glutLeaveMainLoop()

    glutPostRedisplay()


###############################################################
# MAIN

glutInit(sysargv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)  # gestion de profondeur

glutCreateWindow("Terrain 3D")
glutReshapeWindow(width, height)
init()
glutReshapeFunc(reshape)
glutDisplayFunc(display)
# appel de la fonction du clavier
glutKeyboardFunc(keyboard)
init()
matrice = init_matrices()
# print(matrice)
display_terrain(matrice)

glutMainLoop()
