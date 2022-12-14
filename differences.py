from skimage.metrics import structural_similarity
import cv2
import numpy as np

def main():

    primero = cv2.imread('firma.jpg')
    segundo = cv2.imread('firmaccR.jpg')
    
    primero_gray = cv2.cvtColor(primero, cv2.COLOR_BGR2GRAY)
    segundo_gray = cv2.cvtColor(segundo, cv2.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(primero_gray, segundo_gray, full=True)
    print("Porcentaje de similaridad: {:.4f}%".format(score * 100))

    diff = (diff * 255).astype("uint8")
    diff_box = cv2.merge([diff, diff, diff])

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(primero.shape, dtype='uint8')
    filled_segundo = segundo.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(primero, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(segundo, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (255,255,255), -1)
            cv2.drawContours(filled_segundo, [c], 0, (0,255,0), -1)

    cv2.imshow('primero', primero)
    cv2.imshow('segundo', segundo)
    cv2.imshow('diff_box', diff_box)
    cv2.imshow('mask', mask)
    cv2.imshow('filled segundo', filled_segundo)
    cv2.waitKey()
    return 0

main()