# A Star and Best First Search Algorithm
This is the implementation of A* and Best First Search Algorithms in python language. The project comprimise two data structures: stack and heap. So there is four options in this project.

Search algorithms run on the images between start and end pixels. I added R value from RGB value to the h(n) and g(n) functions. Thus, algorithms tend to move from the red areas. Red areas have the lower cost value. The fuctions are listed below.

For Best First Search, we use **f(n) = h(n)**, the heuristic function. It can be shortest line distance for path finding between cities or districts. In this project:

#### f(n) = h(n) = euclideanDistance(point1, point2) * (256 - R)

Computed Euclidean Distance is between the point1 is the point that we add to our stack or heap and point2 is the end point. So we can predict which point is closer to the end point then we can choose it.

For A* Algorithm we add another function to our f(n). This time **f(n) = h(n) + g(n)** where g(n) is the computed cost between the starting point and the current point. In A* algorithm we can choose the closer point with the lower cost. A* is an optimum algorithm. In this project f(n) is:

#### f(n) = h(n) + g(n) = euclideanDistance(point1, point2) * (256 - R) + point1.parent.g + 256 - R

In this formula point1.parent.g stands for the cost between starting point and the parent point. 256 - R term gives the cost value for that point, from its parent.

![Best First Search implemetation](screenshots/bfs.png)

