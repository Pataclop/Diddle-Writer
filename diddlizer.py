#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import cv2
import numpy as np
import sys


tmp = cv2.imread("images/A.png")
LETTER_SIZE = tmp.shape[1]
PAGE_HEIGHT = 35
PAGE_WIDTH = 30
IMAGE_FACTOR = 200


def incruster(im, l, x_offset, y_offset):
    nom = "images/"+l+".png"
    s_img = cv2.imread(nom)
    im[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
    return im

def save(num, im):
    nom = str(num)+".png"
    im = cv2.resize(im, (PAGE_WIDTH*IMAGE_FACTOR, PAGE_HEIGHT*IMAGE_FACTOR), interpolation = cv2.INTER_LANCZOS4)

    cv2.imwrite(nom, im) 

def newPage():
    im = np.ones((PAGE_HEIGHT*LETTER_SIZE,PAGE_WIDTH*LETTER_SIZE,3), np.uint8)
    im[:,:] = (255,255,255)
    return im

def fun():
    interline = 1.6
    posX=0
    posY=0
    pageCount=0
    file1 = open(sys.argv[1], 'r') 
    Lines = file1.readlines() 
    text=""
    for l in Lines :
        l=l.replace("\n", " ")
        l=l.replace(".", ";")
        l=l.replace(";", ",")
        l=l.replace("?", "!")
        l=l.replace("0", "zero")
        l=l.replace("1", "un")
        l=l.replace("2", "deux")
        l=l.replace("3", "trois")
        l=l.replace("4", "quatre")
        l=l.replace("5", "cinq")
        l=l.replace("6", "six")
        l=l.replace("7", "sept")
        l=l.replace("8", "huit")
        l=l.replace("9", "neuf")
        l=l.upper()
        text=text+l

    words = text.split()
    im=newPage()

    for w in words:
        if len(w)>(PAGE_WIDTH-1)-posX:
            posX=0
            posY=posY+1
        
        if posY>(PAGE_HEIGHT/interline)-1:
            posX=0
            posY=0
            save(pageCount, im)
            pageCount=pageCount+1
            im[:,:] = (255,255,255)
        for l in w:
            im=incruster(im, l, posX*LETTER_SIZE, int(posY*LETTER_SIZE*interline))
            posX=posX+1
        
        im=incruster(im, ' ', posX*LETTER_SIZE, int(posY*LETTER_SIZE*interline))
        posX=posX+1

    save(pageCount, im)


fun()
