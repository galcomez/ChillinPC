import GPUtil
import wmi
import ctypes
import sys 
import psutil
#The GPU temperature reader
DEBUG = not getattr(sys, "frozen", False)
try:
    import pynvml
    pynvml.nvmlInit()
    Has_Invidia = True
except Exception:
    Has_Invidia =False

def temperaturegpu(unit="C"):
    celzijG = None
    if Has_Invidia:
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            celzijG = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        except Exception:
            celzijG = None
    if celzijG is None:
        try:
            w = wmi.WMI(namespace="root\\OpenHardwwareMonitor")
            temperature_infos = w.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == "Temperature" and "GPU" in sensor.Name:
                    celzijG = sensor.Value
                    break
        except Exception:
            celzijG = None
    if celzijG is None:
        return "GPU not supported!"
    if DEBUG: 
        if unit == "F":
            return f"{round((celzijG * 1.8) + 32, 1)}"
        return f"{round(celzijG, 1)}"
#The CPU temperatur reader
def cpu_temperature(unit="C"):
    administrator_detector = ctypes.windll.shell32.IsUserAnAdmin() !=0
    if not administrator_detector:
        return "Administrator privileges needed for this feature to work correctly!"
    try:
        w = wmi.WMI(namespace="root\\wmi")
        convertion = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
        celzij = (convertion / 10.0) - 273.15
        
        if unit =="F":
            farenheit = (celzij * 1.8) + 32
            return f"{round(farenheit, 1)} °F"
        return f"{round(celzij, 1)} °C"
    except Exception:
        return "Motherboard not supported, WMI unable to receive data about the current CPU temperature"