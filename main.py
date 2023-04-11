import cv2
import mediapipe as mp
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.texture import Texture

Window.size = (400, 700)  # phone size

Builder.load_file('styles.kv')  # gets display styles from styles.kv file

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class MainPage(Screen):  # Initial Screen
    pass


class PageOne(Screen):  # Page 1
    def on_enter(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.texture = Texture.create(size=(640, 480))
        # self.texture.flip_vertical()

        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0/60.0)

        self.counter = 0
        self.rep = [0, 0]
        self.position = ""

    def on_leave(self):
        Clock.unschedule(self.update)
        self.capture.release()

    def calculate_angle(a, b, c):
        a = np.array(a)  # first
        b = np.array(b)  # middle
        c = np.array(c)  # end
        ba = a-b
        bc = c-b

        cosine_angle = np.dot(ba, bc) / \
            (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        if angle > 180.0:  # ajust angle according to the size arm is facing
            angle = 360-angle

        return np.degrees(angle)

    def update(self, dt):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            success, frame = self.capture.read()
            # flip camera to right position
            frame = cv2.flip(frame, 0, dst=None)
            # flip camera to right position
            frame = cv2.flip(frame, 1, dst=None)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                self.landmarks = results.pose_landmarks.landmark
                # get landmarks for arms
                #  RIGHT ARM
                right_shoulder = [self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                  self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_elbow = [self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                               self.landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                right_wrist = [self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                               self.landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_arm_angle = self.calculate_angle(
                    right_shoulder, right_elbow, right_wrist)  # CALCULATES ANGLE / RIGHT ARM

                #  LEFT ARM
                left_shoulder = [self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                left_elbow = [self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              self.landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                left_wrist = [self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              self.landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                left_arm_angle = self.calculate_angle(
                    left_shoulder, left_elbow, left_wrist)

                # check if person is in squat position
                if left_arm_angle < 90 and right_arm_angle < 90:
                    self.position = "DOWN"

                if left_arm_angle > 135 and right_arm_angle > 135:
                    self.position = "UP"

                # ["DOWN", "UP"] = 1 repetition
                if self.position == 'DOWN':
                    if self.rep[0] == 0:
                        self.rep[0] = 'DOWN'

                if self.position == 'UP':
                    if self.rep == ['DOWN', 0]:
                        self.counter += 1
                        print(f"Squat count: {self.counter}")
                        rep = [0, 0]  # reset repetition
            except:
                pass
            # display landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,                                      # connection appearance
                                      mp_drawing.DrawingSpec(
                                          color=(255, 200, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(
                                          color=(0, 255, 255), thickness=5, circle_radius=2)  # joint appearance
                                      )
            if success:
                # display frame
                # Update Kivy texture
                buffer = image.tobytes()
                self.texture.blit_buffer(
                    buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.image.texture = self.texture


class PageTwo(Screen):  # Page 2
    def on_enter(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.texture = Texture.create(size=(640, 480))
        # self.texture.flip_vertical()

        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0/60.0)

        self.counter = 0
        self.rep = [0, 0]
        self.position = ""

    def on_leave(self):
        Clock.unschedule(self.update)
        self.capture.release()

    def calculate_angle(a, b, c):
        a = np.array(a)  # first
        b = np.array(b)  # middle
        c = np.array(c)  # end
        ba = a-b
        bc = c-b

        cosine_angle = np.dot(ba, bc) / \
            (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        if angle > 180.0:  # ajust angle according to the size arm is facing
            angle = 360-angle

        return np.degrees(angle)

    def update(self, dt):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            success, frame = self.capture.read()
            # flip camera to right position
            frame = cv2.flip(frame, 0, dst=None)
            # flip camera to right position
            frame = cv2.flip(frame, 1, dst=None)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                self.landmarks = results.pose_landmarks.landmark
                # get landmarks for arms
                #  RIGHT ARM
                right_shoulder = [self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                  self.landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_hip = [self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                             self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_knee = [self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                              self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                right_side_angle = self.calculate_angle(
                    right_shoulder, right_hip, right_knee)  # CALCULATES ANGLE / RIGHT ARM

                #  LEFT ARM
                left_shoulder = [self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 self.landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                left_hip = [self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                left_knee = [self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                             self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                left_side_angle = self.calculate_angle(
                    left_shoulder, left_hip, left_knee)

                # check if person is in squat position
                if left_side_angle < 75 and right_side_angle < 75:
                    self.position = "DOWN"

                if left_side_angle > 90 and right_side_angle > 90:
                    self.position = "UP"

                # ["DOWN", "UP"] = 1 repetition
                if self.position == 'DOWN':
                    if self.rep[0] == 0:
                        self.rep[0] = 'DOWN'

                if self.position == 'UP':
                    if self.rep == ['DOWN', 0]:
                        self.counter += 1
                        print(f"Squat count: {self.counter}")
                        rep = [0, 0]  # reset repetition
            except:
                pass
            # display landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,                                      # connection appearance
                                      mp_drawing.DrawingSpec(
                                          color=(255, 200, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(
                                          color=(0, 255, 255), thickness=5, circle_radius=2)  # joint appearance
                                      )
            if success:
                # display frame
                # Update Kivy texture
                buffer = image.tobytes()
                self.texture.blit_buffer(
                    buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.image.texture = self.texture


class PageThree(Screen):  # Page 3
    def on_enter(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.texture = Texture.create(size=(640, 480))
        # self.texture.flip_vertical()

        self.capture = cv2.VideoCapture(0)

        Clock.schedule_interval(self.update, 1.0/60.0)

        self.counter = 0
        self.rep = [0, 0]
        self.position = ""

    def on_leave(self):
        Clock.unschedule(self.update)
        self.capture.release()

    def calculate_angle(a, b, c):
        a = np.array(a)  # first
        b = np.array(b)  # middle
        c = np.array(c)  # end
        ba = a-b
        bc = c-b

        cosine_angle = np.dot(ba, bc) / \
            (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        if angle > 180.0:  # ajust angle according to the size arm is facing
            angle = 360-angle

        return np.degrees(angle)

    def update(self, dt):
        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            success, frame = self.capture.read()
            # flip camera to right position
            frame = cv2.flip(frame, 0, dst=None)
            # flip camera to right position
            frame = cv2.flip(frame, 1, dst=None)

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                self.landmarks = results.pose_landmarks.landmark
                # get landmarks for arms
                #  RIGHT ARM
                right_hip = [self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, self.landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                right_knee = [self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, self.landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                right_ankle = [self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,  self.landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_leg_angle = self.calculate_angle(
                    right_hip, right_knee, right_ankle)  # CALCULATES ANGLE / RIGHT ARM

                #  LEFT ARM
                left_hip = [self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, self.landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                left_knee = [self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, self.landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                left_ankle = [self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, self.landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                left_leg_angle = self.calculate_angle(
                    left_hip, left_knee, left_ankle)

                # check if person is in squat position
                if left_leg_angle < 100 and right_leg_angle < 100:
                    self.position = "DOWN"

                if left_leg_angle > 135 and right_leg_angle > 135:
                    self.position = "UP"

                # ["DOWN", "UP"] = 1 repetition
                if self.position == 'DOWN':
                    if self.rep[0] == 0:
                        self.rep[0] = 'DOWN'

                if self.position == 'UP':
                    if self.rep == ['DOWN', 0]:
                        self.counter += 1
                        print(f"Squat count: {self.counter}")
                        rep = [0, 0]  # reset repetition
            except:
                pass
            # display landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,                                      # connection appearance
                                      mp_drawing.DrawingSpec(color=(255, 200, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec( color=(0, 255, 255), thickness=5, circle_radius=2)  # joint appearance
                                      )
            if success:
                # display frame
                # Update Kivy texture
                buffer = image.tobytes()
                self.texture.blit_buffer(
                    buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.image.texture = self.texture


class ScreenManagement(ScreenManager):  # Manages all the pages
    pass


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Background Dark
        self.theme_cls.primary_palette = "DeepPurple"  # Details Purple
        sm = ScreenManagement()  # define ScreenManager as 'sm'
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(PageOne(name='page_one'))
        sm.add_widget(PageTwo(name='page_two'))
        sm.add_widget(PageThree(name='page_three'))
        return sm


if __name__ == '__main__':
    MyApp().run()




