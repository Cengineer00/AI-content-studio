from faster_whisper import WhisperModel

model_size = "medium"
model = WhisperModel(model_size)

audiofilename = "shorts_deneme.mp3"

segments, info = model.transcribe(audiofilename, word_timestamps=True)
segments = list(segments)  # The transcription will actually run here.
for segment in segments:
    for word in segment.words:
        print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
