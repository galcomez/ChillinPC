import psutil
import GPU_analyzer
import time
import json
import os
from datetime import datetime
import temp_recorder
import cpuinfo
import GPUtil
import queue
import multiprocessing
import sys
import subprocess

if __name__ == "__main__":
    multiprocessing.freeze_support()
gpuname = None
cpuname = None
running = True
GALBYTEALERT_FILE = "GalBytePCHelthchecker.json"
ui_callb = None
def registeer_ui_callb(function):
    global ui_callb
    ui_callb = function
def event_detecetd(message, type="warning"):
    alert_queue = queue.Queue()
def stop_monitoring():
    global running
    running = False
ALARM_LIMIT_CPU = 98.0
ALARM_LIMIT_GPU= 100.0

def load_alarms():
    if os.path.exists(GALBYTEALERT_FILE):
        try:
            with open(GALBYTEALERT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data is not None:
                    today = datetime.now().strftime("%d.%m.%Y")
                    alarms_day = []
                    for alarm in data:
                        alarm_date = alarm.get("date", "").split(" ")[0]
                        if alarm_date == today:
                            alarms_day.append(alarm)
                    return alarms_day 
                
                
                return[]
        except: 
            return[]
    return[]

    
def save_alarm(component, details, game):
    alarms = load_alarms()
    new_alarm = {                                                                 #This is all of the data the program saves when the CPU load goes higher than expected...
        "date": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "component": component,
        "details": details,
        "active_process": game, 
        "severity": "high",
        "archived": False,
        "read": False,
    }

    alarms.append(new_alarm)
    with open(GALBYTEALERT_FILE, "w", encoding="utf-8") as f:
        json.dump(alarms, f, indent=4, ensure_ascii=False)

            
    
def monitor_strt():
    global gpuname, cpuname, running
    if gpuname is None:
        gpuname = GPUtil.getGPUs()[0].name
    if cpuname is None:
        cpuname = cpuinfo.get_cpu_info()["brand_raw"]
    print("GalByte PC monitor is running in the background. . . Press Ctrl+C to exit it")

    try:
        while running:
            joint_cpu = psutil.cpu_percent(interval=2)
            joint_ram = psutil.virtual_memory().percent                                                  
            
            if joint_cpu > ALARM_LIMIT_CPU:
                the_most_difficult_process = "unable to detect"
                biggest_cpu = 0
                
                for proc in psutil.process_iter(['name']):
                    try:
                        if "idle" in proc.info['name'].lower() or "system" in proc.info['name'].lower():
                            continue
                        current_cpu = proc.cpu_percent(interval=None)
                        
                        if current_cpu > biggest_cpu:
                            biggest_cpu = current_cpu
                            the_most_difficult_process = proc.info['name']
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                save_alarm("CPU", f"Usage hit {joint_cpu} %", the_most_difficult_process) #The CPU block ends, here starts the GPU part which most of it is in the other file.
        #GPU block! Most of the files in the other file called GPU_analyzer.py
            is_critical, gpuussage, gpunamingN= GPU_analyzer.GPUc(ALARM_LIMIT_GPU)
            if is_critical:
                save_alarm("GPU",f"Usage hit {gpuussage:.1f} %", gpunamingN)

            #RAM block!
            ALERT_SYSTEM_RAM = 95.0
            if joint_ram > ALERT_SYSTEM_RAM:
                top_process_spending = "unable to detect"
                biggest_ram = 0
                try:
                    for proc in psutil.process_iter(['name']):
                        try:
                            curently_ram = proc.memory_percent()
                            if curently_ram > biggest_ram:
                                biggest_ram = curently_ram
                                top_process_spending = proc.info['name']
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                except Exception:
                    pass
                save_alarm("RAM", f" Hit usage limits of {joint_ram}%", top_process_spending)
            #temperatures reader block
            cpu_temperature = temp_recorder.cpu_temperature()
            gpu_temperature = temp_recorder.temperaturegpu()
            cpu_alert =False
            gpu_alert = False
            #CPU temperature alert system
            if isinstance(cpu_temperature, str) and ("°C" in cpu_temperature or "°F" in cpu_temperature):
                temp_number_cpu = float(cpu_temperature.replace(" °C", "").replace(" °F", ""))
                if temp_number_cpu > 100.0:                                                   
                    cpu_alert = True

        
            #GPU temperature alert system
            if isinstance(gpu_temperature, str) and ("°C" in gpu_temperature or "°F" in gpu_temperature):
                temp_number_gpu = float(gpu_temperature.replace(" °C", "").replace(" °F", ""))
                if temp_number_gpu > 100.0:
                    gpu_alert= True

        
        
            time.sleep(2)
    except KeyboardInterrupt:
        ("\n GalByte PC Monitor successfully stopped, you can finprintd recorded critical usage in 'GalBytePCHelthchecker.json' ")   #If I'm honest I have no clue to where the .json file is saved... Good luck!
if __name__ == "__main__":
    monitor_strt()
ui_callb = None