import sympy as sp
import scipy.spatial.distance as dist
import matplotlib.lines as lines
import matplotlib.pyplot as plt
import numpy as np

# Determine the point closest to c = (cx, cy) on the line p1 = (p1x, p1y), p2 = (p2x, p2y)
#
# This involves finding r that minimises |p1 + r * (p2 - p1) - c| 

r, p1x, p1y, p2x, p2y, cx, cy = sp.symbols('r p1x p1y p2x p2y cx cy')

# You could solve this by hand but why bother
expr = (p1x + r * (p2x - p1x)  - cx)**2 + (p1y + r * (p2y - p1y)  - cy)**2
soln = sp.simplify(sp.solve(sp.diff(expr, r), r))

# Using the result in soln 
def line_intersects_circle(p1, p2, circle):
    r = (-circle[0]*p1[0] + circle[0]*p2[0] - circle[1]*p1[1] + circle[1]*p2[1] + p1[0]**2 - p1[0]*p2[0] + p1[1]**2 - p1[1]*p2[1])/(p1[0]**2 - 2*p1[0]*p2[0] + p1[1]**2 - 2*p1[1]*p2[1] + p2[0]**2 + p2[1]**2)
    
    r = min(max(r, 0), 1)
            
    p = [p1[0] + r * (p2[0] - p1[0]), p1[1] + r * (p2[1] - p1[1])]
 
    return {
        'closest_point': p,
        'insects_circle': dist.pdist([p, circle[0:2]])[0] < circle[2]
    }


# Visual test - draw some random lines and highlight the ones that intersect with the circle
n = 10
points = [[np.random.normal(0), np.random.normal(0)] for t in range(n)]

fig, ax = plt.subplots()
ax.set_aspect('equal')

for i in range(len(points)):
    for j in range(len(points)):
        if i != j:
            if line_intersects_circle(points[i], points[j], [0, 0, 1]):
                ax.add_line(lines.Line2D([points[i][0], points[j][0]], [points[i][1], points[j][1]], linewidth=1, color='red'))
            else:
                ax.add_line(lines.Line2D([points[i][0], points[j][0]], [points[i][1], points[j][1]], linewidth=1, color='black'))

ax.scatter([p[0] for p in points], [p[1] for p in points])

circle = plt.Circle((0, 0), 1, alpha=0.2, color='r')
ax.add_artist(circle)

plt.show()

# Illustration
fig, ax = plt.subplots()
ax.set_aspect('equal')

p1 = [-2.0, 0.0]
p2 = [2.0, 2.5]
c = [0.0, 0, 1]

p = line_intersects_circle(p1, p2, c)['p']

ax.add_line(lines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], linewidth=1, color='black'))

ax.set_xlim([-3, 3])
ax.set_ylim([-1.5, 3])

ax.text(p1[0], p1[1], 'p1', verticalalignment='bottom', horizontalalignment='right')
ax.text(p2[0], p2[1], 'p2', verticalalignment='bottom', horizontalalignment='right')
ax.text(p[0], p[1], 'p', verticalalignment='bottom', horizontalalignment='right')
ax.text(c[0], c[1], 'c', verticalalignment='bottom', horizontalalignment='right')

ax.scatter([p1[0], p2[0], c[0], p[0]], [p1[1], p2[1], c[1], p[1]], s=10)

circle = plt.Circle((c[0], c[1]), c[2], alpha=0.2, color='r')
ax.add_artist(circle)

plt.show()