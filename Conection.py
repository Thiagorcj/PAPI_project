import requests
import json
import time
import telebot
import requests
import os


diretorio_atual = os.path.dirname(os.path.abspath(__file__))
chave = "6380261490:AAHduix4ROprVAgBnKU64EzuFUpJkm3WCXI"
bot  = telebot.TeleBot(chave)#Cria o bot 
download_url = f'https://api.telegram.org/file/bot{chave}/'
flag = '0'

def translate_audio(filename,mensagem):
    api_key = "8ee4c4b7-191c-432a-9e17-3c0b7b700ff7" #Music AI API key
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
        "workflow": "Transcription-TTS", #Replace with the name of your workflow
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
    bot.send_message(mensagem.from_user.id,f"Aqui está o link do seu audio traduzido:{output_url}")

        