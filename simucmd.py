import os
import subprocess, sys, getpass

class SimuCmd:
    def __init__(self):
        ###################################################################
        #init variable
        self.camera_samples=8
        self.bdpt_samples=512
        self.bounce_streak=4
        self.max_bounces=8

        #this data require 256 by 256
        #but this simulator need this (257,257) setting
        self.height=257
        self.width=257

        self.time_res=2220
        self.toffset=0
        self.exp=0.008993773740

        self.camera_pos='0 1 3'
        self.camera_at='0 1 2'
        self.camera_lookup='0 2 3'
        self.camera_fov=40

        self.point_light = self.camera_pos+' 1 1 1'

        self.objfile='model/export_bathroom_small.obj'

        # Don't use underbar in name
        self.name='create-simple-python-about5m-light01-bathroom-small'
        self.hdr_folder = 'scene-results/bathroom-small/00000/hdrs/'

    def create_simufile(self,filepath):
        ######################################################################
        #make script
        script_strings = '#!/bin/bash\n'
        script_strings += 'camera_samples='+str(self.camera_samples)+'\n'
        script_strings += 'bdpt_samples='+str(self.bdpt_samples)+'\n'
        script_strings += 'bounce_streak='+str(self.bounce_streak)+'\n'
        script_strings += '#max_bounces='+str(self.max_bounces)+'\n'
        script_strings += 'height='+str(self.height)+'\n'
        script_strings += 'width='+str(self.width)+'\n'
        script_strings += 'time_res='+str(self.time_res)+'\n'
        script_strings += 'toffset='+str(self.toffset)+'\n'
        script_strings += 'exp='+str(self.exp)+'\n'
        script_strings += "camera_pos=\'"+str(self.camera_pos)+'\'\n'
        script_strings += "camera_at=\'"+str(self.camera_at)+'\'\n'
        script_strings += "camera_lookup=\'"+str(self.camera_lookup)+'\'\n'
        script_strings += "camera_fov="+str(self.camera_fov)+'\n'
        script_strings += "point_light=\'"+str(self.point_light)+'\'\n'
        script_strings += "objfile=\'"+str(self.objfile)+'\'\n'
        script_strings += "name=\'"+str(self.name)+'\'\n\n\n'

        script_strings += "sudo docker container run -v $(pwd):/root bunnykiller BunnyKiller \\\n"
        script_strings += "    -log-name $name.txt \\\n"
        script_strings += "    -film-name $name -new-seed '12' \\\n"
        script_strings += "    -camera-spp $camera_samples -camera-fov $camera_fov \\\n"
        script_strings += "    -film-size-x $width -film-size-y $height \\\n"
        script_strings += "    -film-size-t $time_res -film-exposure $exp -film-offset $toffset \\\n"
        script_strings += "    -camera-position $camera_pos -camera-focus $camera_at -camera-up $camera_lookup \\\n"
        script_strings += "    -point-light-source $point_light \\\n"
        script_strings += "    -name-mesh $objfile -lambertian 1 1 1 \\\n"
        script_strings += "    -bidirectional-path-tracing $bdpt_samples -multibounce-streak $bounce_streak \\\n"
        script_strings += "    -film-store-depth -scattering-level all -lambertian-rho 1.0 -no-background -transient-state\n\n"

        script_strings += "if [ ! -d "+self.hdr_folder+" ]; then\n"
        script_strings += "  mkdir -p "+self.hdr_folder+";\n"
        script_strings += "fi\n"
        script_strings += "mv ./$name* "+self.hdr_folder

        with open(filepath, mode='w') as f:
            f.write(script_strings)

###################################################################
#execute sh file

# passwd = (getpass.getpass() + '\n').encode()
# cp = subprocess.run(['sudo', '-S', 'bash', 'simu_from_python.sh'],input=passwd, check=True)
# if cp.returncode != 0:
#     print('cmd failed.', file=sys.stderr)
#     sys.exit(1)


if __name__ == '__main__':
    simucmd = SimuCmd()
    simucmd.camera_pos = '0.6488918  0.8883101 -0.6742092'
    simucmd.camera_at = '-0.28068353  0.81088318 -0.31380001'
    simucmd.camera_lookup = '0.57670093  1.88530813 -0.6462198'
    simucmd.camera_fov = 40
    simucmd.point_light = simucmd.camera_pos+' 1 1 1'
    simucmd.objfile = 'scene-results/bathroom-small/export_bathroom_small.obj'
    # Don't use underbar in name
    simucmd.name = 'simu-bathroom-small'

    simucmd.hdr_folder = 'scene-results/bathroom-small/00000/hdrs/'
    simucmd.create_simufile(os.path.join('scene-results/bathroom-small/00000','simu_from_python1.sh'))