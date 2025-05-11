# SCVXController

Controller Implementation and source code for successive convex trajectory optimization of a drone landing. The drone will feature a thrust vector controlled motor/propeller and will use an onboard flight computer to minimize the energy required to land the drone at a chosen landing spot. 

The manufacturing and creation of the drone and its flight controller will be created by me. However, the optimal trajectory generation code is not my own. I have made some small changes to [SCVx](https://github.com/EmbersArc/SCvx?tab=readme-ov-file) for the trajectory generation to work on my home computers. As the project progresses, I hope to document each phase of the drone's creation and operation to this page.

As of 5/10, I am working on developing a thrust vector control system for the drone. As a proof of functionality, I will likely combine a camera to track an object with the thrust vector control system. This should also be useful should I decide to have a descent camera aiding in the state estimation of the drone for trajectory generation and/or helping determine the real trajectory of the drone during landing.
