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
line_bot_api = LineBotApi('1URSFws7hTE4/3R5QWTFuYrMqU3x9fgkiL3y9AlHJcgb3X2j8WYZLhEXxQr2Taoczii6D3zHnWfsyRiiC6XqY9GRf79yRNkqz/c/oB/zsYFe+wzmbg6X9FUi/zGtVc0b/XJL2EnJ8ToGAl1XbC5fawdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('7d787028825e0a82de4c61310da0c826')
#===========[ NOTE SAVER ]=======================
notes = {}

# def carimhs(nrp):
#     URLmhs = "http://www.aditmasih.tk/api_aisyah/show.php?nrp=" + nrp
#     r = requests.get(URLmhs)
#     data = r.json()
#     err = "data tidak ditemukan"

#     flag = data['flag']
#     if(flag == "1"):
#         nrp = data['data_sel'][0]['nrp']
#         nama = data['data_sel'][0]['nama']
#         jurusan = data['data_sel'][0]['jurusan']

#     # munculin semua, ga rapi, ada 'u' nya
#     # all_data = data['data_angkatan'][0]
#     data = "Nama : "+nama+"\nNrp : "+nrp+"\nJurusan : "+jurusan
#     return data
#     # return all_data

#     elif(flag == "0"):
#         return err

#input data
def inputmhs(nrp, nama, jurusan):
    r = requests.post("http://www.aditmasih.tk/api_aisyah/insert.php", data={'nrp': nrp, 'nama': nama, 'jurusan': jurusan})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allmhs():
        r = requests.post("http://www.aditmasih.tk/api_aisyah/all.php")
        data = r.json()

        flag = data['flag']
       
        if(flag == "1"):
            hasil = ""
            for i in range(0,len(data['data_sel'])):
                nrp = data['data_sel'][int(i)][0]
                nama = data['data_sel'][int(i)][2]
                jurusan = data['data_sel'][int(i)][4]
                hasil=hasil+str(i+1)
                hasil=hasil+". Nrp : "
                hasil=hasil+nrp
                hasil=hasil+"\nNama : "
                hasil=hasil+nama
                hasil=hasil+"\nJurusan : "
                hasil=hasil+jurusan
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

def updatemhs(nrpLama,nrp,nama,jurusan):
    URLmhs = "http://www.aditmasih.tk/api_aisyah/show.php?nrp=" + nrpLama
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    nrp_lama = nrpLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api_aisyah/update.php", data={'nrp': nrp, 'nama': nama,'jurusan': jurusan, 'nrp_lama':nrp_lama})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+nrp_lama+'berhasil diupdate\n'
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
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    elif(data[0]=='waifuku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allmhs()))
    elif(data[0]=='menu'):
        menu = "Ketikkan sesuai format di bawah ini\n\n 1. lihat-[nrp]\n2. tambah-[nrp]-[nama]-[jurusan]\n3. hapus-[nrp] Untuk menghapus selingkuhan anda.\n4. ganti-[nrp lama]-[nrp baru]-[nama]-[jurusan baru] jika anda ingin mengganti selingkuhan anda.\n5. waifuku , untuk menampilkan seluruh selingkuhan anda"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)