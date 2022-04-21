from pathlib import Path
import subprocess
import requests,os,sys,cv2,numpy,threading,time
class ADB:
    KEYCODE_0 = 0,
    KEYCODE_SOFT_LEFT = 1,
    KEYCODE_SOFT_RIGHT = 2,
    KEYCODE_HOME = 3,
    KEYCODE_BACK = 4,
    KEYCODE_CALL = 5,
    KEYCODE_ENDCALL = 6,
    KEYCODE_0_ = 7,
    KEYCODE_1 = 8,
    KEYCODE_2 = 9,
    KEYCODE_3 = 10,
    KEYCODE_4 = 11,
    KEYCODE_5 = 12,
    KEYCODE_6 = 13,
    KEYCODE_7 = 14,
    KEYCODE_8 = 0xF,
    KEYCODE_9 = 0x10,
    KEYCODE_STAR = 17,
    KEYCODE_POUND = 18,
    KEYCODE_DPAD_UP = 19,
    KEYCODE_DPAD_DOWN = 20,
    KEYCODE_DPAD_LEFT = 21,
    KEYCODE_DPAD_RIGHT = 22,
    KEYCODE_DPAD_CENTER = 23,
    KEYCODE_VOLUME_UP = 24,
    KEYCODE_VOLUME_DOWN = 25,
    KEYCODE_POWER = 26,
    KEYCODE_CAMERA = 27,
    KEYCODE_CLEAR = 28,
    KEYCODE_A = 29,
    KEYCODE_B = 30,
    KEYCODE_C = 0x1F,
    KEYCODE_D = 0x20,
    KEYCODE_E = 33,
    KEYCODE_F = 34,
    KEYCODE_G = 35,
    KEYCODE_H = 36,
    KEYCODE_I = 37,
    KEYCODE_J = 38,
    KEYCODE_K = 39,
    KEYCODE_L = 40,
    KEYCODE_M = 41,
    KEYCODE_N = 42,
    KEYCODE_O = 43,
    KEYCODE_P = 44,
    KEYCODE_Q = 45,
    KEYCODE_R = 46,
    KEYCODE_S = 47,
    KEYCODE_T = 48,
    KEYCODE_U = 49,
    KEYCODE_V = 50,
    KEYCODE_W = 51,
    KEYCODE_X = 52,
    KEYCODE_Y = 53,
    KEYCODE_Z = 54,
    KEYCODE_COMMA = 55,
    KEYCODE_PERIOD = 56,
    KEYCODE_ALT_LEFT = 57,
    KEYCODE_ALT_RIGHT = 58,
    KEYCODE_SHIFT_LEFT = 59,
    KEYCODE_SHIFT_RIGHT = 60,
    KEYCODE_TAB = 61,
    KEYCODE_SPACE = 62,
    KEYCODE_SYM = 0x3F,
    KEYCODE_EXPLORER = 0x40,
    KEYCODE_ENVELOPE = 65,
    KEYCODE_ENTER = 66,
    KEYCODE_DEL = 67,
    KEYCODE_GRAVE = 68,
    KEYCODE_MINUS = 69,
    KEYCODE_EQUALS = 70,
    KEYCODE_LEFT_BRACKET = 71,
    KEYCODE_RIGHT_BRACKET = 72,
    KEYCODE_BACKSLASH = 73,
    KEYCODE_SEMICOLON = 74,
    KEYCODE_APOSTROPHE = 75,
    KEYCODE_SLASH = 76,
    KEYCODE_AT = 77,
    KEYCODE_NUM = 78,
    KEYCODE_HEADSETHOOK = 79,
    KEYCODE_FOCUS = 80,
    KEYCODE_PLUS = 81,
    KEYCODE_MENU = 82,
    KEYCODE_NOTIFICATION = 83,
    KEYCODE_APP_SWITCH = 187
    def __init__(self) -> None:
        pass
    def GetDevices(self):
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
    def KeyEvent(self, emulator, key):
        os.system(f"adb -s {emulator} shell input keyevent {str(key)}")
    def InpuText(self, emulator, text):
        os.system(f"adb -s {emulator} shell input text '{text}'")
    def Wipe(delf, emulator, x1, y1, x2, y2):
        os.system(f"adb -s {emulator} shell input touchscreen swipe {x1} {y1} {x2} {y2}")
    def OpenLink(self, emulator, link):
        subprocess.call("adb -s "+emulator+" shell am start -a android.intent.action.VIEW -d '"+link+"'")
    def Screen_Capture(self, emulator):
        os.system(f"adb -s {emulator} shell screencap /sdcard/Download/{emulator}.png")
        os.system(f"adb -s {emulator} pull /sdcard/Download/{emulator}.png {emulator}.png")
    def Click(self, emulator, x, y):
        os.system(f"adb -s {emulator} shell input tap {x} {y}")
    def find_template(self, emulator, target_pic_name = '', template_pic_name = False, threshold = 0.99):
        if template_pic_name == False:
            self.Screen_Capture(emulator)
            template_pic_name = emulator+".png"
        else:
            self.Screen_Capture(template_pic_name)
        img = cv2.imread(target_pic_name)
        img2 = cv2.imread(template_pic_name)
        w = img2.shape[1]
        h = img2.shape[0]
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED) 
        location = numpy.where(result >= threshold)
        test_data = list(zip(*location[::-1]))
        is_match = len(test_data) > 0
        point = []
        if is_match:
            point.append((test_data[0][0] + w/2, test_data[0][1] + h/2))
            return is_match, point, test_data
        else:
            return "","",""
    def Tap_Img(self, emulator, img_path):
        is_match, point, test_data = self.find_template(emulator, target_pic_name=img_path)
        if is_match!="":
            x, y = test_data[0][0], test_data[0][1]  
            self.Click(emulator, x, y)
    def Change_Proxy(self, emulator, proxy):
        os.system(f"adb -s {emulator} shell settings put global http_proxy {proxy}")
    def Remove_Proxy(self, emulator):
        os.system(f"adb -s {emulator} shell settings put global http_proxy :0")
class LDPlayer:
    def __init__(self):
        self.pathLD = "D:\\LDPlayer\\LDPlayer4.0\\ldconsole.exe"
    def Open(self, param, NameOrId):
        subprocess.call(f"{self.pathLD} launch --{param} {NameOrId}")
    def Open_App(self, param, NameOrId, Package_Name):
        subprocess.call(f"{self.pathLD} launchex --{param} {NameOrId} --packagename {Package_Name}")
    def Close(self, param, NameOrId):
        subprocess.call(f"{self.pathLD} quit --{param} {NameOrId}")
    def CloseAll(self):
        subprocess.call(f"{self.pathLD} quitall")
    def Rebot(self, param, NameOrId):
        subprocess.call(f"{self.pathLD} reboot --{param} {NameOrId}")
    def Create(self, Name):
        subprocess.call(f"{self.pathLD} add --name {Name}")
    def Copy(self, Name, From_NameOrId):
        subprocess.call(f"{self.pathLD} copy --name {Name} --from {From_NameOrId}")
    def Remove(self, param, NameOrId):
        subprocess.call(f"{self.pathLD} remove --{param} {NameOrId}")
    def Rename(self, param, NameOrId, title_new):
        subprocess.call(f"{self.pathLD} rename --{param} {NameOrId} --title {title_new}")
    def InstallApp_File(self, param, NameOrId, File_Name):
        subprocess.call(f"{self.pathLD} installapp --{param} {NameOrId} --filename '{File_Name}'")
    def InstallApp_Package(self, param, NameOrId, Package_Name):
        subprocess.call(f"{self.pathLD} installapp --{param} {NameOrId} --packagename {Package_Name}")
    def UnInstallApp(self, param, NameOrId, Package_Name):
        subprocess.call(f"{self.pathLD} uninstallapp --{param} {NameOrId} --packagename {Package_Name}")
    def RunApp(self, param, NameOrId, Package_Name):
        subprocess.call(f"{self.pathLD} runapp --{param} {NameOrId} --packagename {Package_Name}")
    def KillApp(self, param, NameOrId, Package_Name):
        subprocess.call(f"{self.pathLD} killapp --{param} {NameOrId} --packagename {Package_Name}")
    def Locate(self, param, NameOrId, Lng, Lat):
        subprocess.call(f"{self.pathLD} locate --{param} {NameOrId} --LLI {Lng},{Lat}")
    def Change_Property(self, param, NameOrId, cmd):
        subprocess.call(f"{self.pathLD} modify --{param} {NameOrId} {cmd}")
    def SetProp(self, param, NameOrId, key, value):
        subprocess.call(f"{self.pathLD} setprop --{param} {NameOrId} --key {key} --value {value}")
    def InstallAGetProppp_Package(self, param, NameOrId, key):
        return subprocess.check_output(f"{self.pathLD} getprop --{param} {NameOrId} --key {key}")
    def ADB_LD(self, param, NameOrId, cmd):
        return subprocess.check_output(f"{self.pathLD} adb --{param} {NameOrId} --command {cmd}")
    def DownCPU(self, param, NameOrId, rate):
        subprocess.call(f"{self.pathLD} downcpu --{param} {NameOrId} --rate {rate}")
    def IsDevice_Running(self, param, NameOrId):
        a = subprocess.check_output(f"{self.pathLD} isrunning --{param} {NameOrId}")
        if "running"  in a:
            return True
        else:
            return False
    def DownCPU(self, param, NameOrId, audio, fast_play, clean_mode):
        subprocess.call(f"{self.pathLD} globalsetting --{param} {NameOrId} --audio {audio} --fastplay {fast_play} --cleanmode {clean_mode}")
    def GetDevices(self):
        list = str(subprocess.check_output(f"{self.pathLD} list")).replace("b'","").replace("'","").split("\\r\\n")
        list.pop()
        return list
    def GetDevices2(self):
        list2 = str(subprocess.check_output(f"{self.pathLD} list2")).replace("b'","").replace("'","").split("\\r\\n")
        list2.pop()
        Info_Devices = []
        for i in list2:
            item = i.split(",")
            Info_Devices.append({"name":item[1],"index":item[0],"adb_id":"-1"})
        return Info_Devices