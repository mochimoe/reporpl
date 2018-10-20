from flask import Flask, request, abort
from random import randint

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('tTJPhQw5bMtRmYbrUWYPwxcqY6U2NyCxkVLPocX/hGZF+SuZt4idRIvXxXYa9GkN41Ok4ummQWUAQ1kIbb6pNvJjuKdHvbq/VxpZFsP73Sp8G8dW18ZDmEzUkJfg7VYo1WxGvSliuGsHTEnBKSRJwQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7ad6255242a16b933bf3cf50b3340099')
#===========[ NOTE SAVER ]=======================
notes = {}

def saldo(  ):
    URLmhs = "http://www.aditmasih.tk/api_aisyah/saldo.php"
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"

    flag = data['flag']
    if(flag == "1"):
        
        # nama = data['data_sel'][0]['nama']
        # masuk = data['data_sel'][0]['masuk']

    # munculin semua, ga rapi, ada 'u' nya
    # all_data = data['data_angkatan'][0]
        saldo = data['data_sel'][0]
        data = "Saldo anda saat ini adalah : "+saldo+'\n'
        return data
    # return all_data

    elif(flag == "0"):
        return err

#input data
def inputuang(nrp, nama, masuk):
    r = requests.post("http://www.aditmasih.tk/api_aisyah/insert.php", data={'nrp': nrp, 'nama': nama, 'masuk': masuk})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Uang sudah dimasukkan ke dalam tabungan :D'
    elif(flag == "0"):
        return 'Uang gagal dimasukkan\n'

def allmhs():
        r = requests.post("http://www.aditmasih.tk/api_aisyah/all.php")
        data = r.json()

        flag = data['flag']
       
        if(flag == "1"):
            hasil = ""
            for i in range(0,len(data['data_sel'])):
                nrp = data['data_sel'][int(i)][0]
                nama = data['data_sel'][int(i)][2]
                masuk = data['data_sel'][int(i)][4]

                hasil=hasil+str(i+1)
                hasil=hasil+". Nrp : "
                hasil=hasil+nrp
                hasil=hasil+"\nNama : "
                hasil=hasil+nama
                hasil=hasil+"\nUang : "
                hasil=hasil+masuk
                hasil=hasil+"\n\n"
            return hasil
        elif(flag == "0"):
            return 'Data gagal dimasukkan\n'

#DELETE DATA MHS
def hapusmhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api_aisyah/delete.php", data={'nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatemhs(nrpLama,nrp,nama,masuk):
    URLmhs = "http://www.aditmasih.tk/api_aisyah/show.php?nrp=" + nrpLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama = nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_aisyah/update.php", data={'nrp': nrp, 'nama': nama,'masuk': masuk, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+' berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err

# Post Request

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

    data=text.split('-')
    if(data[0]=='saldo'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=saldo()))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputuang(data[1],data[2],data[3])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    elif(data[0]=='uangku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allmhs()))
    elif(data[0]=='intro'):
        menu = "Selamat Datang di Piggy Bank ChatBot\n\nbot ini membantumu untuk bisa menghitung uang yang\nsudah kamu masukkan kedalam celenganmu ^_^\n Ketik menu untuk melanjutkan"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))
    elif(data[0]=='menu'):
        menu = "Ketikkan sesuai format di bawah ini\n\n 1. saldo, untuk melihat saldo terkini anda\n2. tambah-[tanggal]-[nama]-[uang masuk] untuk memasukkan uang anda kedalam celengan\n5. uangku , untuk menampilkan seluruh tabungan anda"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)