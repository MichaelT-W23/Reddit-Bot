"""
New file 7/22
"""

from dotenv import load_dotenv
import os
from termcolor import colored as c


load_dotenv()

current_user = int(os.getenv('CURRENT_USER'))

def get_reddit_credentials():
    match current_user:
        case 0:
            user_name = os.getenv("USER_NAME")
            
            print(c(user_name, color="white", on_color="on_yellow"))
            return (
                os.getenv("CLIENT_ID"),
                os.getenv("CLIENT_SECRET"),
                os.getenv("USER_AGENT"),
                os.getenv("REFRESH_TOKEN")
            )
        case 1:
            user_name = os.getenv("ONE_USER_NAME")
            
            print(c(user_name, color="white", on_color="on_magenta"))
            return (
                os.getenv("ONE_CLIENT_ID"),
                os.getenv("ONE_CLIENT_SECRET"),
                os.getenv("ONE_USER_AGENT"),
                os.getenv("ONE_REFRESH_TOKEN")
            )
        case 2:
            user_name = os.getenv("TWO_USER_NAME")
            
            print(c(user_name, color="white", on_color="on_green"))
            return (
                os.getenv("TWO_CLIENT_ID"),
                os.getenv("TWO_CLIENT_SECRET"),
                os.getenv("TWO_USER_AGENT"),
                os.getenv("TWO_REFRESH_TOKEN")
            )
        case 3:
            user_name = os.getenv("THREE_USER_NAME")
            
            print(c(user_name, color="white", on_color='on_cyan'))
            return (
                os.getenv("THREE_CLIENT_ID"),
                os.getenv("THREE_CLIENT_SECRET"),
                os.getenv("THREE_USER_AGENT"),
                os.getenv("THREE_REFRESH_TOKEN")
            )
        case _:
            print(c("USER NOT FOUND", color="white", on_color='on_red'))
            print(c("SET CURRENT_USER in .env", color="white", on_color='on_red'))
            exit(0)