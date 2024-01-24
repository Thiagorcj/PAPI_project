![Logo PAPI](https://i.imgur.com/AjKQdz9.png)
# Projeto PAPI (Personal Assistant for processing information) by BitBeats

## Processo inicial:

Nesse repositório está presente o código do bot do Telegram. Para rodar na sua máquina você deve baixar a biblioteca como está abaixo e quando rodar o código lembrar de colocar o token.

```bash
pip install pytelegrambotapi

```
## Bora lá para a explicação do código:
Para que serve o os? Bom, ele funciona para ,indepedente do local que você está executando o código, os arquivos criados dentro das funções sejam colocados no mesmo diretório do chatbot.py, abaixo está a parte em que ele foi aplicado.
```python
import os
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
#Dentro da função:
audio_file_name = os.path.join(diretorio_atual, f'{mensagem.from_user.first_name}_audio_{mensagem.id}.ogg')
```
Para que serve a flag? Ela serve para meio que selecionarmos qual dos processos ela vai fazer(flag == 1 or 2 or 3...), ou se ela não vai fazer nenhum(flag == 0).


Criei uma função para baixar o audio que a pessoa envia salvar e devolver o nome do arquivo, porque com o nome conseguimos abrir o arquivo enviar para API da moises o conteudo e fazer as ações propriamente ditas.
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
A seguir está as funções que servem para indentificar os comandos dos usuários que são o /start,/help, /resumo, /translate, /totext, /portuguese, /english. As cinco ultimas citadas é modificada a flag para receber audio e fazer determinada ação.  

```python
#/start
@bot.message_handler(commands=["start"])
def responder(mensagem):
    bot.reply_to(mensagem,'''Olá, eu sou o PAPI
Você pode acessar os seguintes comandos:
/resumo: Faço o resumo de um áudio.
/totext: Transcrevo um áudio para você.
/translate: Traduzo um áudio para você.
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
/translate: Eu traduzo um aúdio para você'''
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
    bot.send_message(mensagem.from_user.id,f'''{mensagem.from_user.first_name},Selecione uma lingua:
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

``` 
Por fim, essa é a função que recebe um audio verifica a flag e faz determinada ação:
```python
@bot.message_handler(content_types=['voice'])
def audio(mensagem):
    global flag
    #Resumo
    if flag=='1':
        file_name = process_audio(mensagem)
        #Função do resumo aqui
        flag = '0'
    #Totext
    elif flag=='2':
        file_name = process_audio(mensagem)
        #Função do totext aqui
        flag = '0'
    #Translate
    elif flag=='4':
        file_name = process_audio(mensagem)
        #Função do translate(portuquese) aqui
        flag = '0'    
    elif flag=='5':
        file_name = process_audio(mensagem)
        #Função do translate(english) aqui
        flag = '0'
```
