from customtkinter import*
import socket
import threading
import PIL
from dg import*
window=AuthWindow()
window.mainloop()
env=window.env


class Window(CTk):
    def __init__(self,fg_color=None,**kwargs):
        super().__init__(fg_color,**kwargs)
        self.geometry("500x500")
        self.title("Logi Talk")
        self.name="ANONIM"
        self.name=env.get("name","ANONIM")
        self.text=CTkTextbox(self,width=450,height=300,text_color="red",fg_color="white")
        self.text.configure(state="disabled")
        self.text.pack(pady=5,fill="both",expand=True)
        self.qq=CTkFrame(self,fg_color="transparent")
        self.qq.pack(padx=20,pady=10,fill="x")
        self.sent_text=CTkEntry(self.qq,placeholder_text="Видіть повідомлення")
        self.sent_text.pack(side="left",fill="x",expand=True)
        self.ww=CTkButton(self.qq,text="📎")
        self.ww.pack(side="left",padx=(0,5))
        self.sent=CTkButton(self.qq,text="відправити",command=self.sent_message)
        self.sent.pack(side="right",pady=(5,0))
        self.host="localhost"
        self.port=8080
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.sock.connect((self.host,self.port))
        
            self.sock.send(f"TEXT@{self.name}@{self.name}приєднався до \n".encode())
            threading.Thread(target=self.recv_msg,daemon=True).start()
        except:
            
            self.add_message("Не вдалоса підключитися до серверу")
    def recv_msg(self):
        buffer=""
        while True:
            try:
                chunk=self.sock.recv(4096)
                if not chunk:
                    break
                buffer+=chunk.decode(errors="ignore")
                while "\n"in buffer:
                    line,buffer = buffer.split("\n",1)
                    self.handle_line(line.strip())
            except:
                print("server error")
        self.sock.close()
    def handle_line(self,line):
        if not line:
            return
        parts=line.split("@",3)
        msg_type=parts[0]
        if msg_type=="TEXT":
            if len(parts)>=3:
                author=parts[1]
                message="@".join(parts[2:])
                self.add_message(f"{author}:{message}")

        elif msg_type=="PLC":
            pass      
    def add_message(self,text):
        self.text.configure(state="normal")
        self.text.insert(END,text+"\n")
        self.text.configure(state="disabled")
    def sent_message(self):
        message=self.sent_text.get()
        if message:
            self.add_message(f"{self.name}:{message}")
            data=f"TEXT@{self.name}@{message}\n"
            try:
                self.sock.send(data.encode())
            except:
                print("Error in sentting message")
        self.sent_text.delete(0,END)    
Window().mainloop()        