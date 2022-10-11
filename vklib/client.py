import requests
from . import Api

class VK:
    oauth_api_base="https://oauth.vk.com/"
    api_version=5.131
    access_token=None
    __id=-1

    def __init__(self,app_id,app_secret,scopes=5059598):
        self.app=app_id,app_secret
        self.scopes=scopes
    
    def __format_clientinfo(self):
        return "client_id={}&client_secret={}".format(*self.app)
    
    def auth(self, username, password):
        url = self.oauth_api_base+"token?grant_type=password&" + \
            self.__format_clientinfo() + "&" + \
            "username={}&password={}".format(username,password) + "&" + \
            "v={}".format(self.api_version) + "&" \
            "scopes={}".format(self.scopes)
        req=requests.get(url)
        data=req.json()
        if data.get("error"):
            print("ERROR LOGIN: UNIMPLEMENTED")
        self.access_token=data.get("access_token")
        self.__id=data.get("user_id")
    
    @property
    def id(self):
        return self.__id

    @property
    def isAuth(self):
        return self.access_token!=None and self.__id > 0
    
    @property
    def api(self):
        return VKApiRunner(self)

class VKApiRunner:
    def __init__(self, vk, method=""):
        self.vk=vk
        self.method=method

    def __getattribute__(self, __name: str):
        d=object.__getattribute__(self, "method").split(".")
        if d[0]=="":
            d=[]
        return type(self)(
            object.__getattribute__(self, "vk"),
            ".".join([*d, __name])
        )
    def __call__(self, **kwargs):
        return Api.post(
            object.__getattribute__(self, "vk").access_token,
            object.__getattribute__(self, "method"),
            object.__getattribute__(self, "vk").api_version,
            **kwargs
        )