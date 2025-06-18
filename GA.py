import configs
import numpy as np
import random
import torch
import heapq

def roulette_wheel_selection(population):
    # Computes the totallity of the population fitness
    population_fitness = sum([bird.get_fitness() for bird in population])
    # Computes for each chromosome the probability
    chromosome_probabilities = [bird.get_fitness() /
                                population_fitness for bird in population]
    index_only = list(range(configs.NUM_INDIVIDUAL))
    # Selects one chromosome based on the computed probabilities
    selected_indices = np.random.choice(
        index_only, size=configs.NUM_CROSSOVER, p=chromosome_probabilities, replace=False)
    return [population[i] for i in selected_indices]


def mutation(chromosome_tensor: torch.Tensor):
    new_chromosome = []
    chromosome = chromosome_tensor.tolist()
    for gene in chromosome:
        if random.random() <= configs.MUTATION_RATE:
            # Apply Gaussian mutation
            mutated_gene = np.random.normal(loc=gene, scale=configs.MUTATION_STD)
            new_chromosome.append(mutated_gene)
        else:
            new_chromosome.append(gene)
    return torch.tensor(new_chromosome)

def single_point_crossover(chromosome_1: torch.Tensor, chromosome_2: torch.Tensor):
    total_lenght = (configs.IN_DIM * configs.HIDDEN_1) + (configs.HIDDEN_1 * configs.OUT_DIM)
    half_point = total_lenght // 2
    split = random.randint(half_point-5, half_point+5)

    frac_p1_back = chromosome_1[split:]
    frac_p2_front = chromosome_2[:split]
    frac_p1_front = chromosome_1[:split]
    frac_p2_back = chromosome_2[split:]

    new_chromosome_1 = torch.concat([frac_p1_front, frac_p2_back])
    new_chromosome_2 = torch.concat([frac_p2_front, frac_p1_back])

    return new_chromosome_1, new_chromosome_2

def layer_wise_crossover(chromosome_1: torch.Tensor, chromosome_2: torch.Tensor):
    split_layer = configs.IN_DIM * configs.HIDDEN_1
    
    input_gene_1 = chromosome_1[:split_layer]
    hidden_gene_1 = chromosome_1[split_layer:]
    input_gene_2 = chromosome_2[:split_layer] 
    hidden_gene_2 = chromosome_2[split_layer:]

    new_chromosome_1 = torch.concat([input_gene_1, hidden_gene_2])
    new_chromosome_2 = torch.concat([input_gene_2, hidden_gene_1])

    return new_chromosome_1, new_chromosome_2


def elitism(population):
    fitness_list = [bird.get_fitness() for bird in population]
    max_val = heapq.nlargest(configs.NUM_ELITE, fitness_list)
    max_ind = [fitness_list.index(i) for i in max_val]
    elite = [population[ind] for ind in max_ind]
    
    return elite


