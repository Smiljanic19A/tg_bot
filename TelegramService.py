import telebot
import random

class TelegramService:

    def __init__(self):
        self.bot_token = "7246431038:AAHeRM0kTy9bFwyO7-BK0811m54ZVMx-aEQ"
        self.bot = telebot.TeleBot(self.bot_token)
        self.chat_id = "-4558240587"


    def send_message(self, chain, name, link):
        message = self.build_message(random.randint(1, 4), chain, name, link)
        self.bot.send_message(self.chat_id, message)

    def build_message(self, id, chain, name, link):
        if id == 1:
            return f""" 
            New Alpha on {chain} Boyz:\nBuy NOW\n{link}
            """
        elif id == 2:
            return f""" 
            Blessing you all with a runner on {chain}:\nBuy or regret it \n{link}
            """
        elif id == 3:
            return f""" 
            Lets go to the moon boyz: \nOn {chain}\nBuy NOW \n{link}
            """
        elif id == 4:
            return f""" 
            Who wants to GM on {chain}:\nLFG\n{link}
            """


    
    

