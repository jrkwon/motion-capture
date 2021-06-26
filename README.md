# Video Capture Software

6/25/2021

## Software Installation

### Required Software

- Python3

  - https://www.python.org/downloads/windows/ 

- Anaconda

  - https://www.anaconda.com/products/individual

  - Quick Note to see if your Windows is 64-Bit.

    If the "C:\Program Files (32)” folder exists, you’re using 64-Bit Windows.

    

## Create a Conda Environment

- After installing Anaconda, create an environment for the capture software.
  - `$ conda env create -f environment.yml`
- Activate the environment.
  - `$ conda activate motion-capture`

## Use video-recorder.py

### How to use

#### Specify Target Data Directory: Mandatory

This will be useful if you want to save data in a separate folder or external storage. A relative path is accepted. (e.g. `../data/yunju`)

- `$ python video-recorder.py target_dir`

#### Camera ID: Optional

If you have multiple USB cameras, you can specify which camera should be used.

- `$ python video-recorder.py target_dir --camera_id 1`

#### Time Zone: Optional

- The default time zone is UTC. If you want to use the LOCAL time, use the `local` option.
  - `$ python video-recorder.py target_dir --time_zone local`

#### All options

`$ python video-recorder.py -h`

```
usage: video-recorder.py [-h] [-c {0,1,2,3}] [-t {utc,local}] target_dir

Video Recorder ver 0.1

positional arguments:

 target_dir      target directory name

optional arguments: -h, --help      show this help message and exit

 -c {0,1,2,3}, --camera_id {0,1,2,3}            camera id number

 -t {utc,local}, --time_zone {utc,local}            time zone: default utc
```

## Data Folder Structure

If you specify, ‘./data’ as the target_dir, 

`$ python video-recorder.py ./data`

Then, the program will automatically create a folder named with the current UTC time. Then save all captured images will be saved into the newly created folder. 

```./data/unix_time=yyyy-mm-dd-hh-mm-ss-mmmmmm/unix_time=yyyy-mm-dd-hh-mm-ss-mmmmmm.jpg```

