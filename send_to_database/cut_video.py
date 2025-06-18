import argparse
import os
import subprocess

# Définir les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-tps_deb", "--tps_deb", required=True, type=str)
ap.add_argument("-tps_fin", "--tps_fin", required=True, type=str)
args = ap.parse_args()
tps_deb, tps_fin = args.tps_deb, args.tps_fin

# Récupérer le nom de la vidéo
video_name = os.listdir("../temp")[0]

# Lancer le découpage de la vidéo
subprocess.run(f"ffmpeg -ss {tps_deb} -i ../temp/{video_name} -to {tps_fin} -c:v copy -c:a copy ../temp/video_cut.mp4", shell=True)
