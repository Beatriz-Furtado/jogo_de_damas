"""
Módulo que contém as constantes usadas no jogo
"""

tam = 8
pino = '●'
c1 = 31
c2 = 33
inicio = 'JOGO DE DAMAS'
quad_branco = '.'
quad_preto = '-'
pino_vermelho = 'x'
pino_amarelo = 'o'
dama_vermelha = 'X'
dama_amarela = 'O'
regras ='''\033[1;35m1. Objetivo: imobilizar ou capturar todas as peças do adversário.
2. O lance inicial cabe sempre ao jogador que estiver com as peças vermelhas.
3. A pedra anda só para frente, uma casa de cada vez, na diagonal.
4. Quando a pedra atinge a última linha do tabuleiro, ela é promovida à Dama.
5. A Dama é uma peça de movimentos mais amplos.
6. A Dama anda para frente e para trás, quantas casas quiser, não podendo saltar sobre uma peça da mesma cor.
7. A captura é obrigatória. Duas ou mais peças juntas, na mesma diagonal não podem ser capturadas.
8. A pedra pode capturar a Dama e a Dama pode capturar a pedra.
9. A pedra e a Dama podem capturar, tanto para frente, como para trás, uma ou mais peças.
10. A pedra que durante o lance de captura de várias peças, apenas passe por qualquer casa de coroação, sem aí parar, não será promovida à Dama.
11. Na execução do lance de captura, é permitido passar mais de uma vez pela mesma casa vazia.
12. Na execução do lance de captura, não é permitido capturar a mesma peça mais de uma vez.
13. As peças capturadas não podem ser retiradas do tabuleiro antes de completar o lance de captura.
14. A dama no último movimento de captura pode parar em qualquer casa livre na diagonal em que está capturando.
15. Empate: após 20 (vinte) lances sucessivos de Damas de cada jogador, sem captura ou deslocamento de pedra, a partida é declarada empatada.\033[m'''
