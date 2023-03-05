import cv2
import mediapipe as mp
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

Window.size = (400,700) # size of the window

Builder.load_file('styles.kv') # gets display styles from main.kv file

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class MainPage(Screen): # Initial Screen
    pass


class PageOne(Screen): # Page 1 
    num_one = ObjectProperty(None)
    num_two = ObjectProperty(None)

    def calculate(self):
        result = int(self.num_one.text) * int(self.num_two.text)
        self.parent.get_screen('result').ids.result_label.text = str(result)
        self.parent.current = 'result'

class Result(Screen): # Screen to show result of Page 1 action
    result_label = ObjectProperty(None)
    
class PageTwo(Screen):  # Page 2
    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands.Hands()
        Clock.schedule_interval(self.update, 1.0/30.0)

    def on_leave(self):
        self.capture.release()
        self.mp_hands.close()

    def update(self, dt):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame,1) # Mirror the image so it looks correct
        if ret:
            results = self.mp_hands.process(frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for landmark in hand_landmarks.landmark:
                        print(landmark)

            # convert frame to texture
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.image.texture = texture

class PageThree(Screen):  # Page 3
    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.mp_pose = mp.solutions.pose.Pose()
        self.mp_holistic = mp.solutions.holistic.Holistic()
        self.in_squat = False
        self.squat_count = 0
        self.prev_l_hip_y = None
        Clock.schedule_interval(self.update, 1.0/30.0)

    def on_leave(self):
        self.capture.release()
        self.mp_pose.close()
        self.mp_holistic.close()

    def update(self, dt):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)
        if ret:
            # process pose estimation
            results_pose = self.mp_pose.process(frame)
            pose_landmarks = results_pose.pose_landmarks

            # process holistic estimation
            results_holistic = self.mp_holistic.process(frame)
            holistic_landmarks = results_holistic.pose_landmarks

            # get landmarks for left hip and left knee
            if pose_landmarks is not None and holistic_landmarks is not None:
                l_hip_x = int(
                    pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP].x * frame.shape[1])
                l_hip_y = int(
                    pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP].y * frame.shape[0])
                l_knee_x = int(
                    pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE].x * frame.shape[1])
                l_knee_y = int(
                    pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE].y * frame.shape[0])
                l_hip_z = holistic_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_HIP].z
                l_knee_z = holistic_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_KNEE].z

                # check if person is in squat position
                connections = mp.solutions.pose.POSE_CONNECTIONS
                if pose_landmarks is not None and holistic_landmarks is not None:
                    l_hip_idx = mp.solutions.pose.PoseLandmark.LEFT_HIP.value
                    l_knee_idx = mp.solutions.pose.PoseLandmark.LEFT_KNEE.value
                    if pose_landmarks.landmark[l_hip_idx].visibility > 0 and pose_landmarks.landmark[l_knee_idx].visibility > 0:
                        if (l_hip_idx, l_knee_idx) in connections and l_hip_z > l_knee_z:
                            if not self.in_squat:
                                self.in_squat = True
                                if self.prev_l_hip_y is not None and l_hip_y < self.prev_l_hip_y:
                                    self.squat_count += 1
                                    self.ids.squat_label.text = f"Squat count: {self.squat_count}"
                                    print(f"Squat count: {self.squat_count}")
                            self.prev_l_hip_y = l_hip_y
                        else:
                            self.in_squat = False

                # display landmarks
                for lm in pose_landmarks.landmark:
                    x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                # display frame
                buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                buf = buf.tostring()
                texture = Texture.create(
                    size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.ids.image.texture = texture

class ScreenManagement(ScreenManager): # Manages all the pages
    pass


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark" # Background Dark
        self.theme_cls.primary_palette = "DeepPurple" # Details Purple 
        sm = ScreenManagement() # define ScreenManager as 'sm'
        sm.add_widget(MainPage(name='main'))
        sm.add_widget(PageOne(name='page_one'))
        sm.add_widget(PageTwo(name='page_two'))
        sm.add_widget(PageThree(name='page_three'))
        sm.add_widget(Result(name='result'))
        return sm


if __name__ == '__main__':
    MyApp().run()




