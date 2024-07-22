from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.config as mpy_config
from textwrap3 import wrap
import os
from dotenv import load_dotenv

#__________________________________Functions_______________________________________

def text_wrapper_function(screen_width, text, font_size, is_heading=False):
    # Calculate the maximum width for wrapping the text (accounting for padding)
    if is_heading:
        max_width = screen_width - 50  # 25 pixels padding on each side
    else:
        max_width = screen_width - 40  # 20 pixels padding on each side

    max_characters_per_line = max_width // (font_size // 2)  # Approximate character width
    wrapped_text_lines = wrap(text, width=max_characters_per_line)
    wrapped_text = "\n".join(wrapped_text_lines)
    return wrapped_text

def place_on_screen(heading_clip, text_clip, screen_height):
    # Get the height of the heading and description text clips
    heading_height = heading_clip.size[1]
    description_height = text_clip.size[1]

    # If sum of heading, description height and space is less than half of screen's height
    if (description_height + heading_height + 30) < (screen_height // 2):
        # Define vertical positions
        heading_vertical_position = screen_height // 2 - 100  # 100px above the center
        text_vertical_position = heading_vertical_position + heading_height + 30  # 30 pixels below the heading

        # Update position settings
        heading_clip = heading_clip.set_pos(('center', heading_vertical_position))
        text_clip = text_clip.set_pos(('center', text_vertical_position))
    else:
        # Define vertical positions
        heading_vertical_position = 50  # 50 pixels from the top
        text_vertical_position = heading_vertical_position + heading_height + 30  # 30 pixels below the heading

        # Update position settings
        heading_clip = heading_clip.set_pos(('center', heading_vertical_position))
        text_clip = text_clip.set_pos(('center', text_vertical_position))

    return heading_clip, text_clip

def add_text_to_video(video_path, heading, text, output_path, heading_font_size=40, text_font_size=30):
    # Load the video file
    clip = VideoFileClip(video_path)
    screen_width, screen_height = clip.size

    # Wrap the text to fit the screen width
    wrapped_heading = text_wrapper_function(screen_width, heading, heading_font_size, is_heading=True)
    wrapped_text = text_wrapper_function(screen_width, text, text_font_size)

    # Create TextClips with wrapped text
    heading_clip = TextClip(
        wrapped_heading,
        fontsize=heading_font_size,
        color='yellow',
        font='Weaselic.ttf',  # Use a standard font if custom font path is not needed
    ).set_duration(clip.duration)

    text_clip = TextClip(
        wrapped_text,
        fontsize=text_font_size,
        color='yellow',
        font='Weaselic.ttf',  # Use a standard font if custom font path is not needed
    ).set_duration(clip.duration)

    # Place the text clips on the screen
    heading_clip, text_clip = place_on_screen(heading_clip, text_clip, screen_height)

    # Combine VideoClip with both TextClips
    composite_clip = CompositeVideoClip([clip, heading_clip, text_clip])

    # Write the final video to a file
    composite_clip.write_videofile(output_path, fps=24)

    return True

#____________________________________________________________________________________

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Setting ImageMagick path
    mpy_config.change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

    # Example usage
    video_path = "superman.mp4"
    heading = "Mount Everest"
    text = 'Wow text that needs to be wrapped so that it fits within the screen width properly.'
    output_path = "output_video.mp4"

    add_text_to_video(video_path, heading, text, output_path)
