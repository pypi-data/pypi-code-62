import ctypes
global hwnd
hwnd = ctypes.windll.user32.GetForegroundWindow()
WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_UP = 10
APPCOMMAND_VOLUME_DOWN = 9
APPCOMMAND_VOLUME_MUTE = 8
'''
pack-name:Volume
using Module: ctypes
other-files in this script:user32.dll
'''
class Volume_control():
    '''
    base class for control volume on windows
    function in this class:
        SetVolUp(self,volume)
            make the system-volume += volume
        SetVolDown(self,volume)
            make the system-volume -= volume
        SetVolMute(self)
            make system-volume mute
        SetVolTo(self,volume)
            make the system-volume to volume
    if function run successfuly,retuen 0
    if some things wrong with function,return -1
    '''
    def SetVolUp(self,volume):
        '''
        make the system-volume += volume
        '''
        try:
            for i in range(int(int(volume)/int(2))):
                ctypes.windll.user32.PostMessageA(hwnd, WM_APPCOMMAND, 0,APPCOMMAND_VOLUME_UP * 0x10000)
            return 0
        except:
            return -1
    def SetVolDown(self,volume):
        '''
        make the system-volume -= volume
        '''
        try:
            for i in range(int(int(volume)/int(2))):
                ctypes.windll.user32.PostMessageA(hwnd, WM_APPCOMMAND, 0,APPCOMMAND_VOLUME_DOWN * 0x10000)
            return 0
        except:
            return -1
    def SetVolMute(self):
        '''
        make system-volume mute
        '''
        try:
            ctypes.windll.user32.PostMessageA(hwnd, WM_APPCOMMAND, 0,APPCOMMAND_VOLUME_MUTE * 0x10000)
            return 0
        except:
            return -1
    def SetVolTo(self,volume):
        '''
        make the system-volume to volume
        '''
        try:
            self.SetVolDown(100)
            for i in range(int(int(volume)/int(2))):
                ctypes.windll.user32.PostMessageA(hwnd, WM_APPCOMMAND, 0,APPCOMMAND_VOLUME_UP * 0x10000)
            return 0
        except:
            return -1
            


