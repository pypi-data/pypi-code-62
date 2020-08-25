import serial
from serial.tools import list_ports
from pylsl import StreamInfo, StreamOutlet, local_clock
import threading
import time


def byb_byte_to_float(high, low):
    return float(int(low) + (int(high) & 127) << 7)


def convert_and_stream(outlet, ser, pause_dur):
    while True:
        data_bytes = ser.read(2 * chunksize)

        tstart = time.process_time()

        if len(data_bytes) > 0:
            if data_bytes[0] < 127:
                data_bytes = data_bytes[1:]
                data_bytes += ser.read(1)

            data_float = []
            for i in range(chunksize):
                data_float.append(byb_byte_to_float(data_bytes[0], data_bytes[1]))

            elapsed_time = time.process_time() - tstart
            outlet.push_chunk(data_float)


            if pause_dur > elapsed_time:
                time.sleep((pause_dur - elapsed_time))


baudrate = 230_400
chunksize = 32
samplingrate = 10_000.
channelrate = 10_000


if __name__ == "__main__":

    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 1 channels, 10000 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover).
    info = StreamInfo('ByB Heart&Brain', 'EEG', 1, channelrate, 'float32', 'byb_heart_brain')

    # next make an outlet
    outlet = StreamOutlet(info)

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

    with serial.Serial(port, baudrate, timeout=1) as ser:
        t = threading.Thread(target=convert_and_stream, args=(outlet, ser, chunksize / samplingrate))
        t.run()
        t.join()