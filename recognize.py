#!/usr/bin/env python3

# https://stackoverflow.com/questions/48954246/find-sudoku-grid-using-opencv-and-python

import numpy as np
import cv2
import os

from operator import itemgetter

INPUT_DIR = 'sudoku_img/sudoku_1.png'
OUTPUT_DIR = 'out/'

def main():

        img = cv2.imread(INPUT_DIR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

        cv2.imwrite(OUTPUT_DIR + 'canny.jpg', edges)

        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

        if not lines.any():
            print('No lines were found')
            exit()

        lines = [line[0] for line in lines]

        sorted_1 = sorted(lines, key=itemgetter(0))
        min_1, max_1 = sorted_1[0], sorted_1[-1]

        sorted_2 = sorted(lines, key=itemgetter(1))
        min_2, max_2 = sorted_2[0], sorted_2[-1]


        # draw lines on the image
        for rho, theta in (min_1, max_1, min_2, max_2):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

        # write the lines to the image
        cv2.imwrite(OUTPUT_DIR + 'houghlines3.jpg',img)

if __name__ == "__main__":
    main()
