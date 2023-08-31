from tkinter import *
import os
import sys
from tkinter import messagebox
import psutil
from PIL import Image, ImageTk
from lcu_driver import Connector
Window_Width = 380
Window_Height = 200

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


connector = Connector()
def onStart():
    @connector.ready
    async def connect(connection):
        summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
        
        data = str(await summoner.json())
        loot = await connection.request("get", "/lol-loot/v1/player-loot")
        lootList = await loot.json()
        disenchantValueBE = 0
        totalValueBE = 0
        disenchantValueOE = 0
        totalValueOE = 0

        for x in range(len(lootList)):
            if lootList[x]["disenchantLootName"] == "CURRENCY_champion":
                disenchantValueBE += lootList[x]["disenchantValue"]
                totalValueBE += lootList[x]["value"]
            elif lootList[x]["disenchantLootName"] == "CURRENCY_cosmetic":
                disenchantValueOE += lootList[x]["disenchantValue"]
                totalValueOE += lootList[x]["value"]
        

        MainWindow.owned_champion_count = f'{disenchantValueBE:,} ({totalValueBE:,} raw)'
        MainWindow.owned_skin_count = f'{disenchantValueOE:,} ({totalValueOE:,} raw)'
    connector.start()





        
class MainWindow:
    owned_champion_count = ""
    owned_skin_count = ""

    def __init__(self, master):
        master.iconbitmap(f'{resource_path("./assets/icon.ico")}')
        self.master = master
        master.title('Essence Emporium')
        canvas = Canvas(master, height=Window_Height, width=Window_Width)
        canvas.pack()
        main_window_background = Image.open(f'{resource_path("./assets/background_main.jpg")}')
        main_window_background = main_window_background.resize((400, 225), Image.LANCZOS)
        main_window_background = ImageTk.PhotoImage(main_window_background)
        main_background = Label(master, image=main_window_background)
        main_background.image = main_window_background
        main_background.place(relwidth=1, relheight=1)
        messagebox.showinfo(title="ALERT", message="Fork of https://github.com/MManoah/lol-champion-and-skin-count \nCredit to MManoah edited by aroglwr")
        champion_info = Text(master, fg='#8080ff', bg='#0E0E0E', borderwidth=2, relief="groove")
        champion_info.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
        champion_info.insert('end', 'Blue Essence:\t\t')
        champion_info.insert('end', self.owned_champion_count)
        skin_info = Text(master, fg='#ed7014', bg='#0E0E0E', borderwidth=2, relief="groove")
        skin_info.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.1)
        skin_info.insert('end', 'Orange Essence:\t\t ')
        skin_info.insert('end', self.owned_skin_count)

def process_exists():
    for p in psutil.process_iter():
        try:
            if p.name() == 'LeagueClient.exe':
                return True
        except psutil.Error:
            return False

if __name__ == '__main__':
    if process_exists():
        onStart()
        root = Tk()
        root.resizable(0, 0)
        application = MainWindow(root)
        root.mainloop()
    else:
        messagebox.showerror("ERROR", "LEAGUE CLIENT IS NOT OPEN")
