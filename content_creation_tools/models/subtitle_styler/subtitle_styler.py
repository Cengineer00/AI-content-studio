from content_creation_tools.core import BaseModel
from content_creation_tools.utils import read_srt_file

from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from typing import Dict, Any
import os


class SubtitleStyler(BaseModel):
    def __init__(self):
        super().__init__("SubtitleStyler")
        
        self.parameter_schema = {
            'font': {
                'type': str,
                'description': 'Font name (e.g., "Arial-Bold").',
                'default': 'Arial_Bold'
            },
            'font_size': {
                'type': int,
                'description': 'Font size.',
                'default': 14
            },
            'color': {
                'type': str,
                'description': 'Text color (hex or name).',
                'default': 'white'
            },
            'bg_color': {
                'type': tuple,
                'description': 'Background color (RGB).',
                'default': (0, 0, 0)
            },
            'bg_opacity': {
                'type': float,
                'description': 'Background opacity (0.0 to 1.0).',
                'default': 0.6
            },
            'stroke_color': {
                'type': str,
                'description': 'Text stroke/border color.',
                'default': 'red'
            },
            'stroke_width': {
                'type': int,
                'description': 'Stroke width.',
                'default': 1
            },
            'position': {
                'type': tuple,
                'description': 'Text position (e.g., ("center", "bottom", "top")).',
                'default': ("center", "bottom")
            },
            'padding': {
                'type': tuple,
                'description': 'Background padding (horizontal, vertical).',
                'default': (10, 5)
            },
        }
        
    def get_input(self) -> dict:
        """
        Get subtitles path and video path from user.
        Validates both paths exist and are files.
        Returns dictionary with paths or error message.
        
        Returns:
            dict: {
                "subtitle_path": str, 
                "video_path": str
            } or {"error": str}
        """
        # Get subtitles path
        while True:
            subtitle_path = input("Enter subtitles file path (.srt): ").strip()
            if os.path.isfile(subtitle_path):
                break
            print("Subtitle file not found or invalid path")
        
        # Get video path
        while True:
            video_path = input("Enter video file path: ").strip()
            if os.path.isfile(video_path):
                break
            print("Video file not found or invalid path")
        
        return {
            "subtitle_path": subtitle_path,
            "video_path": video_path
        }
    
    def generate(self, params: Dict[str, Any], video_path: str, subtitle_path: str = None, subtitles: list = None) -> CompositeVideoClip:
        """
            Generate a video with subtitles
            take either subtitle_path or subtitles as input
        """

        if subtitles is None:
            subtitles = read_srt_file(subtitle_path)
            
        return self._add_subtitles_to_video(
            video_path,
            subtitles,
            params['font'],
            params['font_size'],
            params['color'],
            params['bg_color'],
            params['bg_opacity'],
            params['stroke_color'],
            params['stroke_width'],
            params['position'],
            params['padding']
        )

    def _add_subtitles_to_video(
            self,
            video_path,
            subtitles,
            font="Arial_Bold",
            font_size=14,
            color="white",
            bg_color=(0, 0, 0),
            bg_opacity=0.6,
            stroke_color="red",
            stroke_width=1,
            position=("center", "bottom"),
            padding=(10, 5),
    ):
        """
        Add styled subtitles to a video with customizable font, background, and more.
        
        Args:
            video_path (str): Path to the input video.
            subtitles (list): List of [[start_time, end_time, subtitle_text], ...].
            font (str): Font name (e.g., "Arial-Bold").
            font_size (int): Font size.
            color (str): Text color (hex or name).
            bg_color (float): Background color (RGB).
            bg_opacity (float): Background opacity (0.0 to 1.0).
            stroke_color (str): Text stroke/border color.
            stroke_width (int): Stroke width.
            position (tuple): Text position (e.g., ("center", "bottom")).
            padding (tuple): Background padding (horizontal, vertical).
        """

        # Load the video
        video = VideoFileClip(video_path)
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

        return final_video