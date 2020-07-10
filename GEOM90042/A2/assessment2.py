# Author:       Bingkun Chen
# StudentID:    992113
# UserName:     BINGKUNC
# Description:  This is the code for Geom90042 Assigment2.
# Written:      8/4/2020
# Last updated: 12/4/2020

import os
import csv
import math
from pyproj import CRS, Proj, transform, Transformer
from datetime import datetime


def import_csv(filename):
    '''This function reads and processes data(removed non-data rows: header and blank row)
        from a CSV file into a nested list '''
    with open(filename, 'r') as f:
        content = f.read()
        nested_list = content.split('\n')
        nested_list.pop()
        nested_list.pop(0)
        for i in range(len(nested_list)):
            nested_list[i] = nested_list[i].split(',')
    return nested_list


def output_csv(filename, inputList):
    '''This function add the header to inputlist and write it into a new csv file'''
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        header = ["trajectory_id", "node_id", "latitude", "longitude", "altitude", "time", "X_UTM", "Y_UTM"]
        writer.writerow(header)
        for i in range(len(inputList)):
            writer.writerow(inputList[i])


def project_coordinate(inProj, outProj, in_x, in_y):
    '''This function project a lat/lon coordinate to X/Y coordinate, and transform from input projection
        to output projection, return a tuple of X_UTM,Y_UTM'''
    proj = Transformer.from_crs(inProj, outProj, always_xy = True)
    x_utm, y_utm = proj.transform(in_x, in_y)
    return (x_utm, y_utm)


def compute_distance(from_x, from_y, to_x, to_y):
    '''This function is to compute a distance between two UTM coordinate, and return the result'''
    distance = math.sqrt((to_x - from_x) ** 2 + (to_y - from_y) ** 2)
    return distance


def compute_time_difference(start_time, end_time):
    '''This function is to compute the time difference between start_time and end_time,
        return the time in seconds'''
    start = datetime.strptime(start_time, '%H:%M:%S')
    end = datetime.strptime(end_time, '%H:%M:%S')
    dif = end - start
    return dif.seconds


def compute_speed(total_distance, total_time):
    '''This function is to compute the speed, return the speed in m/s'''
    speed = float(total_distance) / float(total_time)
    return speed


def process_trajectory(computedData_list):
    '''This function is for analytical processing to each trajectory, compute the total length of the trajectory,
        find the longest segment, the segment with lowest and highest speed,
        compute the average sampling rate for trajectory in seconds and
        average speed (using total length of the trajectory/total sampling time for trajectory),
        store all the data in a nested list and return'''
    trajectory = []
    length = computedData_list[0][2]
    longest_segment = computedData_list[0][2]
    index_longest_segment = 1
    total_sampling_time = computedData_list[0][3]
    count = 1
    lowest_speed = computedData_list[0][4]
    index_lowest_speed = 1
    highest_speed = computedData_list[0][4]
    index_highest_speed = 1

    for i in range(len(computedData_list) - 1):
        if computedData_list[i][0] == computedData_list[i + 1][0] and i != len(computedData_list) - 2:
            trajectory_id = computedData_list[i][0]
            length += computedData_list[i + 1][2]
            total_sampling_time += computedData_list[i + 1][3]
            count += 1
            if computedData_list[i + 1][2] > longest_segment:
                longest_segment = computedData_list[i + 1][2]
                index_longest_segment = computedData_list[i + 1][1]
            if computedData_list[i + 1][4] > highest_speed:
                highest_speed = computedData_list[i + 1][4]
                index_highest_speed = computedData_list[i + 1][1]
            if computedData_list[i + 1][4] < lowest_speed:
                lowest_speed = computedData_list[i + 1][4]
                index_lowest_speed = computedData_list[i + 1][1]
        elif computedData_list[i][0] != computedData_list[i + 1][0]:
            sampling_rate = float(total_sampling_time) / count
            avg_speed = float(length) / float(total_sampling_time)
            trajectory.append([trajectory_id, length, index_longest_segment, longest_segment,
                               sampling_rate, index_lowest_speed, lowest_speed,
                               index_highest_speed, highest_speed, avg_speed])
            length = computedData_list[i + 1][2]
            longest_segment = computedData_list[i + 1][2]
            lowest_speed = computedData_list[i + 1][4]
            highest_speed = computedData_list[i + 1][4]
            total_sampling_time = computedData_list[i + 1][3]
            count = 1
            index_longest_segment = 1
            index_lowest_speed = 1
            index_highest_speed = 1
        elif i == len(computedData_list) - 2:
            length += computedData_list[i + 1][2]
            total_sampling_time += computedData_list[i + 1][3]
            count += 1
            sampling_rate = float(total_sampling_time) / count
            avg_speed = float(length) / float(total_sampling_time)
            if computedData_list[i + 1][2] > longest_segment:
                longest_segment = computedData_list[i + 1][2]
                index_longest_segment = computedData_list[i + 1][1]
            if computedData_list[i + 1][4] > highest_speed:
                highest_speed = computedData_list[i + 1][4]
                index_highest_speed = computedData_list[i + 1][1]
            if computedData_list[i + 1][4] < lowest_speed:
                lowest_speed = computedData_list[i + 1][4]
                index_lowest_speed = computedData_list[i + 1][1]
            trajectory.append([trajectory_id, length, index_longest_segment, longest_segment,
                               sampling_rate, index_lowest_speed, lowest_speed,
                               index_highest_speed, highest_speed, avg_speed])
    return trajectory


def print_output(trajectory_list, filename):
    '''This function is to compute the total length for all trajectories, and find the longest one with its avg_speed,
        also, it will print the final result and write it into a txt file'''
    with open(filename, 'a') as f:
        total_length = 0
        longest_trajectory = 0
        avg_speed = 0
        for i in range(len(trajectory_list)):
            total_length += trajectory_list[i][1]
            index = 1 + int(trajectory_list[i][0])
            output_str = ("Trajectory " + str(index) + "'s length is " + "%.2f" % trajectory_list[i][1] + "m."
                          + "\n" + "The length of its longest segment is " + "%.2f" % trajectory_list[i][3]
                          + "m, and the index is " + str(trajectory_list[i][2]) + "." + "\n"
                          + "The average sampling rate for the trajectory is " + "%.2f" % trajectory_list[i][4] + "s."
                          + "\n" + "For the segment index " + str(trajectory_list[i][5])
                          + ", the minimal travel speed is reached." + "\n" + "For the segment index "
                          + str(trajectory_list[i][7]) + ", the maximum travel speed is reached." + "\n" + "----")
            print(output_str)
            f.write(output_str + "\n")
            if trajectory_list[i][1] > longest_trajectory:
                longest_trajectory = trajectory_list[i][1]
                index_longest_trajectory = index
                avg_speed = trajectory_list[i][9]
        all_trajectories = [total_length, index_longest_trajectory, avg_speed]
        output_str = ("The total length of all trajectories is " + "%.2f" % total_length + "m." + "\n"
                      + "The index of the longest trajectory is " + str(index_longest_trajectory)
                      + ", and the average speed along the trajectory is " + "%.2f" % avg_speed + "m/s."
                      + "\n" + "Program complete")
        print(output_str)
        f.write(output_str)


def main():
    # setup constant
    filename = os.path.join(os.getcwd(), "trajectory_data.csv")
    result_file = os.path.join(os.getcwd(), "assessment2.csv")

    # import trajectory data file
    result = import_csv(filename)

    # processing the coordinate and output the result into a new csv file
    computedData = []
    for i in range(len(result)):
        lat = result[i][2]
        lon = result[i][3]
        coordinate = list(project_coordinate(4326, 4796, lon, lat))
        result[i].extend(coordinate)
    output_csv(result_file, result)

    # run task 2
    for i in range(len(result) - 1):
        if result[i][0] == result[i + 1][0]:
            trajectory_id = result[i][0]
            segment_index = result[i + 1][1]
            segment_length = compute_distance(result[i][6], result[i][7], result[i + 1][6], result[i + 1][7])
            segment_time = compute_time_difference(result[i][5], result[i + 1][5])
            segment_speed = compute_speed(segment_length, segment_time)
            temp_list = [trajectory_id, segment_index, segment_length, segment_time, segment_speed]
            computedData.append(temp_list)

    # run task 3
    trajectory = process_trajectory(computedData)
    output_file = os.path.join(os.getcwd(), "assessment2_out.txt")
    print_output(trajectory, output_file)


if __name__ == '__main__':
    main()
