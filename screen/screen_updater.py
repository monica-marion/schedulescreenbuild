import sqlite3
from datetime import date, time, datetime, timedelta
from PIL import Image, ImageDraw

DATABASE = '../database.db'
DEBUG = True

if not DEBUG:
    # load inky hat object using auto-detect
    from inky.auto import auto
    display = auto()

########### Screen Update Methods ###########

def get_screen(current_time, start_time, end_time, current_icon, next_icon):
    print(f'current_time: {current_time}')
    print(f'start_time: {start_time}')
    print(f'end_time: {end_time}')
    print(f'current_icon: {current_icon}')
    print(f'next_icon: {next_icon}')
    progress = (current_time - start_time) / (end_time - start_time)
    print(f'progress: {progress:.4f}')
    if DEBUG:
        return Image.new('1', (400, 300))
    else:
        return Image.new('1', display.resolution)

def display(image):
    if DEBUG:
        image.show()
    else:
        display.set_image(image)

############# Database handling #############
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def get_info():
    if DEBUG:
        icons = ["1.png", "2.png", "3.png", "4.png", "5.png"]
        time_strings = ["00:20", "00:30", "01:30", "4:50", "12:00"]
        t = "00:01"
        current_time = datetime.combine(date.today(), time(*map(int, t.split(':'))))
    else:
        # TODO: load icons, times from db
        icons = []
        time_strings = []
        current_time = datetime.now()
        raise Exception("get_info() not implemented")
    try:
        # Convert strings into datetime objects
        times = [datetime.combine(date.today(), time(*map(int, t.split(':')))) for t in time_strings]
    except:
        print(f'Error converting user-supplied times to datetimes {times}')
        raise e
    return current_time, icons, times

if __name__ == "__main__":
    current_time, icons, times = get_info()
    try:
        # Get the index of the next icon/time
        next_index = next(i for i, t in enumerate(times) if t > current_time)
        rollover = timedelta()
    except StopIteration:
        # If we're at the end of the list, use a rollover of one day
        next_index = 0
        rollover = timedelta(days=1)
    current_index = next_index - 1
    # If we're at the very start of the day, use a rollunder of one day
    rollunder = timedelta(days=1) if current_index < 0 else timedelta()

    # Get image to display
    img = get_screen(current_time,
                    times[current_index] - rollunder,
                    times[next_index] + rollover,
                    icons[current_index],
                    icons[next_index])
    display(img)
