from VSBscrape import seatsavailability
import time

time_interval = 10  # Number of minutes between each scrape

while True:
    seatsavailability("Winter 2022", "MECH", "360")
    time.sleep(time_interval*60)
