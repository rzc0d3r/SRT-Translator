import colorama

import os

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class MenuAction(object):
    def __init__(self, title, func):
        self.title = title
        self.function = func

    def render_title(self):
        return self.title
    
    def run(self):
        if isinstance(self.function, ViewMenu):
            self.function.view()
        else:
            self.function()

class OptionAction(object):
    def __init__(self, args, title, action, args_names, choices=[], default_value=None):
        self.args = args
        self.title = title
        self.action = action
        self.value = default_value
        self.choices = choices
        self.args_names = args_names
        
    def render_title(self):
        if self.action in ['store_true', 'choice']:
            return f'{self.title} (selected: {colorama.Fore.YELLOW}{self.value}{colorama.Fore.RESET})'
        elif self.action == 'manual_input':
            return f'{self.title} (saved: {colorama.Fore.YELLOW}{self.value}{colorama.Fore.RESET})'
        elif self.action == 'bool_switch':
            if self.args[self.args_names.replace('-', '_')]:
                return f'{self.title} {colorama.Fore.GREEN}(enabled){colorama.Fore.RESET}'
            return f'{self.title} {colorama.Fore.RED}(disabled){colorama.Fore.RESET}'
        
    def run(self):
        if self.action == 'bool_switch':
            self.args[self.args_names.replace('-', '_')] = not self.args[self.args_names.replace('-', '_')]
            return True
        while True:
            clear_console()
            print(self.title+'\n')
            menu_items = []
            if self.choices != []:
                menu_items = self.choices
            else:
                menu_items = self.args_names
            if self.action != 'manual_input':
                for index in range(0, len(menu_items)):
                    menu_item = menu_items[index]
                    print(f'{index+1} - {menu_item}')
                print()
            try:
                if self.action == 'manual_input':
                    self.value = input('>>> ').strip()
                    self.args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                    break
                index = int(input('>>> ').strip()) - 1
                self.value = menu_items[index]
                if index in range(0, len(menu_items)):
                    if self.action == 'store_true':
                        for args_name in self.args_names: # self.args_names is list
                            self.args[args_name.replace('-', '_')] = False
                        self.args[self.value.replace('-', '_')] = True # self.value == args_name
                    elif self.action == 'choice':
                        self.args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                    break
            except ValueError:
                pass

class ViewMenu(object):
    def __init__(self, title):
        self.title = title
        self.items = []

    def add_item(self, menu_action_object: MenuAction):
        self.items.append(menu_action_object)
    
    def view(self):
        while True:
            clear_console()
            print(self.title+'\n')
            for item_index in range(0, len(self.items)):
                item = self.items[item_index]
                print(f'{item_index+1} - {item.render_title()}')
            print()
            try:
                selected_item_index = int(input('>>> ')) - 1
                if selected_item_index in range(0, len(self.items)):
                    print(self.items[selected_item_index].run())
            except ValueError:
                pass