
import random
import operator

boardSize = 24
maxP = int(boardSize * ((boardSize - 1) / 2))
mutationChance = 0.08
mutationFactor = 0.6
numOfIndividuals = 1000
killPrecentage = 0.75
strictMating = True

class Population:
    def __init__(self, numOfIndividuals):
        self.indviduals = sorted(self.generateIndviduals(numOfIndividuals), key=operator.attrgetter("points"))
        self.bestIndividual = self.indviduals[len(self.indviduals) - 1]
        self.generation = 0

    
    def generateIndviduals(self, num):
        population = []
        for _ in range(num):
            population.append(Individual())
        return population

    def kill(self, precentage):
        self.indviduals = self.indviduals[int(len(self.indviduals)*precentage):]

    def reproducePopulation(self):
        newPopulation = []
        for i in range(numOfIndividuals): 
            parent1 = self.indviduals[random.randint(0, len(self.indviduals) - 1 )]               
            parent2 = self.indviduals[random.randint(0, len(self.indviduals) - 1 )]  
            while(parent2 in parent1.banedPartners and strictMating):
                parent1 = self.indviduals[random.randint(0, len(self.indviduals) - 1 )]             
                parent2 = self.indviduals[random.randint(0, len(self.indviduals) - 1 )] 
            child = parent1.reproduce(parent2)
            newPopulation.append(child)
        self.generation += 1
        self.indviduals = newPopulation
        self.indviduals = sorted(self.indviduals, key=operator.attrgetter("points"))
        self.bestIndividual = self.indviduals[len(self.indviduals) - 1]
        
    def getPointArr(self):
        points = []
        for indiv in self.indviduals:
            points.append(indiv.points)
        return points

class Individual:
    def __init__(self, genetics = None):
        if(genetics != None):
            queenLocations = genetics
        else:
            queenLocations = self.generateQueens()
        self.queenLocations = queenLocations
        self.tryToMutate()
        self.points = self.fitnessPoints()
        self.banedPartners = [self]
    
    def __str__(self):
        return str(self.queenLocations)

    def generateQueens(self):
        queens = []
        for _ in range(boardSize):
            queens.append(random.randint(0, boardSize - 1))
        return queens

    def fitnessPoints(self):
        points = maxP
        for i in range(len(self.queenLocations)):
            q = self.queenLocations[i]
            for c in range(i + 1, len(self.queenLocations)): 
                q2 = self.queenLocations[c]
                if(abs(q2 - q) is c - i):
                    points = points - 1
                if(q2 is q):
                    points = points - 1
        return points

    def reproduce(self, otherParent):
        invidLen = len(self.queenLocations)
        randCut = random.randint(0, invidLen-1)
        genetics = self.queenLocations
        if(randCut % 2 is 0):
            genetics = genetics[:randCut] + otherParent.queenLocations[randCut:]
        else:
            genetics = genetics[randCut:] + otherParent.queenLocations[:randCut]
        self.banedPartners.append(otherParent)
        otherParent.banedPartners.append(self)
        return Individual(genetics)

    def tryToMutate(self):
        if(random.randint(0, 100) <= mutationChance * 100):
            invidLen = len(self.queenLocations)
            numOfMutations = int(invidLen * mutationFactor)
            for _ in range(numOfMutations):
                self.queenLocations[random.randint(0, invidLen - 1)] = random.randint(0, invidLen - 1)

def geneticAlgorithm(population):

    while(True):

        bestIndividual = population.bestIndividual

        print(f"Generation: {population.generation} has the best child: { bestIndividual.queenLocations} with points {bestIndividual.points} of {maxP}")

        if(bestIndividual.points is maxP):
            print(bestIndividual.queenLocations)
            break

        global killPrecentage    

        population.kill(killPrecentage)
        population.reproducePopulation()

        #if(population.generation == 300):
            #if(killPrecentage < 1):
             #   killPrecentage += 0.1
         #   population = Population(numOfIndividuals)

geneticAlgorithm(Population(numOfIndividuals))