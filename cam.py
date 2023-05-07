import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("asdfasdf")

img_counter = 0

while True:
    ret, frame = cam.read()

    if not ret:
        break

    cv2.imshow('test', frame)

    k = cv2.waitKey(1)

    if k%256 == 27:
        break

    elif k%256 == 32:
        img_name = f'frame_{img_counter}'
        cv2.imwrite(img_name, frame)
        img_counter += 1

cam.release()

cam.destroyAllWindows()
