# 2D Physics Engine

A simple 2D physics simulator built with Pygame where you can spawn and interact with bouncing circles.

## Features
- Click to spawn circles with customizable properties
- Real-time physics simulation including gravity and collisions
- Adjustable circle size using slider
- Color selection (Red, Green, Blue)
- Preview of circle before spawning

## Requirements
- Python 3.x
- Pygame

## Installation
1. Clone this repository or download the source code
2. Install Pygame:
```bash
pip install pygame
```

## Usage
1. Run the program:
```bash
python main.py
```

2. Controls:
- Use the slider at the top to adjust circle size (5-50 pixels)
- Click the colored buttons to change circle color
- Click anywhere in the main window to spawn circles
- Circles will automatically fall, bounce, and interact with each other

## Physics Parameters
You can modify these constants in the code to adjust the simulation:
- `GRAVITY`: Controls fall speed
- `ELASTICITY`: Controls bounce strength (0-1)
- `FRICTION`: Controls speed decay (0-1)