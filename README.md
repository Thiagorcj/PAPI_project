![Logo PAPI](https://i.imgur.com/p04xQix.png)
# Projeto PAPI (Personal Assistant for processing information) by BitBeats

## Processo inicial:

Nesse repositório está presente o código do bot do Telegram. Para rodar na sua máquina você deve baixar as bibliotecas como está abaixo e quando rodar o código lembrar de colocar os tokens das APIs.

```bash
pip install pytelegrambotapi
pip install summy
```
## Bora lá para a explicação do código:
### Organização geral e o arquivo  Conection.py
Bom, com o objetivo de ficar mais legível e organizado o arquivo foi decidido criar funções que recebem como inputs de forma geral o nome do arquivo e a mensagem(objeto que possui diversas informações com relação a mensagem) e e mandam para API do Music.AI os áudios, recebem os outputs e mandam para o usuário. A seguir está dois exemplos de funções presentes no Conection.py:
```python
import requests
import time
import telebot
import requests
import os
import shutil
import random
from sumy_example import resumindo
import uuid

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
chave = "Token do bot"
bot  = telebot.TeleBot(chave)#Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = '0'

# Translate - acrescenta-se o parametro Workflow porque a mesma função pode ser usada tanto para inglês quanto para português)

def translate_audio(filename,mensagem,workflow):
    api_key = "api_key_acess" #Music AI API key
    url_get_upload = "https://api.music.ai/api/upload"
    headers_get_upload = {"Authorization": api_key}

    response_get_upload = requests.get(url_get_upload, headers=headers_get_upload)
    data_get_upload = response_get_upload.json()
    upload_url = data_get_upload.get("uploadUrl")

    url_upload_file = upload_url
    file_path = filename #Change to the path of the input
    headers_upload_file = {"Content-Type": "audio/mpeg"}

    headers = {
        "Content-Type": "audio/mpeg"
    }

    with open(file_path, "rb") as file:
        response_upload_file = requests.put(url_upload_file, headers=headers_upload_file, data=file)

    download_url = data_get_upload.get("downloadUrl")
    url_create_job = "https://api.music.ai/api/job"
    headers_create_job = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Parameters for creating a new job
    job_params = {
        "name": f"{mensagem.from_user.first_name}.{mensagem.from_user.id}", #Replace with the desired name for the job
        "workflow": workflow, #Replace with the name of your workflow
        "params": {
            "inputUrl": download_url
        }
    }

    # Create a new job
    response_create_job = requests.post(url_create_job, headers=headers_create_job, json=job_params)
    data_create_job = response_create_job.json()

    # Get the ID of the created job
    job_id = data_create_job.get("id")

    url_get_job_results = f"https://api.music.ai/api/job/{job_id}"
    headers_get_job_results = {"Authorization": api_key}

    # Retrieve job results
    job_succeeded = False
    while (job_succeeded == False):
        response_get_job_results = requests.get(url_get_job_results, headers=headers_get_job_results)
        data_get_job_results = response_get_job_results.json()
        if (data_get_job_results['status'] == "SUCCEEDED"):
            job_succeeded = True;
            break
        elif data_get_job_results['status'] == "FAILED":
            print(f"-x- Process Failed -x-")
            break
        else:
            time.sleep(10)
            print("Waiting...")

    output_url = data_get_job_results['result']
    local_file_path = f'{mensagem.from_user.id}.ogg'
    response = requests.get(output_url['Output 1'], stream=True)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        print(f'A stem foi baixada e salva em: {local_file_path}')
        # sendVoice
        voice = open(local_file_path, 'rb')
        bot.send_voice(mensagem.from_user.id, voice)
    else:
        print(f'O download falhou. Código de status: {response.status_code}')

# Transcription
def transcription(file_name,mensagem):
    api_key = "api_key_acess" #Music AI API key
    url_get_upload = "https://api.music.ai/api/upload"
    headers_get_upload = {"Authorization": api_key}

    response_get_upload = requests.get(url_get_upload, headers=headers_get_upload)
    data_get_upload = response_get_upload.json()
    upload_url = data_get_upload.get("uploadUrl")


    url_upload_file = upload_url
    file_path = file_name #Change to the path of the input
    headers_upload_file = {"Content-Type": "audio/mpeg"}

    headers = {
        "Content-Type": "audio/mpeg"
    }

    with open(file_path, "rb") as file:
        response_upload_file = requests.put(url_upload_file, headers=headers_upload_file, data=file)


    download_url = data_get_upload.get("downloadUrl")
    url_create_job = "https://api.music.ai/api/job"
    headers_create_job = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Parameters for creating a new job
    job_params = {
        "name": f"{mensagem.from_user.first_name}.{random.randint(1000, 10000)}" , #Replace with the desired name for the job
        "workflow": "Transcription", #Replace with the name of your workflow
        "params": {
            "inputUrl": download_url
        }
    }

    # Create a new job
    response_create_job = requests.post(url_create_job, headers=headers_create_job, json=job_params)
    data_create_job = response_create_job.json()

    # Get the ID of the created job
    job_id = data_create_job.get("id")

    url_get_job_results = f"https://api.music.ai/api/job/{job_id}"
    print(url_get_job_results)
    headers_get_job_results = {"Authorization": api_key}

    # Retrieve job results
    job_succeeded = False
    while (job_succeeded == False):
        response_get_job_results = requests.get(url_get_job_results, headers=headers_get_job_results)
        data_get_job_results = response_get_job_results.json()
        if (data_get_job_results['status'] == "SUCCEEDED"):
            job_succeeded = True
            break
        elif data_get_job_results['status'] == "FAILED":
            print(f"-x- {file_name} -x- Process Failed -x-")
            break
        else:
            time.sleep(10)
            print("Waiting...")

    # Getting the output url
    output_url = data_get_job_results['result']['Output 1']
    #local_file_path = f'{mensagem.from_user.id}.json'
    response = requests.get(output_url, stream=True)
    content = response.json()
    bot.send_message(mensagem.from_user.id,f"Transcrição: {content[0]['text']}")

```
### Para que serve o sumy_example.py?
É um arquivo que serve para armazenar a função resumindo que resume um texto:
```python
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words



def resumindo(text,language,sentences_count):
    resumo = ''
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    
    stemmer = Stemmer(language)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    for sentence in summarizer(parser.document, sentences_count):
        resumo += f" {str(sentence)}"
    return resumo
```
### Para que serve o os?
 Bom, ele funciona para, indepedente do local que você está executando o código, os arquivos criados dentro das funções sejam colocados no mesmo diretório do chatbot.py, abaixo está a parte em que ele foi aplicado.
```python
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
#Dentro da função:
audio_file_name = os.path.join(diretorio_atual, f'{mensagem.from_user.first_name}_audio_{mensagem.id}.ogg')
```
### Para que servem as flags, o dicionário e a classe Update? 
Elas serve selecionar, quando recebe um arquivo audio, qual dos processos ela vai fazer(flag == 1 or 2 or 3...), ou se ela não vai fazer nenhum dos processos (flag == 0). A criação da classe e o do dicionário (que utiliza o ID do usuário) foi utilizado para impossibilita o conflito quando mais de uma pessoa estivesse usando o bot. Caso isso não fosse feito, flag de um usuário podia se confundir com de outro usuário que estivesse usando ao mesmo tempo.
```python
class UserState:
    def __init__(self):
        self.flag = '0'

# Um dicionário para armazenar o estado de cada usuário
user_states = {}
#Recebe áudio e músicas
@bot.message_handler(content_types=['voice', 'audio'])
def audio(mensagem):
    user_id = mensagem.from_user.id
    current_user_state = user_states.get(user_id, UserState())

    if current_user_state.flag == '1':
        # Resumo
        file_name = process_audio(mensagem)
        resumo(file_name,portuguese,2, mensagem)
        current_user_state.flag = '0'

    elif current_user_state.flag == '2':
        # Totext
        file_name = process_audio(mensagem)
        transcription(file_name, mensagem)
        current_user_state.flag = '0'
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
```


### Como funciona para processar o audio?
Cria-se uma função para baixar o audio que a pessoa envia, salvar e retornar o nome do arquivo, porque com o nome conseguimos abrir o arquivo, enviar para API da moises o conteúdo e fazer as ações propriamente ditas.
```python
def process_audio(mensagem):
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

    return audio_file_name
```
A seguir está as funções que servem para indentificar os comandos dos usuários que são o /start, /help, /translate, /resumo, /totext, /portuguese, /english e /separate. Com as cinco últimas citadas ocorre modificação da flag para receber audio e fazer determinada ação.  

```python
#/start
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

```
### Planos para o futuro?
A ideia é trazer novas funcionalidades, tornando o PAPI cada vez mais completo. Além disso, deve-se criar uma arquitetura mais organizada para salvar os dados que o PAPI tem contato. 
