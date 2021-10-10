import requests
import base64
import json
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

# config tkinter
window = tk.Tk()
window.title('Top 10 Songs Finder')
window.configure(bg='#111111')

# credentials
clientId = CLIENT_ID
clientSecret = CLIENT_SECRET

# encode credentials
message = f"{clientId}:{clientSecret}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)

# decode credentials
base64Message = base64Bytes.decode('ascii')

# define headers and body
headers = {}
body = {}

# populate header and body
headers['Authorization'] = f"Basic {base64Message}"
body['grant_type'] = "client_credentials"

# request token
url = "https://accounts.spotify.com/api/token"
resp = requests.post(url, headers=headers, data=body)

# get token out of response
token = resp.json()['access_token']

#create frame
frm_entry = tk.Frame(master=window, bg='#1db954',padx=100)
frm_entry2 = tk.Frame(master=window, bg='#121212', borderwidth=2, relief="groove" )
frm_photo = tk.Frame(master=window, bg='#121212', borderwidth=2, relief="groove" )

# create input and button
spacer1a = tk.Label(master=frm_entry, text="Enter a name:", padx=50, pady=10, bg='#1db954', fg='white', font=('Ubuntu','15', 'bold'))
textBox = tk.Entry(master=frm_entry, borderwidth=2, relief="groove", bg='#121212', fg='white')
buttonCommit = Button(master=frm_entry,height=1, width=30, text="Find", command=lambda: table(), bg='#1db954', fg='white', font=('Ubuntu', '10', 'bold'))

spacer1a.grid(row=2, column=0, padx=10)
frm_entry.grid(row=2, column=0, padx=10)
frm_entry2.grid(row=4, column=0, padx=10)
frm_photo.grid(row=20, column=0, padx=10)
textBox.grid(row=2, column=1, padx=10)
buttonCommit.grid(row=2, column=2, padx=10)

# populate header with token
headers = {
    "Authorization": "Bearer " + token
}

# request artist id
def get_artist_id():
    # get item from searchbox
    a = textBox.get()

    # create url
    zoekurl = f"https://api.spotify.com/v1/search?q={a}&type=artist&limit=2"

    # send request
    res = requests.get(url=zoekurl, headers=headers)

    # parse response
    out = (json.dumps(res.json(), indent=2))
    ob = json.loads(out)

    #check user input
    if len(ob['artists']['items']) >= 1:
        id = ob['artists']['items'][0]['id']
        return id, a, ob
    else:
        spacer1b = tk.Label(master=frm_entry2, text="Not Found, Try Again", bg='#282828', fg='white')
        spacer1b.grid(row=3, column=1)
        id = 'fout'
        return id, a, ob


def top_tracks(a):
    # get top tracks
    top_tracks_url = f"https://api.spotify.com/v1/artists/{a}/top-tracks?market=NL"
    get_top_tracks = requests.get(url=top_tracks_url, headers=headers)

    # parse response
    topp = json.dumps(get_top_tracks.json(), indent=2)
    top = json.loads(topp)
    return top


def get_image(a):
    img = requests.get(a['tracks'][0]['album']['images'][1]['url']).content
    with open('image.jpg', 'wb') as file:
        file.write(img)


def tijd(a):
    tijd_liedjes = []
    for i in range(10):
        # ms to minutes and seconds
        ms = int(a['tracks'][i]['duration_ms'])
        seconds = int((ms / 1000) % 60)
        minutes = int(ms / (1000 * 60)) % 60
        formaat = (str(minutes).strip("(") + "," + str(seconds).strip(')') + "m")
        tijd_liedjes.append(formaat)

    return tijd_liedjes


# get top tracks out response
def top_tracks_parse(a):
    araay = []
    for i in range(10):
        araay.append(a['tracks'][i]['name'])
    return araay


# get popularity
def pop(a):
    p = []
    for i in range(10):
        p.append(str(a['tracks'][i]['popularity']))
    return p


# create table
def table():
    artist = get_artist_id()
    id = artist[0]
    top_tracks_lijst = top_tracks(id)
    img = get_image(top_tracks_lijst)
    lijst = top_tracks_parse(top_tracks_lijst)
    tijd_liedjes_format = tijd(top_tracks_lijst)
    populariteit = pop(top_tracks_lijst)
    image_open = Image.open('image.jpg')
    photo = ImageTk.PhotoImage(image_open)

    # Create an image label
    img_label = tk.Label(image=photo, bg='#1db954')
    img_label.image = photo
    img_label.grid(row=0, column=0)

    #title lable
    title = tk.Label(window, text=artist[1].capitalize(), font=('Gotham','31','bold',), bg='#121212', fg='white')


    #header labels
    header1 = tk.Label(master=frm_entry2, text="Song:", bg='#1db954', fg='white',borderwidth=2, relief="groove", padx=200)
    header2 = tk.Label(master=frm_entry2, text="Duration", bg='#1db954', fg='white', padx=80, borderwidth=2, relief="groove")
    header3 = tk.Label(master=frm_entry2, text="Popularity", bg='#1db954', fg='white', padx=20, borderwidth=2, relief="groove")

    #headers locations
    header1.grid(row=4, column=0, sticky="w")
    header2.grid(row=4, column=1, sticky="w")
    header3.grid(row=4, column=2, sticky="w")
    title.grid(row=1, column=0)
    for i in range(10):
        table1 = tk.Label(master=frm_entry2, text=lijst[i], background="#121212", fg='white')
        table2 = tk.Label(master=frm_entry2, text=tijd_liedjes_format[i], background="#121212", fg='white')
        table3 = tk.Label(master=frm_entry2, text=populariteit[i], background="#121212", fg='white')

        table1.grid(row=5 + i, column=0, sticky="w")
        table2.grid(row=5 + i, column=1, sticky="w")
        table3.grid(row=5 + i, column=2, sticky="w")
    info(artist)
    related(id)

def info(a):
    ar = a[2]
    followers = ar['artists']['items'][0]['followers']['total']
    genre = ar['artists']['items'][0]['genres']
    g1 = genre[0].strip('[').strip(']').strip("'")
    info_title = tk.Label(window, text="Information:", bg='#121212', fg='white', font=('Ubuntu', '15', 'bold'))
    followers_title = tk.Label(window, text=f"Followers: {followers}", bg='#121212', fg= 'white')
    genre_title = tk.Label(window, text=f'Genre: {g1.capitalize()}', bg='#121212', fg= 'white')

    info_title.grid(row=16, column=0, sticky='nsew', pady=3)
    followers_title.grid(row=17, column=0, sticky='nsew')
    genre_title.grid(row=18, column=0, sticky='nsew')

def related(a):
    ttz = requests.get(f'https://api.spotify.com/v1/artists/{a}/related-artists', headers=headers)
    ttx = (json.dumps(ttz.json(), indent=2))
    tty = json.loads(ttx)
    for i in range(3):
        name = tty['artists'][i]['name']
        photo = tty['artists'][i]['images'][2]['url']

        img = requests.get(photo).content
        with open(f'image{i}.jpg', 'wb') as file:
            file.write(img)

        image_open = Image.open(f'image{i}.jpg')
        photo = ImageTk.PhotoImage(image_open)

        # Create an image label
        img_label = tk.Label(master=frm_photo,image=photo, bg='#1db954')
        img_label.image = photo
        name_label = tk.Label(master=frm_photo, text=name, bg='#121212', fg='white')

        img_label.grid(row=20, column=i)
        name_label.grid(row=21, column=i)


    heading_label = tk.Label(text='Related Artists', bg='#1db954', fg='white', font=('Ubuntu', '18', 'bold'), pady=5, padx= 100)
    heading_label.grid(row=19, column=0)


# Open window
tk.mainloop()
