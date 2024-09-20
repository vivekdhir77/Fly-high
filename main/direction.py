def direction(centroid2, centroid1):
    # Calculate the center of the bird in frame 1 and frame 2
    centroid_x1 = centroid1[0]
    centroid_y1 = centroid1[1]
    centroid_x2 = centroid2[0]
    centroid_y2 = centroid2[1]

    # Determine the direction based on the movement of the bird's center
    if centroid_x2 > centroid_x1:  # Bird moved to the right
        if centroid_y2 > centroid_y1:  # Bird moved down
            return 2
        elif centroid_y1 < centroid_y2:  # Bird moved up
            return 1
        else:  # Bird moved horizontally to the right
            return 0
    else:  # Bird did not move to the right
        return -1