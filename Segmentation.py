import os
import open3d as o3d

# from Picker import pick_points
import pandas as pd
import numpy as np
def ply_segmentation(file_path,file_name,output_dir = 'out'):
    print("Processing file: ", file_name)
    # 加载PLY格式的点云数据
    pcd = o3d.io.read_point_cloud(file_path)

    # 进行统计滤波，移除噪点
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    pcd = pcd.select_by_index(ind)

    # 使用欧几里得聚类将点云分割成多个部分
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

    # 计算每个聚类部分的点数
    unique_labels, counts = np.unique(labels, return_counts=True)
    label_counts = dict(zip(unique_labels, counts))

    # 去除噪声的部分（label为-1）
    if -1 in label_counts:
        del label_counts[-1]

    # 筛选点数大于等于5000的聚类部分
    filtered_labels = [label for label, count in label_counts.items() if count >= 9000]

    # 合并所有符合条件的聚类部分
    filtered_points = []
    for label in filtered_labels:
        filtered_points.append(pcd.select_by_index(np.where(labels == label)[0]))

    # 如果有符合条件的聚类部分，合并它们
    if filtered_points:
        main_cluster = filtered_points[0]
        for cluster in filtered_points[1:]:
            main_cluster += cluster
    else:
        main_cluster = o3d.geometry.PointCloud()

    # 可视化结果
    o3d.visualization.draw_geometries([main_cluster])
    # 保存处理后的点云
    o3d.io.write_point_cloud(os.path.join(output_dir, file_name), main_cluster)
    print("Filtered point cloud saved.")





def get_sorted_ply_files(folder_path):
    """Returns a sorted list of .ply files in the given folder."""
    ply_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]
    ply_files.sort()
    return ply_files





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
        ply_segmentation(file_path, ply_file)


if __name__ == "__main__":
    main()
