# Schedule Screen Build

## Website

#### Environment

- `cd website`
- Install python requirements (probably just flask) with `pip install -r requirements.txt` depending on your python environment

#### Testing

Will likely work on either raspberry pi or on a desktop/laptop

`python website.py`

#### Service Setup

- Create `schedule_website.service` (to be added)
- Move file to `/etc/systemd/system/`
- `sudo systemctl enable schedule_website.service`
- `sudo systemctl start schedule_website.service`
- Verify website is running

## Screen App

#### Environment

- `cd screen`
- Install python requirements (probably just e-ink library) with `pip install -r requirements.txt` depending on your python environment

#### Testing

Will likely only work on raspberry pi unless we set it up to output the image

`python screen_updater.py`

#### Scheduling

- Create `update_screen.sh` (to be added)
- Add scheduling to cron (how many minutes between update?)
