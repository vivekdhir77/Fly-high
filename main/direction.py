import matplotlib.pyplot as plt
import time

def direction(centroid2, centroid1):
    centroid_x1 = centroid1[0]
    centroid_y1 = centroid1[1]
    centroid_x2 = centroid2[0]
    centroid_y2 = centroid2[1]

    if centroid_x2 > centroid_x1:
        if centroid_y2 > centroid_y1:
            direction_code = 2
        elif centroid_y1 < centroid_y2:
            direction_code = 1
        else:
            direction_code = 0
    else:
        direction_code = -1

    plt.figure(figsize=(5, 5))
    plt.title("Direction Visualizer")

    plt.scatter(centroid_x1, centroid_y1, color="blue", label="Start")
    plt.scatter(centroid_x2, centroid_y2, color="red", label="End")

    if direction_code == 0:
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")
    elif direction_code == 1:
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")
    elif direction_code == 2:
        plt.plot([centroid_x1, centroid_x2], [centroid_y1, centroid_y2], color="green", label="Direction")

    plt.legend()
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()

    return direction_code