import random

def get_reponse(message:str) -> str:
    p_message = message.lower()

    if p_message == 'Ping':
        return 'Hello world'
    
    if p_message == '!help':
        return 'Oskour'

        return 'Aled'