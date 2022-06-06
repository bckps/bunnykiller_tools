from scipy.spatial.transform import Rotation as R
import numpy as np
np.set_printoptions(suppress=True)

class RotVector:
    def __init__(self):
        # When Blender objects are no rotation, lookup and lookat are following values.
        self.lookat = np.array([0, 0, -1])
        self.lookup = np.array([0, 1, 0])

    def convert_blender2simu(self, blen_vec):
        simu_vec = np.array([blen_vec[0],blen_vec[2], -blen_vec[1]])
        return simu_vec


    def apply_coordinates_LookatLookup(self, locvec, rotvec):
        """
        # rotation order is x, y, z in Blender. If you change this order, results change.
        # lookat specipy position.(global position) Not direction vector.
        # lookup specipy direction vector.(local rotation)
        """
        rx = R.from_rotvec(np.array([rotvec[0], 0, 0]).astype(float), degrees=True)
        ry = R.from_rotvec(np.array([0, rotvec[1], 0]).astype(float), degrees=True)
        rz = R.from_rotvec(np.array([0, 0, rotvec[2]]).astype(float), degrees=True)
        rot = rz * ry * rx

        lookat = self.convert_blender2simu(rot.apply(self.lookat)) + self.convert_blender2simu(locvec)
        lookup = self.convert_blender2simu(rot.apply(self.lookup))
        return lookat, lookup


if __name__ =='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=float, help='positioin x')
    parser.add_argument('y', type=float, help='positioin y')
    parser.add_argument('z', type=float, help='positioin z')
    parser.add_argument('rx', type=float, help='rotation rx')
    parser.add_argument('ry', type=float, help='rotation ry')
    parser.add_argument('rz', type=float, help='rotation rz')
    args = parser.parse_args()
    rotv = RotVector()
    lookat, lookup = rotv.apply_coordinates_LookatLookup(np.array([args.x, args.y, args.z]).astype(float),
                                                         np.array([args.rx, args.ry, args.rz]).astype(float))
    print('Look up: ',lookup)
    print('Look at: ', lookat)