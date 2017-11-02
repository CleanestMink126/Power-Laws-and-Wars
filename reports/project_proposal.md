# Agent-Based Simulation of Wars and State Formation
## Nick Steelman and Seungin Lyu

### Abstract



### Replication and Extension Plans

Questions:
- forest fires models : too many mechanism level differences between forest fires and state formation, but "key to any explanation of war sizes depends on how wars spread"

Methodology:
GeoSim - Transitions baetween equilbria
- Cumulative relative frequencies of war sizes(cumulative frequency as a function of the severity s of interstate wars)
- Sand Pile steram -> process of technological change, Avalanches : chains of war decisions triggered by context activation
- Model
    - 50*50 square lattice, 200 composite state-like agents
    - Interactions take place in a dynamic network (not directly in the lattice)
    - half of resources go to front, half gets distributed proportional to neighbohrs' power
    - Grim-trigger strategy (normal - reciprocate neighbors's actions, unprovoked attacks as soon as in a sufficiently superior situation)
    - Contextual activation - increased alertness to geopolitical cahnges in case of conflict in a state's immediate neighborhood
    - The victor absortbs targeted unit(if capital, complete collapse)
    - Capitals "tax" provinces
    - Advancements in technology is modeled by shifting the tax threshold to the right(capital extracts more tax from distant provinces)

Expected Results:
- Lines : borders, dots : capitals
- Identify conflict clusters (spatiotemporal cluster-finding algorithm, distinguished btween active and inactive states)
- then measure severity(total battle damage incurred by all parties to a confilct cluster)
-



Extension Plans
- Predict the status of an actual region in the world! Run the simulation and see what happens

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
