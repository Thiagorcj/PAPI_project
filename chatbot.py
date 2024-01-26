import telebot
import requests
import os
from Conection import translate_audio, transcription, resumo, stem_separation

class UserState:
    def __init__(self):
        self.flag = '0'

# Um dicionário para armazenar o estado de cada usuário
user_states = {}

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
chave = "token do bot"
bot  = telebot.TeleBot(chave)#Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = '0'
# Algumas coisas que achei interessante pra deixar o PAPI mais completo
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

@bot.message_handler(commands=["start"])
def responder(mensagem):
    user_id = mensagem.from_user.id
    bot.reply_to(mensagem,'''Olá, eu sou o PAPI
Você pode acessar os seguintes comandos:
/resumo: Faço o resumo de um áudio.
/totext: Transcrevo um áudio para você.
/translate: Traduzo um áudio para você.
/separate: Separo o áudio em vocais e instrumentos.
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
/separate: Separo o áudio em vocais e instrumentos.'''
    bot.reply_to(mensagem,texto)

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
# /resumo
@bot.message_handler(commands=['resumo'])
def resumir(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    user_states[user_id].flag = '1'
    bot.send_message(user_id, f"{mensagem.from_user.first_name}, manda o audio pro PAPI aqui, que eu faço um resumão pra você")

# /totext
@bot.message_handler(commands=['totext'])
def totext(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    user_states[user_id].flag = '2'
    bot.send_message(user_id, f"{mensagem.from_user.first_name}, manda a audio pro PAPI aqui, que eu transcrevo para você")

# /translate
@bot.message_handler(commands=['translate'])
def translate(mensagem):
    user_id = mensagem.from_user.id
    bot.send_message(user_id, f'''{mensagem.from_user.first_name}, selecione uma lingua:
/portuguese: Traduzo para português
/english: Traduzo para inglês''')

# /portuguese
@bot.message_handler(commands=['portuguese'])
def portuguese(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    user_states[user_id].flag = '4'
    bot.send_message(user_id, f"Beleza, manda a audio pro PAPI aqui, que eu traduzo para você")

# /english
@bot.message_handler(commands=['english'])
def english(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    user_states[user_id].flag = '5'
    bot.send_message(user_id, f"Beleza, manda a audio pro PAPI aqui, que eu traduzo para você")

# /separate
@bot.message_handler(commands=['separate'])
def separate_elements(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    user_states[user_id].flag = '6'
    bot.send_message(user_id, f"Beleza, me manda o áudio que o PAPI separa para você")

# /reset
@bot.message_handler(commands=['reset'])
def reset_state(mensagem):
    user_id = mensagem.from_user.id
    user_states[user_id] = UserState()
    bot.send_message(user_id, "Estado redefinido.")

@bot.message_handler(content_types=['voice', 'audio'])
def audio(mensagem):
    user_id = mensagem.from_user.id
    current_user_state = user_states.get(user_id, UserState())

    if current_user_state.flag == '1':
        # Resumo
        file_name = process_audio(mensagem)
        resumo(file_name, mensagem)
    elif current_user_state.flag == '2':
        # Totext
        file_name = process_audio(mensagem)
        transcription(file_name, mensagem)
        
    elif current_user_state.flag == '4':
        # Translate
        file_name = process_audio(mensagem)
        translate_audio(file_name, mensagem, "Transcription-TTS")
    elif current_user_state.flag == '5':
        # Translate (english)
        file_name = process_audio(mensagem)
        translate_audio(file_name, mensagem, "Transcription-TTS-(To-English)")
    elif current_user_state.flag == '6':
        # Separate
        file_name = process_audio(mensagem)
        stem_separation(file_name, mensagem)

    # Reinicializa o estado do usuário após a conclusão da ação
    user_states[user_id] = UserState()


bot.polling()#Gera o loop infinito da conversa do chat