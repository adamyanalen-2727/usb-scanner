#!/usr/bin/env python3
import usb.core
import usb.util

devices = usb.core.find(find_all=True)

if devices is None:
    print("No USB devices found (or permission issue). Try with sudo.")
    exit(1)

print(f"Found {len(list(devices))} USB devices.\n")

for dev in devices:
    try:
        manufacturer = usb.util.get_string(dev, dev.iManufacturer) or "N/A"
        product      = usb.util.get_string(dev, dev.iProduct) or "N/A"
        serial       = usb.util.get_string(dev, dev.iSerialNumber) or "N/A"
    except Exception as e:
        manufacturer = product = serial = f"Error: {e}"

    print(f"Bus {dev.bus:03d} Dev {dev.address:03d}  ID {dev.idVendor:04x}:{dev.idProduct:04x}")
    print(f"  Manufacturer: {manufacturer}")
    print(f"  Product     : {product}")
    print(f"  Serial      : {serial}")
    print("-" * 50)
