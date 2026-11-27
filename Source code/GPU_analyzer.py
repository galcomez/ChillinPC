import GPUtil
import time 
print("GPU detection turned on")
graphicalps = GPUtil.getGPUs()
print(f"DEBUG INFO: found GPU: {len(graphicalps)}")
def GPUc(alarm_limit):
    try: 
        graphicalps = GPUtil.getGPUs()
        if not graphicalps:
            return False, 0, ""
        for gpu in graphicalps:
            gpuussage = gpu.load *100
            if gpuussage > alarm_limit:
                return True, gpuussage, "Unable to detect"
        
        return False, 0, ""
    except Exception as e:
        print(f"Error while reading GPU: {e}")
        return False, 0, ""

