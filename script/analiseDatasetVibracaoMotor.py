import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# Definicao de tamanho dos pacotes
TAMANHO_PACOTE = 128

# Carregar o padrão de vibração
with open('PADRAOVIBRACAOMOTORSTREAM009CC.txt', 'r') as f:
    padrao = [float(linha.strip()) for linha in f.readlines()]

# Carregar os dados de vibração
with open('VIBRACAOMOTORSTREAM009CC.txt', 'r') as f:
    dados = [float(linha.strip()) for linha in f.readlines()]

# Definir número de pacotes
num_pacotes = len(dados) // TAMANHO_PACOTE

# Analisar pacotes
resultados = []
anomalias_detectadas = []
for i in range(num_pacotes):
    inicio = i * TAMANHO_PACOTE
    fim = inicio + TAMANHO_PACOTE
    pacote = dados[inicio:fim]
    
    # Ajustar tamanho do padrão se necessário
    padrao_ajustado = padrao[:len(pacote)]
    
    # Calcular correlação
    df = pd.DataFrame({'Padrão': padrao_ajustado, 'Pacote': pacote})
    correlacao = df.corr().iloc[0, 1]  # Correlação entre Padrão e Pacote
    
    # Classificar o pacote
    if correlacao >= 0.8:
        status = "Vibração Ok"
    elif 0.5 <= correlacao < 0.8:
        status = "Atenção"
    else:
        status = "Anomalia"
        anomalias_detectadas.append(pacote)  # Armazena pacotes anômalos
    
    resultados.append(status)
    print(f"Pacote {i+1}: {status} (Correlação: {correlacao:.2f})")

# Verificar estado final do motor
anomalias = resultados.count("Anomalia")
if anomalias > num_pacotes * 0.3:
    print("\nO motor está ruim e precisa de revisão!")
else:
    print("\nO motor está em bom estado.")

# Plotar gráfico do padrão de vibração
plt.figure(figsize=(10, 5))
plt.plot(padrao, label='Padrão de Vibração', color='green')
plt.xlabel('Amostras')
plt.ylabel('Intensidade de Vibração')
plt.title('Padrão de Vibração do Motor')
plt.legend()
plt.show()

# Plotar gráfico de vibração do motor
plt.figure(figsize=(10, 5))
plt.plot(dados, label='Vibração do Motor', color='blue')
plt.xlabel('Amostras')
plt.ylabel('Intensidade de Vibração')
plt.title('Gráfico de Vibração do Motor')
plt.legend()
plt.show()

# Plotar gráfico de uma anomalia detectada
if anomalias_detectadas:
    plt.figure(figsize=(10, 5))
    plt.plot(anomalias_detectadas[0], label='Anomalia Detectada', color='red')
    plt.xlabel('Amostras')
    plt.ylabel('Intensidade de Vibração')
    plt.title('Exemplo de Anomalia Detectada')
    plt.legend()
    plt.show()
