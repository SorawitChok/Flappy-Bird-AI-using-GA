import pygame.sprite
import torch
import assets
import configs
from layer import Layer
from objects.column import Column
from objects.floor import Floor
from model import FlappyBirdModel
import numpy as np


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, name, *groups):
        self._layer = Layer.PLAYER

        self.images = [
            assets.get_sprite("redbird-upflap"),
            assets.get_sprite("redbird-midflap"),
            assets.get_sprite("redbird-downflap")
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.mask = pygame.mask.from_surface(self.image)

        self.flap = 0

        self.name = name

        self.model = FlappyBirdModel(configs.IN_DIM, configs.HIDDEN_1, configs.OUT_DIM)

        self.score = 0

        self.alive_time = 0

        self.still_alive = True

        super().__init__(*groups)

    def update(self):
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]

        self.flap += configs.GRAVITY
        self.rect.y += self.flap

        self.alive_time += 1

        if self.rect.x < 50:
            self.rect.x += 3

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.flap = 0
            self.flap -= 6
            assets.play_audio("wing")

    def check_collision(self, sprites):
        for sprite in sprites:
            if ((type(sprite) is Column or type(sprite) is Floor) and sprite.mask.overlap(self.mask, (
                    self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)) or
                    self.rect.bottom < 0):
                return True
        return False
    
    def increase_score(self):
        self.score += 1

    def get_fitness(self):
        return self.score + self.alive_time / 1000

    def infer_event(self, bird_x, bird_y, obstacle_x, obstacle_y_top, obstacle_y_bottom, obstacle_x_end, y_velocity):
        self.model.eval()
        with torch.no_grad():
            output = self.model(torch.tensor(np.array([bird_x, bird_y, obstacle_x, obstacle_y_top, obstacle_y_bottom, obstacle_x_end, y_velocity]), dtype=torch.float32))

        if output >= configs.THRESHOLD:
            self.flap = 0
            self.flap -= 6
    
    def get_gene(self):
        return torch.concat([self.model.layer_1.weight.flatten(), self.model.layer_2.weight.flatten()])
    
    def transform_gene_to_weight(self, gene: torch.Tensor):
        in_dim, hidden_dim, out_dim = configs.IN_DIM, configs.HIDDEN_1, configs.OUT_DIM
        layer1_weight = gene[:in_dim*hidden_dim].reshape((hidden_dim, in_dim))
        layer2_weight = gene[in_dim*hidden_dim:].reshape((out_dim, hidden_dim))
        with torch.no_grad():
            self.model.layer_1.weight = torch.nn.Parameter(layer1_weight)
            self.model.layer_2.weight = torch.nn.Parameter(layer2_weight)

