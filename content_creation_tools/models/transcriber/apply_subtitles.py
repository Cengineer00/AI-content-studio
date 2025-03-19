from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip


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

def add_subtitles_to_video(
    input_video_path,
    subtitles,
    output_video_path,
    font="Arial_Bold",
    font_size=14,
    color="white",
    bg_color=(0, 0, 0),
    bg_opacity=0.6,
    stroke_color="black",
    stroke_width=1,
    position=("center", "bottom"),
    padding=(20, 10),
):
    """
    Add styled subtitles to a video with customizable font, background, and more.
    
    Args:
        input_video_path (str): Path to the input video.
        subtitles (list): List of [[start_time, end_time, subtitle_text], ...].
        output_video_path (str): Path to save the output video.
        font (str): Font name (e.g., "Arial-Bold").
        fontsize (int): Font size.
        color (str): Text color (hex or name).
        bg_color (float): Background color (RGB).
        bg_opacity (float): Background opacity (0.0 to 1.0).
        stroke_color (str): Text stroke/border color.
        stroke_width (int): Stroke width.
        position (tuple): Text position (e.g., ("center", "bottom")).
        padding (tuple): Background padding (horizontal, vertical).
    """
    # Load the video
    video = VideoFileClip(input_video_path)
    video_w, video_h = video.size
    
    # List to hold all subtitle clips (background + text)
    subtitle_clips = []
    
    for start_time, end_time, text in subtitles:
        duration = end_time - start_time
        
        # Create TextClip with styling
        txt_clip = TextClip(
            font=font,
            text=text,
            font_size=font_size,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            # size=(int(video_w * 0.9), None),  # 90% width, auto height
            # method="caption",  # Auto-wrap text
        ).with_duration(duration)
        
        # Calculate background size (text size + padding)
        text_w, text_h = txt_clip.size
        bg_w = text_w + padding[0]
        bg_h = text_h + padding[1]
        
        # Create background clip (semi-transparent)
        bg_clip = ColorClip(
            size=(bg_w, bg_h),
            color=bg_color,
            duration=duration,
        ).with_opacity(bg_opacity)
        
        # Composite text over background
        combined_clip = CompositeVideoClip([bg_clip, txt_clip.with_position("center")])
        
        # Position the combined clip (center-bottom by default)
        combined_clip = combined_clip.with_position(position).with_start(start_time)
        
        subtitle_clips.append(combined_clip)
    
    # Overlay all subtitles on the video
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    # Export the video
    final_video.write_videofile(output_video_path, fps=video.fps, codec="libx264")

# Example usage:
if __name__ == "__main__":
    subtitles_file = "subtitles.txt"
    subtitles = read_subtitles_from_file(subtitles_file)
    add_subtitles_to_video("shorts_deneme.mp4", subtitles, "shorts_deneme_subtitle.mp4", position=("center", "bottom"))