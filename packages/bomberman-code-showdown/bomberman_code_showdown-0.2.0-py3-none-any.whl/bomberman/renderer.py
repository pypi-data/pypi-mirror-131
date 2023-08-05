import argparse
import json
import subprocess
import sys
import time
from collections import namedtuple

import pygame
from pygame.event import Event

from bomberman.events import EVENT_PLAYER_1
from bomberman.game import BombermanGame
from bomberman.http_controller import HttpController
from bomberman.objects.player import Player

GRID_SIZE = 64
MAP_SIZE = pygame.Vector2(11, 11)

# rgb(27, 94, 32)
BACKGROUND_COLOR = (27, 94, 32)


class RenderInfo:
    def __init__(self, screen_size):
        self.screen_size = screen_size


class GameRenderer:
    def __init__(self, game: BombermanGame, screen_size: pygame.Vector2):
        self.game = game
        self.screen_size = screen_size
        self.screen = None

    def render(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        print(f'Initialized game screen: {self.screen}')

        while True:
            self.game_loop()

    def game_loop(self):
        for _ in pygame.event.get(eventtype=[pygame.QUIT]):
            print('Received QUIT. Exiting')
            sys.exit()

        for ev in pygame.event.get(eventtype=[pygame.KEYDOWN]):
            if ev.key in (pygame.K_DOWN, pygame.K_s):
                direction = 'down'
            elif ev.key in (pygame.K_UP, pygame.K_w):
                direction = 'up'
            elif ev.key in (pygame.K_LEFT, pygame.K_a):
                direction = 'left'
            elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                direction = 'right'
            else:
                direction = None

            if direction:
                pygame.event.post(Event(EVENT_PLAYER_1, action='move', direction=direction))

            if ev.key in (pygame.K_SPACE,):
                pygame.event.post(Event(EVENT_PLAYER_1, action='bomb'))

        self.game.update_game_state()
        self.screen.fill(BACKGROUND_COLOR)
        self.render_game()
        if self.game.finished:
            if self.game.winner:
                pygame.display.set_caption(f'Winner: {self.game.winner.name} - time left: {self.game.timer:.2f}')
            else:
                pygame.display.set_caption('Draw!')
        else:
            pygame.display.set_caption(f'Time left: {self.game.timer:.2f}')
        pygame.display.flip()

    def render_game(self):
        for obj in self.game.iter_game_objects():
            pos = obj.position[1] * GRID_SIZE, obj.position[0] * GRID_SIZE
            obj_image_rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            self.screen.blit(
                pygame.transform.scale(obj.image, (GRID_SIZE, GRID_SIZE)),
                obj_image_rect
            )


class PlayerConfig:
    def __init__(self, id, color, command):
        self.id = id
        self.color = color
        self.command = command


CommandLineConfig = namedtuple('CommandLineConfig', 'teams show_ai_output')


def get_cmd_args() -> CommandLineConfig:
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('current_players')
    parser.add_argument('--show-all-ai-output', action='store_true')
    parser.add_argument('--show-ai-output')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    teams = []
    for player_id in args.current_players.split(','):
        for team in config["teams"]:
            if team['id'] == player_id:
                teams.append(PlayerConfig(id=team['id'], color=team['color'], command=team['command']))

    show_output = []
    if args.show_all_ai_output or args.show_ai_output:
        if args.show_all_ai_output:
            show_output = [t.id for t in teams]
        else:
            show_output = [t.id for t in teams if t.id in args.show_ai_output.split(',')]

    return CommandLineConfig(teams, show_output)


def main():
    cmd_args = get_cmd_args()

    game = BombermanGame(
        players=[
            Player(t.id, t.color) for t in cmd_args.teams
        ],
        map_size=MAP_SIZE
    )

    # start scripts
    processes = []
    for i, player in enumerate(cmd_args.teams):
        cmd = player.command + ' ' + f'http://localhost:8000/player-{i + 1}'
        print(f'Starting {cmd}')
        if player.id in cmd_args.show_ai_output:
            kwargs = {}
        else:
            kwargs = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
        processes.append(subprocess.Popen(cmd, shell=True, **kwargs))

    print('Waiting one second to let the scripts start')
    time.sleep(1)

    try:
        HttpController('0.0.0.0', 8000, game).start_server()
        renderer = GameRenderer(game, GRID_SIZE * MAP_SIZE)
        renderer.render()
    except KeyboardInterrupt:
        player_data = []
        for player in game.players:
            player_data.append(player.stats.to_json())
        with open('stats.json', 'w') as f:
            json.dump({
                "time_left": game.timer,
                "finished": game.finished,
                "winner": game.winner.name,
                "players": player_data
            }, f)
        print('Stats written to stats.json')

        print('Stopping the scripts')
        for proc in processes:
            proc.kill()


if __name__ == '__main__':
    main()
