import neat
import pickle
from FlappyBird.Bird import Bird
from FlappyBird.Pipe import Pipe
import pygame

genomeFile = './bestGenomes/2_732.p' #CHANGE ME
FPS = 200
SCREENWIDTH = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE = 180  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79
SCORE = 0

BACKGROUND = pygame.image.load('./assets/bg.png')

GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0


def game(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    global SCORE

    bird = Bird(DISPLAY, SCREENWIDTH, SCREENHEIGHT)
    pipe1 = Pipe(DISPLAY, SCREENWIDTH + 100, PIPEGAPSIZE, SCREENWIDTH)
    pipe2 = Pipe(DISPLAY, SCREENWIDTH + 100 + (SCREENWIDTH / 2), PIPEGAPSIZE, SCREENWIDTH)

    pipeGroup = pygame.sprite.Group()
    pipeGroup.add(pipe1.upperBlock)
    pipeGroup.add(pipe2.upperBlock)
    pipeGroup.add(pipe1.lowerBlock)
    pipeGroup.add(pipe2.lowerBlock)

    # birdGroup = pygame.sprite.Group()
    # birdGroup.add(bird1)

    moved = False

    time = 0

    while True:

        DISPLAY.blit(BACKGROUND, (0, 0))

        if (pipe1.x < pipe2.x and pipe1.behindBird == 0) or (pipe2.x < pipe1.x and pipe2.behindBird == 1):
            input = (bird.y, pipe1.x, pipe1.upperY, pipe1.lowerY)
            centerY = (pipe1.upperY + pipe1.lowerY) / 2
        elif (pipe1.x < pipe2.x and pipe1.behindBird == 1) or (pipe2.x < pipe1.x and pipe2.behindBird == 0):
            input = (bird.y, pipe2.x, pipe2.upperY, pipe2.lowerY)
            centerY = (pipe2.upperY + pipe2.lowerY) / 2

        # print(input)
        vertDist = (((bird.y - centerY) ** 2) * 100) / (512 * 512)
        time += 1

        fitness = SCORE - vertDist + (time / 10.0)

        t = pygame.sprite.spritecollideany(bird, pipeGroup)

        if t != None or (bird.y == 512 - bird.height) or (bird.y == 0):
            return (fitness)

        output = net.activate(input)

        # for event in pygame.event.get():
        # 	if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        # 		pygame.quit()
        # 		sys.exit()

        if output[0] >= 0.5:
            bird.move("UP")
            moved = True

        if moved == False:
            bird.move(None)
        else:
            moved = False

        pipe1Pos = pipe1.move()
        if pipe1Pos[0] <= int(SCREENWIDTH * 0.2):
            if pipe1.behindBird == 0:
                pipe1.behindBird = 1
                SCORE += 10
            # print("SCORE IS %d"%(SCORE+vertDist))

        pipe2Pos = pipe2.move()
        if pipe2Pos[0] <= int(SCREENWIDTH * 0.2):
            if pipe2.behindBird == 0:
                pipe2.behindBird = 1
                SCORE += 10
            # print("SCORE IS %d"%(SCORE+vertDist))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def eval_genomes(genomes, config):
    i = 0
    global SCORE
    global GENERATION, MAX_FITNESS, BEST_GENOME

    GENERATION += 1
    for genome_id, genome in genomes:

        genome.fitness = game(genome, config)
        print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f" % (GENERATION, i, genome.fitness, MAX_FITNESS))
        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
        SCORE = 0
        i += 1


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config')

genome = pickle.load(open(genomeFile, 'rb'))

fitnessScores = []

for i in range(10):
    fitness = game(genome, config)
    SCORE = 0
    print('Fitness is %f' % fitness)
    fitnessScores.append(fitness)
