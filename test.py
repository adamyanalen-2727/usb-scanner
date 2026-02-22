#!/usr/bin/env python3
"""
Detect USB Mass Storage devices (flash drives) using pyusb.
Tries hard to detach kernel drivers and read configurations.

"""

import sys
import usb.core
import usb.util

def get_string_safe(dev, index):
    """Safely get USB string descriptor"""
    try:
        return usb.util.get_string(dev, index) or "N/A"
    except Exception:
        return "N/A (read error)"


def detect_usb_flashes():
    print("Scanning for USB devices...\n")

    devices = usb.core.find(find_all=True)
    if devices is None:
        print("→ No devices found (run with sudo?)")
        return []

    found_flashes = []

    for dev in devices:
        # Skip Linux root hubs
        if dev.idVendor == 0x1d6b:
            continue

        vid = hex(dev.idVendor)
        pid = hex(dev.idProduct)
        bus = dev.bus
        addr = dev.address

        print(f"→ Checking device {vid}:{pid}  Bus {bus:03d} Addr {addr:03d}")

        # Try to get basic info even without full access
        manuf = get_string_safe(dev, dev.iManufacturer)
        prod  = get_string_safe(dev, dev.iProduct)
        ser   = get_string_safe(dev, dev.iSerialNumber)

        print(f"    Manufacturer: {manuf}")
        print(f"    Product:      {prod}")
        print(f"    Serial:       {ser}")

        detached = False

        # Try to detach kernel driver from ALL possible interfaces (0–7)
        for iface_num in range(8):
            try:
                if dev.is_kernel_driver_active(iface_num):
                    print(f"    Detaching kernel driver from interface {iface_num}...")
                    dev.detach_kernel_driver(iface_num)
                    detached = True
                    print(f"    → Detached interface {iface_num}")
            except usb.core.USBError as e:
                err_str = str(e)
                if "not found" in err_str.lower() or "Entity not found" in err_str:
                    # Normal - interface probably doesn't exist
                    pass
                elif "busy" in err_str.lower() or "Resource busy" in err_str:
                    print(f"    → Resource busy on interface {iface_num} (driver in use)")
                else:
                    print(f"    Detach failed on intf {iface_num}: {e}")

        # Now try to access configuration
        cfg = None
        try:
            cfg = dev.get_active_configuration()
            if cfg is None:
                print("    No active config → trying set_configuration()")
                dev.set_configuration()           # try default (first) config
                cfg = dev.get_active_configuration()
        except usb.core.USBError as e:
            print(f"    Config error: {e}")
            if "busy" in str(e).lower():
                print("    → Typical when mass storage driver is bound")

        if cfg:
            print("    Configuration found. Checking interfaces...")
            for intf in cfg:
                print(f"      Interface {intf.bInterfaceNumber}: class {intf.bInterfaceClass:02x}h")
                if intf.bInterfaceClass == 0x08:  # Mass Storage
                    print("\n" + "="*60)
                    print(">>> USB FLASH / MASS STORAGE DEVICE DETECTED <<<")
                    print(f"    VID:PID     {vid}:{pid}")
                    print(f"    Bus/Addr    {bus:03d}/{addr:03d}")
                    print(f"    Manufacturer: {manuf}")
                    print(f"    Product:      {prod}")
                    print(f"    Serial:       {ser}")
                    print(f"    Interface:    {intf.bInterfaceNumber}")
                    print("="*60 + "\n")
                    found_flashes.append({
                        'vid': vid, 'pid': pid,
                        'bus': bus, 'addr': addr,
                        'manufacturer': manuf,
                        'product': prod,
                        'serial': ser
                    })

        # Optional: re-attach drivers if we detached them (good practice)
        if detached:
            print("    Re-attaching kernel drivers (if possible)...")
            for iface_num in range(8):
                try:
                    dev.attach_kernel_driver(iface_num)
                    print(f"    → Re-attached interface {iface_num}")
                except Exception:
                    pass  # many will fail - that's ok

        print("-" * 70)

    if not found_flashes:
        print("\nNo mass storage devices detected.")
        print("Common reasons:")
        print("  • usb_storage / uas driver is bound → detach often fails")
        print("  • Run with sudo")
        print("  • No flash connected")
        print("  • Device uses UAS protocol (harder to detach)")

    return found_flashes


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)

    print("USB Mass Storage Detector (aggressive detach mode)\n")
    print("Warning: Needs sudo. May temporarily hide /dev/sdX devices!\n")

    detect_usb_flashes()

    print("\nDone.")
