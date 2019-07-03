# Intelligent-Pathfinding
This repository attempts to solve the problem of pathfinding and route planning, using Artificial Intelligence algorithms

#### Algorithm A* 
#### Genetic Algorithm
<br>

## Author
You can get in touch with me on <a class="btn-linkedin" href="https://www.linkedin.com/in/ibrahim-zfr/">LinkedIn</a>!

If you liked my repository, kindly support my work by giving it a ⭐! <br>
<br>

## About this Repository

Algorithm A* and Genetic Algorithm were used to solve the problem of dymanic route planning for an abmulance. <br>
As such, this repository will contain terms such as 'patients' and 'ambulance' etc. <br>


The grid size is 200 x 400 by default. Area equivalent to 0.5% of the total area in the grid is bloacked, randomly. 
The starting position of the ambulance and the location of the patients on the grid is also randomly initialized. 

<br>

## Algorithm A * 
The cost function for the A* algotihm is as given. 
``` 
F(n) = G(n) + H(n) 
```
where G(n) represents the cost on travelling upto this node, and
H(n) represents the estimated cost from current node to the goal node/patient location.

<br>

The optimal route for the ambulance that has to tend to 20 patients, as given by the A* algorithm is:

![alt text](https://github.com/ibrahimzafar/Intelligent-Pathfinding/blob/master/A_star_output.png "Algorithm A* ") 

<br>


## Genetic Algorithm 
This is the biologically inspired process of finding solutions to problems. Every solution is a "chromosome". All the "chromosomes" from a fixed population size, compete with each other and those with the highest fitness, are selected to create offspring (1-point and 2-point crossovers), mutate, and are sometimes passed on to the next generation of competing chromosomes as is(elitism). 

<br>

The chromosome for the A* algorithm (length 5) is as given. 
``` 
[start] - [intermediate] - [intermediate] - [intermediate] - [goal]
```
<br>

The grid is 200x400, and as such, the complete path taken by the ambulance cannot fit in the chromosome. 
The chromosome contains 3 intermediate points, randomly initialized, and there exists a direct straight line path between any 2 nodes. 
An n length chromosome has a path of n-1 lines, taking the ambulance from starting position to its goal position (5 length chromosome has 4 lines). 

<br>

The crossovers are biologically inspired by chromosomal crossovers, as shown in image. 
![alt text](https://banner2.kisspng.com/20180808/xrl/kisspng-genetics-mutation-genome-chromosomal-crossover-chr-how-do-you-map-a-genome-facts-yourgenome-org-5b6a92c3109fa1.0640223915337110430681.jpg "Chromosomal Crossover") 
Picture taken from: https://www.kisspng.com/png-genetics-mutation-genome-chromosomal-crossover-chr-6214158/

<br>

The algorithm runs for 200 iterations in which solutions("chromosomes") of a certian population size go through crossover and mutation. 
Initial fitness is set to an arbitrary value of 50000, and fitness is reduced by an exponential function of distance and blocked nodes that come in the chromosome's path. 

The fitness function is:
```
fitness = 50000 - (distances ** 2) - (100000 ** blocks)
```
<br>

The optimal route for the ambulance that has to tend to 20 patients, as given by the A* algorithm is:

![alt text](https://github.com/ibrahimzafar/Intelligent-Pathfinding/blob/master/A_star_output.png "Algorithm A* ") 

<br>


## Contributions are Welcome!
Feel free to improves the code by generating a pull request!<br>

<br>


## License
[MIT License](https://github.com/ibrahimzafar/Intelligent-Pathfinding/blob/master/LICENSE)



