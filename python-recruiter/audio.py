import threading
import pyaudio
import wave


def record(subject_input):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = sample_rate()
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = subject_input

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    def record_service(frames):
        print("* START RECORDING *")

        while recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #     data = stream.read(CHUNK)
        #     frames.append(data)

        print("* END RECORDING *")

    input("Press ENTER to START talking.")

    frames = []

    recording = True
    record_thread = threading.Thread(
        name="record_service", target=record_service, args=(frames, ))
    record_thread.start()
    input("Press ENTER to STOP talking.")
    recording = False

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def sample_rate():
    p = pyaudio.PyAudio()
    sample_rate = p.get_device_info_by_index(0)["defaultSampleRate"]
    p.terminate()

    return int(sample_rate)
