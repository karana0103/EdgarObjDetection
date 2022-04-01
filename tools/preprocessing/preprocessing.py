import os
import numpy as np
import sys


class kitti_object(object):
    '''Load and parse object data into a usable format.'''    
    def __init__(self, root_dir, split="sys.argv[2]"):
        '''root_dir contains training and testing folders'''
        self.root_dir = root_dir
        self.split = split
        self.split_dir = os.path.join(root_dir, split)
        self.lidar_dir = os.path.join('velodyne', self.split_dir)
    def get_lidar(self, idx): 
        lidar_filename = os.path.join(self.lidar_dir, '%06d.bin'%(idx))
        return load_velo_scan(lidar_filename)


def load_velo_scan(velo_filename):
    scan = np.fromfile(velo_filename, dtype=np.float32)
    scan = scan.reshape((-1, 4))
    print(scan)
    return scan

#algorithm to edit from new dataset to shift x +20, z plus 1 and normalize the intensity
dataset = kitti_object('sys.argv[1]')
for x in range(sys.argv[3]):
    data_idx = x
    lidar_data = dataset.get_lidar(data_idx)
    lidar_data_edited=lidar_data 
    lidar_data_edited[:,3]=lidar_data_edited[:,3]/np.max(lidar_data[:,3]) #normalize intensity
    lidar_data_edited[:,0]=lidar_data_edited[:,0]+20 #shift the x of center axis to make object in front
    lidar_data_edited[:,2]=lidar_data_edited[:,2]-1 #shift the height of center axis
    lidar_data_edited.tofile(str(x)+'.bin')
