# Air-Sea Battle Remake

This game is a remake of the classic *Air-Sea Battle* from Atari 2600, implemented in Python using Pygame library. The game consists of controlling a cannon to destroy enemy planes passing through your territory. 

## How to play

- **Moving the Cannon**: Use the arrow keys **←** and **→** to move the cannon left and right, respectively.
- **Changing the Cannon's Angle**: Use the arrow keys **↑** e **↓** to change the firing angle between 30°, 60°, 90°, 120° e 150°. The cannon starts at 90°, and the **↓** changes to lower angles, while the **↑** arrow increases the angle.
- **Firing**: Press the **spacebar** to fire a cannonball. The projectile will travel at a lowering speed through the current direction that the cannon's angle defines. It will disappear as it reaches the end of the screen or hits a plane.

## Mechanics

1. **Starting A Match**: To start a match, select the option 'Create Server' in the main menu. Configure a port value between 1025 and 65535 and wait for another player in your local network to connect to the server you just opened. To connect to a server, select the option 'Connect to Server' and type the IPv4 address of the host, plus the port they configured for the server.

2. **Move the Cannon**: The cannon can move until half the screen. Manage the angle and the ammunition to defeat as many enemies as possible.

3. **Control Your Ammunition**: Each cannon has a 5-bullet limit. The ammo recharges as the cannonball leaves the screen. Control your firing so you never run out of it!
  
4. **Enemy Planes**: The enemy planes appear in groups of 3 to 5 at a time. All the planes move in the same direction and at the same speed. Some planes are special and will drop technology that makes your cannon stronger. The abilities are: 
   - *Yellow Plane*: gives you infinite ammunition. 
   - *Red Plane*: gives you double points for every plane you defeat.
   - *Purple Plane*: it's more resistant and takes two cannonballs to be destroyed, but gives you 3 points instead of 1.

5. **Be the Best Defender**: Within the duration of the battle, be the best cannon controller and score the most points.

## Accessiblity
The game is currently available in English, Brazilian Portuguese, and Simplified Chinese. The music can be turned on and off.  

## Setup

### For players
In the link below, the game executable will be available in zip files. Get the version compatible with your operational system. Currently, McAffe Antivirus is known for quarantining the game in its win64 version because of PyInstaller. If you have issues with antivirus, download the 'Console-Release' zip file. 
```bash
https://drive.google.com/drive/folders/1cW0n8iTvlNjva47w_67vK8rMmGOCZwHj?usp=sharing
```

### For developers
Clone this repository in a folder of your computer with:
```bash
git clone https://github.com/andersonprizzi/AirSeaBattleRemake
```

Then, activate the virtual environment in that folder:
- In Windows:
```bash
python -m venv environment
environment\Scripts\activate
```

- In Linux:
```bash
python -m venv environment
source environment/bin/activate
```

With the virtual environment set, download the libraries used for the development:
```bash
pip install -r requirements.txt
```

After that, you should be able to continue developing using the game.

## Credits
The game was entirely developed by **Anderson Pastore Rizzi** and **Eduardo Eberhardt Pereira**. Art by: krystonschwarze, Noah Jacobus, Konstantin Filatov, ansimuz, and gamedeveloperstudio. The song is "Price of Freedom" by Zakhar Valaha.