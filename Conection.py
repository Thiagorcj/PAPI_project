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
chave = "chave do bot"
bot  = telebot.TeleBot(chave) #Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = '0'


# Translate
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

#Resumo
def resumo(file_name,mensagem):
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
    resumo = resumindo(content[0]['text'],'portuguese',1)
    bot.send_message(mensagem.from_user.id,f"Resumo: {resumo}")

def stem_separation(file_name, mensagem):
    api_key = "api_key_acess"  # Music AI API key
    url_get_upload = "https://api.music.ai/api/upload"
    headers_get_upload = {"Authorization": api_key}

    response_get_upload = requests.get(url_get_upload, headers=headers_get_upload)
    data_get_upload = response_get_upload.json()
    upload_url = data_get_upload.get("uploadUrl")
    url_upload_file = upload_url
    file_path = file_name  # Change to the path of the input
    headers_upload_file = {"Content-Type": "audio/mpeg"}

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
        "name": "teste123",  # Replace with the desired name for the job
        "workflow": "Stem-Separation-2.0",  # Replace with the name of your workflow
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
    max_attempts = 20
    current_attempt = 0

    while not job_succeeded and current_attempt < max_attempts:
        response_get_job_results = requests.get(url_get_job_results, headers=headers_get_job_results)
        data_get_job_results = response_get_job_results.json()

        if data_get_job_results['status'] == "SUCCEEDED":
            job_succeeded = True
            break
        elif data_get_job_results['status'] == "FAILED":
            print(f"-x- {file_name} -x- Process Failed -x-")
            break
        else:
            time.sleep(10)
            print("Waiting...")
            current_attempt += 1

    if not job_succeeded:
        print("Timeout: Job did not complete within the specified attempts.")
        # Handle as needed, e.g., raise an exception or log a message.
        return

    results = data_get_job_results['result']

    # Define um diretório de saída com base no nome do usuário ou algum identificador único
    output_directory = f'{mensagem.from_user.id}_{str(uuid.uuid4())}_stems'
    output_directory_path = os.path.join(os.getcwd(), output_directory)

    os.makedirs(output_directory_path, exist_ok=True)

    for stem_type, url in results.items():
        desired_stem_name = f'{stem_type.lower()}'
        local_file_name = f"{desired_stem_name}_stem.mp3"
        local_file_path = os.path.join(output_directory_path, local_file_name)

        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(local_file_path, 'wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)

            # Envia o arquivo de áudio
            with open(local_file_path, 'rb') as audio_file:
                bot.send_message(mensagem.from_user.id, f"{desired_stem_name}: ")
                bot.send_audio(mensagem.from_user.id, audio_file)

            # Mensagem adicional, se necessário
        else:
            print(f'O download falhou para {stem_type}. Código de status: {response.status_code}')
