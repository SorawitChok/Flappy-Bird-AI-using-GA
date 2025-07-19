# Build an AI to Play Flappy Bird using Pytorch and Genetic Algorithm

In this repository, we develop an AI that outperforms the average human at Flappy Bird by leveraging the artificial neural network (ANN) architecture created with PyTorch and training it using Genetic Algorithm (GA) [[1]](#references). This evolutionary approach mimics the principle of natural selection coined by Charles Darwin [[2]](#references), making our AI learn and adapt to the environment with uncertainty and randomness, just like a species does in nature. This repository will guide you through several fascinating mechanisms and algorithms behind this process, including genetic crossover, mutation, and elitism (Survival of the fittest).

> This repository was developed based on the [Flappy Bird Game](https://github.com/mehmetemineker/flappy-bird), which is the github repository that create a clone of the Flappy Bird game using Pygame library.

## Table of Contents

- [Introduction](#introduction)
- [Game Objectives](#game-objectives)
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

## Genetic Algorithm

### Initial Population

### Fitness Function

### Selection

### Genetic Operators

### Termination

## Setup

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
