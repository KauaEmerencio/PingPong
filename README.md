# PingPong
Recriação do Pong em Python com Pygame. Foco na aplicação prática de Programação Orientada a Objetos (POO), Encapsulamento e Classes, migrando da lógica procedural para objetos estruturados. Projeto acadêmico para a disciplina de Laboratório de Programação.
# 🏓 Pong: POO Edition

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?style=for-the-badge&logo=pygame)

> Uma recriação clássica do jogo Pong desenvolvida em Python, focada na aplicação prática dos pilares da **Programação Orientada a Objetos**.

---

## 📸 Demonstração

![Screenshot do Jogo](screenshot.png)
*(Não esqueça de subir uma imagem do jogo com este nome na pasta do projeto)*

---

## 🧠 Conceitos Aplicados

Este projeto aplica conceitos fundamentais de engenharia de software ensinados em sala:

- **Orientação a Objetos:** Uso de Classes (`Game`, `Paddle`, `Ball`) para modelar o sistema, substituindo a lógica procedural e variáveis globais.
- **Encapsulamento:** Proteção de atributos (como posição e velocidade) através do `self` e construtores `__init__`.
- **Estruturas de Dados:** Uso de **Tuplas** (imutáveis) para configurações de cores e **Listas** implícitas no gerenciamento de eventos.
- **Game Loop:** Controle de fluxo otimizado com `while` para garantir performance sem estouro de pilha.

---

## 🎮 Controles

O jogo termina quando um jogador atinge **10 pontos**.

| Ação | Jogador 1 (Esq) | Jogador 2 (Dir) |
| :--- | :---: | :---: |
| **Mover Cima** | `W` | `Seta Cima` |
| **Mover Baixo** | `S` | `Seta Baixo` |
| **Pausar** | `P` | `P` |
| **Sair** | `ESC` | `ESC` |

---

## 🚀 Como Rodar

1. **Clone este repositório:**
   ```bash
   git clone [https://github.com/kauaemerencio/pong-poo.git](https://github.com/kauaemerencio/pong-poo.git)
