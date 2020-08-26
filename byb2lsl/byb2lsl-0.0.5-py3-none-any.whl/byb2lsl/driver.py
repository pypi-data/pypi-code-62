import serial
from serial.tools import list_ports
from pylsl import StreamInfo, StreamOutlet
import threading
import time
import numpy as np


def byb_byte_to_float(high: np.uint16, low: np.uint16) -> np.float32:
    return np.float32(np.uint16(np.uint8(low) + (np.uint8(high & 127) << 7)))


def convert_and_stream(outlet, ser, pause_dur, downsample: int):
    while True:
        # tstart = time.process_time()

        data_bytes = ser.read(2 * downsample)

        if len(data_bytes) > 0:
            if data_bytes[0] <= 127:
                data_bytes = data_bytes[1:]
                data_bytes += ser.read(1)

            data_float = [byb_byte_to_float(np.uint8(data_bytes[0]), np.uint8(data_bytes[1]))]
            # for i in range(chunksize):
            #     data_float.append(byb_byte_to_float(np.uint8(data_bytes[0]), np.uint8(data_bytes[1])))

            outlet.push_sample(data_float)

            #
            # elapsed_time = time.process_time() - tstart
            #
            # if pause_dur > elapsed_time:
            #     time.sleep((pause_dur - elapsed_time) / 2)

baudrate = 230_400
chunksize = 20
samplingrate = 10_000
downsample = 10
stream_name = 'ByB Heart&Brain'
stream_uid = "byb_heart_brain"
stream_mode = "EEG"
stream_type = "float32"
stream_nchan = 1
stream_chanrate = samplingrate / downsample


if __name__ == "__main__":
    ports = list_ports.comports()
    if len(ports) == 1:
        port = ports[0].device
    elif len(ports) < 1:
        raise(RuntimeError("No port connected."))
    else:
        for i, p in enumerate(ports):
            print(p.device)
        idx = input('Please enter port index:')
        try:
            port = ports[idx].device
        except IndexError:
            raise(IndexError("Invalid index"))

    info = StreamInfo(stream_name, stream_mode, stream_nchan, stream_chanrate, stream_type, stream_uid)
    outlet = StreamOutlet(info)

    s = "LSL Driver for the Backyard Brain Heart and Brain kit"
    print('#' * (len(s) + 4))
    print('# %s #'%s)
    print('#' * (len(s) + 4))

    with serial.Serial(port, baudrate, timeout=1) as ser:
        ser.read_until('\r')
        print("Connected to %s w/ baudrate %d. Sampling rate set to %dHz, downsampled by %d"%(port, baudrate, samplingrate, downsample ))

        print("Driver running.")
        print("# Stream properties: ")
        print("## name:", stream_name)
        print("## uid:", stream_uid)
        print("## mode:", stream_mode)
        print("## channels:", stream_nchan)
        print("## rate: %dHz" % stream_chanrate)
        print("## type:", stream_type)

        t = threading.Thread(target=convert_and_stream, args=(outlet, ser, downsample / samplingrate, downsample))

        t.run()
        t.join()