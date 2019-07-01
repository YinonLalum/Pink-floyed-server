import socket


LISTEN_PORT = 49060

def remove_duplification(list):
    """
    Function will return a list composed of the given list with no duplifications
    Input: the list to remove the duplifications from
    Output: the non repeating list
    """
    new_list = []
    for item in list:
        if new_list.count(item) == 0:
            new_list.append(item)
    return new_list



def listen_and_accept():
    # Create a TCP/IP socket
    listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding to local port 80
    server_address = ('', LISTEN_PORT)
    listening_sock.bind(server_address)

    # Listen for incoming connections
    print("Listening")
    listening_sock.listen(2)

    # Create a new conversation socket
    client_soc, client_address = listening_sock.accept()
    print("connected")
    
    return client_soc
    
def send_menu(sock):
    """
    Function will send the menu to the client, through the given socket
    :param sock:
    :return: none
    """
    line1 = "1. List of songs: get a list of albums\n"
    line2 = "2. List of songs in an album: enter name of album and and get list of songs in that album\n"
    line3 = "3. Length of song: enter name of song and get it's length\n"
    line4 = "4. Get all lyrics of a song: Enter song's name and get his lyrics\n"
    line5 = "5. Get song's album: enter song's name and get the album it belonges to\n"
    line6 = "6. search song by name: enter a word and get all songs that include that word in their name\n"
    line7 = "7. search song by word in lyrics: enter a word and get all songs that include that word in their lyrics\n"
    line8 = "8. get 50 most common words!\n"
    line9 = "9. Exit: exit the program\n"
    line10 = "10. Get albums from longest to shortest"
    menu = line1+line2+line3+line4+line5+line6+line7+line8+line9+line10
    sock.sendall(menu.encode())

def establish_connection(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connecting to remote computer 80
    server_address = (ip, port)
    sock.connect(server_address)
    return sock

    
def get_dictionarys(data):
    """
    Function will return a dictionery of albums which values are the albums date and dictionerys of song swhich values are the song's name,preformer,length and lyrics
    :param data: the database
    :return: a dictionery of albums wich values are the albums date and dictionerys of song swhich values are the song's name,preformer,length and lyrics
    """
    albums = {}
    songs = {}
    raw_albums = data.split("#")
    del raw_albums[0]
    for album in raw_albums:
        raw_songs = album.split('*')
        albums[raw_songs[0].split("::")[0]] = (raw_songs[0].split("::")[1].split('\n')[0],songs)
        del raw_songs[0]
        for song in raw_songs:
            songs[song.split("::")[0]] = {'singer': song.split("::")[1], 'length': song.split("::")[2], 'lyrics': song.split("::")[3]}
        songs = {}
    return albums
    #Lots of splitting, ummm, the date of the album is kept in a tuple next to the songs dictionary, so when accessing the songs you have to choose that dict from the tuple, it's the second object in the tuple so [1]before entering the value for the song
    
    
def f1(DB,param):
    #the param isn't actually used here but for unison sake it is still recived
    param = ''
    answer = ''
    for album in DB.keys():
        answer += album+'\n'
    return answer
    
def f2(DB,param):
    answer = ''
    for song in DB[param][1].keys():
        answer += song+'\n'
    return answer

def f3(DB,param):
    for album in DB.keys():
        if param in DB[album][1].keys():
            answer = "The length of the song "+param+" is "+DB[album][1][param]["length"]+'\n'
    return answer

def f4(DB,param):
    for album in DB.keys():
        if param in DB[album][1].keys():
            answer = "The lyrics of the song "+param+" are \n\n\n"+DB[album][1][param]["lyrics"]
    return answer

def f5(DB,param):
    for album in DB.keys():
        if param in DB[album][1].keys():
            answer = album+'\n'
    return answer
def f6(DB,param):
    answer = ''
    for album in DB.keys():
        for song in DB[album][1].keys():
            if param.lower() in song.lower():
                answer += song+'\n'
    return answer
def f7(DB,param):
    answer = ''
    for album in DB.keys():
        for song in DB[album][1].keys():
            if param.lower() in DB[album][1][song]["lyrics"].lower():
                answer += song+'\n'
    return answer

def f8(DB,param):
    lyrics = ''
    answer = ''
    orders = []
    for album in DB.keys():
        for song in DB[album][1].keys():
            lyrics +=DB[album][1][song]["lyrics"]
    lyrics.replace('\n','')
    lyrics = lyrics.split(' ')
    for word in lyrics:
        orders.append((word,lyrics.count(word)))
    orders = sorted(orders, key=lambda tup: tup[1], reverse = True)
    orders = remove_duplification(orders)
    for i in range(0,50):
        answer += orders[i][0]+', '
    return answer+'\n'

def f9(DB,param):
    answer = ''
    length = 0
    orders = []
    for album in DB.keys():
        for song in DB[album][1].keys():
            len = DB[album][1][song]["length"]
            length += int(len.split(":")[0]) + int(len.split(':')[1])/10
        orders.append((album,length))
    orders = sorted(orders, key=lambda tup: tup[1], reverse = True)
    for album in orders:
        answer += album[0]+'\n'
    return answer

"""
with open("Pink_Floyd_DB.txt") as f:
    data = f.read()
get_dictionarys(data)
"""
