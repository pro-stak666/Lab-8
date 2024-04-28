import cv2
import time


def task1():
    img = cv2.imread('images/variant-6.png')
    w, h = img.shape[:2]
    resized_img = cv2.resize(src=img, dsize=(w * 2, h * 2), fx=2, fy=2)
    cv2.imshow('resized_img', resized_img)


def task2():
    cap = cv2.VideoCapture("video.mp4")
    down_points = (640, 480)
    i = 0
    counter_right = 0
    counter_left = 0
    last_pos = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh,
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if i % 5 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
                if a <= 320 and last_pos != -1:
                    last_pos = -1
                    counter_left += 1
                elif a > 320 and last_pos != 1:
                    last_pos = 1
                    counter_right += 1
                print(a, last_pos)
            cv2.putText(frame, f'{counter_left}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)
            cv2.putText(frame, f'{counter_right}', (590, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()


if __name__ == '__main__':
    # task1()
    task2()

cv2.waitKey(0)
cv2.destroyAllWindows()
