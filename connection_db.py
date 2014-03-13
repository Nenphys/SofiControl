__author__ = 'Chapo'

import MySQLdb
import serial
import time
import sys
import bitState


messageToSend = ''
respuesta = ''
data_toPrint = ''
cmd =''

def SendCommand(cmd_cfg):
    global tenSec, Rx, messageToSend, errorCounter, respuesta,data_toPrint,cmd

    data_toPrint = ""
    print("TxST: SendCommand Thread Running ...")
    port.flushOutput()
    command = cmd_cfg
    Rx = True

    data_toPrint = command[:-1]
    print("[{}]TxST: Tx Data->[{}]".format(time.clock(), data_toPrint))
    port.write(command)

    while Rx:
        try:
            MessageFromSerial = port.readline()
            # Remove last 3 chars (CR LF)
            data_toPrint = MessageFromSerial[:-2]
            if data_toPrint[3] != 'X':
                respuesta = data_toPrint
            print("[{}]RxST: Rx Data->[{}]".format(time.clock(), data_toPrint))
            cmd ==""
            Rx = False

        except serial.SerialException as e:
            print("Error: ...{0}".format(e))
            respuesta = "Error de Comunicacion"
            Rx = False
        except IndexError as i:
            print("Error: ...{0}".format(i))
            respuesta = "Error de Comunicacion"
            Rx = False
        except TimeoutError as t:
            print("Error: ...{0}".format(t))
            respuesta = "Error de Comunicacion"
            Rx = False
global port

port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=1)



print("Python-MySQL connection: OK")
while True:
     try:
        db = MySQLdb.connect(host="localhost", user="admin", passwd="petrolog", db="sofi")
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        time.sleep(.5)
        cursor.execute("SELECT * FROM Eventos")
        rowEvent = cursor.fetchone()

        tx_db = rowEvent["tx"]
        refresh_db= rowEvent ["refresh"]

        if refresh_db == 1:

            #traemos SP
            cmd = "01S?2\x0D"
            SendCommand(cmd)
            if respuesta !="Error de Comunicacion":
                resp_s2 = respuesta

                print (resp_s2[5:9])
                print (resp_s2[9:13])
                print (resp_s2[41:45])
                print (resp_s2[37:41])
                cursor.execute("UPDATE Eventos SET   dia_de_paro={0}, hora_paro={1}, dia_de_arranque={2}, hora_arranque={3},  refresh=0".format(resp_s2[9:13],resp_s2[41:45],resp_s2[5:9],resp_s2[37:41]))
                db.commit()
                respuesta = ""

            #traemos el estado del motor
            cmd= "01E\x0D"
            SendCommand(cmd)
            cmd_e = respuesta
            if respuesta !="Error de Comunicacion":
                print (cmd_e[18:20])
                print(bitState.getBitState(cmd_e[18:20],7))
                if bitState.getBitState(cmd_e[18:20],7) == "true":
                    print ("prendido")
                    cursor.execute("UPDATE Estado SET   estado=1")
                    db.commit()
                    respuesta = ""
                else:
                    print ("Apagado")
                    cursor.execute("UPDATE Estado SET   estado=0")
                    db.commit()
                    respuesta = ""


        if tx_db == 1:
            id_evento = rowEvent["id_evento"]

            dia_de_paro = rowEvent["dia_de_paro"]
            cmd = "01SX2000{0}\x0D".format(dia_de_paro)
            SendCommand(cmd)

            hora_paro = str(rowEvent["hora_paro"])
            print("HORA STRING {0}".format(hora_paro))
            if len(hora_paro) > 3:
                cmd = "01SXA{0}\x0D".format(hora_paro)
                SendCommand(cmd)
            elif len(hora_paro) == 1:
                cmd = "01SXA000{0}\x0D".format(hora_paro)
                SendCommand(cmd)
            elif len(hora_paro) == 2:
                cmd = "01SXA00{0}\x0D".format(hora_paro)
                SendCommand(cmd)
            else:
                cmd = "01SXA0{0}\x0D".format(hora_paro)
                SendCommand(cmd)

            dia_de_arranque = rowEvent["dia_de_arranque"]
            cmd = "01SX1000{0}\x0D".format(dia_de_arranque)
            SendCommand(cmd)

            hora_arranque = str(rowEvent["hora_arranque"])
            print("HORA STRING {0}".format(hora_arranque))
            if len(hora_arranque) > 3:
                cmd = "01SX9{0}\x0D".format(hora_arranque)
                SendCommand(cmd)
            elif len(hora_arranque) == 1:
                cmd = "01SX9000{}\x0D".format(hora_arranque)
                SendCommand(cmd)
            elif len(hora_arranque) == 2:
                cmd = "01SX900{0}\x0D".format(hora_arranque)
                SendCommand(cmd)
            else:
                cmd = "01SX90{0}\x0D".format(hora_arranque)
                SendCommand(cmd)


            if respuesta != "Error de Comunicacion":
                cursor.execute("UPDATE Eventos SET tx=0 WHERE id_evento={0}".format(id_evento))
                db.commit()
                print(
                    "Eventos Guardados: DiaP: {0} Hora: {1} DiaE {2} HoraE: {3}".format(dia_de_paro, hora_paro, dia_de_arranque,
                                                                                    hora_arranque))
        else:
            cursor.execute("SELECT * FROM Comandos ")
            rowCmd = cursor.fetchone()
            print("Sin Eventos Nuevos")

            try:
                resp_cmd = rowCmd['resp_cmd']
            except TypeError:
                print ("Tabla de Comandos Vacia")
            else:
                print(resp_cmd)
                if resp_cmd == '0':
                    cmd_enviar = rowCmd['cmd']
                    cmd = "{0}\x0D".format(cmd_enviar)
                    SendCommand(cmd)
                    cursor.execute("UPDATE Comandos SET resp_cmd=\"{0}\"".format(respuesta))
                    db.commit()
                    cursor.execute("SELECT * FROM Comandos ")
                    temp= cursor.fetchone()
                    print ("YA CALLESE!!!!!!!!!!!!!!!! {0}".format(temp['resp_cmd']))
                    respuesta = ""
        cursor.close()
        db.close()

     except:
        print ("Unexpected error:", sys.exc_info()[0])
        break

print("Error Cerrando BD")
cursor.close()
db.close()
