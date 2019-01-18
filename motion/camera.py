import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out_image = cv2.VideoWriter(
            'recording.avi', fourcc, 20.0, (640, 480))

    def mask_image(self, lower, upper):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        cv2.flip(mask, 1)
        _, self.mask = cv2.threshold(
            mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return self.mask

    def give_max_contour(self):
        im2, contours, hierarchy = cv2.findContours(
            self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return max(contours, key=cv2.contourArea)

    def give_contour_area(self, contour):
        contour_area = cv2.contourArea(contour)
        print("Contour Area = ", contour_area)
        return contour_area

    def centroid_if_object_present(self):
        contour = self.give_max_contour()
        contour_area = self.give_contour_area(contour)

        if contour_area > 20000:
            print("OBJECT PRESENT")
            x, y, w, h = cv2.boundingRect(contour)

            # TODO: Remove this line.
            cv2.rectangle(self.image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cx, cy = (x + w/2), (y + h/2)
            self.draw_centroid(self.image, cx, cy)
            return cx, cy

        return False

    def should_touch_manoeuver(self):
        contour = self.give_max_contour()
        contour_area = self.give_contour_area(contour)
        if contour_area > 420000:
            return True
        return False

    def draw_centroid(self, overlay, cx, cy):
        cv2.circle(overlay, (int(cx), int(cy)), 20, (0, 0, 255), -1)

    def read(self):
        self.rec, self.image = self.cap.read()
        return self.image

    def tearDown(self):
        """
        Call as API to release camera.
        """
        self.cap.release()
        self.out_image.release()
        cv2.destroyAllWindows()
