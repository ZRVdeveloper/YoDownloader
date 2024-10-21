from tkinter import *
from tkinter.ttk import Combobox as Cbox
from tkinter.ttk import Progressbar as Progress
from tkinter.scrolledtext import ScrolledText
import customtkinter, tkinter
from customtkinter import *
from CTkMenuBar import *
import yofun


class YoDownloadFaceTk(tkinter.Toplevel):    
    def choice(self):
        selected_option = self.select_type.get()
        all_link = self.input_link.get("0.0", "end")
        links = all_link.split('\n')
        links[len(links)-1] = selected_option
        #print(selected_option,'\n',links)
        yofun.YoFun(links,self) # self.procent_label, self.progress, 
    def __init__(self,me):
        super().__init__()
        self.geometry("670x250+300+100")
        self.help = Label (master = self,text = 'Вставте посилання на Youtube відео',font=[me.font[0],14])
        self.help.place(x=20, y=10)
        self.input_link = Text(master = self, height = 5,width = 60,bg = "white",font=[me.font[0],11])
        self.input_link.place(x=20, y=60)
        #self.progress_var = IntVar()
        self.progress = Progress(master = self,orient="horizontal", variable=0, length=400, value = 0)        
        self.progress.place(x=20, y=160)
        self.procent_label = Label(master = self,text = '0%',font=[me.font[0],14])
        self.procent_label.place(x=470, y=160)
        self.s_type = ["Завантажити у найкращій якості","Завантажити","Завантажити аудіо","Інформація"]
        self.select_type = Cbox(master = self, values = self.s_type, width = 40)
        self.select_type.set("Що робити?")
        self.select_type.place(x=20, y=200)
        self.btn = Button(master = self, text = "Start", command = self.choice)
        self.btn.place(x=400, y=200)
        self.info = ScrolledText(master = self, height = 15,width = 100,bg = "white",font=[me.font[0],8])
        self.info.place(x=20, y=250)
        

        

class YoDownloadFaceCustomTk(customtkinter.CTkToplevel):
    font = ("Arial",10)
    
    def choice(self):
        selected_option = self.select_type.get()
        all_link = self.input_link.get("0.0", "end")
        links = all_link.split('\n')
        links[len(links)-1] = selected_option
        print(selected_option,'\n',links)
        
        
    def __init__(self,me):
        super().__init__()
        self.menubar = CTkMenuBar(self)
        self.config(menu=self.menubar)
        self.menubar.add_cascade("Інший вигляд", command=self.destroy)
        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        self.geometry("670x250")
        self.help = CTkLabel(master = self,text = 'Вставте посилання на Youtube відео', font=(me.font[0],16))
        self.help.place(x=20, y=40)                 
        self.input_link = CTkTextbox(master = self, height = 100,width = 400,border_width=2,font=(self.font[0],14))
        self.input_link.place(x=20, y=80)
        self.progress_var = IntVar(value=50)
        self.progress = CTkProgressBar(master = self,orientation="horizontal", variable=self.progress_var, border_width=400)        
        self.progress.place(x=20, y=190)
        self.procent_label = CTkLabel(master = self,text = '0%',font=(self.font[0],14))
        self.procent_label.place(x=450, y=190)
        self.s_type = ["Завантажити у найкращій якості","Завантажити","Завантажити аудіо","Інформація"]
        self.select_type = CTkComboBox(master = self, values = self.s_type, width = 200)
        self.select_type.set("Що робити?")
        self.select_type.place(x=20, y=220)
        self.btn = CTkButton(master = self, text = "Start", command = self.choice)
        self.btn.place(x=400, y=220)
class YoDownloadFace(Tk):
    font = ("Arial",10)
    def do_some(self,face):
        if face == 'tkinter':
            self.t = YoDownloadFaceTk(self)
            self.t.mainloop()
        if face == 'CustomTk':
            self.c = YoDownloadFaceCustomTk(self)
            self.c.mainloop()
    def __init__(self):
        super().__init__()
        self.geometry("200x230+100+100")
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.menubar.add_command(label='Tkinter', command=lambda:self.do_some('tkinter'))
        self.menubar.add_command(label='Custom Tkinter', command=lambda:self.do_some('CustomTk'))
        opys = 'Програмний продукт\nYoDownloader\nGUI надбудова для PyTube'
        i = Label(self, text = opys, font=[self.font[0],8])
        i.pack()

if __name__== "__main__":
    print ("Function for Youtube Dowloader by zrv")
    #yo = YoDownloadFaceTk()    
    #yo.mainloop()
    yo2 = YoDownloadFace()    
    yo2.mainloop()
