import pydbus
import os
import gi

gi.require_version('Gtk', '3.0')


class BluetoothInformation():
    def __init__(self):
        super().__init__()
        self.name = ""
        if self.device_exist():
            self.exist = True
            rfkill_bluetooth_id_command = """rfkill | grep 'bluetooth' | awk '{print $1}' """
            rfkill_bluetooth_id = os.popen(rfkill_bluetooth_id_command).read()

            command = """cat /sys/class/bluetooth/hci0/rfkill{0}/state""".format(rfkill_bluetooth_id[:-1])
            result = os.popen(command).read()
            powered_on = int(result)
            if powered_on > 0:
                self.power = True

                bus = pydbus.SystemBus()
                bus.get('org.bluez', '/org/bluez/hci0')
                mngr = bus.get('org.bluez', '/')

                mngd_objs = mngr.GetManagedObjects()
                for path in mngd_objs:
                    con_state = mngd_objs[path].get('org.bluez.Device1', {}
                                                    ).get('Connected', False)
                    if con_state:
                        self.name = mngd_objs[path].get(
                            'org.bluez.Device1', {}
                        ).get('Name')
            else:
                self.power = False
                self.name = ""
        else:
            self.exist = False
            self.power = False
            self.name = ""

    def device_exist(self):
        command = """cat /sys/class/bluetooth/hci0/device/uevent | grep -i driver"""
        result = os.popen(command).read()
        if len(result) > 0:
            return True
        else:
            return False

    def exists(self):
        return self.exist

    def is_powered_on(self):
        return self.power

    def get_name(self):
        return self.name
