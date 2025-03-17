from moviepy import VideoFileClip, clips_array, CompositeAudioClip, ColorClip, CompositeVideoClip, AudioFileClip
import tempfile
import subprocess
import argparse


def speed_up_with_pitch_correction(clip, speed_factor):
    """Speed up video with pitch correction using temp files"""

    if speed_factor == 1.0:
        return clip
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create temp file paths
        input_path = f"{tmp_dir}/input.mp4"
        output_path = f"{tmp_dir}/output.mp4"
        
        # Write original clip to temp file
        clip.write_videofile(input_path, logger=None)
        
        # Build FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-vf', f'setpts={1/speed_factor}*PTS',
            '-af', f'atempo={speed_factor}',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-pix_fmt', 'yuv420p',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', '+faststart',
            output_path
        ]
        
        # Run FFmpeg
        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Return processed clip
        return VideoFileClip(output_path)

def merge_videos(video1_path, video2_path, t1_start, t1_end, t2_start, t2_end, 
                 output_path, line_color=(255,255,255), line_width=5, target_resolution=(1920, 1080)):

    target_width_per_clip = target_resolution[1]
    target_height_per_clip = target_resolution[0] // 2

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
    speed_factor = 1.01
    clip1_resized = process_clip(clip1)
    clip2_resized = process_clip(clip2)

    clip1_resized = speed_up_with_pitch_correction(clip1_resized, speed_factor)
    clip2_resized = speed_up_with_pitch_correction(clip2_resized, speed_factor)

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


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process and merge two video clips with a divider line.")
    
    parser.add_argument("--video1_path", type=str, default="main.mov", help="Path to the first video.")
    parser.add_argument("--video2_path", type=str, default="main.mov", help="Path to the second video.")
    parser.add_argument("--t1_start", type=int, default=0, help="Start time for the first video (seconds).")
    parser.add_argument("--t1_end", type=int, default=5, help="End time for the first video (seconds).")
    parser.add_argument("--t2_start", type=int, default=0, help="Start time for the second video (seconds).")
    parser.add_argument("--t2_end", type=int, default=5, help="End time for the second video (seconds).")
    parser.add_argument("--output_path", type=str, default="merged_output.mp4", help="Output file path.")
    parser.add_argument("--line_color", type=int, nargs=3, default=(255, 0, 0), help="RGB color of the divider line.")
    parser.add_argument("--line_width", type=int, default=3, help="Width of the divider line in pixels.")
    parser.add_argument("--target_resolution", type=int, nargs=2, default=(1080, 1920), help="Target resolution for the output video.")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    merge_videos(
        video1_path=args.video1_path,
        video2_path=args.video2_path,
        t1_start=args.t1_start,
        t1_end=args.t1_end,
        t2_start=args.t2_start,
        t2_end=args.t2_end,
        output_path=args.output_path,
        line_color=args.line_color,
        line_width=args.line_width,
        target_resolution=args.target_resolution
    )
