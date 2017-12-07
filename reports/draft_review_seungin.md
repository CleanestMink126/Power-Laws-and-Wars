1. Question :
      * I believe the question you are asking is : <i>"We want to see whether it is better for the community as a whole for each router to only connect to a single other router that has access--in theory decreasing the number of routers connected through any one given router--or to connect to any router with access in range--increasing the number of connected routers for any other router, but also distributing the work routed through any access point."</i>. I definetely do understand the question, but it took me a while to parse the question when I read it the first time. Perhaps this sentence can be shortened a bit.

      * <i>"..Through this model, they begin to analyze what factors contribute to the system being more likely to end in a state of high performance, where most packets are successfully transmitted."</i>. I would find a short summary of their analysis results helpful for understanding the overall context of this report.

      * As a reader being introduced to "mesh network" for the first time, I expected a little more background (2~3 sentences) explaining the definition of mesh network. I found the following description : <i>"..where super-routers service an area of routers, and those routers in turn provide wifi to others.""</i>, but then I was again curious, "what's the key difference between a normal router and a super-router?"

2. Methodology:
      * The model configuration is well explained and the list of steps of the model is detailed. Though, I was curious what threshold value was used to define "too much latency".
      * How is the range of each router defined? Are they randomly assigned or are they given a uniform value?
      * I didn't get why <i>"If it is connected to a super-router, A is 0."</i> Is this a simplification you made just for this model? or is this actually a thing?

3. Results
      * For the coverage plot(Figure 2), wouldn't it be more intersting to experiment with differnt parameters (time stpes, initial condition) and provide a plot of the coverage(percentage) instead of providing a single snapshot?
      * Figure 1 is only one instance of the comparison between single-connection graph and multi-connection graph. I would be more convinced if there was a plot that contained multiple instances of such comparison (again with different initial conditions)
4. Interpretation:
      * The captions of each figures only contain the 'title' of the figure. One of two sentences guiding the reader where to look would be really helpful.
5. Replication:
      * There isn't a direct subject for replication since this is a new model inspired by the original paper.

6. Extension:
      * This entire report is more of an extension of the original paper.

7. Progress:
      * I see that the implementation of the model is complete and the paper is mostly done.
