from gpumeter import Meter
import time

if __name__ == "__main__":
    m = Meter(0.5)
    time.sleep(5)
    m.stop()