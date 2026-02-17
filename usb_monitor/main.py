from usb_monitor.disable_USBstorage import disable_usb_storage
from usb_monitor.devices import get_usb_serial_num
disable_usb_storage()
serial_nums = get_usb_serial_num()
for i in serial_nums:
    print(i)
