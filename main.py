from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction='left'
        self.manager.current="sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users=json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = 'login_screen_success'
        else:
            self.ids.login_info.text = "Wrong username or password."



class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
    def get_quote(self, feeling):
        feel = feeling.lower()
        feelings=glob.glob("quotes/*txt")
        
        feelings = [Path(filename).stem for filename in
                     feelings]
        if feel in feelings:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text ="There are only three feelings. Happy, sad and unloved. Try again."

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class SignUpScreen(Screen):
    def add_user(self, username, password, vpassword):
        with open("users.json") as file:
            users=json.load(file)
            if password == vpassword:
                users[username] = {'username': username, 'password': password,
                                    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                self.manager.current="sign_up_success"
                
                with open("users.json", 'w') as file:
                    json.dump(users, file)
            elif password != vpassword:
                self.ids.sign_up_info.text = "Passwords did not match."
            else:
                pass
    def go_back(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class SignSuccess(Screen):
    def go_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class RetrievePasswordScreen(Screen):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()