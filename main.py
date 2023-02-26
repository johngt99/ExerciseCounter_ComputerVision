from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Define our different screens
class MainPage(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

# Designate our .kv file > Design file
kv = Builder.load_file('styles.kv')

class AwesomeApp(App):
    def build(self):
        return kv
    
if __name__ == '__main__':
    AwesomeApp().run()


