---
typora-root-url: ./README WriteUp.md
---

# PROJECT 3 - CONTROLS

In this project we get to investigate and recreate the control systems that enable our drones to fly from one position to another in our previous simulations. To accomplish this, we will be implementing a cascaded PID controller as detailed below.

The first step is to get our IDE working and compiling C++ code as C++ is the standard when working with flight controllers, such as the PX 4. 

### OS X ###

For Mac OS X, the recommended IDE is XCode, which you can get via the App Store.

1. Download and install XCode from the App Store if you don't already have it installed.
2. Open the project from the `<simulator>/project` directory.
3. After opening project, you need to set the working directory:
  1. Go to *(Project Name)* | *Edit Scheme*
  2. In new window, under *Run/Debug* on left side, under the *Options* tab, set Working Directory to `$PROJECT_DIR` and check ‘use custom working directory’.
  3. Compile and run the project. You should see a single quadcopter, falling down.

Tips: For those working on older laptops still running mac OS' as old as 10.11.6 (El Capitan, circa 2010), it is still possible to work with Xcode as an IDE for this project, but two significant adjustments must be made. Without these changes, it may not be possible to compile.

![](/../images/OldLapTops.png)



Most of the code is to be written in **src/QuadControl.cpp**. However, most of my time spent interating was spent in another document altogether, namely  **QuadControlParams.txt.**


### SCENARIO 1 ###

Watching the seed project compile error free is an excitement which is quickly dashed as our simulator starts up and we see our virtual drone plummet repeatedly crashing to the ground. 

Thus the first step is to adjust the mass of our drone in **QuadControlParams.txt** until we achieve a near hover. This scenario highlights how significantly mass will affect our calculations. One of the most difficult scenarios will occur later when we try to work with non-ideal drones. There are many threads on RC forums dedicated to propellor balancing, an obsession I never fully understood until studying this course. Later in scenario **4_NonIdealities**, we will start to see why such detailed attention and the quest for balance is more then just an rc geek pastime. 

With some tuning we eventually arrive at a *Mass = 0.5*:

![](/Users/admin/miniconda3/UDACITY/P3_Controls/FCND-Controls-CPP/WriteUp/images/1_Intro-Pass.png)

## The Tasks ##

For this project, you will be building a controller in C++.  You will be implementing and tuning this controller in several steps.

You may find it helpful to consult the [Python controller code](https://github.com/udacity/FCND-Controls/blob/solution/controller.py) as a reference when you build out this controller in C++.

1. **Parameter Ranges**: You can find the vehicle's control parameters in a file called `QuadControlParams.txt`. The default values for these parameters are all too small by a factor of somewhere between about 2X and 4X. So if a parameter has a starting value of 12, it will likely have a value somewhere between 24 and 48 once it's properly tuned.

2. **Parameter Ratios**: In this [one-page document](https://www.overleaf.com/read/bgrkghpggnyc#/61023787/) you can find a derivation of the ratio of velocity proportional gain to position proportional gain for a critically damped double integrator system. The ratio of `kpV / kpP` should be 4.

### Scenario 2 ###

For this portion we will be implementing a cascaded PID controller as seen below:

![](/../images/PID_Cascaded_ControlArchitecture.png)

Here we implement body rate and roll / pitch control. To do this we need to implment the following equations:

```
thurst = mass * CONST_GRAVITY
```

![](/../images/taoTotal.png)

Where:

![](/../images/Ftotal.png)

From these equations we see the significance of the drone's arm length (l) in determining Mx. 

![](/../images/Length_L.png)

Our drone model is an X frame where we can infer symmetry. But other models do exist, such as the H - frame that is popular in drone racing. Below left we see the Drone Racing Leagues version 2.0 model. On the right we see the 2019 Drone Racing League model 3.0. If diagonal symmetry is broken along an axis, such as we see in the H - model, what effect does that have on performance and PID tuning? Although this isn't a scenario we can explore given our simulation drone is a fixed X model, it is a point worthy of consideration.

![](/../images/on-the-left-the-racer2-on-the-right-the-racer3.jpeg)

​														- image: Drone Racing League, 2019

After Implementation but prior to our tuning efforts we see that we are getting some overshoot. It is suggested we tune our inner control loops first as the inner loops affect the outer loops.
After some extensive tuning, we are able to halt our drone's continual perishing plunge downwards. P's usable range seemed quite high. Looking for the envelopes of usable flight for P we observe:![](/../images/Scenario2_ThreePositions_P-10_100_300.png)

**P = 10**
![](/../images/Scenario_2_P-10.png)

**P = 100**
![](/../images/Scenario_2_P-100.png)

**P = 300**
![](/../images/Scenario_2_P-300.png)

With the goal of a happy median between the acute trajectories bounded by **P [10:300]**, we finally settle on **P= 100** which causes the drone to fly up in a roughly vertical direction as seen in the middle slate. It should be noted that the range **P** **[10:338]** is upper bound exclusive in this notation and **338** marks the threshold for P which, if input, causes the drone to tumble to the ground.

### SCENARIO 3 ###

Here we have two identical quads, but with different intial Yaw settings (0, 45 degrees). It is up to us to implement the LateralPositionControl, AltitudeControl and Yaw control, noting that the Yaw control is a first order system. During the process of tuning we see some unusual behaviour.
As P increases upwards of 300, we see the drone flying towards camera left. Lower near zero values send it shooting off camera right. Again we aim for something reasonable and choose to keep P = 100, which  now has a slight favored bias derived from our Scenario 2's tuning experience. Next we turn to our Q parameter. 

Normally we would just tune Q to "Pass", Q = 100 would be sufficient here. However, with Sim(t) = 4 seconds, tuning to find the bounds of the parameter Q reveals an interesting possible discontinuity or inflection point surrounding Q = 600 as shown below:

**Q = 100** : Both drones fly.
![](/../images/Scenario_3_Q-100.png)

**Q= 600** : Both drones crash.
![](/../images/Scenario_3_Q-600.png)

**Q = 700** : One flutters and then survives. The other crashes.
![](/../images/Scenario_3_Q-700.png)

**Q = 1000** : Surprisingly, both drones fly again.
![](/../images/Scenario_3_Q-1000.png)



However we aim for a reasonable value of Q = 50. Lastly we find a value for R. The range for R lies roughly between [20:520]. Again we aim for something reasonable, like R = 20. Once the Altitude, LateralPositionControl and the Yaw methods are implemented, it is possible to continue tuning. kpYaw should remain below 8 but above 1 giving the drone lots of "Yaw Authority" is preferred. Here we find "less is more." Again, the tuning is iterative and this is about round three for this stage already, since all the  parameters for one scenario 3 must work with all the other scenarios, especially the figure 8 path in the trajectory follow scenario. 
Luckily we get some hints to tuning as follows:

![](/../images/TuningTips.png)

### SCENARIO 4 ###

This is one of the hardest scenarios to pass. Intuitively I would expect Scenario_5 to be the most difficult with its figure 8 path, however this one is a very close second, and indeed, tuning one scenario has a negative effect on the other - as if I were trying to squeeze a balloon in one place. 

In this scenario, the off-center mass of drone 1 and the additional mass of drone 3 truly test our PID Controls. Here we really start to see how a poor CG affects a drone's flight characteristics and why a drone pilot might spend several hours balancing his props and finding the perfect placement for his batteries and camera mounts to arrive at a near perfect CG.
After adding an integral term to our AltitudeControl. With additional tuning we are able to get a respectable flight from our Yellow drone. However our overweight drone still cannot reach its target in time and either under or overshoots. This is an opportunity to tune kpVelZ to perfection.

**VelZ = 0 :** Leads to massive oscillations.

![](/../images/Scenario_4_kpVelZ-0.png)



**VelZ = 8 :** Leads to passable results!

![](/../images/Scenario_4_kpVelZ-8.png)

Tuning is like solving a Rubik's Cube, every move on one side affects all the other five sides. Here is a particularly challenging scenario. For an optional challenge I would like to fly a Helix. After passing scenarios 1 - 5, I tune in hopes of generating a circular trajectory for the optional challenge that will eventually look like this:

**kpBank = 12**
![](/../images/Scenario_6_Bank-12_OutOfRound.png)

 

**kpBank = 10** : Yields some slightly improved results.
![](/../images/Scenario_6_Bank-12-Improved.png)

Now I check the preceding Scenarios to see if everything still passes. 
**Scenario 4, kpBank 10** : Passes!
![](/../images/Scenario_4_Bank-10-PASS.png)

**Scenario 2, kpBank 10** : It FAILS.

![](/../images/Scenario_2_Bank-10-FAIL.png)

I adjust kpBank back to 12 for Scenario 2 and it PASSES!
**Scenario 2, kpBank 12** :  It PASSES.
![](/../images/Scenario_2_Bank-12-PASS.png)

However fixing scenario 2 now causes Scenario 4 to Fail.
**Scenario 4, kpBank 12** : FAILS
![](/../images/Scenario_4_Bank-12-FAIL.png)

|           | Scenario 2 | Scenario 4 | Scenario 6*   |
| --------- | ---------- | ---------- | ------------- |
| kpBank 10 | FAIL       | PASS       | Improved      |
| kpBank 12 | PASS       | FAIL       | Oblong Circle |

It seems impossible to satisfy both Scenario 2 and Scenario 4 at the same time and that we are stuck. This can lead to iterative frustration until we think outside of the box or the table referenced and tweek other parameters such as Q. 

**Q = 100** : FAIL.

![](/../images/Scenario_4_Bank-12_Q-100-FAIL.png)

**Q = 80** : Scenarios 1 - 5 : PASSES, but only for 2/3 drones.

![](/../images/Scenario_6_Bank-12_Q-80-PASS.png)

Unfortunately in previous days of tuning on my laptop I had shrunk Xcode window to allow me to see the Simulator and the IDE simultaneously, saving time while tuning. The narrowed dialog box containing our PASS / FAIL messages cropped 1 of the 3 messages. Two of the 3 messages said "PASSED so I was under the wrong impression. When truly revealed, the message showed:

![](/../images/Obscured Fail Message.png)

Instead of all of our problems being suddenly solved, to which there would have been much rejoicing, I must return to the drawing board knowing that all my previous hours of tuning are probably for nought. If I tune kpVelz = 6, I can pass Scenario 4, but all my beautiful trajectories of figure 8's and Helix's are no longer feasible with this tuning. Passing is possible but doing it with style remains out of reach.

### Scenario 5 ###

This is last step is the most interesting, which is trying to get our drone to fly a figure 8. Again this involves lots of iterations of tuning - again this is the trickiest part. Before discovering the obscured "Quad1.PosFollowErr : Fail" error, I was trying to match the end to end tilt of the figure 8 in the Z plane. 

Profile (figure 8)

![](/../images/Scenario_5_Figure8-profile.png)

Front (figure 8)

![](/../images/Scenario_5_Figure8-front.png)

Comparing the plates above to those below will surely convince any drone pilot of the benefits of finding the proper center of gravity of ones vehicle. After adjusting the parameters required for passing scenario 4 completely, we arrive at an ugly but somehow still passing performance for the figure 8. This is atrocious compared to other trajectories flown with other parameters.

![](/../images/Scenario_5_Ugly-Passing.png)



### Scenario 6 (My optional challenge) ###

During our early course work in the Backyard Flyer, we saw a diagram of a drone flying a Helix. Obviously we did not get a chance to implement such a path in the backyard flyer, but I was still interested when we got to this stage of our cos. I was also intrigued by making our own paths as suggested by the inclusion of several "MakeTrajectory.py" files. 

Given that one size doesn't fit all (yet) we load in a new set of parameters specifically for this use case (as noted in QuadControlParams.txt file), thus we are able to get some fairly beautiful trajectories (6_Lightshow) - so long as our drone is assumed to be ideally weighted with a proper CG, the results can be quite satisfying.

![](/../images/Scenario_6_Triple-profile.png)

![](/../images/Scenario_6_Triple_tplus1-profile.png)

![](/../images/Scenario_6_Triple_ThreeQuarterView.png)



Though just simulations, the flights are fun to watch!

## FUTURE STEPS ##

The first "next step" would be continuing to tune the PID to attempt to find the holy grail of parameters that allows me to pass all five scenarios and still fly scenario six beautifully. Further research would also go into exploring why the drones bottle neck at the end of the Helix, but stop shy of the actual endpoint. I would also like to create paths that "fly" against the initial direction of the Helix. Lastly the ability to control the color of the trajectories over time would truly allow for some fun flying - especially for those of us who loved to fly kites as a kid. May the sky be the limit for one and for all of us.

* Special thanks to all the staff, students and mentors at Udacity for making this possible.

