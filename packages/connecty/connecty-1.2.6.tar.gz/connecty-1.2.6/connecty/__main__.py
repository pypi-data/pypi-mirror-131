import tkinter.filedialog
from configparser import ConfigParser
import connecty
from tkinter import *
from tkinter import ttk
import colorama
from importlib import resources
colorama.init()

CBLUE = "\33[34m"
CVIOLET = "\33[35m"
CEND = "\033[0m"
CBOLD = "\033[1m"

def wrap(cl):
    def fu(txt):
        return cl + txt + CEND
    return fu

print(wrap(CBLUE)("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"))
print(wrap(CBLUE)("▉") + CBOLD + " JOIN THE SUPPORT SERVER FOR HELP!! https://discord.gg/fcZBB2v " + wrap(CBLUE)("█"))
print(wrap(CBLUE)("█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█"))

args = connecty.parser.parse_args()
config = ConfigParser()
config.read_string(resources.read_text(connecty, "defaults.ini"))
config.read(args.config)
bot = connecty.Bot()
bot_config = dict(config["BOT"])
del config["BOT"]
connecty.GB.bot = bot
connections = {sec: [int(id) for id in config[sec]["channels"].split()] for sec in config.sections()}
async def init():
    for con in connections.values():
        await bot.register(con)
bot.startup = init
def start():
    # root.quit()
    bot.run(bot_config["token"])
if __name__ == "__main__":
    start()




    """
    con_selection = None
    cha_selection = None
    root = Tk()
    root.title("Connecty")
    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))

    con_inp = ttk.Entry(frame, textvariable=StringVar(value=""))
    con_inp.grid(column=0, row=1)

    con_combo = ttk.Combobox(frame, values=list(connections.keys()), state="readonly")
    con_combo.grid(column=1, row=1)
    def fun_cha_combo(*args):
        selection = con_combo.get()
        cha_combo.config(values=connections[selection])
    con_combo.bind("<<ComboboxSelected>>", fun_cha_combo)

    def fun_con_add(*args):

        connections[con_inp.get()] = []
        con_combo.config(values=list(connections.keys()))
        con_combo.set(con_inp.get())
    con_add = ttk.Button(frame, text="Add", command=fun_con_add)
    con_add.grid(column=0, row=0, sticky=(W, E))

    def fun_con_rem(*args):
        del connections[con_inp.get()]
        con_combo.config(values=list(connections.keys()))
        cha_combo.config(values=[])
        con_combo.set('')
        cha_combo.set('')
    con_rem = ttk.Button(frame, text="Remove", command=fun_con_rem)
    con_rem.grid(column=1, row=0, sticky=(W, E))


    cha_inp = ttk.Entry(frame, textvariable=StringVar(value=""))
    cha_inp.grid(column=2, row=1)

    cha_combo = ttk.Combobox(frame, values=[], state="readonly")
    cha_combo.grid(column=3, row=1)

    cha_add = ttk.Button(frame, text="Add", command=lambda: ...)
    cha_add.grid(column=2, row=0, sticky=(W, E))

    cha_rem = ttk.Button(frame, text="Remove", command=lambda: ...)
    cha_rem.grid(column=3, row=0, sticky=(W, E))


    ttk.Label(frame, text="").\
        grid(column=0, row=2)
    ttk.Button(frame, text="Load", command=lambda: ...).\
        grid(column=0, row=3, sticky=(W, E))
    ttk.Button(frame, text="New", command=lambda: ...).\
        grid(column=1, row=3, sticky=(W, E))
    token = StringVar(value="<Token>")
    ttk.Entry(frame, textvariable=token).\
        grid(column=2, row=3, columnspan=2, sticky=(W, E))
    Button(frame, text="Run", bg='#8CEFFF', command=lambda: ...).\
        grid(column=0, row=4, columnspan=4, sticky=(W, E))


    def update():
        if con_selection is None:
            con_combo.set('')
            con_inp.config(value='')
            cha_combo.set('')
            cha_combo.config(values=[])
            cha_inp.config(value='')
        else:
            con_combo.set(con_selection)
            con_inp.config(value=con_selection)
            cha_combo.config(values=connections[con_selection])
        if cha_selection is None:
            cha_combo.set('')
            cha_inp.config(value='')
        else:
            cha_combo.set(cha_selection)
            cha_inp.config(value=cha_selection)


    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)



    root.mainloop()
    """