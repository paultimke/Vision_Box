import serial
import serial.tools.list_ports
import time
from vbox_logger import logger

class light_controller:
    def __init__(self):
        """ Light Controller object constructor\
            Establishes serial port connection to MCU """
        self.setup_complete = False

        # Automatically looks for device in listed ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            try:
                self._ser = serial.Serial(port.device, 
                                         baudrate=19200,
                                         timeout=0.5)
                
                # Send dummy byte and wait for response to ensure
                # connection with real light controller device was made
                DUMMY_BYTES = b'255'
                self._ser.write(DUMMY_BYTES)
                if self._wait_mcu_ack(DUMMY_BYTES):
                    self.setup_complete = True
                    logger.debug(f"[VB]: Connection to {port.device} successful")
                else:
                    # If ACK was not received, close connection with
                    # connected serial port
                    self._ser.close()
            except:
                continue
        
        if not self.setup_complete:
            logger.warning("[VB]: Could not establish a connection with " 
                  "Light Controller Hardware")

    def detach(self):
        """ Light Controller object destructor\
            Closes serial port connection with MCU """
        if self.setup_complete:
            self._ser.close()
            logger.debug(f"[VB]: Connection with {self._ser.port} closed")

    def set_brightness(self, luxes: int):
        """ Command to set Vision Box light brightness level"""
        if self.setup_complete:
            tx_bytes = self._serialize_luxes(luxes)
            self._ser.write(tx_bytes)
            # Confirm data sent was received well
            if self._wait_mcu_ack(tx_bytes):
                logger.info(f"[VB]: Light brightness succesfully set to {luxes} lux")

    def _serialize_luxes(self, luxes: int):
        """ Converts int lux value into corresponding string to be sent\
            prefixed by MCU start char sequence for UART interrupt trigger """
        if self.setup_complete:
            MCU_START_CHAR_SEQUENCE = ""
            tx_bytes = bytearray(MCU_START_CHAR_SEQUENCE + str(luxes), 'utf-8')
            return tx_bytes

    def _wait_mcu_ack(self, compare_string):
        """ Waits for MCU acknowledge to a previously sent command.\n
            Returns True if data received by MCU is equal to data sent
            and False otherwise.
            Data echoed by MCU must match format RX<NL> where X is a number"""
        # Give time for light controller device to respond
        time.sleep(0.5)

        # Wait for acknowledge and verify data format
        valid = False
        response = self._ser.readline().decode('utf-8')
        if response.startswith('R') and response.endswith('\n'):
            response = response.removeprefix('R').strip()
            if response == compare_string.decode('utf-8'):
                valid = True
        return valid

def Set_light(luxes):
    light_control = light_controller()
    light_control.set_brightness(luxes)
    light_control.detach()
