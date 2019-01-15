import math;

def fmt(value):
    return "%.3f" % value

period = 4
radius = 0.5
timestep = 0.05
maxtime = period*1
# center = [200, 200, 200]

with open('SpiralNoFF.txt', 'w') as the_file:
    t=0;
    while t <= maxtime:
        x = math.sin(t * 3 * math.pi / period) * radius;
        y = math.cos(t * 3 * math.pi / period) * radius;
        z = math.cos(t * 3 * math.pi / period) * radius;
        the_file.write(fmt(t) + "," + fmt(x) + "," + fmt(y) + "," + "-1\n");
        # the_file.write(fmt(t) + "," + fmt(x) + "," + fmt(y) + "," + fmt(z) + "-1\n");
        t += timestep;
        radius += 0.01    
