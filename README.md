# Build an AI to Play Flappy Bird using Pytorch and Genetic Algorithm

In this repository, we develop an AI that outperforms the average human at Flappy Bird by leveraging the artificial neural network (ANN) architecture created with PyTorch and training it using Genetic Algorithm (GA) [[1]](#references). This evolutionary approach mimics the principle of natural selection coined by Charles Darwin [[2]](#references), making our AI learn and adapt to the environment with uncertainty and randomness, just like a species does in nature. This repository will guide you through several fascinating mechanisms and algorithms behind this process, including genetic crossover, mutation, and elitism (Survival of the fittest).

> This repository was developed based on the [Flappy Bird Game](https://github.com/mehmetemineker/flappy-bird), which is the github repository that create a clone of the Flappy Bird game using Pygame library.

## Table of Contents

- [Introduction](#introduction)
- [Game Objectives](#game-objectives)
- [From Objectives to Model Design](#from-objectives-to-model-design)
- [Genetic Algorithm](#genetic-algorithm)
  - [Initial Population](#initial-population)
  - [Fitness Function](#fitness-function)
  - [Selection](#selection)
  - [Genetic Operators](#genetic-operators)
  - [Termination](#termination)
- [Setup](#setup)
- [References](#references)
- [License](#License)
- [Citation](#citation)
- [Contributing](#Contributing)
- [Authors](#Authors)

## Introduction

Flappy Bird was one of the most popular and well-known mobile games a decade ago. It was first introduced in 2013 by Vietnamese programmer Dong Nguyen, the same year that Apple announced the colourful iPhone 5C. This game features late 90s style arcade art with a yellow pixelate bird that the player needs to control and navigate through the small opening between the green Mario-like pipe to get a score. The ultimate aim of people playing this game is to apparently get higher scores than their peers and pals, making this game competitive and somewhat addictive.

## Game Objectives

- **Goal**: Navigate the bird through an endless series of pipes by controlling its vertical movement.
- **Score Mechanism**:
  - +1 point for each pair of pipes successfully passed.
- **Control**:
  - The bird flaps upward each time the player (or AI agent) triggers a flap.
  - Gravity continuously pulls the bird downward.
- **Terminate Conditions**:
  - The bird collides with a pipe (obstacle).
  - The bird falls to the ground (touches the floor).
- **Challenge**:
  - Requires precise timing and coordination to pass through narrow gaps between pipes.
  - Speed and pipe positioning vary to increase difficulty over time.

## From Objectives to Model Design

## Genetic Algorithm

### Initial Population

### Fitness Function

### Selection

```python
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
```

```python
def elitism(population):
    fitness_list = [bird.get_fitness() for bird in population]
    max_val = heapq.nlargest(configs.NUM_ELITE, fitness_list)
    max_ind = [fitness_list.index(i) for i in max_val]
    elite = [population[ind] for ind in max_ind]

    return elite
```

### Genetic Operators

**Crossover**

```python
def layer_wise_crossover(chromosome_1: torch.Tensor, chromosome_2: torch.Tensor):
    split_layer = configs.IN_DIM * configs.HIDDEN_1

    input_gene_1 = chromosome_1[:split_layer]
    hidden_gene_1 = chromosome_1[split_layer:]
    input_gene_2 = chromosome_2[:split_layer]
    hidden_gene_2 = chromosome_2[split_layer:]

    new_chromosome_1 = torch.concat([input_gene_1, hidden_gene_2])
    new_chromosome_2 = torch.concat([input_gene_2, hidden_gene_1])

    return new_chromosome_1, new_chromosome_2
```

**Mutation**

```python
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
```

### Termination

## Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.9+

### Installation

1. **Clone the repository:**

```
git clone https://github.com/SorawitChok/Flappy-Bird-AI-using-GA.git
```

2. **Create virtual environment:**

```
python -m venv env
source env/bin/activate  # Linux/Mac
env/Scripts/activate  # Windows
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

### Running the GA Training

After installation, you can run the training script as follows:

```
python main.py
```

### Running the Demo

You can also test the trained agent on the real game by running the following script:

```
python demo.py
```

Don't forget to change the model path to load your desired model weights version.

## References

[1] Holland, J. H. (1992). [Genetic algorithms](https://www.jstor.org/stable/24939139). Scientific american, 267(1), 66-73

[2] Darwin, C. (1861). [On the origin of species by means of natural selection, or, the preservation of favoured races in the struggle for life](https://books.google.co.th/books?hl=en&lr=&id=AEC20ISHJkQC&oi=fnd&pg=PR13&dq=On+the+Origin+of+Species+by+Means+of+Natural+Selection,+Or,+The+Preservation+of+Favoured+Races+in+the+Struggle+for+Life&ots=nqU5awrT1d&sig=eBtjWMoZnqlvrV3JyYrxoWbdGq0&redir_esc=y#v=onepage&q=On%20the%20Origin%20of%20Species%20by%20Means%20of%20Natural%20Selection%2C%20Or%2C%20The%20Preservation%20of%20Favoured%20Races%20in%20the%20Struggle%20for%20Life&f=false). _J. Murray_.

## License

This code is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Citation

## Contibuting

Feel free to fork this repository and submit pull requests. Any contributions are welcome!

## Authors

This repository was created by [Sorawit Chokphantavee](https://github.com/SorawitChok) and [Sirawit Chokphantavee](https://github.com/SirawitC).
