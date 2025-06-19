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

import time
import torch
import operator
import numpy as np

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.0.2")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)

Font=pygame.font.SysFont('timesnewroman',  18)

clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
model_inference_event = pygame.USEREVENT + 1
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

gene_pool = dict()

def create_sprites(generation, num_indiviual):
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    birds = [Bird(50, 50, f"gen_{generation}_inv_{i}", sprites) for i in range(num_indiviual)]

    return birds, GameStartMessage(sprites), Score(sprites)


sprites.empty()

birds, game_start_message, score = create_sprites("test", 1)

gene = torch.tensor(np.load(".\\model_weights\\gen_57_inv_54.npy"))

birds[0].transform_gene_to_weight(gene)

running = True
gameover = False
gamestarted = False


pygame.time.set_timer(column_create_event, 1500)
pygame.time.set_timer(model_inference_event, 100)
    
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
                birds, game_start_message, score = create_sprites("Test", 1)


        if not gameover and event.type == model_inference_event:

            column_sprites = [(col.rect.x, col.rect.y, col.sprite_rect.height, col.gap) for col in sprites if type(col) is Column and col.rect.x > 50 - 52]
            if column_sprites:
                min_col = min(column_sprites, key=operator.itemgetter(0))
                obs_x, obs_y, t_h, g = min_col
            else:
                obs_x = -50
                obs_y = configs.SCREEN_HEIGHT // 2
                t_h = 0
                g = 0

            for bird in birds:
                bird.infer_event(bird.rect.x, bird.rect.y, obs_x, obs_y+t_h, obs_y+t_h+g, obs_x+52, bird.flap)         

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    for bird in birds:
        if bird.check_collision(sprites):
            bird.still_alive = False
            bird.kill()
    
    if all([not bird.still_alive for bird in birds]) and not gameover:
        gameover = True
        gamestarted = False
        GameOverMessage(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audio("hit")

        time.sleep(0.5) 
        running = False

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            for bird in birds:
                if bird.still_alive:
                    bird.increase_score()
            assets.play_audio("point")

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
