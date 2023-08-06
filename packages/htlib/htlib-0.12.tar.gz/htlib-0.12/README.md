libserial
    
    Este módulo facilita algunas tareas con pyserial y provee conexion a ubidots consumiendo su API

    def action_read(value):#function to print value that receive from serial port
        print(value)

    s = BSerial(port='COM1',baudrate=9600)
    s.start_read_string_port(action_read)#start to read serial port

    while True:
        valor = input("Ingrese un valor - x para terminar")
        if valor == "x":break
        s.write_string_port(valor)
        sleep(1)#only for sthetic, if you wish try like comment
    s.stop_read_string_port()
    s.close()
