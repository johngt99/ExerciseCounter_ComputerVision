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

Builder.load_file('main.kv') # gets display styles from main.kv file

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
    pass

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



