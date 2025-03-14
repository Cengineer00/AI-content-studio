from moviepy import VideoFileClip, clips_array, CompositeAudioClip


def merge_videos(video1_path, video2_path, t1_start, t1_end, t2_start, t2_end, output_path):
    # Load and trim the clips
    clip1 = VideoFileClip(video1_path).subclipped(t1_start, t1_end)
    clip2 = VideoFileClip(video2_path).subclipped(t2_start, t2_end)
    
    # Resize clips to have the same height (adjust width proportionally)
    target_height = min(clip1.h, clip2.h)
    clip1_resized = clip1.resized(height=target_height)
    clip2_resized = clip2.resized(height=target_height)
    
    # Combine clips horizontally
    # merged_clip = clips_array([[clip1_resized, clip2_resized]])

    # Combine clips vertically
    merged_clip = clips_array([[clip1_resized], [clip2_resized]])

    # Combine audio tracks
    audio1 = clip1_resized.audio
    audio2 = clip2_resized.audio
    combined_audio = CompositeAudioClip([audio1, audio2])  # Mix both audios
    
    # Set the combined audio to the merged clip
    merged_clip.audio = combined_audio
    
    # Write the result to a file
    merged_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
merge_videos(
    video1_path="Dumbledore.mp4",
    video2_path="Dumbledore.mp4",
    t1_start=10,  # Start time for video1 (seconds)
    t1_end=15,    # End time for video1
    t2_start=10,   # Start time for video2
    t2_end=20,    # End time for video2
    output_path="merged_output.mp4"
)

