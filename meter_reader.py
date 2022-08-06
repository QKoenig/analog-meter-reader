import math
import cv2
import numpy as np

# original_img = cv2.imread('meter.jpeg')

img = cv2.imread('meter_cropped.jpeg')
# img = cv2.imread('meter2.jpeg')

# grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# blur
blur = cv2.GaussianBlur(gray, (5,5), 200)

# I played around with using an image run through the canny edge detector but found worse results
# low_threshold = 150
# high_threshold = 200
# edges = cv2.Canny(blur, low_threshold, high_threshold)


# Hough circles algorithm requires a good bit of tuning for each image.
# The following two calls are set up for meter_cropped.jpeg and meter2.jpeg respectively

# FOR ORIGINAL METER
maybe_dials = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,50,
                            param1=50,param2=30,minRadius=10,maxRadius=50)


# FOR METER 2
# maybe_dials = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,100,
#                             param1=50,param2=30,minRadius=50,maxRadius=100)

circles = np.uint16(np.around(maybe_dials))

# function for line generation
def bresenham(x1,y1,x2, y2):
 
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)
 
    y=y1

    points = []

    for x in range(x1,x2+1):
     
        # print("(",x ,",",y ,")\n")
        points.append((x,y))
        # Add slope to increment angle formed
        slope_error_new =slope_error_new + m_new
 
        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y=y+1
            slope_error_new =slope_error_new - 2 * (x2 - x1)
    
    return points

for circle in circles[0,:]:
    #        row          col
    center = (circle[0],circle[1])
    y1, x1 = (circle[1],circle[0])
    radius = circle[2]

    square_size = math.floor(radius/2)

    # This draws the original circles and square used to compute COM
    # cv2.circle(img,(circle[0],circle[1]),circle[2],(0,255,0),2)
    # cv2.circle(img,(circle[0],circle[1]),2,(0,255,0),3)
    # cv2.rectangle(img, (x1 + square_size, y1 + square_size), (x1 - square_size, y1 - square_size), (255,0,0), 2)
    
    xtop = 0
    ytop = 0
    bot = 0.001

    if center[1] + radius * 1.5 >= img.shape[0]  or center[0] + radius * 1.5 >= img.shape[1]:
        continue

    # Finding center of mass
    for i in range(square_size * 2):
        for j in range(square_size * 2):
            px = gray[center[1] - square_size + i, center[0] - square_size + j]
            
            if px > 50:
                px  = 0
            else:
                px = 1


            ytop += px * i
            xtop += px * j
            bot += px

    # print('COM:') 
    # print( f'x: {math.floor(xtop/bot)}/{square_size}')
    # print( f'y: {math.floor(ytop/bot)}/{square_size}')

    cv2.circle(img,(circle[0] - square_size + math.floor(xtop/bot), circle[1] - square_size + math.floor(ytop/bot)),2,(0,0,255),3)
    x = circle[0] - square_size + math.floor(xtop/bot)
    y = circle[1] - square_size + math.floor(ytop/bot)

    # keys are angles, values are lists of points
    lineDic = {}

    # bresenham only allows for slopes of 0 - 1 so each line is reflected 7 times
    for i in range(45):
        ylen = int(square_size*1.5 * math.sin(math.radians(i)))
        xlen = int(square_size*1.5 * math.cos(math.radians(i)))

        points = bresenham(x, y, x + xlen, y + ylen)

        lineDic[i] = points

        # Draws original bresenham lines
        # for point in points:
        #     img[point[1], point[0], 0] = 0
        #     img[point[1], point[0], 2] = 0
        #     img[point[1], point[0], 1] = 255


        lineDic[89 - i] = []
        lineDic[90 + i] = []
        lineDic[179 - i] = []
        lineDic[180 + i] = []
        lineDic[269 - i] = []
        lineDic[270 + i] = []
        lineDic[359 - i] = []
        for point in points:
            ydisp = abs(point[1] - y)
            xdisp = abs(point[0] - x)

            lineDic[179 - i].append((x - xdisp, y + ydisp))
            lineDic[180 + i].append((x - xdisp, y - ydisp))
            lineDic[359 - i].append((x + xdisp, y - ydisp))


            xdisp = abs(point[1] - y)
            ydisp = abs(point[0] - x)
            
            lineDic[89 - i].append((x + xdisp, y + ydisp))
            lineDic[90 + i].append((x - xdisp, y + ydisp))
            lineDic[269 - i].append((x - xdisp, y - ydisp))
            lineDic[270 + i].append((x + xdisp, y - ydisp))

        # Draws all additional lines
        # for point in points:
        #     ydisp = abs(point[1] - y)
        #     xdisp = abs(point[0] - x)

        #     315 - 360
        #     img[y - ydisp, x + xdisp, 0] = 0
        #     img[y - ydisp, x  + xdisp, 1] = 0
        #     img[y - ydisp, x  + xdisp, 2] = 255

        #     135 - 180
        #     img[y + ydisp, x - xdisp, 0] = 0
        #     img[y + ydisp, x  - xdisp, 1] = 0
        #     img[y + ydisp, x  - xdisp, 2] = 255

        #     180 - 225
        #     img[y - ydisp, x - xdisp, 0] = 0
        #     img[y - ydisp, x  - xdisp, 1] = 0
        #     img[y - ydisp, x  - xdisp, 2] = 255

        #     xdisp = abs(point[1] - y)
        #     ydisp = abs(point[0] - x)

        #     270 - 315
        #     img[y - ydisp, x + xdisp, 0] = 0
        #     img[y - ydisp, x  + xdisp, 1] = 0
        #     img[y - ydisp, x  + xdisp, 2] = 255

        #     90 - 135
        #     img[y + ydisp, x - xdisp, 0] = 0
        #     img[y + ydisp, x  - xdisp, 1] = 0
        #     img[y + ydisp, x  - xdisp, 2] = 255

        #     45 - 90
        #     img[y + ydisp, x + xdisp, 0] = 0
        #     img[y + ydisp, x  + xdisp, 1] = 0
        #     img[y + ydisp, x  + xdisp, 2] = 255

        #     225 - 270
        #     img[y - ydisp, x - xdisp, 0] = 0
        #     img[y - ydisp, x  - xdisp, 1] = 0
        #     img[y - ydisp, x  - xdisp, 2] = 255
    


    # Draws one line
    # for point in lineDic[0]:
    #     img[point[1], point[0], 0] = 0
    #     img[point[1], point[0], 1] = 255
    #     img[point[1], point[0], 2] = 255
    

    # Find line with lowest sum
    bestKey = -1
    bestVal = 9999
    for key, line in lineDic.items():
        val = 0
        for point in line:
            val += gray[point[1], point[0]]
        if val < bestVal:
            bestKey = key
            bestVal = val
    
    # Draw line with lowest sum
    if bestKey != -1:
        for point in lineDic[bestKey]:
            img[point[1], point[0], 0] = 0
            img[point[1], point[0], 1] = 0
            img[point[1], point[0], 2] = 255
    

    # Find max line length
    maxLength = -1
    for key, line in lineDic.items():
        if len(line) > maxLength:
            maxLength = len(line)

    plottedLines = np.zeros((maxLength, 360, 1), np.int8)
    # plots lines
    for key, line in lineDic.items():
        for i, point in enumerate(line):
            plottedLines[maxLength - 1 - i, key] = gray[point[1], point[0]]
    
    # shows plotted lines
    # cv2.imshow('line plot', plottedLines)
    # cv2.waitKey(0)


cv2.imshow('meter', img)
cv2.waitKey(0)
