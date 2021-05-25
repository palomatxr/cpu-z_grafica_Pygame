
import pygame
import psutil
import socket

#Atraves das palavras-chaves busca as informaçoes da cpu
def mostra_info_cpu():
    s1.fill(branco)
    mostra_texto(s1, "Nome:", "brand_raw", 10)
    mostra_texto(s1, "Arquitetura:", "arch", 30)
    mostra_texto(s1, "Palavra (bits):", "bits", 50)
    mostra_texto(s1, "Frequência (MHz):", "freq", 70)
    mostra_texto(s1, "Núcleos (físicos):", "nucleos", 90)
    tela.blit(s1, (0, 0))
  
# Mostra texto de acordo com uma chave:
def mostra_texto(s1, nome, chave, pos_y):
    text = font.render(nome, True, preto)
    s1.blit(text, (10, pos_y))
    if chave == "freq":
        s = str(round(psutil.cpu_freq().current, 2))
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    else:
        s = str(info_cpu[chave])
    text = font.render(s, True, cinza)
    s1.blit(text, (160, pos_y))

# Obtém informações da CPU
info_cpu = cpuinfo.get_cpu_info()


#Escreve texto no pygame 
def escreve_texto(texto, pos_y):
    font = pygame.font.Font(None, 24)
    text = font.render(texto, 1, preto)
    tela.blit(text, (10, pos_y))


#Mostra a informação da memoria ram
def mostra_memoria() :
    mem = psutil.virtual_memory()
    capacidade = round(mem.total/(1024*1024*1024), 2)
    escreve_texto(f"Capacidade total de memoria ram: {capacidade}GB", 120)

#Mostra a informação do disco
def mostra_disco() :
    disco = psutil.disk_usage('.')
    
    escreve_texto(f"Capacidade Total de disco: {round(disco.total/(1024*1024*1024), 2)}GB" , 140)
    escreve_texto(f"Em uso: {round(disco.used/(1024*1024*1024), 2)}GB"  , 160)
    escreve_texto(f"Livre:  {round(disco.free/(1024*1024*1024), 2)}GB"  , 180)

    escreve_texto(f"Percentual de Disco Usado: {disco.percent}% " , 200)    


#Função principal para identificar o ip
def enderecamento_ip(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield (interface, snic.address)
                
ipv4s = list(enderecamento_ip(socket.AF_INET))
ipv6s = list(enderecamento_ip(socket.AF_INET6))

#Mostra o ip no pygame 
def mostra_ip():
    escreve_texto(f"Endereço de ip - Adaptador Ethernet: {ipv4s[4][1]}", 230)
    escreve_texto(f"Endereço de ip - Adaptador de Rede sem Fio: {ipv4s[6][1]}",250)
    
#Barra de indicação da cpu
def mostra_uso_cpu():
    capacidade = psutil.cpu_percent(interval=0)
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, preto, (5, 300, larg, 70))
    larg = larg*capacidade/100
    pygame.draw.rect(tela, amarelo, (5, 300, larg, 70))
    text = font.render("Uso de CPU:", 1, preto)
    tela.blit(text, (5,280))

#Barra de indicação da ram
def mostra_uso_memoria():
    mem = psutil.virtual_memory()
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, preto, (5, 500, larg, 70))
    larg = larg*mem.percent/100
    pygame.draw.rect(tela, vermelho, (5, 500, larg, 70))
    total = round(mem.total/(1024*1024*1024),2)
    texto_barra = "Uso de Memória (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, preto)
    tela.blit(text, (5, 480))

#Barra de indicação do disco
def mostra_uso_disco():
    disco = psutil.disk_usage('.')
    larg = largura_tela - 2*20
    pygame.draw.rect(tela, preto, (5, 700, larg, 70))
    larg = larg*disco.percent/100
    pygame.draw.rect(tela, roxo, ( 5, 700, larg, 70))
    total = round(disco.total/(1024*1024*1024), 2)
    texto_barra = "Uso de Disco: (Total: " + str(total) + "GB):"
    text = font.render(texto_barra, 1, preto)
    tela.blit(text, (5, 680))


# Cores:
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
azul = (0,0,255)
vermelho = (255,0,0)

amarelo = (242, 242, 16)
roxo = (193, 136, 211)


#Iniciando a janela principal
largura_tela = 1000
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Informações de CPU")
pygame.display.init()

# Superfície para mostrar as informações:
s1 = pygame.surface.Surface((largura_tela, altura_tela))

# Para usar na fonte
pygame.font.init()
font = pygame.font.Font(None, 24)
 
# Cria relógio
clock = pygame.time.Clock()
# Contador de tempo
cont = 60

terminou = False
# Repetição para capturar eventos e atualizar tela
while not terminou:
    # Checar os eventos do mouse aqui:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True

    # Fazer a atualização a cada segundo:
    if cont == 60:
        mostra_info_cpu()
        mostra_memoria()
        mostra_disco()
        mostra_ip()
        mostra_uso_memoria()
        mostra_uso_cpu()
        mostra_uso_disco()
        cont = 0

    # Atualiza o desenho na tela
    pygame.display.update()

    # 60 frames por segundo
    clock.tick(60)
    cont = cont + 1

# Finaliza a janela
pygame.display.quit()