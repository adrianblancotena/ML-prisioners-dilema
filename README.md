# 🧠 Dilema del Prisionero - IA Evolutiva

## 📜 Resumen

Este proyecto simula el famoso "Dilema del Prisionero", un escenario teórico de la teoría de juegos donde dos jugadores deben decidir entre cooperar o no cooperar, sin conocer la elección del otro jugador. El dilema se presenta porque las decisiones individuales que maximizan las recompensas personales pueden llevar a un peor resultado colectivo.

## 🎮 ¿Cómo Funciona el Juego?

En cada ronda del juego, ambos jugadores eligen simultáneamente entre dos opciones:

- **Cooperar**: Si ambos cooperan, cada jugador recibe 3 monedas.
- **No Cooperar**: Si uno coopera y el otro no, el que no coopera recibe 5 monedas, mientras que el que cooperó recibe 0.
- **Mutuamente No Cooperar**: Si ambos eligen no cooperar, cada jugador recibe 1 moneda.

El dilema radica en que aunque la cooperación mutua proporciona un buen resultado colectivo, individualmente puede ser tentador no cooperar para maximizar las ganancias, a costa del otro jugador.

## 🤖 ¿Por Qué se Ha Hecho Este Proyecto?

Este proyecto fue creado para explorar cómo una inteligencia artificial puede aprender a ganar consistentemente en el Dilema del Prisionero, adaptándose a diferentes tipos de oponentes. En lugar de aplicar una estrategia fija, la IA evolutiva busca la mejor estrategia para cada tipo de jugador (que puede ser siempre cooperador, siempre traidor, jugador aleatorio o seguir una estrategia tipo *Tit for Tat*).

## 🧬 Inteligencia Artificial Evolutiva

El enfoque principal de este proyecto es una IA evolutiva, que se entrena a lo largo de múltiples rondas contra distintos oponentes. La IA utiliza algoritmos genéticos para encontrar las mejores estrategias posibles con el objetivo de siempre ganar o, al menos, empatar en el juego.

El proceso consta de dos fases principales:

1. **Entrenamiento de la IA**: La IA juega repetidamente contra diferentes tipos de oponentes, ajustando su estrategia en función de los resultados obtenidos en cada ronda.
2. **Pruebas contra Oponentes**: Una vez entrenada, la IA puede ser probada contra cualquier oponente en el juego, permitiendo al usuario ver cómo se adapta y si logra ganar.

## 🚀 Características Principales del Proyecto

- **Interfaz Gráfica (GUI)**: El proyecto incluye una interfaz gráfica interactiva creada con `Tkinter` que permite seleccionar el oponente, entrenar a la IA y visualizar los resultados.
- **Tabla de Resultados**: Tras cada fase de pruebas, los resultados de las decisiones tomadas por la IA y el oponente, junto con las monedas obtenidas, se muestran en una tabla detallada.
- **Multiinstancia y Persistencia**: El progreso de la IA se guarda y puede continuarse aunque el programa se cierre, lo que permite entrenamientos prolongados.
- **Modularidad**: El código está dividido en módulos que hacen más fácil su mantenimiento y ampliación.

## 🖥️ ¿Qué Verás en la GUI?

En la interfaz, el usuario puede:

- **Entrenar la IA** contra distintos perfiles de jugadores.
- **Seleccionar un oponente** para probar la IA.
- **Visualizar los resultados** después de 100 rondas, viendo las decisiones de cada jugador y las monedas acumuladas.

El objetivo es crear una herramienta intuitiva que permita a cualquier persona interactuar con este experimento de inteligencia artificial y el dilema del prisionero.
