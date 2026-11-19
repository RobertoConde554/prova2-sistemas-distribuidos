import threading
import time

# Servidores simulados
principal = {
    "online": True,
    "estoque": 10,
}

replica = {
    "online": True,
    "estoque": 10,
}

# Controle de concorrencia
MAXIMO_SIMULTANEO = 3

semaforo = threading.Semaphore(MAXIMO_SIMULTANEO)
trava = threading.Lock()

pedidos_confirmados = []
pedidos_falhos = []


def processar_pedido(numero):
    with semaforo:
        time.sleep(0.1)

        with trava:
            if not principal["online"]:
                pedidos_falhos.append(numero)
                return

            if principal["estoque"] > 0:
                principal["estoque"] -= 1
                pedidos_confirmados.append(numero)
            else:
                pedidos_falhos.append(numero)


def sincronizar():
    # Antes copiava replica["estoque"] para ela mesma; agora espelha o principal
    with trava:
        if replica["online"]:
            replica["estoque"] = principal["estoque"]


def consultar_estoque():
    if principal["online"]:
        return ("PRINCIPAL", principal["estoque"])

    # Antes repetia 'if principal["online"]:', impedindo o fallback para a replica
    if replica["online"]:
        return ("REPLICA", replica["estoque"])

    return "INDISPONIVEL", None


print("CENTRAL DE PEDIDOS".center(50, "="))
print("limite simultaneo:", MAXIMO_SIMULTANEO)
print("Estoque Inicial:", principal["estoque"])

trabalhadores = [
    threading.Thread(target=processar_pedido, args=(numero,))
    for numero in [101, 102, 103]
]

for trabalhador in trabalhadores:
    trabalhador.start()

for trabalhador in trabalhadores:
    trabalhador.join()

print("Pedidos confirmados:", sorted(pedidos_confirmados))
if pedidos_falhos:
    print("Pedidos falhos:", sorted(pedidos_falhos))
print("Estoque principal:", principal["estoque"])
print("Replica antes:", replica["estoque"])

sincronizar()

print("Replica depois:", replica["estoque"])

# Simulacao de falha
principal["online"] = False

nome, estoque = consultar_estoque()
print("Consulta apos falha:", nome, estoque)
