import os
import open3d as o3d

from Picker import pick_points
import pandas as pd
import numpy as np


def get_sorted_ply_files(folder_path):
    """Returns a sorted list of .ply files in the given folder."""
    ply_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]
    ply_files.sort()
    return ply_files


def process_ply(ply_file, file_name, output_dir="annotations"):

    pcd = o3d.io.read_point_cloud(ply_file)
    print(f"Processing file: {file_name}")

    if not pcd.is_empty():
        print("Point cloud loaded successfully.")
    else:
        print("Failed to load point cloud. Please check the file path.")
        return

    picked_points = pick_points(pcd)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

        # Extract points based on picked_points indices
    points = [pcd.points[i] for i in picked_points]

    # Convert points to a NumPy array
    points_array = np.array(points)


    # Create a DataFrame from the NumPy array
    df = pd.DataFrame(points_array, columns=['x', 'y', 'z'])

    # Save DataFrame to CSV
    csv_path = os.path.join(output_dir, file_name+'.csv')
    df.to_csv(csv_path, index=False)
    print(f"Points saved to {csv_path}")




def main():
    folder_path = input("Enter the folder path containing .ply files: ")
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    ply_files = get_sorted_ply_files(folder_path)
    if not ply_files:
        print("No .ply files found in the folder.")
        return

    start_index_str = input(
        f"Enter the start index (0 to {len(ply_files) - 1}), or press Enter to start from the beginning: ")
    start_index = 0
    if start_index_str.isdigit():
        start_index = int(start_index_str)
        if start_index < 0 or start_index >= len(ply_files):
            print("Invalid start index. Starting from the beginning.")
            start_index = 0

    for i in range(start_index, len(ply_files)):
        print(i)

        ply_file = ply_files[i]
        file_path = os.path.join(folder_path, ply_file)
        process_ply(file_path, ply_file)


if __name__ == "__main__":
    main()
