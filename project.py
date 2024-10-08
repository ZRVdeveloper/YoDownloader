#! Завантажувач з Youtube
from tkinter import *
import customtkinter
from customtkinter import *  # <- import the CustomTkinter module
from CTkMessagebox import CTkMessagebox
from pytubefix import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import os



class YoDowloader(customtkinter.CTk):
    def on_closing(self):
        msg = CTkMessagebox(title="Exit?", message="Закрити програму?",
                        icon="question", option_1="Скасувати", option_2="Ні", option_3="Так")
        
        if msg.get() == "Так":            
            self.after_cancel(self)
            self.destroy()
    
    def addType(self):
        print(self.radio_var.get())
    def error(self, t = 1):
        CTkMessagebox(title="Помилка", message="Недійсна адреса",
                        icon="question", option_1="Ок")
    def v_prog(self, stream, chunk, toEnd):
        #print(stream.filesize,"$$$$$$$$$$$")
        size = (1-(toEnd/stream.filesize))*100
        #print(chunk, "++++++++++++")
        #print(round(size,1), "%")
        self.info.configure(text=f"Завантажено: {round(size,1)} %")
        self.update()
    def test (self, v = 0):
        if v == 0:
            #print(self.project.get())
            #self.info.configure(text="Завантажую...")
            #if self.test() == True:
            self.line = "https://www.youtube.com/watch?v="
            self.line2 = "https://www.youtube.com/shorts/"
            self.link = self.project.get()
            if self.link.startswith(self.line) or self.link.startswith(self.line2):
                return True
            else: self.error()
            
        
        elif v == 1:
            self.line = "https://www.youtube.com/playlist"
            self.link = self.project.get()
            if self.link.startswith(self.line):
                return True
            else: self.error()
            
        
    def convert(self,path):
        video_path = f"vnew.mp4"
        audio_path = f"anew.aac"
        path = str(f'{path.rstrip()}').replace(" ", "_")        
        path = str(f'{path.rstrip()}').replace("?", "")        
        path = str(f'{path.rstrip()}').replace("!", "")
        if self.file_is_ready(path):
            print(ok)
        else:
            cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy {path}.mp4"        
            os.system(cmd)
            self.info.configure(text=f"{self.info.cget('text')}. Convert - ok")
            print(self.info.cget('text'))
            d1, d2 = f"del {video_path}", f"del {audio_path}"
            os.system(d1)
            os.system(d2)
            self.info.configure(text=f"{self.info.cget('text')}. path del - ok")
            print(self.info.cget('text'))
            return self.info.cget('text')
    def download (self):
        if self.test():
            try:
                self.video = YouTube (self.link, on_progress_callback=self.v_prog)
            except VideoUnavailable:
                print(f'Video  is unavaialable, skipping.')
            else:
                Dtype = int(self.radio_var.get())
                if Dtype == 2: 
                    self.stream = self.video.streams.get_audio_only()
                else:
                    self.stream = self.video.streams.get_highest_resolution()        
                self.stream.download()        
                self.info.configure(text="Завантаження виконано")
                self.insert.delete(0, 100)
            
    def download_list(self):        
        self.list_info.place(x=320, y=80)
        self.geometry("800x200")
        self.btn_info_stream_v.destroy()
        self.btn_info_stream_a.destroy()
        self.radiobutton_1.destroy()
        self.radiobutton_2.destroy()
        self.update()
        if self.test(v=1):
            
            p = Playlist(self.link)
            self.list_size = len(p.video_urls)
            self.list_download_ok = 0
            self.list_info.configure(text=f"{self.list_size} у списку \nЗавантаженно: {self.list_download_ok}")
            for vv in p.video_urls:                
                print(vv)
                self.project.set(value=vv)
                self.download_best()
                self.list_download_ok += 1
                self.list_info.configure(text=f"{self.list_size} у списку \nЗавантаженно: {self.list_download_ok} \nЗавантажуємо \n {self.t}")
                self.update()
            self.list_info.configure(text=f"{self.list_size} у списку \nЗавантаженно: {self.list_download_ok}")
            self.update()
        
    def download_by_tag(self):
        if self.test():
            try:
                self.video = YouTube (self.link, on_progress_callback=self.v_prog)
            except VideoUnavailable:
                print(f'Video  is unavaialable, skipping.')
            finally:
                self.stream = self.video.streams.get_by_itag(self.project.get())
                v_type = (str(self.stream).split(" "))[2].split('/')[1]
                #print(self.stream.title, self.stream, v, self.video)
                self.stream.download()        
                self.info.configure(text="Завантаження виконано")
                self.insert.delete(0, len(self.link))
    def download_best(self):
        if self.test():
            try:
                self.video = YouTube (self.link, on_progress_callback=self.v_prog)
            except VideoUnavailable:
                print(f'Video  is unavaialable, skipping.')
            finally:
                self.stream = self.video.streams.filter(file_extension='mp4')
                
                #вантажим відео
                oll = str(self.stream).split(">,")
                v_tag = (oll[1].split('"\','))[0].split('="')[1].split(" ")[0]
                v_tag = v_tag[:-1]
                    #print(v_tag)
                self.stream = self.video.streams.get_by_itag(v_tag)
                    #v_video = str(self.stream).split(">,")[0]
                self.t = self.stream.title
                if self.file_is_ready(self.stream.title) != True:
                    self.stream.download(filename_prefix = 'v', filename = 'new.mp4')
                else:
                    print('video-ok')
                
            try:
                self.video = YouTube (self.link, on_progress_callback=self.v_prog)
            except VideoUnavailable:
                print(f'Video  is unavaialable, skipping.')
            finally:
                #вантажим звук
                self.stream = self.video.streams.filter(file_extension='mp4')
                oll = str(self.stream).split(">,")
                a_tag = (oll[len(oll)-1].split('"\','))[0].split('="')[1].split(" ")[0]
                a_tag = a_tag[:-1]
                self.stream = self.video.streams.get_by_itag(a_tag)
                if self.file_is_ready(self.stream.title) != True:
                    self.stream.download(filename_prefix = 'a', filename = 'new.aac')                    
                    
                    #print(1)
                    self.info.configure(text=self.convert(self.t))
                    self.insert.delete(0, len(self.link))
                else:
                    print('video-ok')
            #обєднуємо файли
            
    def info_str(self,info_type = 1):
        if self.test():
            try:
                self.video = YouTube (self.link, on_progress_callback=self.v_prog)
            except VideoUnavailable:
                print(f'Video  is unavaialable, skipping.')
            else:
                match info_type:
                    case 1: self.info_str1 = str(self.video.streams)
                    case 2: self.info_str1 = str(self.video.streams.filter(file_extension='mp4'))
                    case 3: self.info_str1 = str(self.video.streams.filter(only_audio=True))
                self.info_str1 = self.info_str1.replace(">,",">,\n")
                self.geometry("1100x550")
                self.info_stream.configure(text=self.info_str1)
                self.insert.delete(0,len(self.link))
                self.btn_by_tag.place(x=20, y=140)
                self.btn_best.place(x=20, y=170)
                
    def file_is_ready(self,path):
        self.file_in_dir = os.listdir()
        path = str(f'{path.rstrip()}').replace(" ", "_")        
        path = str(f'{path.rstrip()}').replace("?", "")        
        path = str(f'{path.rstrip()}').replace("!", "")
        path +='.mp4'
        #print(path)
        rez = False
        for name in self.file_in_dir:
            if path == name:
                rez=True
        return rez
    def __init__(self):
        
        super().__init__()
        self.name_file = []
        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        self.geometry("670x150+100+100")
        self.help = CTkLabel (master = self,text = 'Вставте посилання на Youtube відео')
        self.help.place(x=20, y=10)
        self.project = StringVar()
        self.insert = CTkEntry(master = self, textvariable = self.project, width=400)
        self.insert.place(x=20, y=40)
        self.radio_var = IntVar(value=0)
        self.radiobutton_1 = customtkinter.CTkRadioButton(self, text="Відео",
                                             command=self.addType, variable= self.radio_var, value=1)
        self.radiobutton_2 = customtkinter.CTkRadioButton(self, text="Аудіо",
                                             command=self.addType, variable= self.radio_var, value=2)
        self.radiobutton_1.place(x=450, y=40)
        self.radiobutton_2.place(x=450, y=70)
        self.btn5 = CTkButton(master = self, text = "Завантажити", command = self.download)
        self.btn5.place(x=20, y=100)
        self.info = CTkLabel (master = self, text = "")
        self.info.place(x=20, y=70)
        self.btn_info_stream = CTkButton(master = self, text = "info", command = self.info_str)
        self.btn_info_stream.place(x=170, y=100)
        self.btn_info_stream_v = CTkButton(master = self, text = "info_video", command = lambda:self.info_str(2))
        self.btn_info_stream_v.place(x=320, y=100)
        self.btn_info_stream_a = CTkButton(master = self, text = "info_audio", command = lambda:self.info_str(3))
        self.btn_info_stream_a.place(x=470, y=100)
        self.info_stream = CTkLabel (master = self, text = "", justify="left")
        self.info_stream.place(x=200, y=140)
        self.btn_by_tag = CTkButton(master = self, text = "Завантажити за тегом", command = self.download_by_tag)
        self.btn_best = CTkButton(master = self, text = "Завантажити найкраще", command = self.download_best)
        self.btn_list = CTkButton(master = self, text = "Завантажити список", command = self.download_list)
        self.btn_list.place(x=520, y=40)
        self.list_info = CTkLabel(master = self, text = "", justify="left")
        
        
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
    
if __name__=="__main__":
      

    yo = YoDowloader()
    
    yo.mainloop()
