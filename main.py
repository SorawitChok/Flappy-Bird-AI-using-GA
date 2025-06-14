import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.gameover_message import GameOverMessage
from objects.gamestart_message import GameStartMessage
from objects.score import Score

from model import FlappyBirdModel

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.0.2")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)


clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites(num_indiviual):
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    birds = [Bird(-50, 50+30*i, f"inv_{i}", sprites) for i in range(num_indiviual)]

    return birds, GameStartMessage(sprites), Score(sprites)


birds, game_start_message, score = create_sprites(configs.NUM_INDIVIDUAL)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                birds, game_start_message, score = create_sprites(configs.NUM_INDIVIDUAL)

        # if not gameover:
        #     for bird in birds:
        #         bird.handle_event(event)
        if not gameover:
            obs_x = 999
            obs_y = 999
            for sprite in sprites:
                if type(sprite) is Column:
                    if sprite.rect.x < obs_x:
                        obs_x = sprite.rect.x
                        obs_y = sprite.rect.y
                    else:
                        obs_x = 0
                        obs_y = 0
            for bird in birds:
                bird.infer_event(bird.rect.x, bird.rect.y, obs_x, obs_y)
            

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()
    
    if all([bird.check_collision(sprites) for bird in birds]) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
