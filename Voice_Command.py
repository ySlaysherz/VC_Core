import speech_recognition as sr
import keyboard
import os
import subprocess
import webbrowser
import json

# Carregar configurações do arquivo JSON
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

def reconhecer_comando():
    """Reconhece o comando de voz do usuário enquanto a tecla '1' do teclado numérico estiver pressionada."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            if keyboard.is_pressed('num 1'):
                print("Ouvindo...")
                try:
                    audio = recognizer.listen(source, timeout=5)
                    comando = recognizer.recognize_google(audio, language='pt-BR')
                    print(f"Você disse: {comando}")
                    executar_comando(comando.lower())
                except sr.UnknownValueError:
                    print("Desculpe, não entendi o que você disse.")
                except sr.RequestError:
                    print("Erro ao conectar-se ao serviço de reconhecimento.")
                except sr.WaitTimeoutError:
                    print("Nenhum comando detectado.")
            else:
                break

def normalizar_comando(comando):
    """Remove artigos e preposições comuns do comando."""
    palavras_para_remover = {"o", "a", "os", "as", "de", "do", "da", "dos", "das", "pasta", "pastas"}
    palavras = comando.lower().split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in palavras_para_remover]
    return ' '.join(palavras_filtradas)

def executar_comando(comando):
    """Executa ações com base no comando reconhecido."""
    comando_normalizado = normalizar_comando(comando)
    palavras = comando_normalizado.split()
    verbo = palavras[0]
    objeto = ' '.join(palavras[1:])

    if verbo in ["abrir", "abre", "abra"]:
        objeto = normalizar_comando(objeto)
        if objeto in config['aplicativos']:
            app_path = config['aplicativos'][objeto]
            print(f"Abrindo {objeto}.")
            subprocess.run(app_path)
        elif objeto in config['urls']:
            url = config['urls'][objeto]
            print(f"Abrindo {objeto} no navegador.")
            webbrowser.open(url)
        elif objeto in config['pastas']:
            caminho_pasta = config['pastas'][objeto]
            if os.path.exists(caminho_pasta):
                print(f"Abrindo a pasta '{objeto}'.")
                os.startfile(caminho_pasta)
            else:
                print(f"A pasta '{objeto}' não foi encontrada.")
        else:
            print(f"Pasta '{objeto}' não encontrada nas configurações.")
    elif verbo in ["pesquise", "busque", "buscar", "pesquisa", "busca"]:
        termo_pesquisa = ' '.join(palavras[1:])
        if termo_pesquisa:
            print(f"Pesquisando por {termo_pesquisa}.")
            webbrowser.open(f"https://www.google.com/search?q={termo_pesquisa}")
        else:
            print("Por favor, especifique o termo para pesquisa.")
    elif "criar pasta" in comando:
        nome_pasta = comando.split("criar pasta")[-1].strip()
        if nome_pasta:
            if not os.path.exists(nome_pasta):
                os.makedirs(nome_pasta)
                print(f"Pasta '{nome_pasta}' criada com sucesso.")
            else:
                print(f"A pasta '{nome_pasta}' já existe.")
        else:
            print("Por favor, especifique o nome da pasta.")
    elif "renomear pasta" in comando:
        partes = comando.split("renomear pasta")[-1].strip().split(" para ")
        if len(partes) == 2:
            nome_atual = partes[0].strip()
            novo_nome = partes[1].strip()
            if os.path.exists(nome_atual):
                os.rename(nome_atual, novo_nome)
                print(f"Pasta '{nome_atual}' renomeada para '{novo_nome}'.")
            else:
                print(f"A pasta '{nome_atual}' não foi encontrada.")
        else:
            print("Por favor, especifique o nome atual e o novo nome da pasta.")
    else:
        print("Comando não reconhecido.")

if __name__ == "__main__":
    while True:
        reconhecer_comando()
