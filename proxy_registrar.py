#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

import sys
import socket
import socketserver
import time
import random
import json
import hashlib
import time


class XML_Prox_Handler(ContentHandler):
    def __init__(self):
        self.diccionario_proxy_xml = {}

#   #Trato el xml###########################################################
    def startElement(self, etiqueta, attrs):
        if etiqueta == 'server':
            self.diccionario_proxy_xml['Mi_Servidor_Proxy'] = attrs.get('name', "")
            self.diccionario_proxy_xml['IP_Proxy_Registrar'] = attrs.get('ip', "")
            self.diccionario_proxy_xml['Puerto_Proxy'] = attrs.get('puerto', "")

        if etiqueta == 'database':
            self.diccionario_proxy_xml['Usuarios'] = attrs.get('path', "")
            self.diccionario_proxy_xml['Contraseñas'] = attrs.get('passwdpath', "")

        if etiqueta == 'log':
            self.diccionario_proxy_xml['Log_Proxy'] = attrs.get('path', "")

    def get_tags(self):
        return self.diccionario_proxy_xml
#   #########################################################################

#   ##TRATO_LAS_PETICIONES_CLIENTE###########################################


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dict = {}
    Dicc_Pass = {}

    def json2register(self):
        try:
            with open('usuarios.json') as client_file:
                self.dict = json.load(client_file)
        except:
            self.register2json()

    def register2json(self):
        json.dump(self.dict, open('usuarios.json', 'w'))

    def handle(self):

        cliente = self.rfile.read().decode('utf-8')
        client = cliente.split()
        print("CLIENTE ----->")
        print(client)

#       #Con esto extraigo los datos de mi fichero passwords.txt
#       #print(diccionario_proxy_xml)
        fich_pass = diccionario_proxy_xml['Contraseñas']
        passwords = open(fich_pass, 'r')
        passwords_datos = passwords.read()

        separo = passwords_datos.split(",")

#       #Usuarios y Contraseñas
        User1_passwd1 = separo[0].split(":")
        User1 = User1_passwd1[0]
        passwd1 = User1_passwd1[1]

        User2_passwd2 = separo[1].split(":")
        User2 = User2_passwd2[0]
        passwd2 = User2_passwd2[1]

#       #Quito un \r\n que sobra
        passwd2 = passwd2.split("\n")
        passwd2 = passwd2[0]

#       #LOG############################
        Log = diccionario_proxy_xml['Log_Proxy']

        fichero_log = Log
        fichero = open(fichero_log, 'a')
        hora = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))

        if client[0] == "REGISTER":
            print("Compruebo que mi procedimiento es " + client[0])
#           #Con esto corto mediante los : y me quedo con el elemento que quiero
            User_Name = client[1].split(':')[1]
            User_Port = client[1].split(':')[2]
            User_IP = self.client_address[0]
            Expires = time.time() + int(client[4])

#           ########################################################################################################
#           #Genero numero
            self.Dicc_Pass[User_Name] = "98765434546545646542"
            Converbyts = bytes(str(self.Dicc_Pass[User_Name]), 'utf-8')
            noncebt = Converbyts
            passwd1 = (bytes(passwd1, 'utf-8'))
            passwd2 = (bytes(passwd2, 'utf-8'))
#           #########################################################################################################

#           #LOG
            informacion = hora + " Starting... \r\n"
            fichero.write(informacion)

#           #Respuesta de cliente no Autorizado
            if len(client) == 8:
                print("Usuario Autorizado")
                print("Tiempo expiracion valido")
                if client[7] != " ":
#           #Necesito comparar mi 1 cliente con la información que me llega
                    cliente_1 = client[1].split(":")
                    cliente_1 = cliente_1[1]


#           #USUARIO_1 REGISTER##############################################
                    if cliente_1 == User1:
                        print("ESTAMOS CON EL CLIENTE " + cliente_1)
                        m = hashlib.sha1()
                        m.update(passwd1)
                        m.update(noncebt)
                        new_response = m.hexdigest()
                        response_1 = client[7].split("response=")
                        response_1 = response_1[1]
                        if response_1 == new_response:
#                       #Si el tiempo de expiracion es distinto de 0
                            Time = time.time()
                            Exp_Time = Time + int(client[4])
                            Tiempo_usuario = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Exp_Time))
                            
                            if client[4] != "0":
                                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                                print("Enviando 200 OK.....")                                
                                self.dict[User_Name] = User_IP,User_Port,Expires,Tiempo_usuario                                                          
                                self.register2json()
                                
#                               #LOG
                                informacion = hora + " Sent to" + " " + str(User_IP) + ":" + str(User_Port) + " " + "SIP/2.0 200 OK" + "\r\n"
                                fichero.write(informacion)
                               
                            else:
                                del self.dict[User_Name]            
                                self.register2json() 
                                
#                               #LOG
                                informacion = hora + " Delete" + " " + User1 + " " + str(User_IP) + ":" + str(User_Port) + " " + "\r\n"
                                fichero.write(informacion)
                                
                        
#                       #Necesito comparar mi 2 cliente con la información que me llega
                        
                    cliente_2 = client[1].split(":")
                    cliente_2 = cliente_2[1]
                    print(cliente_2)
#           ###################################################################
                        
#           #USUARIO_2 REGISTER################################################
                    if cliente_2 == User2:
                        print("ESTAMOS CON EL CLIENTE " + cliente_2)
                        m = hashlib.sha1()
                        m.update(passwd2)
                        m.update(noncebt)
                        new_response = m.hexdigest()
                        response_2 = client[7].split("response=")
                        response_2 = response_2[1]
                        if response_2 == new_response:
#                       #Si el tiempo de expiracion es distinto de 0                       
                            Time = time.time()
                            Exp_Time = Time + int(client[4])
                            Tiempo_usuario = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(Exp_Time))
                            if client[4] != "0":
                                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                                print("Enviando 200 OK.....")
                                self.dict[User_Name] = User_IP, User_Port, Expires, Tiempo_usuario                           
                                self.register2json()
                                
#                               #LOG
                                informacion = hora + " Sent to" + " " + str(User_IP) + ":" + str(User_Port) + " " + "SIP/2.0 200 OK" + "\r\n"
                                fichero.write(informacion)
                                
                            else:
                                del self.dict[User_Name]            
                                self.register2json()
                                
#                               #LOG
                                informacion = hora + " Delete" + " " + User2 + " " + str(User_IP) + ":" + str(User_Port) + " " + "\r\n"
                                fichero.write(informacion)
                                
                    self.json2register()                 
                            
                            
                            
            elif len(client) != 8 and len(client) !=5:
                print("SIP/2.0 400 Bad Request") 
                
#               #LOG
                informacion = hora + " Sent to" + " " + str(User_IP) + ":" + str(User_Port) + " " + "SIP/2.0 400 Bad Request" + "\r\n"
                fichero.write(informacion)                   
                            
            else:
                print("Usuario no Autorizado")               
                self.wfile.write(b"SIP/2.0 401 Unauthorized\r\n" + b"WWW Authenticate: Digest nonce=" + noncebt + \
                                 b"\r\n\r\n") 
                
#               #LOG
                informacion = hora + " Sent to" + " " + str(User_IP) + ":" + str(User_Port) + " " + "SIP/2.0 401 Unauthorized" + "\r\n"
                fichero.write(informacion)             

            
        if client[0] == "INVITE":
            
#           #Obtencion de direcciones SIP origen y destino
            User_Orign = client[6]
            User_Orign = User_Orign.split("=")
            User_Orign = User_Orign[1]
            User_Invit = client[1]
            User_Invit = User_Invit.split(":")
            User_Invit = User_Invit[1]
                        
            print("Usuario al que quiero hacer INVITE " + User_Invit)
            with open('usuarios.json') as file:
                data = json.load(file)
                Informacion = data
                print(Informacion)
                Esta = False
                for Usuario in data:
                    if Usuario == User_Invit:
                        Esta = True
                if Esta == True:
                    print("El Usuario al que quiero invitar Esta")
                    
                    #Creo un socket para mandar la información al usuario del invite
                    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    
                    Info_User_Invit = Informacion[User_Invit]
                    ip_user_inv = Info_User_Invit[0]
                    port_user_inv = Info_User_Invit[1]
                    print("Establezco conexion mediante los siguientes datos:")
                    print("IP " + ip_user_inv + " " + "Puerto " + port_user_inv) 
                    my_socket.connect((ip_user_inv, int(port_user_inv)))
                    
                    print("Este es mi envio al servidor "+ "\r\n" + cliente)
                    my_socket.send(bytes(cliente, 'utf-8'))
                    
                    
#                   #LOG
                    informacion = hora + " Sent to" + " " + str(ip_user_inv) + ":" + str(port_user_inv) + " " + cliente + "\r\n"
                    fichero.write(informacion) 


                    print("Recepción de la conexion establecida")
                    data = my_socket.recv(1024)
                    reception = data.decode('utf-8')
                    print(reception)

                    my_reception = reception.split("\r\n")
                    print(my_reception)

#                   #LOG
                    informacion = hora + " Received from " + " " + str(ip_user_inv) + ":" + str(port_user_inv) + " " + "\r\n" + my_reception[0] \
                                  + "\r\n" + my_reception[2] + "\r\n" + my_reception[4] + "\r\n"
                    fichero.write(informacion)

                    if my_reception[0] == "SIP/2.0 100 TRYING" \
                        and my_reception[2] == "SIP/2.0 180 RINGING" \
                            and my_reception[4] == "SIP/2.0 200 OK":
                        print("Llegan los 3 mensajes de recepcion, reenvio")
                        self.wfile.write(bytes(reception, 'utf-8'))

#                       #LOG
                        informacion = hora + " Sent to" + " " + User_Orign \
                            + "\r\n" + my_reception[0] + "\r\n" \
                            + my_reception[2] + "\r\n" + my_reception[4] \
                            + "\r\n"
                        fichero.write(informacion)

                else:
                    print("El Usuario al que quiero invitar no Esta")
                    request = b'SIP/2.0 404 User Not Found\r\n'
                    self.wfile.write(request)

#                   #request = request.decode('utf-8')
#                   #LOG
                    informacion = hora + " El Usuario" + " " + User_Invit + " No Esta " + "SIP/2.0 404 User Not Found" + "\r\n"
                    fichero.write(informacion)

        if client[0] == "ACK":
            print("SOY UN ACK!!!")
            peticion = client[1]
            usr_cliente = peticion.split(":")
            usr_cliente = usr_cliente[1]
            print(usr_cliente)

#           #LOG
            informacion = hora + " Received from" + " " \
                + User1 + "SIP/2.0 ACK" + "\r\n"
            fichero.write(informacion)

            with open('usuarios.json') as file:
                data = json.load(file)
                for Usuario in data:
                    if Usuario == usr_cliente:
                        print("Coincide")
                        print(client)
                        User_IP = data[Usuario][0]
                        User_Pto = data[Usuario][1]

                        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        my_socket.connect((User_IP, int(User_Pto)))
                        my_socket.send(bytes(cliente, 'utf-8') + b'\r\n')

#                       #LOG
                        informacion = hora + " Sent to" + " " \
                            + str(User_IP) + ":" + str(User_Pto) \
                            + " " + cliente + "\r\n"
                        fichero.write(informacion)

                        data = my_socket.recv(1024)
                        print(data.decode('utf-8'))

#                       #LOG
                        informacion = hora + " Received from" + " " \
                            + str(User_IP) + ":" + str(User_Pto) \
                            + " " + "SIP/2.0 RTP" + "\r\n"
                        fichero.write(informacion)

        if client[0] == "BYE":
            print(client[0])
            peticion = client[1]
            usr_cliente = peticion.split(":")
            usr_cliente = usr_cliente[1]
            print(usr_cliente)

            with open('usuarios.json') as file:
                data = json.load(file)
                for Usuario in data:
#                   #Al contrario que en ACK estoy mandando en otra direccion para darme de baja

#                   #Busco la ip y direccion de uaserver
                    if Usuario != usr_cliente:
                        print("Coincide el BYE")
                        User_IP_Serv = data[Usuario][0]
                        User_Pto_Serv = data[Usuario][1]
                        print(User_IP_Serv)
                        print(User_Pto_Serv)

#                       #Mando al uaserver el BYE
                        print(client)
                        print(cliente)
                        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        my_socket.connect((User_IP_Serv, int(User_Pto_Serv)))
                        my_socket.send(bytes(cliente, 'utf-8') + b'\r\n')
                        print("Enviado BYE" + "\r\n")

#                       #LOG
                        informacion = hora + " Sent to" + " " \
                            + str(User_IP_Serv) + ":" + str(User_Pto_Serv) \
                            + " " + cliente + "\r\n"
                        fichero.write(informacion)

                        data = my_socket.recv(1024)
                        reception = data.decode('utf-8')
                        my_reception = reception.split("\r\n")
                        print(my_reception)
                        if my_reception[0] == "SIP/2.0 200 OK":
                            print("Bien Recibido")
                            self.wfile.write(bytes(reception, 'utf-8'))
#                           #LOG
                            informacion = hora + " Received SIP/2.0 200 OK"
                            fichero.write(informacion)
#############################################################################
if __name__ == "__main__":

    xml_proxy = sys.argv[1]

    if len(sys.argv) > 2:
        print("Usage: python proxy_registrar.py config")
        sys.exit()

#   #######XML#######
#   ###################################################################################
    parser = make_parser()
    cHandler_Proxy = XML_Prox_Handler()
    parser.setContentHandler(cHandler_Proxy)
    try:
        parser.parse(open(xml_proxy))
        mytags = cHandler_Proxy.get_tags()
    except FileNotFoundError:
        sys.exit('Usage: python proxy_registrar.py config')

#   #print(mytags)
#   ###################################################################################

#    ###RECEPCION_MSJ_CLIENTE##########################################################
    diccionario_proxy_xml = mytags
    puerto_proxy = int(diccionario_proxy_xml['Puerto_Proxy'])
    proxy_serv = socketserver.UDPServer(('', puerto_proxy), SIPRegisterHandler)

    MyServer = "Server MiServidorProxy listening at port"
    print(MyServer + " " + str(puerto_proxy) + "...")

    proxy_serv.serve_forever()
