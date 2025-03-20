from typing import List, Tuple
import os


def seconds_to_srt_time(time_seconds: float) -> str:
    """
    Convert seconds (float) to SRT time format: HH:MM:SS,mmm
    """
    total_milliseconds = int(round(time_seconds * 1000))
    milliseconds = total_milliseconds % 1000
    total_seconds = total_milliseconds // 1000
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def srt_time_to_seconds(time_str):
    """
    Convert SRT time format (HH:MM:SS,mmm) to seconds (float).
    """
    hours, minutes, rest = time_str.split(':', 2)
    seconds, milliseconds = rest.split(',', 1)
    return (
        int(hours) * 3600
        + int(minutes) * 60
        + int(seconds)
        + int(milliseconds) / 1000
    )

def write_srt_file(subtitles: List[Tuple[float, float, str]], output_file_path: str) -> None:
    """
    Convert a list of subtitles to .srt format and save to a file.
    """

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for index, (start, end, text) in enumerate(subtitles, start=1):
            # Convert start and end times to SRT format
            start_srt = seconds_to_srt_time(start)
            end_srt = seconds_to_srt_time(end)
            
            # Write the subtitle entry
            file.write(f"{index}\n")
            file.write(f"{start_srt} --> {end_srt}\n")
            file.write(f"{text}\n\n")

def read_srt_file(file_path):
    """
    Read an SRT file and return a list of subtitles in the format:
    [[start_time, end_time, subtitle_text], ...]
    """
    subtitles = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        blocks = content.split('\n\n')  # Split into subtitle blocks
        
        for block in blocks:
            lines = block.strip().split('\n')  # Split block into lines
            
            # Skip invalid blocks (must have at least 3 lines: index, time, text)
            if len(lines) < 3:
                continue
            
            # Parse the time line (e.g., "00:00:00,000 --> 00:00:00,980")
            time_line = lines[1].strip()
            if '-->' not in time_line:
                continue  # Skip malformed time lines
            
            start_str, end_str = time_line.split(' --> ')
            start = srt_time_to_seconds(start_str)
            end = srt_time_to_seconds(end_str)
            
            # Join text lines and strip whitespace
            text = ' '.join(line.strip() for line in lines[2:])
            
            subtitles.append([start, end, text])
    
    return subtitles
