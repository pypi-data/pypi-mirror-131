# bomberman-code-showdown

Welcome to the BomberCUP! Here, you will create an AI which will play Bomberman by itself, competing in a tournament of
last-bomberman-standing and obliterate the other participants' AIs!

To install:

```
pip install bomberman-code-showdown
```

# Task

Make an AI script in your language of choice (except PHP), which, by making HTTP requests to a web server, controls the
Bomberman character in a last-bomberman-standing fashion!

The game supports up to 4 players.

# How to make the AI and run it

You will need to create a program in your language of choice, which will accept a single parameter, a URL for the
current player base URL you will use.

Example: If you receive `http://localhost:8000/player-1`, you will need to make your requests
to `http://localhost:8000/player-1/game-state` and
`http://localhost:8000/player-1/action`. PLEASE DO NOT CHEAT AND MAKE REQUESTS TO YOUR OPPONENT'S URL! IF YOU DO SO, YOU
WILL BE PENALIZED!1!!one!

Your control loop will need to *probe* the API first to make sure the game started. How the scripts flows will look
like:

- player 1 script starts
- player 2 script starts
- game starts, HTTP control server comes live
- game ends
- all scripts are forcefully closed.
- results are collected

So, your script will have a brief period of time when it can't access the API, because the game did not start yet.

You can find examples in the `example_ai` directory:

- `example_ai/pure_randomness.py` - a very dumb "AI" based on pure randomness, usually kills itself in the first seconds

# Playing the game

The purpose of the game is to create an AI that controls the game through HTTP commands.

To run the AI, create a `config.json` with the following contents

```json
{
  "players": [
    {
      "id": "me",
      "color": "red",
      "command": "python3 my_super_awesome_ai.py"
    },
    {
      "id": "ai",
      "color": "blue",
      "command": "node mySuperAwesomeAi.js"
    }
  ]
}
```

Then run this command to start the game:

```shell
bomberman-code-showdown ./config.json "me,ai"
```

First parameter is the path to the created `config.json`, the 2nd parameter is a comma separated list of the ids of the
active players.

### Displaying the AI script output for debug purposes

```shell
bomberman-code-showdown ./config.json "me,ai" --show-all-ai-output
# or to show only a specific AI output
bomberman-code-showdown ./config.json "me,ai" --show-ai-output "ai"
```

## Getting the current game state

`GET /player-[i]/game-state` -> get a representation of the full game state. Information included: game objects such as
walls, bombs, other players.

A response may look like

```
{
  "obejcts": [
    {"type": "player", "is_me": false, "name": "Other player name", "position": [0, 0]},  # other players
    {"type": "player", "is_me": true, "name": "My name", "position": [0, 0]},  # self
    {"type": "descructible", "position": [3, 2]},  # bricks that can be destroyed with bombs
    {"type": "indescructible", "position": [3, 2]},  # indestructible obstacles that can't be destroyed with bombs
    {"type": "bomb", "position": [3, 2]},  # a bomb
    {"type": "more_bombs", "position": [3, 2]},  # poweup, you can place one more bomb (max bombs += 1)
    {"type": "speed", "position": [3, 2]},  # you move faster, speed += 1 (see Speed section for more info)
    {"type": "bigger_explosion", "position": [3, 2]},  # increase the explosion distance by 1
    {"type": "fire", "position": [3, 2]},  # the fire of the explosion. DONT GO IN IT! IF YOU GO IN IT, YOU DIE!
  ],
  "player": {
    "bomb_wait_time": 3, # in seconds
    "current_bombs": 0, # bombs placed which have not exploded yet
    "explosion_range": 2, # how many tiles up/down/left/right bombs explode
    "name": "My name",
    "position": [10, 10], # current position
    "speed": 1.0  # the speed of the player
  }
}
```

## Making a move

`POST /player-[i]/action` -> do something in game

- `{"action": "move", "direction": "up|down|left|right"}` -> move the current player
- `{"action": "bomb"}` -> place a bomb

Each player can make a move once every interval of time, depending on its speed. The formula for speed is
`interval = max(0.5 - 0.05 * speed, 0.1)`

| Speed | Interval |
|-------|----------|
| 1     | 0.45     |
| 2     | 0.4      |
| 3     | 0.35     |
| 4     | 0.3      |
| 5     | 0.25     |
| 6     | 0.2      |
| 7     | 0.15     |
| 8     | 0.1      |
| 9     | 0.1      |
| 10    | 0.1      |

How is speed used: you can blast the control server with requests, but your character will move only once
very `interval` seconds, the commands that come in between are discarded. This is done to ensure a fair game, because
computers have superhuman speeds and we don't really like the matches to end in less than one second.

# The game end

The game can end in the following ways:

- one player is left alive, resulting in a win for the last standing player and a loss for others
- both players die at the same time (highly improbable) resulting in a draw
- the time runs out, resulting in a draw

After the game is finished and stopped, a `stats.json` file is generated in the current directory, containing some stats
about the match:

```json
{
  "time_left": 115.17540764808655,
  "finished": true,
  "winner": "ai2",
  "players": [
    {
      "player": "ai1",
      "bombs_placed": 1,
      "powerups": {
        "bombs": 0,
        "explosion": 0,
        "speed": 0
      },
      "walls_destroyed": 1,
      "powerups_destroyed": 0,
      "max_bomb_count": 1
    },
    {
      "player": "ai2",
      "bombs_placed": 2,
      "powerups": {
        "bombs": 0,
        "explosion": 0,
        "speed": 0
      },
      "walls_destroyed": 1,
      "powerups_destroyed": 0,
      "max_bomb_count": 1
    }
  ]
}
```

======= After you start the game, the game UI will show up and a HTTP control server will be started
at `http://localhost:8000`, with the following available commands:

The URL routes are:

- `GET /player-[i]/game-state` : get a representation of the full game state. Information included: game objects such as
  walls, bombs, other players
- `POST /player-[i]/action`: do something in game
    - `{"action": "move", "direction": "up|down|left|right"}` -> move the current player
    - `{"action": "bomb"}` -> place a bomb

# After the game

The game will stop when all players are dead (draw) or when only one is alive (the winner - last bomberman standing).

There will be a generated JSON file with stats in the current working directory, with some interesting stats about each
participating player:

```json
[
  {
    "player": "Team 1", 
    "bombs_placed": 2, 
    "powerups": {
      "bombs": 0, 
      "explosion": 0, 
      "speed": 0
    }, 
    "walls_destroyed": 1, 
    "powerups_destroyed": 0, 
    "max_bomb_count": 1
  }, 
  {
    "player": "Team 2", 
    "bombs_placed": 0, 
    "powerups": {
      "bombs": 0, 
      "explosion": 0, 
      "speed": 0
    }, 
    "walls_destroyed": 0, 
    "powerups_destroyed": 0, 
    "max_bomb_count": 0
  }
]
