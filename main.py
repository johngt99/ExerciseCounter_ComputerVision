from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (400,700) # size of the window

Builder.load_file('main.kv') # gets display styles from main.kv file


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
    pass


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


