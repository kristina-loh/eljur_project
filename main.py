from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivy.factory import Factory
from kivymd.app import MDApp
from kivymd.uix.scrollview import MDScrollView
from kivy.config import ConfigParser, Config
from  kivymd.uix.screenmanager import MDScreenManager
import requests
import json



def get_token(login, password):
    payload = {
        'phone': login,
        'password': password,
        'remember': False,
    } 
    token = requests.session().post('https://shk24.ru/api/v1/auth/login', json = payload).json()['accessToken']
    return token



def load_profile(token):
    url = 'https://shk24.ru/api/v1/users/1646/profile'
    profile = requests.session().get(url, auth=BearerAuth(token)).json()
    with open("profile.json", "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=2, ensure_ascii=False) 




class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class EljurApp(MDApp):   
    theme_cls = ThemeManager()
    
    def build_config(self, config):
        config.setdefaults(
            'signin',   {
            'login': '',
            'password': '',
            'authorize': 'False'
            }
        )



    def read_profile(self):
        with open('profile.json', 'r') as f:
            profile = json.load(f)
        full_name = profile['last_name'] + ' ' + profile['first_name']
        return full_name

    def auth(self):
        login_input = MDApp.get_running_app().root.auth_screen.login_input
        password_input = MDApp.get_running_app().root.auth_screen.password_input
        error_label = MDApp.get_running_app().root.auth_screen.error_label

        if login_input.text == '' or password_input.text == '':
            error_label.text = 'Поле Пароль/Телефон обязательно для заполнения.'
        else:
            session = requests.session()
            payload = {
                'phone': login_input.text,
                'password': password_input.text,
                'remember': 'False'
            }
            try:
                req = session.post('https://shk24.ru/api/v1/auth/login', json = payload)
                print('try')
                if req.status_code == 422:
                    error_label.text = 'Имя пользователя и пароль не совпадают.'
                else:
                    self.config.set('signin', 'login', login_input.text)
                    self.config.set('signin', 'password', password_input.text)
                    self.config.set('signin', 'authorize', 'True')
                    self.config.write()
                    self.root.current = 'Eljur'
            except requests.exceptions.ConnectionError:
                error_label.text = 'Отсутствует подключение к интернету'
    
    def on_start(self):
        config = self.config
        if config.get('signin', 'authorize') == 'True':
            self.root.current = 'Eljur'

    def build(self):
        # #и сюда тож проверку авторизации(но чо сюда не факт возможно on_start)
        # self.theme_cls.primary_palette = "Pink"
        # self.theme_cls.theme_style = "Dark"
        return Builder.load_file('eljur.kv')



EljurApp().run()