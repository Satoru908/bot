from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.errors import SessionPasswordNeededError
from datetime import datetime, timedelta
from time import sleep
from telethon.tl import types
from telethon.errors import FloodWaitError
from telethon.errors import FloodWaitError, ChatAdminRequiredError
api_id = '26625932'  
api_hash = '12fe26bac8105ae8916dc150ebbfaca7'  


grupo_origen_id = -1004507143315 #<----AQUI EL GRUPO  DE ORIGEN 

tu_numero_telefono = '+51920749530'

def iniciar_sesion():
    client = TelegramClient('session_name', api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(tu_numero_telefono)
            client.sign_in(tu_numero_telefono, input('Ingresa el código que has recibido: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Ingresa la contraseña de la cuenta: '))
    return client

def reenviar_mensajes(client):
    errores_impresos = set()  # Conjunto para almacenar errores ya impresos

    try:
        print("Obteniendo mensajes...")
        messages = client.iter_messages(grupo_origen_id)

        chats = client.get_dialogs()
        for message in messages:
            if isinstance(message, types.MessageService):
                continue
            for chat in chats:
                if chat.is_group and chat.id != grupo_origen_id:
                    try:
                        # Envía el mensaje sin mostrar que es reenviado
                        client.send_message(chat.id, message)
                        print(f"Mensaje enviado al grupo {chat.title}: {message.id}")
                    except Exception as e:
                        error_str = str(e)
                        if error_str not in errores_impresos:
                            print(f"Error al enviar mensaje al grupo {chat.title}: {error_str}")
                            errores_impresos.add(error_str)
            print("Esperar 10 segundos para enviar el proximo mensaje.")
            sleep(10)  # Esperar 10 segundos para enviar el proximo mensaje.

    except Exception as ex:
        print(f"Error general: {ex}")


if __name__ == "__main__":
    client = iniciar_sesion()
    
    while True:
        try:
            reenviar_mensajes(client)
            print("Esperar 10 segundos para enviar el proximo mensaje.")
            sleep(10)  # Esperar 10 segundos para enviar el proximo mensaje.
        except Exception as ex:
            print(f"Error general: {ex}")
