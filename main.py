import asyncio
from time import sleep
from detection import Detection

if __name__ == '__main__':
    detection = Detection()
    asyncio.run(detection.run())
    while True:
        sleep(60)
