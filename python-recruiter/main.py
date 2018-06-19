# [START import_libraries]
import dialogflow
import os
import uuid

import audio
import data
import report
# [END import_libraries]


def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./resources/credentials/e3682f457e02.json"
    os.system("cls")
    project_id = "recruitertest-dd3ab"
    session_id = str(uuid.uuid4().hex[:12])
    language_code = "en-US"
    input_file_path = "./resources/audio/subject_input.wav"

    # [START DIALOG]
    complete_transcript = [[], []]

    # [QUICK DIALOG]
    # complete_transcript = detect_intent_texts(project_id, session_id, [
    #     "DEMO_START", "Diana Moon", "18", "Adaptable , ambitious, clever and blunt", "I have a bachelor in mathematics",
    #     "I have worked for Google as a data scientist of the past 3 years", "I am good at analysis and computers", "My communication is not great", "40 hours", "No"], language_code)

    # [NORMAL DIALOG]
    detect_intent_texts(project_id, session_id, [
        "DEMO_START"], language_code)
    while True:
        # text_input = input("Text input: ")
        # partial_transcript = detect_intent_texts(project_id, session_id, [
        #     text_input], language_code)

        audio.record(input_file_path)
        partial_transcript = detect_intent_audio(project_id, session_id,
                                                 input_file_path, language_code)

        # audio.record(input_file_path)
        # partial_transcript = detect_intent_stream(project_id, session_id,
        #                                           input_file_path, language_code)

        complete_transcript[0] = complete_transcript[0] + partial_transcript[0]
        complete_transcript[1] = complete_transcript[1] + partial_transcript[1]

        if poke(project_id, session_id, language_code):
            break

    # [END DIALOG]

    # [DATA]
    subject_info = get_subject_info(project_id, session_id, language_code)
    clean_subject_info = data.clean(subject_info)
    match_scores = data.match(subject_info)

    report.create(clean_subject_info, match_scores,
                  complete_transcript, session_id)


# [START dialogflow_detect_intent_text]


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    dialog_transcript = [[], []]
    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))

        dialog_transcript[0].append(response.query_result.query_text)
        dialog_transcript[1].append(response.query_result.fulfillment_text)

        audio.text_to_speech(response.query_result.fulfillment_text)

    return dialog_transcript
# [END dialogflow_detect_intent_text]

# [START dialogflow_detect_intent_audio]


def detect_intent_audio(project_id, session_id, input_file_path, language_code):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = audio.sample_rate()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    dialog_transcript = [[], []]
    with open(input_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    dialog_transcript[0].append(response.query_result.query_text)
    dialog_transcript[1].append(response.query_result.fulfillment_text)

    audio.text_to_speech(response.query_result.fulfillment_text)

    return dialog_transcript
# [END dialogflow_detect_intent_audio]

# [START dialogflow_detect_intent_streaming]


def detect_intent_stream(project_id, session_id, input_file_path, language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = audio.sample_rate()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))

    dialog_transcript = [[], []]

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, input_file_path)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
            response.recognition_result.transcript))

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))

    dialog_transcript[0].append(response.query_result.query_text)
    dialog_transcript[1].append(response.query_result.fulfillment_text)

    audio.text_to_speech(response.query_result.fulfillment_text)

    return dialog_transcript
# [END dialogflow_detect_intent_streaming]


def poke(project_id, session_id, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text="POKE", language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    try:
        if response.query_result.output_contexts[1].name[-10:] == "dialog-end":
            return True
    except:
        return False


def get_subject_info(project_id, session_id, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text="POKE", language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    required_parameters = ["given-name", "last-name", "age", "traits-positive", "traits-neutral", "traits-negative",
                           "college-degree", "college-major", "position", "experience", "strengths", "weaknesses", "hours"]

    subject_info = []

    for i in required_parameters:
        try:
            temp0 = response.query_result.output_contexts[0].parameters[i]
            subject_info.append(temp0)
        except:
            subject_info.append("None")

    return subject_info


if __name__ == '__main__':
    main()
