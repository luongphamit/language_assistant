
import random

class CommonLibs():
    def __init__(self) -> None:
        self.space = "="*21
    def get_help_content(self, name):
        return f"""
Hello <b>{name}</b>,

How to use bot
/help - Show this menu
{self.space}

"""