import telebot
import requests
import os
from Conection import translate_audio, transcription, resumo


diretorio_atual = os.path.dirname(os.path.abspath(__file__))
chave = "6380261490:AAHduix4ROprVAgBnKU64EzuFUpJkm3WCXI"
bot  = telebot.TeleBot(chave)#Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = '0'
#Função que processa o aúdio, que pode ser tanto no formato .ogg (voice) quanto mp3/mp4 (audio)
def process_audio(mensagem):
    #Audio file
    if mensagem.content_type == 'audio':
        message = mensagem.audio
    elif mensagem.content_type == 'voice':
        message = mensagem.voice
    #Audio download link
    audio_path = bot.get_file(message.file_id).file_path
    audio_download_link = download_url+audio_path
    #Download do audio
    audio_file = requests.get(audio_download_link)
    # Constrói o caminho para o arquivo de áudio
    audio_file_name = os.path.join(diretorio_atual, f'{mensagem.from_user.first_name}_audio_{mensagem.id}.ogg')
    open(audio_file_name, 'wb').write(audio_file.content)
    bot.reply_to(mensagem,"Áudio processado com sucesso, aguarde um instante")
    return audio_file_name

# Algumas que achei interessante pra deixar o PAPI mais completo
def randon_messages(mensagem):
    if mensagem.text == 'Bom dia' or mensagem.text == 'bom dia':
         bot.send_message(mensagem.from_user.id,f"Bom dia, {mensagem.from_user.first_name}, se quiser ajuda do PAPI, manda /help")
    elif  mensagem.text == 'Boa tarde' or mensagem.text == 'boa tarde':
         bot.send_message(mensagem.from_user.id,f"Boa Tarde, {mensagem.from_user.first_name}, se quiser ajuda do PAPI, manda /help")
    elif  mensagem.text == 'Boa noite' or mensagem.text == 'boa noite':
         bot.send_message(mensagem.from_user.id,f"Boa noite, {mensagem.from_user.first_name}, se quiser ajuda do PAPI, manda /help")
    elif  mensagem.text == 'Ola' or mensagem.text == 'ola' or mensagem.text == 'opa' or mensagem.text == 'Opa':
         bot.send_message(mensagem.from_user.id,f"Olá, {mensagem.from_user.first_name}, se quiser ajuda do PAPI, manda /help")
@bot.message_handler(func=randon_messages)

#/start
@bot.message_handler(commands=["start"])
def responder(mensagem):
    bot.reply_to(mensagem,'''Olá, eu sou o PAPI
Você pode acessar os seguintes comandos:
/resumo: Faço o resumo de um áudio.
/totext: Transcrevo um áudio para você.
/translate: Traduzo um áudio para você.
/separate: Separo um elemento do audio.
/help: Te dou uma ajudinha.
''')
#/help       
@bot.message_handler(commands=['help'])
def responde2(mensagem):
    texto = '''
    Relaxa que o PAPI vai ter ajudar.
Você pode acessar os seguintes comandos:
/resumo: Eu faço o resumo de um áudio.
/totext: Eu transcrevo um aúdio para você.
/translate: Eu traduzo um aúdio para você
/separate: Separo um elemento do audio.'''
    bot.reply_to(mensagem,texto)

# /resumo
@bot.message_handler(commands=['resumo'])
def resumir(mensagem):
    global flag 
    flag = '1'
    bot.send_message(mensagem.from_user.id,f"{mensagem.from_user.first_name}, manda o audio pro PAPI aqui, que eu faço um resumão pra você")

# /totext
@bot.message_handler(commands=['totext'])
def totext(mensagem):
    global flag
    flag = '2'
    bot.send_message(mensagem.from_user.id,f"{mensagem.from_user.first_name}, manda a audio pro PAPI aqui, que eu transcrevo para você")

#/translate
@bot.message_handler(commands=['translate'])
def translate(mensagem):
    global flag
    flag = '3'
    bot.send_message(mensagem.from_user.id,f'''{mensagem.from_user.first_name}, selecione uma lingua:
/portuguese: Traduzo para português
/english: Traduzo para inglês''')
    
#/portuguese
@bot.message_handler(commands=['portuguese'])
def portuguese(mensagem):
    global flag
    flag = '4'
    bot.send_message(mensagem.from_user.id,f"Beleza, manda a audio pro PAPI aqui, que eu traduzo para você")

#/english
@bot.message_handler(commands=['english'])
def english(mensagem):
    global flag
    flag = '5'
    bot.send_message(mensagem.from_user.id,f"Beleza, manda a audio pro PAPI aqui, que eu traduzo para você")

@bot.message_handler(commands=['separate'])
def separate_elements(mensagem):
    bot.send_message(mensagem.from_user.id,f"Beleza, me diz qual elemento você quer que continue no novo áudio,com letra minuscula (vocal, drums, bass, strings ou piano), por favor")
#/separate_elements
def instrumentos(mensagem):
    global flag
    if mensagem.text == 'vocal':
        flag = '6'
        return True
    elif mensagem.text == 'drums':
        flag = '7'
        return True
    elif mensagem.text == 'guitars':
        flag = '8'
        return True
    elif mensagem.text == 'strings':
        flag = '9'
        return True
    elif mensagem.text == 'bass':
        flag = '10'
        return True
    elif mensagem.text == 'piano':
        flag = '11'
        return True

@bot.message_handler(func=instrumentos)
def instrumentos(mensagem):
    bot.send_message(mensagem.from_user.id,f"Tudo certo, manda o audio pro PAPI aqui, que eu separo os elementos para você")

@bot.message_handler(content_types=['voice','audio'])
def audio(mensagem):
    global flag
    #Resumo
    if flag=='1':
        file_name = process_audio(mensagem)
        resumo(file_name,mensagem)
        #Função do resumo aqui
        flag = '0'
    #Totext
    elif flag=='2':
        file_name = process_audio(mensagem)
        transcription(file_name,mensagem)
        #Função do totext aqui
        flag = '0'
    #Translate
    elif flag=='4':
        file_name = process_audio(mensagem)
        translate_audio(file_name,mensagem,"Transcription-TTS")
        flag = '0'    
    elif flag=='5':
        file_name = process_audio(mensagem)
        translate_audio(file_name,mensagem,"Transcription-TTS-(To-English)")
        #Função do translate(english) aqui
    elif flag=='6':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Vocal')
        flag = '0'
    elif flag=='7':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Drums')
        flag = '0'
    elif flag=='8':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Guitars')
        flag = '0'
    elif flag=='9':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Strings')
        flag = '0'
    elif flag=='10':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Piano')
        flag = '0'
    elif flag=='11':
        file_name = process_audio(mensagem)
        #Conection.stem_separation(file_name,"Job_name",'Stem_Separation','Piano')
        flag = '0'

bot.polling()#Gera o loop infinito da conversa do chat


