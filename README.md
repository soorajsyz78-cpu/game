# Football Game

A playable 2D football game built with Python and Pygame featuring player movement, ball control, score tracking, and AI opponents.

## Features

- 🎮 **Playable Football Game** - Control your team and score goals
- ⚽ **Ball Physics** - Realistic ball movement with friction and gravity
- 👥 **AI Opponent** - Computer-controlled opponent team with intelligent movement
- 📊 **Score Tracking** - Real-time score display with game timer
- 🎯 **Goal Detection** - Automatic goal recognition and scoring
- 🎮 **Simple Controls** - Arrow keys for movement, spacebar to kick

## Requirements

- Python 3.7+
- Pygame 2.5+

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/soorajsyz78-cpu/game.git
   cd game
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Game Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Move player |
| **Space** | Kick ball |
| **R** | Restart game |
| **ESC** | Quit game |

## Game Rules

- **Objective**: Score more goals than the opponent in 90 seconds
- **Blue Team**: You control the blue team (left side)
- **Red Team**: Computer-controlled opponent (right side)
- **Scoring**: Get the ball into the opponent's goal (red area)
- **Ball Physics**: Ball moves realistically with friction and bounces off walls
- **Movement**: Each team has 3 players for strategic gameplay

## Game Features

### Player Movement
- Move your controlled player smoothly around the field
- Stay within field boundaries
- Get close to the ball to kick it

### Ball Control
- Kick the ball by pressing spacebar when near it
- Ball responds with physics-based movement
- Ball bounces off walls and field boundaries

### AI Opponent
- Red team players track the ball
- Simple pathfinding toward the ball
- Automatic ball kicks when in range
- Defensive and offensive positioning

### Score Tracking
- Real-time score display at top of screen
- Game timer showing remaining time
- Winner announcement when game ends
- Automatic game reset after completion

## Project Structure

```
.
├── main.py           # Main game entry point
├── game.py           # Core game logic and state management
├── player.py         # Player class with movement and AI
├── ball.py           # Ball physics and behavior
├── field.py          # Game field/arena and goal detection
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Game Flow

1. **Initialization**: Game starts with both teams positioned on the field
2. **Gameplay**: Control your player to reach and kick the ball
3. **Scoring**: When the ball enters the goal, a point is awarded
4. **Game End**: After 90 seconds, the game ends and displays the winner
5. **Restart**: Press 'R' to play again

## Future Enhancements

- [ ] Improved AI with team strategies
- [ ] Multiple difficulty levels
- [ ] Sound effects and music
- [ ] Player animations and sprites
- [ ] More realistic ball physics (curved shots)
- [ ] Multiplayer support (2 humans)
- [ ] Team formation strategies
- [ ] Power-ups and special abilities
- [ ] Different game modes (penalty kicks, etc.)
- [ ] Statistics tracking (goals, assists, etc.)

## Technical Details

### Ball Physics
- Friction coefficient: 0.98 per frame
- Gravity: 0.3 pixels per frame
- Wall bounce damping: 0.8
- Kick power: 20 units

### Game Settings
- Field size: 800x600 pixels
- Game duration: 90 seconds
- Frame rate: 60 FPS
- Player kick range: 40 pixels

## Troubleshooting

**"ModuleNotFoundError: No module named 'pygame'"**
- Run: `pip install pygame`

**Game runs slowly**
- Make sure you're running on Python 3.7+
- Close other applications to free up resources

**Ball sticks to wall**
- This is normal due to physics simulation, ball will bounce away

## License

Free to use and modify

## Author

Developed by soorajsyz78-cpu
