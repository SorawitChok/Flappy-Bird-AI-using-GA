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

import time

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird Game v1.0.2")

img = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(img)

Font=pygame.font.SysFont('timesnewroman',  18)

clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False

assets.load_sprites()
assets.load_audios()

sprites = pygame.sprite.LayeredUpdates()

def create_sprites(generation, num_indiviual):
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)
    birds = [Bird(-50, 50+30*i, f"gen_{generation}_inv_{i}", sprites) for i in range(num_indiviual)]

    return birds, GameStartMessage(sprites), Score(sprites)

for generation in range(configs.NUM_GENERATION):

    sprites.empty()

    birds, game_start_message, score = create_sprites(generation, configs.NUM_INDIVIDUAL)

    running = True
    gameover = False
    gamestarted = False

    if generation > 0:
        game_start_message.kill()
        pygame.time.set_timer(column_create_event, 1500)
        gamestarted = True
    else:
        gamestarted = False    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == column_create_event:
                Column(sprites)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gamestarted and not gameover and generation == 0:
                    gamestarted = True
                    game_start_message.kill()
                    pygame.time.set_timer(column_create_event, 1500)
                if event.key == pygame.K_ESCAPE and gameover:
                    gameover = False
                    gamestarted = False
                    sprites.empty()
                    birds, game_start_message, score = create_sprites(generation, configs.NUM_INDIVIDUAL)

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

        letter1 = Font.render(f"Generation {generation}", False, (0,0,0))
        text_generation = screen.blit(letter1,(170, 3))

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

        # if all([bird.check_collision(sprites) for bird in birds]) and not gameover:
        #     gameover = True
        #     gamestarted = False
        #     GameOverMessage(sprites)
        #     pygame.time.set_timer(column_create_event, 0)
        #     assets.play_audio("hit")

        #     time.sleep(0.5) 
        #     running = False

        for sprite in sprites:
            if type(sprite) is Column and sprite.is_passed():
                score.value += 1
                for bird in birds:
                    if bird.still_alive:
                        bird.increase_score()
                assets.play_audio("point")

        pygame.display.flip()
        clock.tick(configs.FPS)
    
    for bird in birds:
        print(bird.get_gene())

pygame.quit()
