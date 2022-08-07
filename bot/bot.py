# v1

import utils
from handlers import *
from header import *


bot.register_message_handler(commands=["start"], 
                             func=start, 
                             callback="none")


bot.register_message_handler(commands=["help"], 
                             func=help, 
                             callback="none")


bot.register_message_handler(commands=["encrypt"], 
                             func=encrypt, 
                             callback="none")


bot.register_message_handler(commands=["decrypt"], 
                             func=decrypt, 
                             callback="none")




if __name__ == "__main__":
    try:
        print("BOT STARTED")
        utils.log.info("BOT STARTED")
        bot.infinity_polling()
    except Exception as e:
        utils.log.error(e)
        print(e)
