from time import sleep as s

class Colors:
    text_colors = {
                    "BB#":"\033[1m", # Bold/Bright

                    # Dark
                    "W#":"\033[0;37m", # Wihte
                    "R#":"\033[0;31m", # Red
                    "G#":"\033[0;32m", # Green
                    "Y#":"\033[0;33m", # Yellow
                    "B#":"\033[0;34m", # Blue
                    "P#":"\033[0;35m", # Purple
                    "C#":"\033[0;36m", # Cyan
                    "b#":"\033[0;30m", # Black

                    # Light
                    "WL#":"\033[1;37m", # Wihte
                    "RL#":"\033[1;31m", # Red
                    "GL#":"\033[1;32m", # Green
                    "YL#":"\033[1;33m", # Yellow
                    "BL#":"\033[1;34m", # Blue
                    "PL#":"\033[1;35m", # Purple
                    "CL#":"\033[1;36m", # Cyan
                    "bL#":"\033[1;30m", # Gray

                    # Dark
                    "W@":"\033[7m", # bg Wihte
                    "R@":"\033[41m", # bg Red
                    "G@":"\033[42m", # bg Green
                    "Y@":"\033[43m", # bg Yellow
                    "B@":"\033[44m", # bg Blue
                    "P@":"\033[45m", # bg Purple
                    "C@":"\033[46m", # bg Cyan
                    "g@":"\033[47m", # bg Light gray

                    # Light
                    "RL@":"\033[101m", # bg Light Red
                    "GL@":"\033[102m", # bg Light Green
                    "YL@":"\033[103m", # bg Light Yellow
                    "BL@":"\033[104m", # bg Light Blue
                    "PL@":"\033[105m", # bg Light Purple
                    "CL@":"\033[106m", # bg Light Cyan
                    "gL@":"\033[100m", # bg Light Light gray

                    "##":"\033[0m", # Normal
                    "UL#":"\033[4m", # Underlined
                    "B*#":"\033[5m", # Blink
                   }

    @classmethod
    def coloring(cls,text):
        for color_shortcut,color in cls.text_colors.items():
            text = text.replace(color_shortcut,color)
        return text

class Animation:
    def uppercase_and_lowercase_letters(text="uppercase and lowercase letters",lower_text_color="C#",upper_text_color="Y#",time=0.1,repeat=3):
        try:
            text = Colors.coloring(str(text))
            lower_text_color = Colors.coloring(lower_text_color)
            upper_text_color = Colors.coloring(upper_text_color)

            text += " "
            for U in range(repeat):
                for U in range(len(text)):
                    print (lower_text_color+text[:U].lower()+upper_text_color+text[U].upper(),end='\r')
                    s(time)
            print ("")
        except KeyboardInterrupt as k1:
            print (k1)
        except:
            print ("\n[!] Error...\n")
    def loading(text="Loading",text_color="C#",Animated_text="\|/-",Animated_text_color="Y#",time=0.1,repeat=5):
        try:
            text_color = Colors.coloring(text_color)
            Animated_text_color = Colors.coloring(Animated_text_color)

            for L in range(repeat):
                for L in range(len(Animated_text)):
                    print (text_color+text,Animated_text_color+Animated_text[L],end='\r')
                    s(time)
            print ("")
        except KeyboardInterrupt as k2:
            print (k2)
        except:
            print ("\n[!] Error...\n")

    def downloading(Length=30,time=0.1,top_text="                  [Please Wait...]",top_text_color="Y#",left_side_text="Download ",left_side_text_color="Y#",bottom_shape="▒",bottom_shape_color="B#",top_shape="█",top_shape_color="CL#",left_side="┋",left_side_color="B#",right_side="┋",right_side_color="B#",percentage=100,percentage_color="Y#"):
        try:
            top_text_color       = Colors.coloring(top_text_color)
            left_side_text_color = Colors.coloring(left_side_text_color)
            bottom_shape_color   = Colors.coloring(bottom_shape_color)
            top_shape_color      = Colors.coloring(top_shape_color)
            left_side_color      = Colors.coloring(left_side_color)
            right_side_color     = Colors.coloring(right_side_color)
            percentage_color     = Colors.coloring(percentage_color)

            print ("\n"+top_text_color+top_text+"\n")
            if len(left_side_text) >= 0:
                side_text = 0
                side_text += len(left_side_text)
                for i in range(Length):
                    bottom     = bottom_shape_color+bottom_shape*(Length+1+side_text)
                    top        = (top_shape_color+(i)*top_shape)+top_shape
                    percent = i
                    if percent == (Length-1):
                        percent = percentage
                    print (bottom+right_side_color+right_side+" "+percentage_color+"%"+str(percent),end='\r')
                    print (left_side_text_color+left_side_text+left_side_color+left_side+top,end='\r')
                    s(time)
            else:
                pass
            print ("\n\n")
        except KeyboardInterrupt as k3:
            print (k3)
        except:
            print ("\n[!] Error...\n")

    def colors(color='all'):

        c = Colors.coloring

        if color == "all":
            print (c("W#"))
            print ("╭────────────────[Dark]────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ W#  ]  > ",c("[W# Wihte##  ]     │"))
            print ("│  [+] code [ R#  ]  > ",c("[R# Red##    ]     │"))
            print ("│  [+] code [ G#  ]  > ",c("[G# Green##  ]     │"))
            print ("│  [+] code [ Y#  ]  > ",c("[Y# Yellow## ]     │"))
            print ("│  [+] code [ B#  ]  > ",c("[B# Blue##   ]     │"))
            print ("│  [+] code [ P#  ]  > ",c("[P# Purple## ]     │"))
            print ("│  [+] code [ C#  ]  > ",c("[C# Cyan##   ]     │"))
            print ("│  [+] code [ b#  ]  > ",c("[b# Black##  ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
            print ("╭────────────────[Dark]────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ W@  ]  > ",c("[ W@Wihte##  ]     │"))
            print ("│  [+] code [ R@  ]  > ",c("[ R@Red##    ]     │"))
            print ("│  [+] code [ G@  ]  > ",c("[ G@Green##  ]     │"))
            print ("│  [+] code [ Y@  ]  > ",c("[ Y@Yellow## ]     │"))
            print ("│  [+] code [ B@  ]  > ",c("[ B@Blue##   ]     │"))
            print ("│  [+] code [ P@  ]  > ",c("[ P@Purple## ]     │"))
            print ("│  [+] code [ C@  ]  > ",c("[ C@Cyan##   ]     │"))
            print ("│  [+] code [ g@  ]  > ",c("[ g@Gray##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ BB# ]  > ",c("[BB# text##   ]     │"))
            print ("│  [+] code [ B*# ]  > ",c("[B*# text##   ]     │"))
            print ("│  [+] code [ UL# ]  > ",c("[ UL#text##   ]     │"))
            print ("│  [+] code [ ##  ]  > ",c("[## text##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
            print ("╭────────────────[Light]───────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ WL# ]  > ",c("[WL# Wihte##  ]     │"))
            print ("│  [+] code [ RL# ]  > ",c("[RL# Red##    ]     │"))
            print ("│  [+] code [ GL# ]  > ",c("[GL# Green##  ]     │"))
            print ("│  [+] code [ YL# ]  > ",c("[YL# Yellow## ]     │"))
            print ("│  [+] code [ BL# ]  > ",c("[BL# Blue##   ]     │"))
            print ("│  [+] code [ PL# ]  > ",c("[PL# Purple## ]     │"))
            print ("│  [+] code [ CL# ]  > ",c("[CL# Cyan##   ]     │"))
            print ("│  [+] code [ bL# ]  > ",c("[bL# Black##  ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
            print ("╭────────────────[Light]───────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ RL@ ]  > ",c("[ RL@Red##    ]     │"))
            print ("│  [+] code [ GL@ ]  > ",c("[ GL@Green##  ]     │"))
            print ("│  [+] code [ YL@ ]  > ",c("[ YL@Yellow## ]     │"))
            print ("│  [+] code [ BL@ ]  > ",c("[ BL@Blue##   ]     │"))
            print ("│  [+] code [ PL@ ]  > ",c("[ PL@Purple## ]     │"))
            print ("│  [+] code [ CL@ ]  > ",c("[ CL@Cyan##   ]     │"))
            print ("│  [+] code [ gL@ ]  > ",c("[ gL@Gray##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
            # print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # print ("[]  RL#UL#BB#g@ > ",c(" RL#UL#BB#g@Gray##"))
            # print ("[]  R#UL#BB#g@  > ",c(" R#UL#BB#g@Gray##"))
            # print ("code [ BB# ]  > ",c("[BB# UL#text##"))


        elif color == "wihte" or color == "Wihte" or color == "WIHTE":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ BB# ]  > ",c("[BB# text##   ]     │"))
            print ("│  [+] code [ B*# ]  > ",c("[B*# text##   ]     │"))
            print ("│  [+] code [ UL# ]  > ",c("[ UL#text##   ]     │"))
            print ("│  [+] code [ WL# ]  > ",c("[WL# Wihte##  ]     │"))
            print ("│  [+] code [ W#  ]  > ",c("[W# Wihte##  ]     │"))
            print ("│  [+] code [ ##  ]  > ",c("[## text##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "red" or color == "Red" or color == "RED":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ RL# ]  > ",c("[RL# Red##    ]     │"))
            print ("│  [+] code [ RL@ ]  > ",c("[ RL@Red##    ]     │"))
            print ("│  [+] code [ R#  ]  > ",c("[R# Red##    ]     │"))
            print ("│  [+] code [ R@  ]  > ",c("[ R@Red##    ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "green" or color == "Green" or color == "GREEN":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ GL# ]  > ",c("[GL# Green##  ]     │"))
            print ("│  [+] code [ GL@ ]  > ",c("[ GL@Green##  ]     │"))
            print ("│  [+] code [ G#  ]  > ",c("[G# Green##  ]     │"))
            print ("│  [+] code [ G@  ]  > ",c("[ G@Green##  ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "yellow" or color == "Yellow" or color == "YELLOW":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ YL# ]  > ",c("[YL# Yellow## ]     │"))
            print ("│  [+] code [ YL@ ]  > ",c("[ YL@Yellow## ]     │"))
            print ("│  [+] code [ Y#  ]  > ",c("[Y# Yellow## ]     │"))
            print ("│  [+] code [ Y@  ]  > ",c("[ Y@Yellow## ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "blue" or color == "Blue" or color == "BLUE":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ BL# ]  > ",c("[BL# Blue##   ]     │"))
            print ("│  [+] code [ BL@ ]  > ",c("[ BL@Blue##   ]     │"))
            print ("│  [+] code [ B#  ]  > ",c("[B# Blue##   ]     │"))
            print ("│  [+] code [ B@  ]  > ",c("[ B@Blue##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "purple" or color == "Purple" or color == "PURPLE":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ PL# ]  > ",c("[PL# Purple## ]     │"))
            print ("│  [+] code [ PL@ ]  > ",c("[ PL@Purple## ]     │"))
            print ("│  [+] code [ P#  ]  > ",c("[P# Purple## ]     │"))
            print ("│  [+] code [ P@  ]  > ",c("[ P@Purple## ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "cyan" or color == "Cyan" or color == "CYAN":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ CL# ]  > ",c("[CL# Cyan##   ]     │"))
            print ("│  [+] code [ CL@ ]  > ",c("[ CL@Cyan##   ]     │"))
            print ("│  [+] code [ C#  ]  > ",c("[C# Cyan##   ]     │"))
            print ("│  [+] code [ C@  ]  > ",c("[ C@Cyan##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")

        elif color == "gray" or color == "Gray" or color == "GRAY":
            print (c("W#"))
            print ("╭──────────────────────────────────────╮")
            print ("│                                      │")
            print ("│  [+] code [ bL# ]  > ",c("[bL# Black##  ]     │"))
            print ("│  [+] code [ gL@ ]  > ",c("[ gL@Gray##   ]     │"))
            print ("│  [+] code [ b#  ]  > ",c("[b# Black##  ]     │"))
            print ("│  [+] code [ g@  ]  > ",c("[ g@Gray##   ]     │"))
            print ("│                                      │")
            print ("╰──────────────────────────────────────╯")
            print ("")
        else:
            print (c("W#"))
            if len(color) < 5:
                l1 = "╭──────────────────────────────────────╮"
                l2 = "│                                      │"
                l3 = "│ [ "+color+" ] : This color not found !"
                l4 = "│                                      │"
                l5 = "╰──────────────────────────────────────╯"
                a3 = " " * ((len(l2)-len(l3))-1)
                print (l1)
                print (l2)
                print (l3+a3+"│")
                print (l4)
                print (l5)
            else:
                a1 = "─" * len(color)
                a2 = " " * len (color)
                l1 = "╭"+a1+"─────────────────────────────────╮"
                l2 = "│"+a2+"                                 │"
                l3 = "│ [ "+color+" ] : This color not found !"
                l4 = "│"+a2+"                                 │"
                l5 = "╰"+a1+"─────────────────────────────────╯"
                a3 = " " * ((len(l2)-len(l3))-1)
                print (l1)
                print (l2)
                print (l3+a3+"│")
                print (l4)
                print (l5)
    def help():
        Functions = """WL#
╔══════════════════════════════════════════════════════════════════════════════╗
║  ◉                         [ Functions available ]                        ◉  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                                                                              ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [1] uppercase_and_lowercase_letters()                      │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [2] loading()                                              │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [3] downloading()                                          │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [4] colors()                                               │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [5] help()                                                 │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║        ╭────────────────────────────────────────────────────────────╮        ║
║        │ [6] animation_info()                                       │        ║
║        ╰────────────────────────────────────────────────────────────╯        ║
║                                                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

        """
        Functions = Colors.coloring(Functions)
        print (Functions)

    def animation_info(Animation_Name="all"):
        if Animation_Name == "all":
            c1 = "WL#"
            all = """
╔═══════════════════════════════════════════════════════════════════════╗
║ ◈  Functions Info                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [1] The First Function : uppercase_and_lowercase_letters      │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description    : Good                                 │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters     : Look down                            │   ║
║   │                                                               │   ║
║   │  text             = 'The displayed text'                      │   ║
║   │  lower_text_color = 'Color'                                   │   ║
║   │  upper_text_color = 'Color'                                   │   ║
║   │  time             = Duration of rotation of the stick         │   ║
║   │  repeat           = Number of complete cycles                 │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example            : Look down                            │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.uppercase_and_lowercase_letters(                           │   ║
║   │  text = 'uppercase_and_lowercase_letters',                    │   ║
║   │  lower_text_color = 'C#',                                     │   ║
║   │  upper_text_color = 'Y#',                                     │   ║
║   │  time = 0.1,                                                  │   ║
║   │  repeat = 3                                                   │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [2] The Second Function : loading                             │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description     : Very good                           │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters      : Look down                           │   ║
║   │                                                               │   ║
║   │  text                = 'The displayed text'                   │   ║
║   │  text_color          = 'The displayed text color'             │   ║
║   │  Animated_text       = 'Animated_text'                        │   ║
║   │  Animated_text_color = 'color'                                │   ║
║   │  time                = Duration of the animation display      │   ║
║   │  repeat              = Number of complete cycles              │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example             : Look down                           │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.loading(                                                   │   ║
║   │  text="Loading",                                              │   ║
║   │  text_color="C#",                                             │   ║
║   │  Animated_text="\|/-",                                        │   ║
║   │  Animated_text_color="Y#",                                    │   ║
║   │  time=0.1,                                                    │   ║
║   │  repeat=5                                                     │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [3] The Third Function : downloading                          │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description    : Excellent                            │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters     : Look down                            │   ║
║   │                                                               │   ║
║   │  Length               = The length of the loading bar         │   ║
║   │  time                 = Duration of rotation of the stick     │   ║
║   │  top_text             = 'Text above the download bar'         │   ║
║   │  top_text_color       = 'Color'                               │   ║
║   │  left_side_text       = 'Text to the left of the download bar'│   ║
║   │  bottom_shape         = 'Bottom downloading bar'              │   ║
║   │  bottom_shape_color   = 'Color'                               │   ║
║   │  top_shape_color      = 'Color'                               │   ║
║   │  top_shape            = 'Top downloading bar'                 │   ║
║   │  left_side            = 'The left side of the download bar'   │   ║
║   │  left_side_color      = 'Color'                               │   ║
║   │  right_side           = 'The right side of the download bar'  │   ║
║   │  right_side_color     = 'Color'                               │   ║
║   │  percentage           = Percentage number                     │   ║
║   │  percentage_color     = 'Percentage color'                    │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example            : Look down                            │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.downloading(                                               │   ║
║   │  Length=30,                                                   │   ║
║   │  time=0.1,                                                    │   ║
║   │  top_text="                  [Please Wait...]",               │   ║
║   │  top_text_color="Y#",                                         │   ║
║   │  left_side_text="Download ",                                  │   ║
║   │  left_side_text_color="Y#",                                   │   ║
║   │  bottom_shape="▒",                                            │   ║
║   │  bottom_shape_color="B#",                                     │   ║
║   │  top_shape="█",                                               │   ║
║   │  top_shape_color="CL#",                                       │   ║
║   │  left_side="┋",                                               │   ║
║   │  left_side_color="B#",                                        │   ║
║   │  right_side="┋",                                              │   ║
║   │  right_side_color="B#",                                       │   ║
║   │  percentage=100,                                              │   ║
║   │  percentage_color="Y#"                                        │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [4] Fourth Function : colors                                  │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description : Very good                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters  : Look down                               │   ║
║   │                                                               │   ║
║   │  color = 'color name' or 'all'                                │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example         : Look down                               │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.color()                                                    │   ║
║   │  A.color("wihte")                                             │   ║
║   │  A.color("red")                                               │   ║
║   │  A.color("green")                                             │   ║
║   │  A.color("yellow")                                            │   ║
║   │  A.color("blue")                                              │   ║
║   │  A.color("purple")                                            │   ║
║   │  A.color("cyan")                                              │   ║
║   │  A.color("gray")                                              │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [5] Fifth Function  : help                                    │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description : Good                                    │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters  : No Parameters                           │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example         : Look down                               │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.help()                                                     │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [6] Sixth function  : animation_info                          │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description : Very good                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters  : Look down                               │   ║
║   │                                                               │   ║
║   │  Animation_Name = 'function name without ()'                  │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example         : Look down                               │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.animation_info("uppercase_and_lowercase_letters")          │   ║
║   │  A.animation_info("loading")                                  │   ║
║   │  A.animation_info("downloading")                              │   ║
║   │  A.animation_info("help")                                     │   ║
║   │  A.animation_info("animation_info")                           │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c1 = Colors.coloring(c1)
            print (all)

        elif Animation_Name == "uppercase_and_lowercase_letters":
            c2 = "WL#"
            f1 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name :  uppercase_and_lowercase_letters      │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Good                                  │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : Look down                             │   ║
║   │                                                               │   ║
║   │  text             = 'The displayed text '                     │   ║
║   │  lower_text_color = 'Color'                                   │   ║
║   │  upper_text_color = 'Color'                                   │   ║
║   │  time             = Duration of rotation of the stick         │   ║
║   │  repeat           = Number of complete cycles                 │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.uppercase_and_lowercase_letters(                           │   ║
║   │  text = 'uppercase_and_lowercase_letters',                    │   ║
║   │  lower_text_color = 'C#',                                     │   ║
║   │  upper_text_color = 'Y#',                                     │   ║
║   │  time = 0.1,                                                  │   ║
║   │  repeat = 3                                                   │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c2 = Colors.coloring(c2)
            print (f1)

        elif Animation_Name == "loading":
            c3 = "WL#"
            f2 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name : loading                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Very good                             │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : Look down                             │   ║
║   │                                                               │   ║
║   │  text                = 'The displayed text'                   │   ║
║   │  text_color          = 'The displayed text color'             │   ║
║   │  Animated_text       = 'Animated_text'                        │   ║
║   │  Animated_text_color = 'color'                                │   ║
║   │  time                = Duration of the animation display      │   ║
║   │  repeat              = Number of complete cycles              │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.loading(                                                   │   ║
║   │  text="Loading",                                              │   ║
║   │  text_color="C#",                                             │   ║
║   │  Animated_text="\|/-",                                        │   ║
║   │  Animated_text_color="Y#",                                    │   ║
║   │  time=0.1,                                                    │   ║
║   │  repeat=5                                                     │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c3 = Colors.coloring(c3)
            print (f2)

        elif Animation_Name == "downloading":
            c4 = "WL#"
            f3 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name : downloading                           │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Excellent                             │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : Look down                             │   ║
║   │                                                               │   ║
║   │  Length               = The length of the loading bar         │   ║
║   │  time                 = Duration of rotation of the stick     │   ║
║   │  top_text             = 'Text above the download bar'         │   ║
║   │  top_text_color       = 'Color'                               │   ║
║   │  left_side_text       = 'Text to the left of the download bar'│   ║
║   │  bottom_shape         = 'Bottom downloading bar'              │   ║
║   │  bottom_shape_color   = 'Color'                               │   ║
║   │  top_shape_color      = 'Color'                               │   ║
║   │  top_shape            = 'Top downloading bar'                 │   ║
║   │  left_side            = 'The left side of the download bar'   │   ║
║   │  left_side_color      = 'Color'                               │   ║
║   │  right_side           = 'The right side of the download bar'  │   ║
║   │  right_side_color     = 'Color'                               │   ║
║   │  percentage           = Percentage number                     │   ║
║   │  percentage_color     = 'Percentage color'                    │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.downloading(                                               │   ║
║   │  Length=100,                                                  │   ║
║   │  time=0.1,                                                    │   ║
║   │  top_text="                  [Please Wait...]",               │   ║
║   │  top_text_color="Y#",                                         │   ║
║   │  left_side_text="Download ",                                  │   ║
║   │  left_side_text_color="Y#",                                   │   ║
║   │  bottom_shape="▒",                                            │   ║
║   │  bottom_shape_color="B#",                                     │   ║
║   │  top_shape="█",                                               │   ║
║   │  top_shape_color="CL#",                                       │   ║
║   │  left_side="┋",                                               │   ║
║   │  left_side_color="B#",                                        │   ║
║   │  right_side="┋",                                              │   ║
║   │  right_side_color="B#",                                       │   ║
║   │  percentage=100,                                              │   ║
║   │  percentage_color="Y#"                                        │   ║
║   │  )                                                            │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

                """
            c4 = Colors.coloring(c4)
            print (f3)

        elif Animation_Name == "colors":
            c5 = "WL#"
            f4 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name : colors                                │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Very good                             │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : Look down                             │   ║
║   │                                                               │   ║
║   │  color = 'color name' or 'all'                                │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.color()                                                    │   ║
║   │  A.color("wihte")                                             │   ║
║   │  A.color("red")                                               │   ║
║   │  A.color("green")                                             │   ║
║   │  A.color("yellow")                                            │   ║
║   │  A.color("blue")                                              │   ║
║   │  A.color("purple")                                            │   ║
║   │  A.color("cyan")                                              │   ║
║   │  A.color("gray")                                              │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c5 = Colors.coloring(c5)
            print (f4)

        elif Animation_Name == "help":
            c6 = "WL#"
            f5 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name : help                                  │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Good                                  │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : No Parameters                         │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.help()                                                     │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c6 = Colors.coloring(c6)
            print (f5)

        elif Animation_Name == "animation_info":
            c7 = "WL#"
            f6 = """

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Function Name : animation_info                        │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The description   : Very good                             │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] The Parameters    : Look down                             │   ║
║   │                                                               │   ║
║   │  Animation_Name = 'function name without ()' or 'all'         │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║   ╭───────────────────────────────────────────────────────────────╮   ║
║   │ [*] Example           : Look down                             │   ║
║   │                                                               │   ║
║   │  from A4Shape.Shape import Animation                          │   ║
║   │  A = Animation                                                │   ║
║   │                                                               │   ║
║   │  A.animation_info()                                           │   ║
║   │  A.animation_info("uppercase_and_lowercase_letters")          │   ║
║   │  A.animation_info("loading")                                  │   ║
║   │  A.animation_info("downloading")                              │   ║
║   │  A.animation_info("help")                                     │   ║
║   │  A.animation_info("animation_info")                           │   ║
║   │                                                               │   ║
║   ╰───────────────────────────────────────────────────────────────╯   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

            """
            c7 = Colors.coloring(c7)
            print (f6)
