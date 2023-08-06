from serial import Serial
from time import sleep
from threading import Thread
from requests import post
from smtplib import SMTP

class BSerial(Serial):
    """[Class makes the connection, sends data and receives data from serial port.]

    :param Serial: [inherits from Serial class]
    :type Serial: [Serial]
    """
    def __init__(self,**kargs):
        """[constructor of Serial. see more information: init from Serial, more information in https://pyserial.readthedocs.io/en/latest/pyserial_api.html]
        for example:
            port: COM1
            baudrate: 9600
        """
        super().__init__(**kargs)

        self.separator="-"

    def write_string_port(self,value):
        """[write string in serial port]
        :param value: [send value to serial port. It will be converted to string + '\n'. You have to control it]
        :type value: [type]
        """
        self.write((str(value)+'\n').encode())

    def start_read_string_port(self,command:'function', separator="-"):
        """[initialize reading on serial port]

        :param command: [it will receive as parameter a value from serial port.
                        if they are several values, you have to make sure that they are sent separated by a "-".]
        :type command: function
        :param separator: [separator of values], defaults to "-"
        :type separator: str, optional
        """
        self.separator = separator
        self.start_thread = True
        self.thread = Thread(target=self.__Thread_read_port,args=(command,))
        self.thread.start()
        print("[LOG] >> Reading data...")

    def stop_read_string_port(self):
        """[method to stop receiving values]"""
        self.start_thread = False
        self.thread.join()
        del(self.start_thread)
        del(self.thread)
        print("[LOG] >> Connection has been closed.")

    def __Thread_read_port(self,command):
        """[private method]

        :param command: [this method read values from serial port]
        :type command: [function]
        """
        while self.start_thread:
            if self.in_waiting > 0:
                try:
                    value = self.readline().decode().replace("\n","")
                    command(value.split(self.separator))
                except Exception as e:
                    print(f"[ERROR] >> {str(e)}")

class Ubidot_Client:
    """
    This class offers connections to Ubidots platform.
    Now only can values to one device.
    """
    def __init__(self,token,device):
        """ Constructor for client 

            token([str]): CREDENTIALS UBIDOT
            device([str]): Device Label

        """
        self.token = token
        self.label_device = device

        self.HEADERS = {'X-Auth-Token':token}

    def __send_value(self, data, variable_label):
        """this method is executing in thread
        """
        link = f"https://industrial.ubidots.com/api/v1.6/devices/{self.label_device}/{variable_label}/values"
        try:

            self.r = post(link,headers=self.HEADERS,json=data)
            print("[OK] >> DATA HAS BEEN SENDED SUCCESFUL")
        except Exception as e: 
            print(f"[ERROR] >> {str(e)}")

    def __ask_thread(self, inthread, data, variable_label):
        if inthread:
            Thread(target=self.__send_value, args=(data, variable_label)).start()
        else:
            self.__send_value(data, variable_label)

    def send_value(self, variable_label, inthread=True,  **data):
        """[Send one value to ubidots]

        Args:
            variable_label ([str]): [variable name]
            inthread (bool, optional): [if you want send in a thread]. Defaults to True.
        """
        self.__ask_thread(inthread, data, variable_label)
        

    def send_values(self, variable_label, inthread=True, *data):
        """[Send many values to ubidots]

        Args:
            variable_label ([str]): [variable name]
            inthread (bool, optional): [if you want send in a thread]. Defaults to True.
        """

        rpta = all(list(map(data, lambda item: type(item) == dict)))

        if not rpta:
            raise ValueError("[ERROR] >> Each element in data must be dictionary")

        self.__ask_thread(inthread, data, variable_label)

    def close(self):
        self.r.close()
        print("[LOG] >> Connection has been closed.")

class Email:
    """
    this Class offers methods to send a email.
    """
    def __init__(self,email,password):
        """init class Email

        Args:
            email ([str]): [your email]
            password ([str]): [your password]
        """

        self.email = email
        self.password = password

    def send_email(self,dest,message="email from python",server="smtp.live.com",port=587):
        """send an email in a second thread
            It work with gmail by default
        Args:
            dest (str): [destination email]
            message (str, optional): [message of the email]. Defaults to "email from python".
            server (str, optional): [server from the domain]. Defaults to "smtp.live.com".
            port (int, optional): [port from the domain]. Defaults to 587.
        """
        t = Thread(target=self.__thread_send_email,args=(dest,message,server,port))
        t.start()

    def __thread_send_email(self,dest,message,server,port):
        message = '\n'+message
        try:
            with SMTP(server,port) as server:
                server.ehlo() 
                server.starttls() 
                server.login(self.email,self.password)
                server.sendmail(self.email,dest,message)
                server.quit()
        except Exception as e:
            print(f"[RROR] = {str(e)}")


        