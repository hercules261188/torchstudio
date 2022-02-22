import sys
import importlib
import importlib.util
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--gpu", help="install nvidia gpu support", action="store_true", default=False)
args, unknown = parser.parse_known_args()

if importlib.util.find_spec("conda") is None:
    print("Error: A Conda environment is required to install the required packages.", file=sys.stderr)
    exit()

import conda.cli.python_api as Conda

# scipy required by torchvision: Caltech ImageNet SBD SVHN datasets and Inception v3 GoogLeNet models
# pandas required by the dataset tutorial: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
# matplotlib-base required by torchstudio renderers
# python-graphviz required by torchstudio graph
# paramiko required for ssh connections
# pysoundfile required on windows by torchaudio: https://pytorch.org/audio/stable/backend.html#soundfile-backend
if sys.platform.startswith('win'):
    if args.gpu:
        conda_install="pytorch torchvision torchaudio cudatoolkit=11.3 scipy pandas matplotlib-base python-graphviz paramiko pysoundfile"
    else:
        conda_install="pytorch torchvision torchaudio cpuonly scipy pandas matplotlib-base python-graphviz paramiko pysoundfile"
elif sys.platform.startswith('darwin'):
    conda_install="pytorch torchvision torchaudio scipy pandas matplotlib-base python-graphviz paramiko"
elif sys.platform.startswith('linux'):
    if args.gpu:
        conda_install="pytorch torchvision torchaudio cudatoolkit=11.3 scipy pandas matplotlib-base python-graphviz paramiko"
    else:
        conda_install="pytorch torchvision torchaudio cpuonly scipy pandas matplotlib-base python-graphviz paramiko"
else:
    print("Error: Unsupported platform.", file=sys.stderr)
    print("Windows, macOS or Linux is required.", file=sys.stderr)
    exit()

print("Downloading and installing PyTorch and additional packages:")
print(conda_install)
print("")

# channels: pytorch for pytorch torchvision torchaudio, nvidia for cudatoolkit=11.1 on Linux, conda-forge for everything else except anaconda for python-graphviz
conda_install+=" -c pytorch -c nvidia -c conda-forge -c anaconda"

# https://stackoverflow.com/questions/41767340/using-conda-install-within-a-python-script
(stdout_str, stderr_str, return_code_int) = Conda.run_command(Conda.Commands.INSTALL,conda_install.split(),stdout=sys.stdout,stderr=sys.stderr)
