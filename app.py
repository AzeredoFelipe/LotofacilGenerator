import pandas as pd
import random

# ===============================
# CONFIGURAÇÕES
# ===============================
ARQUIVO_EXCEL = "lotofacil.xlsx"
COLUNAS_BOLAS = [f'Bola{i}' for i in range(1, 16)]

TOTAL_NUMEROS = 15
NUM_MIN = 1
NUM_MAX = 25

MIN_PARES = 6
MAX_PARES = 9

SOMA_MIN = 170
SOMA_MAX = 220

FAIXAS_EXATAS = 5

MIN_SEQ = 3
MAX_SEQ = 6


# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def contar_pares(jogo):
    return sum(1 for n in jogo if n % 2 == 0)


def soma_jogo(jogo):
    return sum(jogo)


def contar_faixas(jogo):
    faixas = set()
    for n in jogo:
        if 1 <= n <= 5:
            faixas.add(1)
        elif 6 <= n <= 10:
            faixas.add(2)
        elif 11 <= n <= 15:
            faixas.add(3)
        elif 16 <= n <= 20:
            faixas.add(4)
        elif 21 <= n <= 25:
            faixas.add(5)
    return len(faixas)


def maior_sequencia(jogo):
    jogo = sorted(jogo)
    maior = atual = 1

    for i in range(1, len(jogo)):
        if jogo[i] == jogo[i - 1] + 1:
            atual += 1
            maior = max(maior, atual)
        else:
            atual = 1

    return maior


# ===============================
# SCORE INTELIGENTE
# ===============================

def calcular_score(jogo):
    score = 0

    pares = contar_pares(jogo)
    soma = soma_jogo(jogo)
    seq = maior_sequencia(jogo)

    # Pares
    if pares in (7, 8):
        score += 3
    elif pares in (6, 9):
        score += 2

    # Soma
    if 185 <= soma <= 205:
        score += 3
    elif 170 <= soma <= 220:
        score += 1

    # Sequência
    if seq in (4, 5):
        score += 3
    elif seq in (3, 6):
        score += 1

    return score


# ===============================
# VALIDAÇÃO
# ===============================

def jogo_valido(jogo):
    if not (MIN_PARES <= contar_pares(jogo) <= MAX_PARES):
        return False

    if not (SOMA_MIN <= soma_jogo(jogo) <= SOMA_MAX):
        return False

    if contar_faixas(jogo) != FAIXAS_EXATAS:
        return False

    if not (MIN_SEQ <= maior_sequencia(jogo) <= MAX_SEQ):
        return False

    return True


# ===============================
# GERADOR
# ===============================

def gerar_jogo():
    return sorted(random.sample(range(NUM_MIN, NUM_MAX + 1), TOTAL_NUMEROS))


def gerar_jogos(qtd):
    jogos = []
    tentativas = 0

    while len(jogos) < qtd:
        jogo = gerar_jogo()
        tentativas += 1

        if jogo_valido(jogo) and jogo not in jogos:
            score = calcular_score(jogo)
            jogos.append((jogo, score))

    print(f"\n🎯 Jogos gerados após {tentativas} tentativas.")
    return sorted(jogos, key=lambda x: x[1], reverse=True)


# ===============================
# SALVAR TXT
# ===============================

def salvar_txt(jogos):
    with open("jogos_lotofacil.txt", "w", encoding="utf-8") as f:
        f.write("JOGOS LOTOFÁCIL\n")
        f.write("=" * 40 + "\n\n")

        for i, (jogo, score) in enumerate(jogos, 1):
            nums = " - ".join(f"{n:02d}" for n in jogo)
            f.write(f"Jogo {i}: {nums} | Score: {score}\n")

    print("📄 Arquivo 'jogos_lotofacil.txt' gerado com sucesso!")


# ===============================
# MAIN
# ===============================

def main():
    print("🎯 GERADOR INTELIGENTE — LOTOFÁCIL\n")
    qtd = int(input("Quantos jogos deseja gerar? "))

    jogos = gerar_jogos(qtd)

    print("\n🏆 MELHORES JOGOS:\n")
    for i, (jogo, score) in enumerate(jogos, 1):
        print(f"Jogo {i}: {jogo} | Score: {score}")

    salvar_txt(jogos)
    print("\n✅ Finalizado com sucesso!")


if __name__ == "__main__":
    main()
