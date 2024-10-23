from pytubefix import YouTube, Playlist
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable
import os

class YoFun():
    def v_prog(self, stream, chunk, toEnd):
        #print(stream.filesize,"$$$$$$$$$$$")
        size = (1-(toEnd/stream.filesize))*100
        #print(chunk, "++++++++++++")
        #print(round(size,1), "%")
        self.parent_win.procent_label.config(text=f"{round(size)} %", fg='red')
        self.parent_win.progress.config(value = round(size)) #int(f'{(round(size))}'))
        self.parent_win.update()
    def test (self, url):
        l1 = "https://www.youtube.com/watch?v="
        l2 = "https://www.youtube.com/shorts/"
        l3 = "https://www.youtube.com/playlist"
        if isinstance(url, str) == False: return False
        elif url.startswith(l1): return 'video'
        elif url.startswith(l2): return 'shorts'
        elif url.startswith(l3): return 'playlist'                
        else: return False
    def test_name(self,url):
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
            self.stream = self.video.streams.get_highest_resolution()
        except:
            print(f'Video  is unavaialable, skipping.')
            self.parent_win.info.insert('1.0', f"Помилка завантаження ❕\n")
            self.parent_win.update()
            return [True]
        else:            
            path = self.stream.title
            path = str(f'{path.rstrip()}').replace(" ", "_")        
            path = str(f'{path.rstrip()}').replace("?", "")        
            path = str(f'{path.rstrip()}').replace("!", "")
            print(path)
            if os.path.exists(f"{path}.mp4"):
                self.parent_win.info.insert('1.0',f"{path} ✔ \n" )
                self.parent_win.update()
                return [True]
            else:
                
                return [False,path]
        
    def convert(self,path):
        video_path = f"vnew.mp4"
        audio_path = f"anew.aac"
        path = str(f'{path.rstrip()}').replace(" ", "_")        
        path = str(f'{path.rstrip()}').replace("?", "")        
        path = str(f'{path.rstrip()}').replace("!", "")        
        cmd = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy {path}.mp4"        
        os.system(cmd)
        self.parent_win.info.insert('end', f"Convert - ok")
        print('Convert - ok')
        d1, d2 = f"del {video_path}", f"del {audio_path}"
        os.system(d1)
        os.system(d2)
        self.parent_win.info.insert('1.0', f" path del - ok")
        print('path del - ok')
        return path
    def download (self, url):
        if self.test_name(url)[0] == False:
            self.parent_win.btn.place_forget()
            match self.work:
                case 'Завантажити у найкращій якості': self.download_best(url)
                case 'Завантажити': self.download_video(url)
                case 'Завантажити аудіо': self.download_audio(url)
                case 'Інформація': self.info_str(url)
        else:
            self.parent_win.geometry("670x550")
            self.parent_win.info.insert('end', f"Відео з таким ім'ям є у папці \n")
        
        self.parent_win.btn.place(x=400, y=200)
        
    def download_video (self,url):
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
        except VideoUnavailable:
            print(f'Video  is unavaialable, skipping.')
        else:
            self.stream = self.video.streams.get_highest_resolution()        
            self.stream.download()        
            self.parent_win.procent_label.configure(text="✅", fg='green')
            self.parent_win.info.insert('1.0', f"Відео завантажено \n")
    def download_audio (self,url):
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
        except VideoUnavailable:
            print(f'Video  is unavaialable, skipping.')
        else:
            self.stream = self.video.streams.get_audio_only()        
            self.stream.download()        
            self.parent_win.procent_label.configure(text="✅", fg='green')
    def download_list(self, url):
        self.parent_win.geometry("670x550")
        self.parent_win.info.insert('1.0', f"Завантажуємо список \n")
        v=1
        if v==1:            
            p = Playlist(url)
            self.list_size = len(p.video_urls)
            self.list_download_ok = 0
            self.parent_win.info.insert('1.0', f"{self.list_size} у списку. Завантаженно: {self.list_download_ok}\n")
            for vv in p.video_urls:                
                print(vv)
                if self.test_name(vv)[0] == False:
                    self.download(vv)
                    
                self.list_download_ok += 1
                self.parent_win.info.insert('1.0',f"{self.list_size} у списку \nЗавантаженно: {self.list_download_ok}\n")                
            self.parent_win.info.insert('1.0',f"✅ Завантаження списку завершено ✅ \n")
            
    def download_best(self, url):
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
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
            self.stream.download(filename_prefix = 'v', filename = 'new.mp4')
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
        except VideoUnavailable:
            print(f'Video  is unavaialable, skipping.')
        finally:
            #вантажим звук
            self.stream = self.video.streams.filter(file_extension='mp4')
            oll = str(self.stream).split(">,")
            a_tag = (oll[len(oll)-1].split('"\','))[0].split('="')[1].split(" ")[0]
            a_tag = a_tag[:-1]
            self.stream = self.video.streams.get_by_itag(a_tag)
            self.stream.download(filename_prefix = 'a', filename = 'new.aac')
        #обєднуємо файли
        t = self.stream.title            
        name = self.convert(t)
        self.parent_win.info.insert('end', name)
        
    def info_str(self,url,info_type = 1):
        try:
            self.video = YouTube (url, on_progress_callback=self.v_prog)
        except VideoUnavailable:
            print(f'Video  is unavaialable, skipping.')
        else:
            match info_type:
                case 1: self.info_str1 = str(self.video.streams)
                case 2: self.info_str1 = str(self.video.streams.filter(file_extension='mp4'))
                case 3: self.info_str1 = str(self.video.streams.filter(only_audio=True))
            self.info_str1 = self.info_str1.replace(">,",">,\n")
            self.parent_win.geometry("670x550")
            self.parent_win.info.insert(1.0, self.info_str1)
            self.parent_win.info.place(x=20, y=250)
            
    def __init__(self,urls = None, win = None): #procent_label = None, progress = None, 
        self.parent_win = win
        #self.procent_label = procent_label
        #self.progress = progress
        self.urls = urls
        self.work = urls[len(urls)-1]
        self.urls.pop(len(urls)-1)
        print (self.work)
        if self.urls:
            print(f'Urls catch ')
            for url in urls:
                match self.test(url):
                    case 'video': self.download(url)
                    case 'shorts': self.download(url)
                    case 'playlist': self.download_list(url)
                    case False: print(f'{url} - bad')
                
                    
        
    
if __name__=="__main__":
    print('Почали')
    l = []
    def add_List():
        global l
        while True:
            i = input()
            if i == '':
                break
            else:
                l.append(i)
    add_List()
    YoFun(l)
    
