import telebot
import requests
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
chave = "token"
bot  = telebot.TeleBot(chave)#Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = False
@bot.message_handler(commands=["start"])
def responder(mensagem):
    bot.reply_to(mensagem,'''Olá, eu sou o PAPI
Você pode acessar os seguintes comandos:
/resumo: Eu faço o resumo de um áudio.
/karaoke: Eu monto o karaoke para você S2.
/help: Te dou uma ajudinha.
''')
# /resumo
@bot.message_handler(commands=['resumo'])
def resumir(mensagem):
    global flag 
    flag = True
    bot.send_message(mensagem.from_user.id,f"{mensagem.from_user.first_name}, manda o audio pro PAPI aqui, que eu faço um resumão pra você")

@bot.message_handler(content_types=['voice'])
def resumo_audio(mensagem):
    global flag
    if flag:
        #Audio file
        voice_message = mensagem.voice
        #Audio download link
        audio_path = bot.get_file(voice_message.file_id).file_path
        audio_download_link = download_url+audio_path
        #Download do audio
        audio_file = requests.get(audio_download_link)
        # Constrói o caminho para o arquivo de áudio
        audio_file_name = os.path.join(diretorio_atual, f'{mensagem.from_user.first_name}_audio_{mensagem.id}.ogg')
        open(audio_file_name, 'wb').write(audio_file.content)
        bot.reply_to(mensagem,"Áudio processado com sucesso")
    flag = False

# /karaoke
@bot.message_handler(commands=['karaoke'])
def karaoke1(mensagem):
    global flag
    flag = True
    bot.send_message(mensagem.from_user.id,f"{mensagem.from_user.first_name}, manda a música pro PAPI aqui, que eu separo o som dos intrumentos e a letra pra você")

@bot.message_handler(content_types=['voice'])
def totext(mensagem):
    global flag
    if flag:
        #Audio file
        voice_message = mensagem.audio
        #Audio download link
        audio_path = bot.get_file(voice_message.file_id).file_path
        audio_download_link = download_url+audio_path
        #Download do audio
        music_file = requests.get(audio_download_link)
        music_file_name = os.path.join(diretorio_atual, f'{mensagem.from_user.first_name}_musica_{mensagem.id}.ogg') # Constrói o caminho para o arquivo de áudio
        open(music_file_name, 'wb').write(music_file.content)
        bot.reply_to(mensagem,"Música processada com sucesso")

    flag = 0

@bot.message_handler(commands='help')
def responde2(mensagem):
    texto = '''
    Relaxa que o PAPI vai ter ajudar.
Você pode acessar os seguintes comandos:
/resumo: Eu faço o resumo de um áudio.
/karaoke: Eu monto o karaoke para você S2.'''
    bot.reply_to(mensagem,texto)

bot.polling()#Gera o loop infinito do chat


