#from here to the subprocess.Popen is AI's code since I could not get rid of cmd popups
import os
import subprocess
import sys

_orig_popen = subprocess.Popen
_in_patch = False


def _patched_popen(*args, **kwargs):
  global _in_patch
  if _in_patch:
    return _orig_popen(*args, **kwargs)

  _in_patch = True
  try:
    creationflags = kwargs.get("creationflags", 0)
    kwargs["creationflags"] = creationflags | 0x08000000  # CREATE_NO_WINDOW

    if "startupinfo" not in kwargs or kwargs["startupinfo"] is None:
      si = subprocess.STARTUPINFO()
      si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
      si.wShowWindow = subprocess.SW_HIDE
      kwargs["startupinfo"] = si
    else:
      kwargs["startupinfo"].dwFlags |= subprocess.STARTF_USESHOWWINDOW
      kwargs["startupinfo"].wShowWindow = subprocess.SW_HIDE

    return _orig_popen(*args, **kwargs)
  finally:
    _in_patch = False


subprocess.Popen = _patched_popen
#from now on it's my code
import tkinter as tk
import tkinter as ttk
import platform 
import psutil
import cpuinfo
import GPUtil
import os
import json
import winreg
import locale
import webbrowser
import sys
import multiprocessing
from PIL import Image
import customtkinter as ctk
import main_code
from datetime import datetime
from main_code import load_alarms
from main_code import save_alarm
import subprocess
from temp_recorder import cpu_temperature
import requests
import threading 
import time
from main_code import monitor_strt
from temp_recorder import temperaturegpu
import psutil
import GPUtil
import wmi
import ctypes
import pystray
from pystray import MenuItem as item
import os
import sys
import threading
import customtkinter as ctk
from PIL import Image
import main_code
import sys
import ctypes

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()  
    def system_try_i():
        win_start.win_start()
        tray_thread = threading.Thread(target=system_try_i, daemon=True)
        tray_thread.start()
    window = ctk.CTk()
    window.title("ChillinPC logs")



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


script_dir = os.path.dirname(os.path.abspath(__file__))


GALBYTEALERT_FILE = "GalBytePCHelthchecker.json"
app_version = "beta 1.0"
gist_detect_vers = "https://gist.githubusercontent.com/galcomez/4e82623750156e0576a8c3b90d02e96e/raw/versions.txt"

#detects if update is needed
def updating():
    try:
        res = requests.get(gist_detect_vers, headers={'Cache-Control' : 'no-cache'}, timeout = 3)
        if res.status_code == 200:
            lateest_version = res.text.strip()
            if lateest_version != app_version:
                print(f"DEBUG: New version is available: {lateest_version}")
    except Exception as e:
        print("Update detection failed", e)



ctk.set_appearance_mode("System")
  #For icons so it will work on any computer
def get_path(realitive_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(getattr(sys, '_MEIPASS'), realitive_path)
    return os.path.join(os.path.dirname(__file__), realitive_path)
#System for detecting the unit of temperature based on your PC settings
def detect_unit_temp():
    try:
        path = r"Control Panel\International"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
        try: 
            imeasure, _ = winreg.QueryValueEx(key, "iMeasure")
            winreg.CloseKey(key)
            if str(imeasure).strip():
                return "°C"
            else:
                return "°F"
        except FileNotFoundError:
            winreg.CloseKey(key)
            raise Exception("iMeasure missing")
    except Exception: 
        try:
            code_language = locale.getencoding()
            language, country = locale.getlocale()
            if country and "US" in country.upper():
                return "°F"
            else: 
                return "°C"
        except: 
            return "N/A"
window.title("ChillinPC logs")
window.geometry("500x700")
window.resizable(False, False)

window.iconbitmap(get_path("favicon.ico"))


system_name = platform.system() 
system_version =platform.release()
print(f"DEBUG: Detected {system_name} {system_version}")
joint_ram_bites = psutil.virtual_memory().total
joint_ram = round(joint_ram_bites / (1024 ** 3), 1)
print(f"DEBUG: detected {joint_ram}GB of RAM ")
joint_cpu = cpuinfo.get_cpu_info()['brand_raw']
print(f"DEBUG: CPU {joint_cpu} detected")
try:
    joint_gpu = GPUtil.getGPUs()[0].name
except IndexError:
    joint_gpu = "Integrated graphics/ unable to detect"
print(f"DEBUG: GPU {joint_gpu} detcted")

choosen_unit = detect_unit_temp()
print(f"DEBUG: Current unit is {choosen_unit}")

upper_buttons = ctk.CTkFrame(window)
upper_buttons.pack(side="top", fill="x")
#system tray
def show_tra(icon, item):
    window.after(0, window.deiconify)
    window.after(0, window.focus_force)
def quit(icon=None, item=None):
    main_code.stop_monitoring()
    if icon:
        icon.stop()
        window.destroy()
        os.system(f"taskkill /F /PID {os.getpid()} /T")


if __name__ == "__main__":
    monitoring_thread = threading.Thread(target=main_code.monitor_strt, daemon=True)
    monitoring_thread.start()

def hide_win():
    window.withdraw()
#when X is pressed you only close the UI
window.protocol("WM_DELETE_WINDOW", hide_win)

#System tray icon
def system_try_i():
    icon = Image.open(get_path("favicon.ico"))
    meni = pystray.Menu(item("Check status", show_tra, default = True), item("Quit", quit))
    try_icon = pystray.Icon("PC_Health_Cheecker", icon, "PC Health Checker", meni)
    try_icon.run()
try_trea = threading.Thread(target=system_try_i, daemon = True)
try_trea.start()
    

#Github button
def github_link():
    webbrowser.open("https://github.com/galcomez")
    print("Opened github!")
icons_script = os.path.dirname(__file__)
path_to_github_icon = os.path.join(icons_script, "icons", "github_link.png")
orig_git_img = Image.open(path_to_github_icon)
print(f"DEBUG:{path_to_github_icon} choosen")
img_git_but = ctk.CTkImage(light_image=orig_git_img, dark_image=orig_git_img, size=(20, 20))
print(f"Image {img_git_but} detected! ")
clickable_icon_github = ctk.CTkButton(master=upper_buttons, image=img_git_but, text="", width=35, height=35, fg_color="transparent", hover_color=("#e0e0e0","#414545"), corner_radius=8, command=github_link)
clickable_icon_github.pack(side="right", padx=10, pady=10)

#stats button
def al_stt():
    #creates a new window
    stt_window = ctk.CTkToplevel(window)
    stt_window.title("stats")
    stt_window.geometry("400x150")
    stat_tit = ctk.CTkFrame(stt_window)
    stat_tit.pack(side="top", fill="x")
    
    sta_tit = ctk.CTkLabel(stat_tit, text="WORK IN PROGRESS", font=("San Francisco Pro", 20))
    sta_tit.pack(side="top", padx=10, pady=10)
    stt_window.overrideredirect(True)
    def wip_stat():
        stt_window.destroy()
    btn_close = ctk.CTkButton(stt_window, text="Close", command =wip_stat)
    btn_close.pack(pady=20)
    print("stats opened!")
path_to_stat_icon = os.path.join(icons_script, "icons", "stat_icon.png")
print(f"DEBUG: {path_to_stat_icon} found")
orig_stats_img = Image.open(path_to_stat_icon)
img_stat_but = ctk.CTkImage(light_image=orig_stats_img, dark_image=orig_stats_img, size=(20, 20))
print(f"DEBUG: {img_stat_but} found")
click_stat = ctk.CTkButton(master=upper_buttons, image=img_stat_but, text="", width=35, height=35, fg_color="transparent", hover_color=("#e0e0e0","#414545"), corner_radius=8, command=al_stt)
click_stat.pack(side="left", padx = 10, pady=10)

#quit button
def quit_ap():
    print("Closed app")
    os._exit(0)
path_to_q_ic = os.path.join(icons_script, "icons", "quit_icon.png")
orig_q_st = Image.open(path_to_q_ic)
img_q_but = ctk.CTkImage(light_image=orig_q_st, dark_image=orig_q_st, size=(20, 20))
cl_q = ctk.CTkButton(master=upper_buttons, image=img_q_but, text="", width=35, height=35, fg_color= "transparent", hover_color=("#e0e0e0", "#414545" ), corner_radius=8, command= quit_ap)
cl_q.pack(side="left", padx=10, pady=10)


#Title text
title_name = ctk.CTkLabel(upper_buttons, text="ChillinPC", font=("San Francisco Pro", 20))
title_name.pack(side="top", padx=10, pady=10)

update_inc = ctk.CTkFrame(window)
update_inc.pack(side="top", fill="x")


#update warning
res = requests.get(gist_detect_vers, headers={'Cache-Control' : 'no-cache'}, timeout = 3)
lateest_version = res.text.strip()
#update info gather
def d_and_r():
    try:
        ur_dw = "https://github.com/galcomez/ChillinPC/releases/latest/download/ChillinPC.exe"
        res = requests.get(ur_dw, stream=True, timeout=15)
        new_ex_nm = f"ChillinPC_{lateest_version}"
        with open(new_ex_nm, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        current_app = os.path.basename(sys.executable)
        cmd_windows=(f'timeout 2 /nobreak > nul &&' f'del "{current_app} &&' f'ren "{new_ex_nm}""{current_app}" &&' f'start "" "{current_app}"')
        subprocess.Popen(cmd_windows, shell=True)
        window.quit()
        sys.exit()
    except Exception as e:
        print("Failed to update:", e)
        eroor_upd_back()

#if update fails
def eroor_upd_back():
    for widget in window.winfo_children():
        widget.destroy()
        er_lbl_upd = ctk.CTkLabel(window, text="Update failed, reverting changes in 10 seconds...", font=("Arial", 18, "bold"), text_color= "#FF4D4D")
        er_lbl_upd.pack(expand=True, pady=20)
        window.update()
        
        window.after(10000, restore_before)
        restore_before()
def restore_before():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("500x400")
    window.resizable(False, False)
    github_link()
    al_stt()
#start updating
is_monitoring = True
def update_start():
    global is_monitoring
    is_monitoring = False
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("300x150")
    window.resizable(False, False)
    upd_lbl = ctk.CTkLabel(window, text="Updating... Do not close the application", font=("Arial", 17, "bold"),)
    upd_lbl.pack(expand=True, pady=20)
    window.update()
    threading.Thread(target=d_and_r, daemon=True).start()
def update_warning_s():
    if lateest_version !=app_version:
        path_to_inf_ic = os.path.join(icons_script, "icons", "about_upt.png")
        org_img_inf = Image.open(path_to_inf_ic)
        info_up= ctk.CTkImage(light_image=org_img_inf, dark_image=org_img_inf, size=(20, 20))
        info_show = ctk.CTkButton(master=update_inc, image=info_up, text="", width=50, height=50, fg_color="transparent", hover_color=("#e0e0e0", "#414545"), corner_radius=4, command=update_start)
        info_show.pack(side="left", fill="x", padx=10, pady=10)
        update_now = ctk.CTkLabel(update_inc, text=f"New version of Chillin PC is available. Your version is {app_version}, current version is {lateest_version}, downlaod it now!", wraplength=350)
        update_now.pack(side="top", fill="x", padx=10, pady=10)
    else:
        update_inc.pack_forget()
            
        

#Specs text
down_window = ctk.CTkFrame(window)
down_window.pack()

detected_os = ctk.CTkLabel(down_window, text=f"OS: {system_name} {system_version}", font=("Clash Grotesk", 12))
detected_os.grid(row=0, column=0, padx=10, pady=2, sticky="w")

detected_cpu = ctk.CTkLabel(down_window, text=f"CPU: {joint_cpu}", font=("Clash Grotesk", 12))
detected_cpu.grid(row=1, column=0, padx=10, pady=2, sticky="w")

detected_gpu = ctk.CTkLabel(down_window, text=f"GPU: {joint_gpu}", font=("Clash Grotesk", 12))
detected_gpu.grid(row=2, column=0, padx=10, pady=2, sticky="w")

detected_ram = ctk.CTkLabel(down_window, text=f"RAM: {joint_ram}GB", font=("Clash Grotesk", 12))
detected_ram.grid(row=3,column=0,padx=10,pady=2, sticky="w")

alert_window = ctk.CTkFrame(window)
alert_window.pack ()

#Title ALerts
alrt_tit = ctk.CTkLabel(alert_window, text ="ALERTS", font =("San Francisco Pro", 18))
alrt_tit.pack(side="top" ,padx=10, pady=10)



#selection buttons
selection_wind = ctk.CTkFrame(window)
selection_wind.pack()

GPU_show = ctk.BooleanVar(value=True)
CPU_show = ctk.BooleanVar(value=True)
RAM_show= ctk.BooleanVar(value=True)
Temp_show = ctk.BooleanVar(value=True)

gpu_choice = ctk.CTkCheckBox(master=selection_wind, text="GPU",checkmark_color ="#606061",fg_color="#C2882F", border_color="#5ac8c8", variable=GPU_show, text_color=("#3B4745", "#FFFFFF"), command=lambda: warnings())
gpu_choice.pack(side="left", padx=10, pady=5)
cpu_choice = ctk.CTkCheckBox(master=selection_wind, text ="CPU",checkmark_color ="#606061",fg_color="#C2882F",border_color="#5ac8c8", variable=CPU_show,text_color=("#3B4745", "#FFF7F7"), command=lambda: warnings() )
cpu_choice.pack(side ="left", padx=10, pady=5)
ram_choice = ctk.CTkCheckBox(master=selection_wind, text="RAM",checkmark_color ="#606061", fg_color="#C2882F",border_color="#5ac8c8", variable=RAM_show,text_color=("#3B4745", "#FFFFFF"), command=lambda: warnings() )
ram_choice.pack(side="left", padx=10, pady=5)
temp_choice = ctk.CTkCheckBox(master=selection_wind, text="Temps", checkmark_color ="#606061", fg_color="#C2882F", border_color="#5ac8c8", variable=Temp_show, text_color=("#3B4745", "#FFFFFF"), command=lambda: warnings())
temp_choice.pack(side="left", padx=10, pady=5)
#checking temperature detection, if motherboard does not support it, the button will be grayed out!
temp_resu = cpu_temperature()
if isinstance(temp_resu, str) or "°" not in temp_resu:
    temp_choice.destroy()
    Temp_show.set(False)
#Actual alerts showing up in UI, info taken from main_code.py

live_alerts = ctk.CTkFrame(window)
live_alerts.pack()

live_al = ctk.CTkScrollableFrame(master=live_alerts, height=150)
live_al.pack(fill="x", padx=20, pady=10)

#makes the diffrence bettwen already read and unread messages
def old_alert_sor():
    for child in live_al.winfo_children():
        child.destroy()
    noalarms = ctk.CTkLabel(live_al,text="No reports",font=("Playfair Display", 13),text_color="#666666",)
    noalarms.pack(side="top", padx=10, pady=5)
    if os.path.exists(GALBYTEALERT_FILE):
        try:
            with open(GALBYTEALERT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data and isinstance(data, list):
                for alarm in data:
                    alarm["archived"] = True
                with open(GALBYTEALERT_FILE,"w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            print(f"DEBUG: Error with archive!")
#reset button
path_to_reset = os.path.join(icons_script, "icons", "cleean_alrt.png")
reset_alr_org = Image.open(path_to_reset)
reset_alr = ctk.CTkImage(light_image=reset_alr_org, dark_image=reset_alr_org, size=(40, 40))
reset_show = ctk.CTkButton(master=live_alerts, image=reset_alr, text="", width=50, height=50, fg_color="transparent", hover_color=("#e0e0e0", "#414545"), corner_radius=4, command=old_alert_sor)
reset_show.pack(side="left", fill="x", padx=10, pady=10)

#loads alarms
def load_alrt():
    if os.path.exists(GALBYTEALERT_FILE):
        try:
            with open(GALBYTEALERT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    activce_alarms = [ alarm for alarm in data if not alarm.get("archived", False)]
                    return activce_alarms[::-1]
        except Exception as e:
            print(f"DEBUG: Error while loading alert {e}")
            return[]
        return[]
#starts reading alerts from main_code.py
def warnings(text="", tyoe="info"):
    alarms = load_alrt()
    for child in live_al.winfo_children():  child.destroy()
    if not alarms:
        noalarms = ctk.CTkLabel(live_al, text="No reports", font=("Playfair Display", 13), text_color="#666666")
        noalarms.pack(side="top", padx=10, pady= 5)
    else: 
        for alarm in reversed(alarms):
            acctive_us = alarm.get("active_process", "Unkown")
            gpu_temuj = temperaturegpu()
            date = alarm.get("date", "Unkown date")
            component = alarm.get("component", "system")
            details = alarm.get("details", "")
            if component == "GPU" and not gpu_choice.get(): continue
            if component == "CPU" and not cpu_choice.get(): continue
            if component == "RAM" and not ram_choice.get(): continue
            if component == "Temps" and 'temp_choice' in globals() and not temp_choice.get(): continue 
            bubli = ctk.CTkFrame(live_al, fg_color = ("#2b2b2b", "#575555"), corner_radius=8, border_width= 1, border_color="#3a3a3a",)
            bubli.pack(fill="x", pady=4, padx=5)
            if component !="GPU":
                lbl_comp = ctk.CTkLabel(bubli, text=f"[{component}]", font=("Arial", 13), text_color="#3587ad", anchor="w", justify="left")
                lbl_comp.pack(fill="x", padx=10, pady=(6, 2))
                lbl_temp = ctk.CTkLabel(bubli, text=f"{date}", font=("Arial", 13), text_color="#3587ad", anchor="w", justify="left")
                lbl_temp.pack(fill = "x", padx= 10, pady=10)
                lbl_head = ctk.CTkLabel(bubli, text=f"reason: {acctive_us}", font=("Arial", 13), text_color="#3587ad", anchor="w", justify="left")
                lbl_head.pack(fill="x", padx=10, pady=(6, 2))
                lbl_det = ctk.CTkLabel(bubli, text=f"details:{details}", font=("Arial", 13), text_color="#3587ad", anchor="w", justify="left")
                lbl_det.pack(fill="x", padx=10, pady=(6, 2))
            elif component == "RAM":
                lbl_ram_pr = ctk.CTkLabel(bubli, text=f"usage hit:{joint_ram}", font=("Arial", 13), text_color="#457729", anchor="w", justify="left")
                lbl_ram_pr.pack(fill="x", padx=10, pady=(6, 2))
                lbl_temp_pr = ctk.CTkLabel(bubli, text=f"{date}", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_temp_pr.pack(fill = "x", padx= 10, pady=10)
            elif component =="GPU":
                lbl_comp_g = ctk.CTkLabel(bubli, text=f"[{component}]", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_comp_g.pack(fill="x", padx=10, pady=(6, 2))
                lbl_temp_g = ctk.CTkLabel(bubli, text=f"{date}", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_temp_g.pack(fill = "x", padx= 10, pady=10)
                lbl_head_g = ctk.CTkLabel(bubli, text=f"reason: work in progress", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_head_g.pack(fill="x", padx=10, pady=(6, 2))
                lbl_det_g = ctk.CTkLabel(bubli, text=f"details:{details}", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_det_g.pack(fill="x", padx=10, pady=(6, 2))
                lbl_temp_g = ctk.CTkLabel(bubli, text=f"temps:{gpu_temuj}", font=("Arial", 13), text_color="#ffffff", anchor="w", justify="left")
                lbl_temp_g.pack(fill="x", padx=10, pady=(6, 2))
            elif component == "Temps":
                lbl_comp_t = ctk.CTkLabel(bubli, text=f"[{component}]", font=("Arial", 13), text_color="#c5ee0c", anchor="w", justify="left")
                lbl_comp_t.pack(fill="x", padx=10, pady=(6, 2))
                lbl_temp_t = ctk.CTkLabel(bubli, text=f"{date}", font=("Arial", 13), text_color="#c5ee0c", anchor="w", justify="left")
                lbl_temp_t.pack(fill = "x", padx= 10, pady= 10)
                lbl_head_t = ctk.CTkLabel(bubli, text=f"CPU hit {cpu_temperature}", font=("Arial", 13), text_color="#c5ee0c", anchor="w", justify="left")
                lbl_head_t.pack(fill="x", padx=10, pady=(6, 2))
                
    window.after(5000, warnings)
print("warnings")

eigic = ctk.CTkFrame(window)
eigic.pack(side="top", fill="x")

icone = ctk.CTkLabel(eigic, text ="Icons by icons8", font =("San Francisco Pro", 10))
icone.pack(side="top" ,padx=10, pady=10)

update_warning_s()
updating()
old_alert_sor()
warnings() 
if __name__ == "__main__":
    # Tukaj zaženi svoje niti za CPU/GPU monitoring
    tray_thread = threading.Thread(target=system_try_i, daemon=True)
    tray_thread.start()
window.mainloop()