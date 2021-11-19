from data.jsndrop.jsn_drop_service import jsnDrop
from data.user_manager import UserManager
user_manager = UserManager()
jsn_tok = "74c07043-ce1d-4a68-8c34-fd24639d439f"
jsnDrop = jsnDrop(jsn_tok,"https://newsimland.com/~todd/JSON")

#jsnDrop.select("tblChat",f"PersonID = '123'")
#jsnDrop.select("tblChat",f"DESID = 'placeholder1.csv'")

jsnDrop.store("tblChat",[{'PersonID':'456',
                                                        'DESID':'placeholder1.csv',
                                                        'Chat':'random',
                                                        'Time': '1637297395.7777'}])

jsnDrop.store("tblChat",[{'PersonID':'456',
                                                        'DESID':'placeholder1.csv',
                                                        'Chat':'crazy',
                                                        'Time': '1637297396.6666'}])

jsnDrop.store("tblChat",[{'PersonID':'456',
                                                        'DESID':'placeholder1.csv',
                                                        'Chat':'wowee',
                                                        'Time': '1637297397.5555'}])


user_manager.current_screen = "placeholder1.csv"
result = jsnDrop.select("tblChat",f"DESID = '{user_manager.current_screen}'")
print(result)
messages = ""
sorted_chats = sorted(result, key = lambda i : i['Time'] )
print(sorted_chats)




