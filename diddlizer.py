import cv2
import numpy as np
import sys

# Load a sample image to determine the letter size
tmp = cv2.imread("images/A.png")
LETTER_SIZE = tmp.shape[1]  # Width of a letter image
PAGE_HEIGHT = 35  # Height of the page in letters
PAGE_WIDTH = 30  # Width of the page in letters
IMAGE_FACTOR = 200  # Scaling factor for the final image

# Function to overlay a letter image on the main image at specified coordinates
def incruster(im, l, x_offset, y_offset):
    nom = "images/" + l + ".png"
    s_img = cv2.imread(nom)
    im[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img
    return im

# Function to save the final image with a specific number
def save(num, im):
    nom = str(num) + ".png"
    im = cv2.resize(im, (PAGE_WIDTH * IMAGE_FACTOR, PAGE_HEIGHT * IMAGE_FACTOR), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(nom, im)

# Function to create a new blank page
def newPage():
    im = np.ones((PAGE_HEIGHT * LETTER_SIZE, PAGE_WIDTH * LETTER_SIZE, 3), np.uint8)
    im[:, :] = (255, 255, 255)  # White background
    return im

# Main function to process the input text and create pages
def fun():
    interline = 1.6
    posX = 0
    posY = 0
    pageCount = 0
    file1 = open(sys.argv[1], 'r')  # Open the input file
    Lines = file1.readlines()  # Read all lines
    text = ""
    
    # Process each line to replace characters and convert to uppercase
    for l in Lines:
        l = l.replace("\n", " ")
        l = l.replace(".", ";")
        l = l.replace(";", ",")
        l = l.replace("?", "!")
        l = l.replace("0", "zero")
        l = l.replace("1", "un")
        l = l.replace("2", "deux")
        l = l.replace("3", "trois")
        l = l.replace("4", "quatre")
        l = l.replace("5", "cinq")
        l = l.replace("6", "six")
        l = l.replace("7", "sept")
        l = l.replace("8", "huit")
        l = l.replace("9", "neuf")
        l = l.upper()
        text = text + l

    words = text.split()
    im = newPage()

    # Place each word on the page
    for w in words:
        if len(w) > (PAGE_WIDTH - 1) - posX:
            posX = 0
            posY = posY + 1
        
        if posY > (PAGE_HEIGHT / interline) - 1:
            posX = 0
            posY = 0
            save(pageCount, im)  # Save current page
            pageCount = pageCount + 1
            im[:, :] = (255, 255, 255)  # Reset to white page
        
        for l in w:
            im = incruster(im, l, posX * LETTER_SIZE, int(posY * LETTER_SIZE * interline))
            posX = posX + 1
        
        im = incruster(im, ' ', posX * LETTER_SIZE, int(posY * LETTER_SIZE * interline))
        posX = posX + 1

    save(pageCount, im)  # Save the final page

# Check if a file argument is provided
if len(sys.argv) == 1:
    print("usage : python diddlizer.py file_with_text.txt")
    sys.exit()

fun()
