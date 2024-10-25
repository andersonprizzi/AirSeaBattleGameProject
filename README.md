# Jogo: Air-Sea Battle Remake

Este é um remake do clássico *Air-Sea Battle* do Atari 2600, implementado em Python utilizando a biblioteca Pygame. O jogo consiste em controlar um canhão para derrubar aviões que se movem na parte superior da tela.

## Como Jogar

- **Mover o Canhão**: Use as setas **←** e **→** para mover o canhão para a esquerda e direita, respectivamente.
- **Alterar o Ângulo do Canhão**: Use as setas **↑** e **↓** para mudar o ângulo de disparo entre 30°, 60°, 90°, 120º e 150º. O ângulo inicial do canhão é de 90° e pode ser ajustado durante o jogo.
- **Disparar Projetil**: Pressione a barra de **espaço** para disparar um projétil. O projétil segue a direção atual do ângulo do canhão e desaparece ao atingir um avião ou ultrapassar a borda da tela.

## Funcionalidades do Jogo

1. **Movimentação do Canhão**: O canhão fica na parte inferior da tela e pode ser movido horizontalmente para alinhar o disparo.
  
2. **Aviões Inimigos**:
   - Aviões aparecem em grupos de 3 a 5 na parte superior da tela.
   - Cada grupo se move na mesma direção e com a mesma velocidade.
   - Os aviões desaparecem quando são atingidos por um projétil ou saem da tela.
   - A direção de cada novo grupo de aviões alterna entre esquerda e direita.

3. **Disparo e Pontuação**:
   - Cada projétil dispara em linha reta com o ângulo atual do canhão e desaparece ao ultrapassar a tela ou atingir um avião.
   - A pontuação aumenta a cada acerto em um avião, e o total de pontos é exibido na tela.

4. **Ângulo de Disparo**:
   - O ângulo do canhão pode ser ajustado entre 30°, 60° e 90°, alterando a trajetória do projétil.
   - O ângulo permanece inalterado até que outra tecla seja pressionada para modificá-lo.

5. **Indicadores na Tela**:
   - A tela exibe o tempo restante da partida e a pontuação do jogador.

## Tecnologias Utilizadas

- **Pygame**: Para renderização gráfica, manipulação de eventos, e controle de áudio.

