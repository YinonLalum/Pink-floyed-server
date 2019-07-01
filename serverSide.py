import socket
import data
import hashlib

NAME = 'yinon'
PASS = 'ccc9c73a37651c6b35de64c3a37858ccae045d285f57fffb409d251d'
LISTEN_PORT = 49060
def main():
    is_first_iteration = True
    with open("Pink_Floyd_DB.txt") as file:
        file_data = file.read()
        
    client_soc = data.listen_and_accept()
    while True:
        if is_first_iteration:
            pas = ''
            is_first_iteration = False
            try:
                while hashlib.sha224(pas.encode()).hexdigest() != PASS or NAME != name:
                    msg = client_soc.recv(1024).decode()
                    print(msg)
                    name = msg.split("#")[0]
                    pas = msg.split("#")[1]
                    if hashlib.sha224(pas.encode()).hexdigest() == PASS and NAME == name:
                        client_soc.sendall("TRUE".encode())
                    else:
                        client_soc.sendall("FALSE".encode())
            except:
                client_soc = data.listen_and_accept()
                is_first_iteration = True
                continue
                
        #sending the menu to the client
        #data.send_menu(client_soc)
        
        #handling the case if the user had disconnect unexpcetedly
        try:
            #reciving the client's choice
            client_msg = client_soc.recv(1024)
        except:
            client_soc = data.listen_and_accept()
            is_first_iteration = True
            continue
        
        #handling the msg the client sent
        client_msg = client_msg.decode()
        print(client_msg)
        if client_msg.count("#")>0:
            client_msg = client_msg.split("#")
            request_type = client_msg[0]
            param = client_msg[1]
        else:
            request_type = client_msg
            param = ''
        
        
        DB = data.get_dictionarys(file_data)
        loc = {"DB":DB,"param":param}
        
        #if the user chooses option 10 the program will exit, that does not require a function and is better to be done in the main
        if request_type == '10':
            client_soc.close()
            print("Exiting")
            client_soc = data.listen_and_accept()
            is_first_iteration = True
            continue
        elif not request_type.isdigit() or not (int(request_type)>0 and int(request_type)<=10 ):
            client_soc.sendall("INVALID CHOICE".encode())
            continue
        else:
            #setting the command to execute
            command = "answer = data.f%d(DB,param)"% int(request_type)

        #executing the command in string form, giving it all the function with the globals dic, and the local variables with the loc dic
        #it will put the return value from the function into a variable that is stored inside the loc dic
        try:
            exec(command,globals(),loc)
        except:
            loc["answer"] = "\nINVALID PARAMETERS\n"
        #extracting the variable inside the loc dic into a variable
        answer = str(loc["answer"])
    
        #sending the response
        client_soc.sendall(answer.encode())


if __name__ == "__main__":
    main()
