import numpy as np
import librosa
from moviepy.editor import VideoFileClip, concatenate_videoclips

def detect_silence(audio_path, threshold_db=-30, min_silence_duration=0.5):
    """Detect silent intervals in audio"""
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    
    # Calculate short-term energy
    energy = librosa.feature.rms(y=y)
    times = librosa.times_like(energy, sr=sr)
    
    # Convert to dB
    energy_db = librosa.amplitude_to_db(energy, ref=np.max)
    
    # Find silent intervals
    silent_intervals = []
    in_silence = False
    start_time = 0
    
    for i, db in enumerate(energy_db[0]):
        if db < threshold_db and not in_silence:
            start_time = times[i]
            in_silence = True
        elif db >= threshold_db and in_silence:
            end_time = times[i]
            if (end_time - start_time) >= min_silence_duration:
                silent_intervals.append((start_time, end_time))
            in_silence = False
            
    return silent_intervals

def remove_silence_from_video(input_path, output_path, 
                            threshold_db=-30, 
                            min_silence_duration=0.5,
                            padding=0.2):
    """Remove silent intervals from video"""
    # Load video
    video = VideoFileClip(input_path)
    
    # Extract audio for analysis
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    
    # Detect silent intervals
    silent_intervals = detect_silence(audio_path, threshold_db, min_silence_duration)
    
    # Create clips of non-silent parts
    clips = []
    last_end = 0
    
    for start, end in silent_intervals:
        # Add padding around silence
        clip_start = max(last_end - padding, 0)
        clip_end = start + padding
        
        if clip_start < clip_end:
            clips.append(video.subclip(clip_start, clip_end))
        last_end = end
    
    # Add remaining part after last silence
    if last_end < video.duration:
        clips.append(video.subclip(last_end))
    
    # Concatenate and save
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path,
                         codec="libx264",
                         audio_codec="aac",
                         preset="medium",
                         threads=8)
    
    # Cleanup
    video.close()
    final_clip.close()
    os.remove(audio_path)

# Usage
remove_silence_from_video(
    input_path="input_podcast.mp4",
    output_path="output_edited.mp4",
    threshold_db=-25,       # Adjust based on your recording
    min_silence_duration=0.3,  # Minimum silence duration to cut
    padding=0.1             # Padding around silence for smooth cuts
)