# flake8: noqa

import logging
import sys

from qtpy import QT_VERSION


__appname__ = "vineseg"


# Semantic Versioning 2.0.0: https://semver.org/
# 1. MAJOR version when you make incompatible API changes;
# 2. MINOR version when you add functionality in a backwards-compatible manner;
# 3. PATCH version when you make backwards-compatible bug fixes.
__version__ = "0.0.21"

QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys

from .label_file import LabelFile
from . import testing
from . import utils

### Model version check
## TODO:
import os
import urllib.request

# check current version
script_dir = os.path.dirname(__file__)
version_path = os.path.join(script_dir, "experiments/batch_unet3/VERSION")
with open(version_path, 'r') as file:
    current_ver = int(file.read())
    ###logger.info("Current Vineseg Model Version: {}".format(currentVer))
    print("Current Vineseg Model Version: {}".format(current_ver))


# check online version
fol = urllib.request.urlopen("https://vineseg.s3.eu-central-1.amazonaws.com/NEWEST")
online_ver = int(fol.read())

if online_ver > current_ver:
    print("Found a newer model online! Download started.")
    
        # Replace the current model
    if os.path.exists(os.path.join(script_dir, "experiments/batch_unet3/trained_weights/trained_weights.pth")):
        os.remove(os.path.join(script_dir, "experiments/batch_unet3/trained_weights/trained_weights.pth"))
    if os.path.exists(os.path.join(script_dir, "experiments/batch_unet3/trained_weights_swa/trained_weights.pth")):
        os.remove(os.path.join(script_dir, "experiments/batch_unet3/trained_weights_swa/trained_weights.pth"))
    
    #os.remove(os.path.join(script_dir, "experiments/batch_unet3/VERSION"))
    if not os.path.exists(os.path.join(os.path.sep, script_dir, "experiments", "batch_unet3", "trained_weights")):
        os.makedirs(os.path.join(os.path.sep, script_dir, "experiments", "batch_unet3", "trained_weights"))
    if not os.path.exists(os.path.join(os.path.sep, script_dir, "experiments", "batch_unet3", "trained_weights_swa")):
        os.makedirs(os.path.join(os.path.sep, script_dir, "experiments", "batch_unet3", "trained_weights_swa"))
    
    urllib.request.urlretrieve('https://vineseg.s3.eu-central-1.amazonaws.com/trained_weights/trained_weights.pth', os.path.join(script_dir, "experiments/batch_unet3/trained_weights/trained_weights.pth"))
    urllib.request.urlretrieve('https://vineseg.s3.eu-central-1.amazonaws.com/trained_weights_swa/trained_weights.pth', os.path.join(script_dir, "experiments/batch_unet3/trained_weights_swa/trained_weights.pth"))
    urllib.request.urlretrieve('https://vineseg.s3.eu-central-1.amazonaws.com/NEWEST', os.path.join(script_dir, "experiments/batch_unet3/VERSION"))
    
    print("Updated the model to newest version!")
