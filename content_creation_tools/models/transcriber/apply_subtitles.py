from moviepy import VideoFileClip, TextClip, CompositeVideoClip


def read_subtitles_from_file(file_path):
    """
    Read subtitles from a text file and return a list of [start_time, end_time, subtitle_text].
    """
    subtitles = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into components
            parts = line.strip().split(maxsplit=2)  # Split into 3 parts: start, end, text
            if len(parts) == 3:
                start_time = float(parts[0])
                end_time = float(parts[1])
                subtitle_text = parts[2]
                subtitles.append([start_time, end_time, subtitle_text])
    return subtitles

def add_subtitles_to_video(input_video_path, subtitles, output_video_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)
    
    # Create a list to hold all the text clips
    text_clips = []
    
    for start_time, end_time, subtitle_text in subtitles:
        # Calculate the duration for the subtitle
        duration = end_time - start_time
        
        # Create a TextClip with the subtitle text (customize font, color, etc.)
        txt_clip = TextClip(
            text=subtitle_text,
            font_size=24,
            font='Arial',
            color='white',
            stroke_color='black',
            stroke_width=1,
            size=(int(video_clip.w * 0.9), None),  # 70% of video width, auto height
            method='caption'
        )
        # Set the position, start time, and duration
        txt_clip = txt_clip.with_position(('center', 'top')).with_start(start_time).with_duration(duration)
        
        # Add the text clip to the list
        text_clips.append(txt_clip)
    
    # Overlay the text clips on the original video
    final_clip = CompositeVideoClip([video_clip] + text_clips)
    
    # Write the result to a file (match the video's fps)
    final_clip.write_videofile(output_video_path, fps=video_clip.fps, codec="libx264", audio_codec="aac")

# Example usage:
if __name__ == "__main__":
    subtitles_file = "subtitles.txt"
    subtitles = read_subtitles_from_file(subtitles_file)
    add_subtitles_to_video("shorts_deneme.mp4", subtitles, "shorts_deneme_subtitle.mp4")