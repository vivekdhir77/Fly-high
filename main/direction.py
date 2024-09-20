import matplotlib.pyplot as plt
import time

def direction(centroid2, centroid1):
    # Calculate the center of the bird in frame 1 and frame 2
    centroid_x1 = centroid1[0]
    centroid_y1 = centroid1[1]
    centroid_x2 = centroid2[0]
    centroid_y2 = centroid2[1]

    # Determine the direction based on the movement of the bird's center
    if centroid_x2 > centroid_x1:  # Bird moved to the right
        if centroid_y2 > centroid_y1:  # Bird moved down
            direction_code = 2
        elif centroid_y1 < centroid_y2:  # Bird moved up
            direction_code = 1
        else:  # Bird moved horizontally to the right
            direction_code = 0
    else:  # Bird did not move to the right
        direction_code = -1

    # Create a plot to visualize the direction
    plt.figure(figsize=(5, 5))  # Reduced the window size
    plt.title("Direction Visualizer")

    # Plot the starting point
    plt.scatter(centroid_x1, centroid_y1, color="blue", label="Start")

    # Plot the ending point
    plt.scatter(centroid_x2, centroid_y2, color="red", label="End")

    # Plot the direction line
    if direction_code == 0:  # Right
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")
    elif direction_code == 1:  # Up
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")
    elif direction_code == 2:  # Down
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")

    plt.legend()
    plt.show(block=False)  # Show the plot without blocking
    plt.pause(0.5)  # Pause for half a second
    plt.close()  # Close the plot

    return direction_code