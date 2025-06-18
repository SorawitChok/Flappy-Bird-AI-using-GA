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

import GA

import random

import operator

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

for generation in range(configs.NUM_GENERATION):

    sprites.empty()

    birds, game_start_message, score = create_sprites(generation, configs.NUM_INDIVIDUAL)

    # Genetic Operation
    if generation > 0:
        population = gene_pool[generation-1]
        population = list(population.values())
 
        elite = GA.elitism(population)

        for ind_elite in range(configs.NUM_ELITE):
            birds[ind_elite].transform_gene_to_weight(elite[ind_elite].get_gene())

        selected_individual = GA.roulette_wheel_selection(population)
        
        random.shuffle(selected_individual)

        pairs = [selected_individual[i:i+2] for i in range(0, len(selected_individual), 2)]

        count_cross = 0
        for indvidual_1, indvidual_2 in pairs:
            new_gene_1, new_gene_2 = GA.single_point_crossover(indvidual_1.get_gene(), indvidual_2.get_gene())
            new_gene_1 = GA.mutation(new_gene_1)
            new_gene_2 = GA.mutation(new_gene_2)

            birds[configs.NUM_ELITE + count_cross].transform_gene_to_weight(new_gene_1)
            birds[configs.NUM_ELITE + count_cross + 1].transform_gene_to_weight(new_gene_2)

            count_cross += 2

    running = True
    gameover = False
    gamestarted = False

    if generation > 0:
        game_start_message.kill()
        pygame.time.set_timer(column_create_event, 1500)
        pygame.time.set_timer(model_inference_event, 250)
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
                    bird.infer_event(bird.rect.x, bird.rect.y, obs_x, obs_y+t_h, obs_y+t_h+g, obs_x+52)
                

        screen.fill(0)

        sprites.draw(screen)

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
            if bird.still_alive:
                pygame.draw.line(screen, (255,0,0), (bird.rect.x, bird.rect.y), (obs_x, obs_y+t_h))
                pygame.draw.line(screen, (255,0,0), (bird.rect.x, bird.rect.y), (obs_x, obs_y+t_h+g))

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
    
    generation_dict = dict()
    print("="*10 + f"{generation}" + "="*10)
    for bird in birds:
        generation_dict[bird.name] = bird
    gene_pool[generation] = generation_dict

pygame.quit()
