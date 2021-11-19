from data.jsndrop.jsn_drop_service import jsnDrop
from time import gmtime  #  gmt_time returns UTC time struct  
from datetime import datetime
import os
import hashlib

class UserManager(object):
    current_user = None
    current_pass = None
    current_status = None
    current_screen = None
    chat_list = []
    chat_thread = None
    stop_thread = False
    this_user_manager = None
    thread_lock = False
    jsn_tok = "74c07043-ce1d-4a68-8c34-fd24639d439f"
    latest_time = None



    def now_time_stamp(self):
        time_now = datetime.now()
        time_now.timestamp()
        return time_now.timestamp()



    def __init__(self) -> None:
        super().__init__()

        self.jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")

        result = self.jsnDrop.create("tblUser",{"PersonID PK":('X'*50),
                                                "Email":('X'*50),
                                                "Password":('X'*50),
                                                "Status":"STATUS_STRING"})

        result = self.jsnDrop.create("tblChat",{"PersonID PK":('X'*50),
                                                "DESNumber":('X'*50),
                                                "Chat":('X'*255),
                                                "Time": self.now_time_stamp()})
        UserManager.this_user_manager = self



    def register(self, user_id, email, password):
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' OR Email = '{email}'") 
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus): 
            result = self.jsnDrop.store("tblUser",[{'PersonID':user_id,'Email':email,'Password':password,'Status':'Registered'}])
            UserManager.currentUser = user_id
            UserManager.current_status = 'Logged Out'
            result = "Registration Success"
        else:
            result = "User Already Exists"

        return result



    def login(self, user_id, password):
        result = None
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' AND Password = '{password}'") 
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus): 
            result = "Login Fail"
            UserManager.current_status = "Logged Out"
            UserManager.current_user = None
        else:
            UserManager.current_status = "Logged In"
            UserManager.current_user = user_id
            UserManager.current_pass = password
            api_result = self.jsnDrop.store("tblUser",[{"PersonID":user_id,"Password":password,"Status":"Logged In"}])
            result = "Login Success"
        return result



    def set_current_DES(self, DESScreen):
        result = None
        if UserManager.current_status == "Logged In":
            UserManager.current_screen = DESScreen
            result = "Set Screen"
        else:
            result = "Log in to set the current screen"
        return result



    def chat(self,message):
        result = None
        if UserManager.current_status != "Logged In":
            result = "You must be logged in to chat"
        elif UserManager.current_screen == None:
            result = "Chat not sent. A current screen must be set before sending chat"
        else: 
            user_id = UserManager.current_user
            des_screen = UserManager.current_screen
            api_result = self.jsnDrop.store("tblChat",[{'PersonID':user_id,
                                                        'DESNumber':f'{des_screen}',
                                                        'Chat':message,
                                                        'Time': self.now_time_stamp()}])
            if "ERROR" in api_result :
                result = self.jsnDrop.jsnStatus
            else:
                result = "Chat sent"

        return result



    def get_chat(self):
        result = None

        if UserManager.current_status == "Logged In":
            des_screen = UserManager.current_screen  
            if not(des_screen is None):
                api_result = self.jsnDrop.select("tblChat",f"DESNumber = '{des_screen}'")
                if not ('DATA_ERROR' in api_result) :
                    UserManager.chat_list = self.jsnDrop.jsnResult
                    result = UserManager.chat_list

        return result


    '''
    def logout(self):
        result = "Must be 'Logged In' to 'LogOut' "
        if UserManager.current_status == "Logged In":
            api_result = self.jsnDrop.store("tblUser",[{"PersonID": UserManager.current_user,
                                                        "Password": UserManager.current_pass,
                                                        "Status":"Logged Out"}])
            if not("ERROR" in api_result):
                UserManager.current_status = "Logged Out"
                result = "Logged Out"
            else:
                result = self.jsnDrop.jsnStatus

        return result
    '''