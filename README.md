# SABOTAJE

Juego de palabras con impostores, ambientado en Argentina. Inspirado en el juego *Undercover / Spy*.

## Roles

| Rol | Descripción |
|-----|-------------|
| **LABURANTE** | Civil. Recibe la palabra real. |
| **DOPPELGANGER** | Impostor encubierto. Recibe una palabra *similar* a la civil pero no sabe que es impostor (su carta dice "LABURANTE"). |
| **IMPOSTOR** | Sabe que es impostor. No recibe ninguna palabra. |

## Cómo jugar

1. **Configuración** – Ingresá la dificultad (fácil / medio / difícil) y los nombres de los jugadores (3–10).
2. **Reparto de roles** – Cada jugador, en el orden sorteado, toma el dispositivo, presiona `ESPACIO` para ver su carta y luego `ESPACIO` de nuevo para ocultarla antes de pasarle el dispositivo al siguiente.
3. **Discusión** – Los jugadores hablan sobre su palabra sin decirla directamente. El objetivo es detectar a los impostores.
4. **Votación** – Los jugadores votan para eliminar a alguien. Al ser eliminado se revela su rol verdadero:
   - **LABURANTE** → el juego continúa.
   - **IMPOSTOR / DOPPELGANGER** → tiene la oportunidad de adivinar la palabra civil.
     - Si **adivina** → ¡los impostores ganan!
     - Si **no adivina** → el juego continúa (si quedan impostores).

## Condiciones de victoria

- **LABURANTES ganan** si eliminan a todos los impostores.
- **IMPOSTORES ganan** si igualan o superan en número a los laburantes, o si un impostor/doppelganger eliminado adivina la palabra civil.

## Selección inteligente de impostores

El juego elige automáticamente el número de impostores según los jugadores:

| Jugadores | Impostores | Probabilidad |
|-----------|-----------|--------------|
| 3–4 | 1 | 100 % |
| 5 | 1 ó 2 | 50 / 50 |
| 6 | 1 ó 2 | 20 / 80 |
| 7 | 2 ó 3 | 40 / 60 |
| 8 | 2 ó 3 | 20 / 80 |
| 9 | 3 ó 4 | 40 / 60 |
| 10 | 3 ó 4 | 20 / 80 |

Dentro del grupo de impostores, la proporción IMPOSTOR / DOPPELGANGER también se elige aleatoriamente con igual probabilidad entre todas las distribuciones posibles.

## Base de palabras

`data/palabras.csv` contiene ~300 pares de palabras (civil, doppelganger) ambientadas en Argentina, organizadas en tres niveles de dificultad: `facil`, `medio`, `dificil`.

## Instalación y ejecución

```bash
# Python 3.8+ requerido, sin dependencias externas
python main.py
```

## Estructura del proyecto

```
sabotaje/
├── main.py               # Punto de entrada y lógica del juego
├── game/
│   ├── roles.py          # Enum de roles
│   ├── impostor_logic.py # Selección inteligente de impostores
│   ├── word_database.py  # Carga del CSV de palabras
│   └── display.py        # Utilidades de consola
└── data/
    └── palabras.csv      # ~300 pares de palabras argentinas
```

## Hoja de ruta

- [x] Lógica central del juego (consola, una sola pantalla)
- [x] Selección inteligente de impostores por cantidad de jugadores
- [x] Base de datos con ~300 palabras argentinas (fácil / medio / difícil)
- [ ] IHM gráfica en Windows (PyQt / Pygame)
- [ ] APK para Android (Kivy o Android Studio + Python)
