## Vidsnap

![Version 0.0.2](https://img.shields.io/badge/Version-0.0.2-blue)
![MIT License](https://img.shields.io/badge/License-MIT-success)

Vidsnap is a small python utility to extract stills from video's using opencv.
It focuses on using as little IO's as possible and `ThreadPoolExecutor` to be able to parse large folders relatively quickly.

As it's based on opencv, it will support every video format supported by `cv2.VideoCapture`.


### Installing
#### From Source 
```
git clone https://github.com/jarviscodes/vidsnap
cd vidsnap
pip3 install -r requirements.txt
```

#### From PyPi
```
pip3 install vidsnap
``` 

### Usage

```
python -m vidsnap --help
Usage: vidsnap.py [OPTIONS]

Options:
  -i, --input_path TEXT   Directory where the videos are located
  -o, --output_path TEXT  Directory where the snapshots will be stored
  -e, --extension TEXT    Extension for the videos to process. (e.g. MP4)
  -w, --workers INTEGER   Amount of threadworkers to spawn
  -s, --seconds INTEGER   Amount of seconds between every snap per video.
  --help                  Show this message and exit.
```
