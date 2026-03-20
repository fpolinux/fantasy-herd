import cv2

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: {x}, {y}")

img = cv2.imread(r"C:\Users\nansh\Documents\Python\fantasy_herd\img\cow_243.png")
cv2.imshow('Mapping', img)
cv2.setMouseCallback('Mapping', click_event)
cv2.waitKey(0)