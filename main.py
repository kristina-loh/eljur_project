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
import os.path

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
    
    #вся вот эта функция абсолютно бесполезна и работает как ебучая хуйня:)):):):):):)
    # def get_profile(self):
    #     profile_info = EljurApp().profile_info
    #     Config.read(EljurApp().get_application_config())
    #     login = Config.get('signin', 'login')
    #     password = Config.get('signin', 'password')
    #     payload = {
    #         'phone': login,
    #         'password': password,
    #         'remember': False,
    #     } 
    #     token = requests.session().post('https://shk24.ru/api/v1/auth/login', json = payload).json()['accessToken']
    #     url = 'https://shk24.ru/api/v1/users/1646/profile'
    #     profile = requests.session().get(url, auth=BearerAuth(token)).json()
        
    #     profile_info['full_name'] = profile['last_name'] + ' ' + profile['first_name']
    #     profile_info['class'] = profile['class_name']



    def read_profile(self):
        with open('profile.json', 'r') as f:
            profile = json.load(f)
        full_name = profile['last_name'] + ' ' + profile['first_name']
        return full_name

    def auth(self):
        login_input = MDApp.get_running_app().root.auth_screen.login_input
        password_input = MDApp.get_running_app().root.auth_screen.password_input
        error_label = MDApp.get_running_app().root.auth_screen.error

        if login_input.text == '' or password_input.text == '':
            error_label.text = 'Поле Пароль/Телефон обязательно для заполнения.'

        else:
            session = requests.session()
            payload = {
                'phone': login_input.text,
                'password': password_input.text,
                'remember': 'False'
            }
            req = session.post('https://shk24.ru/api/v1/auth/login', json = payload)
            


        # if self.config.get('signin', 'authorize') == 'False':
        #     self.config.set('signin', 'login', MDApp.get_running_app().root.login_input.text)
        #     self.config.set('signin', 'password', MDApp.get_running_app().root.password_input.text)
        #     self.config.set('signin', 'authorize', 'True')
        #     self.config.write()
        # else:
        #     MDApp.get_running_app().root.password_input.text = self.config.get('signin', 'password')
        #     MDApp.get_running_app().root.login_input.text = self.config.get('signin', 'login')
        # payload = {
        #     'phone': MDApp.get_running_app().root.login_input.text,
        #     'password': MDApp.get_running_app().root.password_input.text,
        #     'remember': False,
        # }
        # session = requests.session()
        # r = session.post('https://shk24.ru/api/v1/auth/login', json = payload)
        # if str(r) == '<Response [422]>':
        #     MDApp.get_running_app().root.error_label.text = 'Имя пользователя и пароль не совпадают.'
        #     MDApp.get_running_app().root.error_label.color = (255/255, 20/255, 83/255, 1)
           
        # elif str(r) == '<Response [200]>':
        #    MDApp.get_running_app().root.error_label.text = 'Успешно'

        #сюда проверку авторизации вставить надо
        #load_profile(get_token('9832655739', 'mamasha228'))
        # self.root.current = 'Eljur'


    # def on_start(self):
    #     print(EljurApp().profile_info)
        
    #     self.get_profile()
    #     print(EljurApp().profile_info)

    def build(self):
        # #и сюда тож проверку авторизации(но чо сюда не факт возможно on_start)
        # self.theme_cls.primary_palette = "Pink"
        # self.theme_cls.theme_style = "Dark"
        return Builder.load_file('eljur.kv')



EljurApp().run()