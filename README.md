# Panopto-Sync-UniVR

Automatically sync new Panopto video lessons  

## Installation

1. Clone this repository
```shell
git clone https://github.com/pizidavi/Panopto-Sync-UniVR.git
```
2. Install requirements
```shell
python install.py
```

## Usage

### Init

_To do only the first time_  

1. Run the command:
```shell
python main.py init
```
2. Enter your GIA credentials
3. Set Master Password to encrypt credentials

### Update Courses

_To do when the courses change_  

1. Run the command:
```shell
python main.py update
```
2. Enter the Master Password

In the file `courses.json` in the folder `configs` there is the possibility of skipping a course
```json
{
  "id": 0,
  "name": "<Course>",
  "skip": false
}
```

### Sync

1. Run the command:
```shell
python main.py sync [ARGS]
```
2. Enter the Master Password

**Note:** Sync is continuous. To sync only once see [Arguments](#Arguments)  

#### Arguments

- `--format [VALUE]` or `-f [VALUE]`  
    Set the format of downloaded video-lessons. Default: `mp4`  
- `--skip-download` or `-s`  
    Only sync new video-lessons, no download. Default: `false`
- `--no-repeat` or `-o`  
    Disable continuous sync. Default: `false`
- `--every [VALUE]` or `-e [VALUE]`  
    Time to wait before a new sync (in minutes). Default: `60`
- `--sync-dir [VALUE]` or `-d [VALUE]`  
    Downloaded video lessons folder. Default: `./downloads`
