# Effects of Defectors on Greedy Routing in Complex Networks
### Nick Steelman, Matt Brucker


### Abstract

Lewis Richardson, in his post-WWII paper analyses the frequency and severity of human conflict. [3]
He finds that the severity of all wars follows a power law distribution. Almost 50 years later, the exact reasons and principals behind this are still not well understood or explained with methods relying on equilibrium based model (Cederman).
Cederman tackles the problem with an agent based model in an attempt to recreate the power law distribution first observed by Richardson [1].
We replicate this model in Python. We extend the ori by simulating it based on real world data and by adding in more complex and realistic actions such as the conecept of alliance to the agents.


### Replication and Extension
Richardson in 1945, reported that the severity of all wars follows a power law distribution [3]. We find only a few occasions when scholars attempted to explain why.
To answer these questions, Cederman designed an agent-based model called GeoSim that illustrates the transitions between equilbria in wars and state formations.
By running simulations with his model, he replicates the plot Richardson generated almost 70 years ago. While one of the previous studies proposed a forest fire model [2], Cederman believed
that the forest fire model of wars has too many mechanism level differences compared to the processes of real world state formation and wars but agreed that the "key to any explanation
of war sizes depends on how wars spread". [1]

By replicating the GeoSim model Cederman proposed with python, we seek to find answer for the following questions : why are casualty levels of wars power-law distributed? how do wars start and spread?
GeoSim model consists of state-like agents on a square lattice. It illustrates the transitions between equilbria. The model draws an analogy which maps the process of technological change to the sand pile stream and maps the chains of war decisions triggered by context activation to Avalanches.
Contextual activation means increased alertness to geopolitical changes in case of conflict in a state's immediate neightborhood. Capitals can "tax" provinces and advancements in technology is modeled by shifting the tax threshold so that capital extracts more tax from distant provinces.

We plan to extend the model by adding in the concept of alliances that the model lacks. Another path we are considering is to predict the status of a power map of an actual region
in the world and observe if any interesting results come out.ed

### Interpreting Results

The figures below show the distribution of wars on a log-log scale with frequency and severity form both the original paper and an updated version through 1997. We can validate our replicated model against these results showing that its distribution of wars behaves the same way.

<p align="center">
 <img src="../resources/1-2.svg" width=1000px height=500px ></img>
</p>

The figures below show the validation from the Cederman paper along with a graphic of the states where the lines represent borders and the dots represent capitals. We should have a graphics similar to both below to show that our model produces a power law and our states seem qualitatively similar to those represented in the paper.

<p align="center">
 <img src="../resources/3-4.svg" width=750px height=300px ></img>
</p>

### Causes For Concern
The author of the agent based approach article very clearly outlines his framework with any parameters he uses, even including pseudocode. But, everything was written, in the Java-base toolkit Repast, which we are obviously not using. So either finding an effective toolkit for geographical modeling, or coding all the state simulation functions ourselves poses a significant hurdle in implementation. Additionally, even with all the pre-defined parameters, the model will inevitably require some fine tuning due to its high number of dials, so it may be difficult to tell if our model is not working because of a value that we set or because of something wrong with our code.
visualization

### Next Steps

First we should review the appendix of the paper which contains all of the implementation information for the project. Once we are appropriately acclimated with the working part we should work on implementation. At this point we should decide whether to implement the environment ourselves or go with a toolbox. Either way, we will have a lot of work to do in setting up the environment to let the states tax and battle. By the end of the first week we should at least be to the point where we can define states and capitals in a program that can interact and tax. Ideally we will be to the point where the states are battling and we can move to setting up the simulation.



#### Impact of System Parameters


#### Previous Results


### Annotated Bibliography

#### 1. Modeling the size of wars : from billard balls to sandpiles

Cederman, L. E. (2003). Modeling the size of wars: from billiard balls to sandpiles. American Political Science Review, 97(1), 135-150.

To answer why the casualty levels of wars are power-law distributed as shown in Richardson's discovery, Cederman proposed an agent-based model of war and state formation called GeoSim that replicates the empirically expected power-law distribution. He agrees that previous models that utilize the characterstic of SOC(sand-pile, forest-fire model) do explain how wars spread, but he points out that those results do not necesarily explain how wars are initiated. His model consists of state-like agents that either fight against neighbors or don't fight over allocated resources. He concludes that technological changes contribute to the decisions to wage war and that the scale-free behavior of wars depend on them.

#### 2. Fractality and Self-Organized Criticality of Wars

Roberts, D. C., and D. L. Turcotte. “Fractality and Self-Organized Criticality of Wars.” Fractals, vol. 06, no. 04, 1998, pp. 351–357., doi:10.1142/s0218348x98000407.

Roberts and Turcotte use the forest fire model to explain the power-law distribution of intensities of wars. They find there is a fractal dependence of number on intensity in which intensity is measured in terms of battle deaths. They extend the ignition of fire to the outbreak for as well as its spread. The "avalanches" in this paper are the eruptions of war that they say follow a fractal frequency-size distribution.

#### 3. Variation of the Frequency of Fatal Quarrels With Magnitude

Richardson, Lewis F. "Variation of the frequency of fatal quarrels with magnitude." Journal of the American Statistical Association 43.244 (1948): 523-546.

Richardson analyzes wars from 1820 to 1945 by classfying them according to the number of dead people. He find that that the frequency of wars with higher intensity follows a power-law distribution.
