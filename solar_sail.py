# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:44:27 2018

@author: Owner
"""

import numpy
import math
import pylab
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 6.67428e-11 # Newton's gravitational constant
AU = (149.6e6 * 1000) # Astronomical unit in metres
timestep = 24 * 3600 # One day in seconds (timestep for the simulation)

class planet(object):
    """
    Planet class.
    Contains information about the planet's
    current position, velocity and mass
    and other general information.
    """

    def __init__(self):
        self.px = 0.0
        self.py = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.mass = None
        self.color = None
        self.size = None
        self.name = None

    def compute_force(self, others):
        """
        Compute the total exerted force on the
        body at any moment in time.
        """
        self.total_fx = self.total_fy = 0.0
        for other in others:
            # Compute the distance of the other body.
            sx, sy = self.px, self.py
            ox, oy = other.px, other.py
            dx = (ox-sx)
            dy = (oy-sy)
            d = numpy.sqrt(dx ** 2 + dy ** 2)

            # Compute the force of attraction
            f = G * self.mass * other.mass / (d ** 2)

            # Compute the direction of the force.
            theta = math.atan2(dy, dx)
            fx = math.cos(theta) * f
            fy = math.sin(theta) * f

            # Add to the total force exerted on the planet
            self.total_fx += fx
            self.total_fy += fy

    def update_position(self):
        """
        Update planet velocity and position based on the
        current exterted total force on the body.
        """
        self.vx += self.total_fx / self.mass * timestep
        self.vy += self.total_fy / self.mass * timestep
        self.px += self.vx * timestep
        self.py += self.vy * timestep

def animate(i, bodies, lines):
    """
    Animation function. Updates the
    plot after each interation.
    """
    for ind, body in enumerate(bodies):
        body.compute_force(numpy.delete(bodies, ind))
    for body in bodies:
        body.update_position()
    for i in range(len(bodies)):
        lines[i].set_data(bodies[i].px / AU, bodies[i].py / AU)
    return lines

def main():
    Sun = planet()
    Earth = planet() 
    mars = planet()
    solar_sail = planet() 
    
    Sun.mass = 1.98892 * 10 ** 30
    Sun.color = 'y'
    Sun.size = 50
    Sun.name = 'Sun'

    Earth.mass = 5.9742 * 10 ** 24
    Earth.px = -1 * AU
    Earth.vy = 29.783 * 1000
    Earth.color = 'b'
    Earth.size = 5
    Earth.name = 'Earth'

    mars.mass = 6.39 * 10 ** 23
    mars.px = 1.524 * AU
    mars.vy = - 24.1 * 1000
    mars.color = 'r'
    mars.size = 5
    mars.name = 'Mars'
    
    solar_sail.mass = 15
    solar_sail.px = -1.02 * AU
    solar_sail.vy = - 34 * 1000
    solar_sail.color = 'm'
    solar_sail.size = 1.5
    solar_sail.name = 'Solar Sail'
    
    #stars:
    x1 = numpy.random.uniform(-2.2, 2.2, size=37)
    y1 = numpy.random.uniform(-2.2, 2.2, size=37)
    
    bodies = [Sun, Earth, mars, solar_sail]
    lines = [None] * len(bodies)
    fig = pylab.figure(figsize=(8,8))
    fig.patch.set_facecolor('black')
    ax = pylab.subplot()

    for i in range(len(bodies)):
        lines[i], = ax.plot(bodies[i].px / AU, bodies[i].py / AU,
        marker='o', color=bodies[i].color, ms=bodies[i].size,
        label=bodies[i].name)
        
    anim = animation.FuncAnimation(fig, animate, numpy.arange(1, 546),
        fargs=[bodies, lines], interval=20, blit=True, repeat=False)

    ax.set_xlabel('x [AU]')
    ax.set_ylabel('y [AU]')
    ax.patch.set_facecolor('black')
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    legend = ax.legend(loc=9, bbox_to_anchor=(0.5, 1.1), ncol=3)
    legend.legendHandles[0]._legmarker.set_markersize(6)
    plt.scatter( x1, y1, c='w', s=1)
    pylab.show()
    
if __name__ == "__main__":
    main()