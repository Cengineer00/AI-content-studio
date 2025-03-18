def parse_subtitles(file_path = "test.txt"):
    """
    Read subtitles from a file in the specified format and return a list of lists:
    [[start_time1, end_time1, subtitle1], ...]
    """
    subtitles = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Extract the time range and subtitle text
            time_range, subtitle_text = line.split(']', 1)  # Split on the first ']'
            time_range = time_range.strip('[')  # Remove the leading '['
            start_time, end_time = time_range.split(' -> ')  # Split into start and end times
            
            # Remove the 's' from the times and convert to float
            start_time = float(start_time.rstrip('s'))
            end_time = float(end_time.rstrip('s'))
            
            # Strip any leading/trailing whitespace from the subtitle text
            subtitle_text = subtitle_text.strip()
            
            # Append to the subtitles list
            subtitles.append([start_time, end_time, subtitle_text])
    
    return subtitles

def merge_segments(segments, max_chars_per_line=30):
    lines = []
    current_line = ""
    current_start = segments[0][0]
    for i in range(len(segments)):
        current_word = segments[i]
        next_word = segments[i + 1] if i + 1 < len(segments) else None

        # Check if next word will exceed the max_chars_per_line or current_word ends with punctuation
        if next_word is not None and (len(current_line) + len(next_word[2]) > max_chars_per_line or current_word[2].endswith((",", ".", "!", "?"))):
            line = current_line + current_word[2].strip()
            lines.append([current_start, current_word[1], line])
            current_line = ""
            current_start = next_word[0]
            continue
        current_line += current_word[2].strip() + " "
            
    # Add the last line
    if current_line:
        lines.append([current_start, current_word[1], current_line])
    return lines

def write_subtitles_to_file(subtitles, file_path):
    """
    Write subtitles to a text file in the format:
    start_time end_time subtitle_text
    """
    with open(file_path, 'w') as file:
        for start_time, end_time, subtitle_text in subtitles:
            # Write the line in the specified format
            file.write(f"{start_time} {end_time} {subtitle_text}\n")

subtitle_segments = parse_subtitles()

merged_segments = merge_segments(subtitle_segments)
print(merged_segments)
subtitles_file = "subtitles.txt"
write_subtitles_to_file(merged_segments, subtitles_file)
print(f"Subtitles saved to {subtitles_file}")