import os, shutil, cv2
import subprocess, sys, getpass
import numpy as np
import matplotlib.pyplot as plt
from dae_parser import CameraPoints
from simucmd import SimuCmd
np.set_printoptions(suppress=True)


"""
# Note
# obj_file : BunnyKiller use triangle hit judge. So Blender export in obj menu, Geometry→Triangulate Faces(check), And Transform setting is (Forward -Z, Up Y).
# dae_file : You would use this code from dae, Blender Export in dae menu 1. Main→Selection Only(check), 2. Geom,Anim→Transform(Decomposed), 3. Anim→Sampling Rate→All Keyed Curves(check).
# simu_name: Don't use underbar in simu_name (Because scripts split filename(simu_name) by underbar)
#
# You should set favorable path.
"""
obj_file = '/home/saijo/labwork/研究結果まとめ/blenderfileBox/5by5-front-plane.obj'
dae_file = '/home/saijo/labwork/研究結果まとめ/blenderfileBox/5by5-front-plane.dae'
simu_name = '5by5-front-plane'

save_folder_path = os.path.join('scene-results',simu_name)



os.makedirs(save_folder_path, exist_ok=True)
shutil.copy(obj_file, save_folder_path)
shutil.copy(dae_file, save_folder_path)

cam = CameraPoints(dae_file)
passwd = (getpass.getpass() + '\n').encode()

for i, [cam_loc, lookat, lookup] in enumerate(cam.cam_loc_lookat_lookup_generator()):
    print(str(i).zfill(5))
    print(str(lookat[0]))
    os.makedirs(os.path.join(save_folder_path,str(i).zfill(5)), exist_ok=True)

    simucmd = SimuCmd()
    simucmd.camera_pos = str(cam_loc[0])+' '+str(cam_loc[1])+' '+str(cam_loc[2])
    simucmd.camera_at = str(lookat[0])+' '+str(lookat[1])+' '+str(lookat[2])
    simucmd.camera_lookup = str(lookup[0])+' '+str(lookup[1])+' '+str(lookup[2])
    simucmd.camera_samples = 4
    simucmd.camera_fov = 40
    simucmd.bdpt_samples = 512
    simucmd.point_light = str(cam_loc[0])+' '+str(cam_loc[1])+' '+str(cam_loc[2]) + ' 1 1 1'
    simucmd.objfile = os.path.join(save_folder_path, os.path.basename(obj_file))

    # Don't use underbar in name
    simucmd.name = simu_name+'-'+str(i).zfill(5)

    simucmd.hdr_folder = os.path.join(save_folder_path, str(i).zfill(5), 'hdrs')
    sh_filename = os.path.join(save_folder_path, str(i).zfill(5), 'simu_cmd.sh')
    simucmd.create_simufile(sh_filename)

    ###################################################################
    # execute sh file

    cp = subprocess.run(['sudo', '-S', 'bash', sh_filename], input=passwd, check=True)
    if cp.returncode != 0:
        print('cmd failed.', file=sys.stderr)
        sys.exit(1)

    hdr_path = os.path.join(save_folder_path, str(i).zfill(5), "hdrs", simu_name + "-" + str(i).zfill(5) + ".hdr")
    img = cv2.imread(hdr_path, flags=cv2.IMREAD_ANYDEPTH)

    tonemap1 = cv2.createTonemap(2.2)
    mapped_img = tonemap1.process(img)

    res_8bit_img = np.clip(mapped_img * 255, 0, 255).astype('uint8')
    plt.imsave(os.path.join(save_folder_path, str(i).zfill(5), simu_name + "-" + str(i).zfill(5) + ".png"), res_8bit_img[:, :, 2], cmap='gray')
