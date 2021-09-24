from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen , ScreenManager
from datetime import datetime
import json,glob,random
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
Builder.load_file('Design.kv')
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current="signup_screen"
    def logged_in(self,uname,pword):
        with open("Data.json") as file:
            users=json.load(file)
        if uname in users and users[uname]["password"]==pword:
            self.manager.transition.direction = "left"
            self.manager.current="login_screen_success"
        else :
            self.ids.wrong_password.text= "Incorrect Credentials"
    def forgot(self):
        self.manager.current="forgot_password"
class RootWidget(ScreenManager):
    pass
class SignUpScreen(Screen):
    def add_entry(self,user,password):
        with open("Data.json") as file:
            users=json.load(file)

        users[user]={'username': user,'password': password,'created': datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}

        with open("Data.json",'w') as file:
            json.dump(users,file)
            self.manager.transition.direction = "left"
            self.manager.current="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def login_page(self):
        self.manager.transition.direction= "right"
        self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"
    def get_quote(self,feel):
        feel=feel.lower()
        available_feelings=glob.glob("quotes/*txt")
        available_feelings=[Path(filename).stem for filename in available_feelings]
        if feel in available_feelings:
            with open(f"quotes\{feel}.txt",encoding="utf8") as file:
                quotes= file.readlines()
                self.ids.quote.text=random.choice(quotes)
        else : self.ids.quote.text="Enter Suggested Choice Only"
class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass
class ForgotPasswordScreen(Screen):
    def go_to_login(self):
        self.manager.current="login_screen"
    def go_to_signup(self):
        self.manager.current="signup_screen"


class MainApp(App):
    def build(self):
        return RootWidget()
if __name__== "__main__" :
    MainApp().run()

