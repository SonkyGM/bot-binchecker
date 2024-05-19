import telebot
import requests
import json
import sys
from colorama import init, Fore, Style

def main():
    # Inicializar colorama
    init(autoreset=True)
    
    # Solicitar el token al usuario
    print(Fore.YELLOW + Style.BRIGHT + "Por favor, introduce tu token de Telegram:")
    TOKEN = input(Fore.GREEN + Style.BRIGHT + "> ")

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['bin'])
    def handle_bin(message):
        bin_input = message.text[len("/bin "):].strip()
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            bot.send_message(message.chat.id, "Debes colocar /bin seguido de un BIN numérico de al menos 6 dígitos.")
            return
        
        try:
            response = requests.get(f"https://data.handyapi.com/bin/{bin_input}")
            response.raise_for_status()
            api = response.json()

            if api["Status"] == "SUCCESS":
                paisNombre = api["Country"]["Name"]
                marca = api["Scheme"]
                tipo = api["Type"]
                nivel = api["CardTier"]
                banco = api["Issuer"]

                bot.send_message(message.chat.id, f"""
Información solicitada:
Bin: {bin_input}
Nivel: {nivel}
Tipo: {tipo}
Marca: {marca}
País: {paisNombre}
Banco: {banco}
                """)
            else:
                bot.send_message(message.chat.id, 'Por favor, ingresa un BIN válido.')

        except requests.exceptions.RequestException as e:
            bot.send_message(message.chat.id, f"Error al conectar con la API: {str(e)}")
        except json.JSONDecodeError:
            bot.send_message(message.chat.id, "Error al procesar la respuesta de la API.")

    def start_bot():
        print(Fore.CYAN + Style.BRIGHT + "El bot está funcionando correctamente. Esperando comandos...")

        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(Fore.MAGENTA + Style.BRIGHT + f"Se perdió la conexión: {e}")
            print(Fore.RED + Style.BRIGHT + "La conexión se perdió. Por favor, reinicia el script manualmente.")
            sys.exit()

    start_bot()

if __name__ == "__main__":
    main()

