class Selector:
    import keyboard, colorama, os
    colorama.init()
    options = []
    menuopt_return = ''
    menucur_option = 0
    menuout_i = 0
    menuselected = 0
    title = ''
    menurunning = False
    def clear():
        if Selector.os.name == 'nt':
            Selector.os.system('cls')
        else:
            Selector.os.system('clear')
    def menudec_option(args):
        global menucur_option, options, menuout_i, menurunning
        if menurunning == True:
            if not menucur_option == len(Selector.options) - 1:
                menucur_option += 1
            else:
                menucur_option = 0
            Selector.menureload()
    def menuinc_option(args):
        global menucur_option, options, menuout_i, menurunning
        if menurunning == True:
            if not menucur_option == 0:
                menucur_option -= 1
            else:
                menucur_option = len(Selector.options) - 1
            Selector.menureload()
    def menureload():
        Selector.clear()
        print(Selector.colorama.Fore.GREEN + Selector.title + Selector.colorama.Style.RESET_ALL)
        global menuout_i, menuselected, menucur_option
        if menucur_option > len(Selector.options):
            menucur_option = 0
        for menuout_i in range(0, len(Selector.options)):
            if menuout_i == menucur_option:
                print(Selector.colorama.Fore.BLUE, Selector.options[menuout_i], Selector.colorama.Style.RESET_ALL)
                menuselected = menuout_i
            else:
                print(Selector.options[menuout_i])
    def showmenu():
        global menuout_i, menurunning, menucur_option
        menurunning = True
        menucur_option = 0
        Selector.menureload()
        Selector.keyboard.wait('enter')
        menurunning = False
        input()
        return Selector.options[menuselected]
        clear()
    keyboard.on_press_key('down', menudec_option)
    keyboard.on_press_key('up', menuinc_option)
if __name__ == "__main__":
    Selector.title = "Choose a number:"
    Selector.options = ['One', 'Two', 'Three', 'Four']
    Selector.showmenu()
    