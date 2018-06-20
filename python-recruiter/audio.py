import threading
import pyaudio
import requests
import wave


def record(audio_file_path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = sample_rate()
    # RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = audio_file_path

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


def text_to_speech(text_input, voice="en-US_AllisonVoice"):
    CHUNK = 1048
    WIDTH = 2
    CHANNELS = 1
    RATE = 22050
    ACCEPT = 'audio/wav'
    URL = "https://stream.watsonplatform.net/text-to-speech/api/"
    USER = "82c893a4-4ff8-41d1-9c53-42123723d6aa"
    PASS = "yqrObzqShtQo"

    req = requests.get(URL + "/v1/synthesize", auth=(USER, PASS), params={
        "text": text_input, "voice": voice, "accept": ACCEPT}, stream=True, verify=True)

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    bytes_read = 0
    data_read = b''

    for data in req.iter_content(1):
        data_read = data_read + data
        bytes_read = bytes_read + 1

        if bytes_read % CHUNK == 0:
            stream.write(data_read)
            data_read = b''

    stream.stop_stream()
    stream.close()
    p.terminate()


def sample_rate():
    p = pyaudio.PyAudio()
    sample_rate = p.get_device_info_by_index(0)["defaultSampleRate"]
    p.terminate()

    return int(sample_rate)
