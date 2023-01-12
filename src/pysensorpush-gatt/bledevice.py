import pexpect
import sys

class BLEDevice():
    DEFAULT_CONNECT_TIMEOUT=10
    TIMEOUT=10
    
    RESPONSE_WRITE_SUCCESS = "Characteristic value was written successfully\r\n"
    RESPONSE_READ_SUCCESS = "Characteristic value/descriptor: "
    RESPONSE_CONNECT_SUCCESS = "Connection successful"


    def __init__(self, mac_address, hci_device='hci0'):
        """
        Initializes the device
        Args:
            mac_address (str): The mac address of the device to connect to
            in the format xx:xx:xx:xx:xx:xx

            hci_device (str):
        """
        self._mac_address = mac_address
        self._child = None
        self._connected = False

        cmd = "gatttool -b {} -i {} -I".format(self._mac_address, hci_device)
        self._child = pexpect.spawn(cmd)
        
    def connect(self, timeout=DEFAULT_CONNECT_TIMEOUT):
        """
        Connects to the device 
        Args:
            timeout (int): The timeout to wait for a connection in seconds
        """
        print("Connecting to "+addr+"..."),
        try:
            self._child.sendline("connect")
            self._child.expect(RESPONSE_CONNECTION_SUCCESS, timeout=TIMEOUT)
        except:
            print("connect error", sys.exc_info()[0])
        return

    def stop(self):
        """
        Disconnects from the device and stops gatttool
        """
        if self._child.isalive():
            self._con.sendline('exit')

            # wait one second for gatttool to stop
            for i in range(100):
                if not self._child.isalive(): break
                time.sleep(0.01)

            self._child.close()
            self._connected = False

    def read_hnd(self, hnd):
        """
        Read bluetooth characteristic handle
        Args:
            hnd (str): The handle to read
        """
        try:
            self._child.sendline("char-read-hnd "+hnd)
            self._child.expect(RESPONSE_READ_SUCCESS, timeout=TIMEOUT)
            self._child.expect("\r\n", timeout=TIMEOUT)
            hex_str = child.before.decode().replace(" ","")
            return hex_str
        except:
            print("connect error", sys.exc_info()[0])
            return ""

    def write_req(hnd, val):
        """
        Write bluetooh characteristic handle
        Args:
            hnd (str): The handle to write to
            val (str): The value to write as a hex string
        Returns:
            True if success, otherwise False
        """
        try:
            child.sendline("char-write-req "+hnd+" "+val)
            child.expect(RESPONSE_WRITE_SUCCESS, timeout=TIMEOUT)
            return True
        except:
            return False
