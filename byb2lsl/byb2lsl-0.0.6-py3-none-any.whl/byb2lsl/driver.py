import serial
from serial.tools import list_ports
from pylsl import StreamInfo, StreamOutlet
from datetime import datetime
import threading
import numpy as np
import argparse


def byb_byte_to_float(high: np.uint8, low: np.uint8) -> np.float32:
    return np.float32(np.uint16(np.uint8(low) + (np.uint8(high & 127) << 7)))


def convert_and_stream(outlet: StreamOutlet, ser: serial.Serial, downsample: int, debug: bool, keyboard_int: threading.Event):
    # A thread is used here but can be replaced by a simple while loop in the main function
    while not keyboard_int.is_set():
        data_bytes = ser.read(2 * downsample)

        if len(data_bytes) > 0:
            if data_bytes[0] <= 127:
                data_bytes = data_bytes[1:]
                data_bytes += ser.read(1)

            data_float = [byb_byte_to_float(np.uint8(data_bytes[0]), np.uint8(data_bytes[1]))]
            outlet.push_sample(data_float)

            if debug:
                print("(%s): sent %.3f"%(datetime.now().strftime("%H:%M:%S.%f"), data_float[0]))


DEFAULTS = {
    "baudrate": 230_400,
    "sampling_rate": 10_000,
    "downsampling_factor": 10,
    "stream_name": "ByB Heart&Brain",
    "stream_uid" : "byb_heart_brain",
    "stream_mode" : "EEG",
    "stream_type" : "float32",
    "stream_nchan" : 1
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A driver to stream EEG data from the Backyard Brain Heart & Brain kit"
                                                 " to the Lab Streaming Layer")

    parser.add_argument("-P", "--port", dest="port", type=str, default=None,
                        help="The serial port to read from")
    parser.add_argument("-B", "--baudrate",  dest="baudrate", type=int, default=DEFAULTS['baudrate'],
                        help="Baudrate configuration for the serial port")
    parser.add_argument("-S", "--srate", dest='sampling_rate', type=int, default=DEFAULTS['sampling_rate'] ,
                        help="Heart & Brain kit sampling rate")
    parser.add_argument("-D", "--downsampling_factor", dest="downsample",  type=int,
                        default=DEFAULTS['downsampling_factor'], help="Integer downsampling factor")
    parser.add_argument("-N", "--name", dest="stream_name", type=str, default=DEFAULTS['stream_name'],
                        help="Name of the LSL stream")
    parser.add_argument("-U", "--uid", dest="stream_uid", type=str, default=DEFAULTS['stream_uid'],
                        help="UID of the LSL stream")
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help="Print data sent to LSL to the standard output")

    args = parser.parse_args()
    if args.port is None:
        # Find connected ports
        ports = list_ports.comports()
        if len(ports) == 1:
            # Use the only connected one
            port = ports[0].device
        elif len(ports) < 1:
            raise(RuntimeError("No port connected."))
        else:
            # Or ask for user input
            for i, p in enumerate(ports):
                print(p.device)
            idx = input('Please enter port index:')
            try:
                port = ports[idx].device
            except IndexError:
                raise(IndexError("Invalid index"))
    else:
        port = args.port

    # Extract user args
    baudrate = args.baudrate
    downsample = args.downsample
    stream_name = args.stream_name
    stream_uid = args.stream_uid
    sampling_rate = args.sampling_rate
    debug = args.debug

    # Set default parameters
    stream_mode = DEFAULTS['stream_mode']
    stream_nchan = DEFAULTS['stream_nchan']
    stream_chanrate = int(sampling_rate / downsample)
    stream_type = DEFAULTS['stream_type']

    # Open LSL stream
    info = StreamInfo(stream_name, stream_mode, stream_nchan, stream_chanrate, stream_type, stream_uid)
    outlet = StreamOutlet(info)

    # Print info to user
    s = "LSL Driver for the Backyard Brain Heart and Brain kit"
    print('#' * (len(s) + 4))
    print('# %s #'%s)
    print('#' * (len(s) + 4))

    # Open the serial port
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # Read the first line until carriage return
        ser.read_until('\r')
        print("Connected to %s w/ baudrate %d. Sampling rate set to %dHz, downsampled by %d"%(port, baudrate, sampling_rate, downsample ))

        # Print connexion info
        print("Driver running.")
        print("# Stream properties: ")
        print("## name:", stream_name)
        print("## uid:", stream_uid)
        print("## mode:", stream_mode)
        print("## channels:", stream_nchan)
        print("## rate: %dHz" % stream_chanrate)
        print("## type:", stream_type)

        keyboard_int = threading.Event()

        # Prepare and launch the thread
        t = threading.Thread(target=convert_and_stream, args=(outlet, ser, downsample, debug, keyboard_int))

        # Start the thread
        t.start()

        while not keyboard_int.is_set():
            try:
                pass
            except KeyboardInterrupt:
                keyboard_int.set()

        # Wait for the thread to exit
        t.join(1)
