from moviepy import VideoFileClip, clips_array, CompositeAudioClip, ColorClip, CompositeVideoClip


"""
so if video resolution is 1920x1080 and the target resolution is 1080x1920 
there will be two videos of each with resolutions 1080x960, 1080x960, right? 
So I want to 1920x1080 video to fill 1080x960 without changing resolution. 
So the way to do it is to crop from sides and zoom a bit. We will zoom 1080/960 
then crop from left and right with the amounts of (1920*(960/1080) - 1080)/2. 
Can you do this?
"""

target_resolution = (1920, 1080)
target_resolution = (target_resolution[0]//8, target_resolution[1]//8)
target_width_per_clip = target_resolution[1]
target_height_per_clip = target_resolution[0] // 2

def merge_videos(video1_path, video2_path, t1_start, t1_end, t2_start, t2_end, 
                 output_path, line_color=(255,255,255), line_width=5):

    # Load and trim the clips
    clip1 = VideoFileClip(video1_path).subclipped(t1_start, t1_end)
    clip2 = VideoFileClip(video2_path).subclipped(t2_start, t2_end)

    def process_clip(clip: VideoFileClip):
        # Scale to height=960 (width becomes ~1706.67 for 1920x1080 input)
        scaled_clip = clip.resized(height=target_height_per_clip)
        
        # Calculate horizontal crop to center the clip
        scaled_width = scaled_clip.w
        crop_x = (scaled_width - target_width_per_clip) // 2
        
        # Crop to 1080x960
        return scaled_clip.cropped(
            x1=crop_x, 
            x2=crop_x + target_width_per_clip, 
            y1=0, 
            y2=target_height_per_clip
        )

    # Resize and crop to focus on the center (simulate "zoom")
    clip1_resized = process_clip(clip1)
    clip2_resized = process_clip(clip2)

    # Combine clips vertically
    merged_clip = clips_array([[clip1_resized], [clip2_resized]])


    # --- ADDED: Create divider line ---
    line = ColorClip(
        size=(target_width_per_clip, line_width),  # Horizontal line width = video width
        color=line_color,
        duration=merged_clip.duration
    )
    
    # Position line between the two clips
    line_position = (0, clip1_resized.h - line_width//2)  # Below first clip
    final_clip = CompositeVideoClip([merged_clip, line.with_position(line_position)])

    # Combine audio
    audio1 = clip1_resized.audio
    audio2 = clip2_resized.audio
    combined_audio = CompositeAudioClip([audio1, audio2])
    final_clip.audio = combined_audio

    # Write output
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
merge_videos(
    video1_path="Dumbledore.mp4",
    video2_path="Dumbledore.mp4",
    t1_start=10,  # Start time for video1 (seconds)
    t1_end=15,    # End time for video1
    t2_start=10,   # Start time for video2
    t2_end=20,    # End time for video2
    output_path="merged_output2.mp4",
    line_color=(255, 0, 0),  # Red divider
    line_width=3
)

