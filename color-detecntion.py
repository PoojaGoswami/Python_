import cv2
import pandas as pd
import argparse

ap = argparse.ArgumentParser()

ap.add_argument('-i', '--image', required=True, help='Image Path')

args = vars(ap.parse_args())

# read image
image_path = args['image']

img = cv2.imread(image_path)

# declaring global variable
clicked = False
xpos = ypos = r = g = b = 0

#Reading csv file with pandas
# and giving names to each column

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header= None)


# formula to calculate distance
# d = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor)
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))

        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]

    return cname


#function to get x, y co ordinates if mouse doudle clicked
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g , r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = image[y, x]

        b = int(b)
        g = int(g)
        r = int(r)


# Set a mouse callback event on a window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


while (1):
    cv2.imshow('image', img)

    if (clicked):

        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display ( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R= ' + str(r) + ' G= ' + str(g) + ' B=' + str(b)

        #cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool) )

        cv2.putText(img, text,(50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)

        if (r+g+b) >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
