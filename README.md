# Monkey Tribe Wars

## Overview
Monkey Tribe Wars is a 2D strategy game where players control a tribe of monkeys competing for resources and territory. The game features resource management, tribe upgrades, and turn-based combat against AI-controlled enemy tribes, all developed using the Python Arcade framework.

---

## Instructions on How to Run the Program

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.11

### Tool Dependencies
- `arcade==3.0.0.dev37`
- `numpy==2.1.3`

### Steps to Set Up and Run
1. Clone the project repository from GitHub:
   ```bash
   git clone [Your GitHub Repository URL]
   cd MonkeyTribeWars
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate # For Linux/Mac
   venv\Scripts\activate # For Windows
3. Install the required dependencies:
   ```bash
   pip install arcade==3.0.0.dev37 numpy==2.1.3
4. Run the game:
   ```bash
   python main.py
## Gameplay Instructions
1. Start the Game: Run the program to enter the main game screen.
2. Navigate the Map: Use arrow keys to move your monkey across the grid.
3. Gather Resources: Approach resource nodes to collect materials.
4. Build Structures: Use collected resources to build shelters and upgrade your monkey.
5. Combat: Engage with enemy tribes using strategic combat mechanics.

## Keys
- Spacebar to attack
- H for building a hut
- T for building a tower
- C for creating AI player
- U for upgrading player spped
- I for upgrading combat strength
- O for upgrading health
- P for upgrading resource efficiency

## Development Tools
The following tools and libraries were uesd to develop Monkey Tribe Wars:
1. Arcade Python Framework: Used for the 2D game environment.
2. NumPy: Used for grid-based calculations and AI behavior management.
3. GitHub: Used for version control and collaboration.

## Troubleshooting
1. Compatibility Issues: Ensure you are using the correct Python and Arcade versions. Python 3.11 and Arcade 3.0.0.dev37 are required.
2. Dependency Errors: If any dependencies fail to install, try upgrading pip:
   ```bash
   pip install --upgrade pip
3. Game Crashes: Ensure all assets (sprites, sounds, etc.) are present in the project directory.
