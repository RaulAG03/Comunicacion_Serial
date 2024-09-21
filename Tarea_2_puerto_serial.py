import sys
import glob
import serial
import time

from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk

#_________________________________________PUERTOS_COM____________________________________________________________________
result = []
def serial_ports():
    """Lists serial port name 
    : raices EnvironmentError:
        :return:
            A list of the serial ports avilable on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s'%(i+1) for i in range (10)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'): 
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('unsupported plataform')

    #result = []
    global result
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#_________________________________________RECONFIGURACION DE PUERTOS COM_________________________________________________

def config():
    puerto_selec = COMcombo.get()
    try:
        ser = serial.Serial(puerto_selec)
        ser.close()
        led_R.config(state="disabled")
        led_V.config(state="normal")
        
        
    except serial.SerialException:
        led_R.config(state="normal")
        led_V.config(state="disabled")
   
#________________________________________Habilitaion o Desasabiltacion de LEDs__________________________________________
def Encender():
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
    time.sleep(2)
    print('led encendido')
    arduino.write(b'1')
    time.sleep(0.05)    
    
def Apagar():
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
    time.sleep(2)
    print('led apagado')
    arduino.write(b'0')
    time.sleep(0.05) 
#____________________________________________________________________________________________________________________________
#________________________________________Habilitacion Tab2_________________________________________________________________
#_________________________________________________________________________________________________________________________
def seleccion():
    var = int(selec.get())
    print(var)
    if var == 1:
        print('seleccion1')
        valor_suma.config(state='normal')            #seleccion 1
        button1.config(state='normal')
        respuesta.config(state="normal")                                                           
        button2.config(state="disabled")        #seleccion 2
        mostrar.config(state="disabled")      
        pwm_inten.config(state="disabled")          #seleccion 3
        button3.config(state="disabled")        
    elif var == 2:
        print('seleccion2')
        valor_suma.config(state='disabled')          #seleccion 1
        button1.config(state='disabled')
        respuesta.config(state="disabled")                                                                  
        button2.config(state="normal")          #seleccion 2
        mostrar.config(state="normal")     
        pwm_inten.config(state="disabled")          #seleccion 3
        button3.config(state="disabled")  
    elif var == 3:
        print('seleccion3')
        valor_suma.config(state='disabled')          #seleccion 1
        button1.config(state='disabled')
        respuesta.config(state="disabled")                                                                 
        button2.config(state="disabled")        #seleccion 2
        mostrar.config(state="disabled")      
        pwm_inten.config(state="normal")            #seleccion 3
        button3.config(state="normal")  
#________________________________________Seleccion 1_____________________________________________________________________

def suma():
    print('suma')
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    
    numero=int(valor_suma.get())
    arduino.write(f"S{numero}\n".encode())
    
    res = arduino.readline().decode().strip()
    print(res)
    respuesta.delete(0, tk.END)
    respuesta.insert(0, res)
    
#________________________________________Seleccion 2_____________________________________________________________________

def convercion():
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2) 
    arduino.write(b'LEER\n')
    
    con = arduino.readline().decode().strip()
    print(con)
    mostrar.delete(0, tk.END)
    mostrar.insert(0, con)
    
#________________________________________Seleccion 3_____________________________________________________________________

def Pwm():
    print('inicio')
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    
    pwm = int(pwm_inten.get())
    if 0 <= pwm <= 255:
            # Enviar el valor al Arduino
            arduino.write(f"P{pwm}\n".encode())
            print(pwm)
    else:
        print('fuera de rango')
        
#________________________________________VENTANA PRINCIPAL________________________________________________________________
root = ThemedTk(theme='equilux' ) #creamos la ventana principal aplicando el tema equilux 
root.title("PUERTO SERIAL") #colocamos el titulo de la ventana
root.geometry('500x500') #dimensiones de la ventana principal 

valor_1 = tk.StringVar()
check_on_var = tk.IntVar()
check_off_var = tk.IntVar()

TabControl = ttk.Notebook(root)
tab1 = ttk.Frame(TabControl)
tab2 = ttk.Frame(TabControl)
TabControl.add(tab1, text='PUERTOS COM')
TabControl.add(tab2, text='CONFIGURACION COM')
TabControl.pack(expand=1, fill="both")
current_value = tk.StringVar()

#______________________________________________________________________________________________________________________
#_______________________________________________TAB1___________________________________________________________________
detectar = ttk.Button(tab1, text="detectar puerto COM", command=serial_ports())
COMcombo = ttk.Combobox(tab1, state="readonly", textvariable= current_value)
print(serial_ports())
COMcombo['values'] = result
detectar.place(x=30, y=20)
COMcombo.place(x=20, y=60)

velocidad = ttk.Button(tab1, text="Velocidad De Conexion")
velocidad.place(x=200, y=20)
velocidadCon = ttk.Combobox(tab1, state="readonly", values=['14400','19200','38400','57600','115200','230400','460800'])
velocidadCon.place(x=200, y=60)

camb = ttk.Button(tab1, text='Aplicar Cambios Al Puerto sleccionado', command=config)
camb.place(x=70, y=110)

led_on = ttk.Button(tab1, text='Encender Led',command= Encender)
led_on.place(x=60, y=280)

led_of= ttk.Button(tab1, text='Apagar Led', command=Apagar)
led_of.place(x=230, y=280)

#_______________________________________________TAB2__________________________________________________________________

selec = ttk.Spinbox(tab2, from_=1, to=3, increment=1, state="readonly")
selec.place(x=40, y=30, width=130)
button_selec = ttk.Button(tab2, text='Iniciar', command=seleccion)
button_selec.place(x=180, y=30, width=135)
                                     #seleccion 1
valor_suma = ttk.Entry(tab2, state="disabled")
valor_suma.place(x=40,y=110, width=130)
respuesta = ttk.Entry(tab2, state="disabled")
respuesta.place(x=350,y=110, width=80)
button1 = ttk.Button(tab2, text='seleccion', state="disabled", command=suma)
button1.place(x=190, y=110, width=130)
                                     #seleccion 2                                     
button2 = ttk.Button(tab2, text='Convertir', state="disabled", command=convercion)
button2.place(x=40,y=170, width=130)
mostrar = ttk.Entry(tab2, state="disabled")
mostrar.place(x=190,y=170, width=130)
                                     #seleccion 3
pwm_inten = ttk.Entry(tab2, state="disabled")
pwm_inten.place(x=40, y=235, width=130)
button3 = ttk.Button(tab2, text='Intensidad', state="disabled", command=Pwm)        
button3.place(x=190,y=235, width=130)

#_____________________________________Imagenes________________________________________________________________________
led_Red =  tk.PhotoImage( file="Rojo.png")
led_R = ttk.Label(tab1, image=led_Red)
led_R.config(state="disabled")
led_R.place(x=100, y=150)


led_G =  tk.PhotoImage( file="Verde.png")
led_V = ttk.Label(tab1, image=led_G)
led_V.config(state="disabled")
led_V.place(x=200, y=150)

root.mainloop()