import json


class inline_keyboard_button():
    """
    Объявление клавиши для клавиатуры: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """


    def __init__(self, text: str, url = None, login_url = None, callback_data = None, switch_inline_query = None, switch_inline_query_current_chat = None, callback_game = None, pay = None):
        self.text = text
        
        if url:
            self.url = url
        elif login_url:
            self.login_url = login_url
        elif callback_data:
            self.callback_data = callback_data
        elif switch_inline_query:
            self.switch_inline_query = switch_inline_query
        elif switch_inline_query_current_chat:
            self.switch_inline_query_current_chat = switch_inline_query_current_chat
        elif callback_game:
            self.callback_game = callback_game
        elif pay:
            self.pay = pay

        else:
            self.url = 'https://eesmth.ml/@canarybot'


    def __call__(self):
        return self.__dict__


class reply_keyboard_button():
    """
    Объявление клавиши для клавиатуры: https://core.telegram.org/bots/api#keyboardbutton
    """


    def __init__(self, text: str, request_contact = False, request_location = False, request_poll = None):
        self.text = text
        
        if request_contact:
            self.request_contact = request_contact

        if request_location:
            self.request_location = request_location

        if request_poll:
            self.request_poll = request_poll


    def __call__(self):
        return self.__dict__

class inline_keyboard():
    """
    Объявление клавиатуры, см. https://core.telegram.org/bots/api#inlinekeyboardbutton
    """


    def __init__(self, lines = 1):
        self.buttons = [[]]


    def __call__(self):
        for i in self.buttons:
            if len(i) == 0:
                self.buttons.remove(i)

        return json.dumps(
            {
                'inline_keyboard': self.buttons
            }
        )


    def add_button(self, button=None):
        self.buttons[len(self.buttons)-1].append(button)


    def add_line(self):
        self.buttons.append([])

class reply_keyboard():
    """
    Объявление клавиатуры, см. https://core.telegram.org/bots/api#replykeyboardbutton
    """


    def __init__(self, lines:int = 1, resize_keyboard:bool = False, one_time_keyboard:bool = False, selective:bool = False):
        self.buttons = [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective


    def __call__(self):
        for i in self.buttons:
            if len(i) == 0:
                self.buttons.remove(i)
        return json.dumps(
            {
                'keyboard': self.buttons,
                'resize_keyboard': self.resize_keyboard,
                'one_time_keyboard': self.one_time_keyboard,
                'selective': self.selective
            }
        )

        
    def add_button(self, button=None):
        self.buttons[len(self.buttons)-1].append(button)


    def add_line(self):
        self.buttons.append([])


class reply_keyboard_remove():
    """
    Отправьте keyboard.reply_keyboard_remove(), чтобы убрать клавиатуру, см. https://core.telegram.org/bots/api#replykeyboardremove
    """
    def __init__(self, selective:bool = False):
        self.selective = selective


    def __call__(self):
        return json.dumps(
            {
                'remove_keyboard': True,
                'selective': self.selective
            }
        )

if __name__ == "__main__":
    keyboard = inline_keyboard()
    keyboard.add_button(inline_keyboard_button('test')())


    print(keyboard.get())