import os
import hashlib
import sys



# Run shell command and remove \n from result
def shell_execute(cmd):
    return os.popen(cmd).read()[:-1]

def get_phone_info():
    serial = shell_execute('adb get-serialno')
    md5 = hashlib.md5(serial.encode()).hexdigest()
    return serial, md5


if __name__ == '__main__':
    
    # In 7.1.1 token to allow flashing is md5 of Phone Serial
    serial, token = get_phone_info()
    print("Phone Serial Number: " + serial + "Phone Token: " +token)

    print("Rebooting into Bootloader")
    shell_execute('adb reboot bootloader')

    #Flashing Service Bootloader & Booting into it
    shell_execute('fastboot oem dm-verity '+ token)
    shell_execute('fastboot flash aboot D1C-emmc_appsboot.mbn')
    shell_execute('fastboot reboot-bootloader')
    shell_execute('fastboot oem dm-verity '+ token ) 
    
    #Flashing TWRP recovery image
    shell_execute('fastboot flash recovery twrp.img')
    #Boot into recovery
    shell_execute('fastboot reboot recovery')

    print("Now you should be booted into TWRP recovery shell")
    print("Go to Advanced -> Magisc Root and apply it")