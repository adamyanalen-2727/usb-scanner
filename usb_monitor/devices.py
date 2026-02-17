import pyudev

def get_usb_serial_num():
    contex = pyudev.Context()
    serial_numbers = {}

    for device in contex.list_devices(subsystem='usb'):
        if device.device_type == 'usb_device':
            vendor_id = device.get('ID_VENDOR_ID')
            product_id = device.get('ID_MODEL_ID')

            # The serial number might be in ID_SERIAL_SHORT or ID_SERIAL
            try:
                serial = device['ID_SERIAL_SHORT']
            except KeyError:
                try:
                    serial = device['ID_SERIAL']
                except KeyError:
                    serial = "N/A" # Some devices don't have a serial number descriptor

            if serial != "N/A":
                serial_numbers[device.device_node] = {
                    'vendor_id': vendor_id,
                    'product_id': product_id,
                    'serial_number': serial
                }

    return serial_numbers

