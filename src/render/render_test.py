import os
import sys
import subprocess


src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_dir)

blender_path = "C:\\Program Files\\Blender Foundation\\Blender 3.3\\blender"
blender_script_path = os.path.join(src_dir, 'render', 'test_script.py')
#
blender_args = [blender_path, '--background', '--python', blender_script_path]
subprocess.check_call(blender_args)