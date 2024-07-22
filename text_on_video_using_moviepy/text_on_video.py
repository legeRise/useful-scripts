from moviepy.editor import VideoFileClip
import moviepy.config as mpy_config
from textwrap3 import wrap
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
from dotenv import load_dotenv



#__________________________________functions_______________________________________

# Wrap the text using textwrap3
def text_wrapper_function(screen_width, text,font_size,is_heading=False):

    # Calculate the maximum width for wrapping the text (accounting for padding)
    if is_heading:
        max_width = screen_width - 50  # 25 pixels padding on each side
    else:
        max_width = screen_width - 40  # 20 pixels padding on each side

    max_characters_per_line = max_width // (font_size // 2) #the space a character  takes on screen is roughly half
    # the fontsize, so dividing font_size by 2 gives us the width of a single character on screen which we divide
    #  by max_width to get total count of possible characters on screen
    
    wrapped_text_lines = wrap(text, width=max_characters_per_line)
    wrapped_text = "\n".join(wrapped_text_lines)
    return wrapped_text

# place the heading and description on screen
def place_on_screen(heading_clip,text_clip,screen_height):

    # Get the height of the heading text clip
    heading_height = heading_clip.size[1]

    print(heading_height,'heading height')

    # Get the height of the description text clip
    description_height = text_clip.size[1]
    print(description_height,'description height')

    # if sum of heading, description height and the 30px space height is less than half of screen's height
    # then heading should start at a little above the center
    if (description_height + heading_height +30) < (screen_height //2):  

        # Define vertical positions
        heading_vertical_position = screen_height //2 -100   # 100px little above the center
        text_vertical_position = heading_vertical_position + heading_height + 30  # 30 pixels below the heading

        # Update position settings
        heading_clip = heading_clip.set_pos(('center', heading_vertical_position))
        text_clip = text_clip.set_pos(('center', text_vertical_position))
    
    else:
        # Define vertical positions
        heading_vertical_position = 50   # 50 pixels from the top
        text_vertical_position = heading_vertical_position + heading_height + 30  # 30 pixels below the heading

        # Update position settings
        heading_clip = heading_clip.set_pos(('center', heading_vertical_position))
        text_clip = text_clip.set_pos(('center', text_vertical_position))

    return heading_clip,text_clip





#__________________________________________________________________________________________________


if __name__ == '__main__':

    # Load environment variables from .env file
    load_dotenv()

    # setting imagemagick path
    mpy_config.change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})


    # Load a video file
    clip = VideoFileClip("superman.mp4")
    screen_width, screen_height = clip.size


    # text
    heading = "Mount Everest"
    heading_font_size = 40  # Adjust fontsize as needed
    
    text = ' wow text that needs to be wrapped so that it fits within the screen width properly so that it fits within the screen width properly so that it fits within'
    text_font_size = 30  # Adjust fontsize as needed


    # wrapping the overlay text w.r.t screen_size
    wrapped_heading = text_wrapper_function(screen_width,heading,heading_font_size,is_heading=True)
    wrapped_text = text_wrapper_function(screen_width,text,text_font_size)

    

    # Create TextClip with heading wrapped text
    heading_clip = TextClip(
        wrapped_heading,
        fontsize=heading_font_size,
        color='yellow',
        font='Weaselic.ttf',  # Use a standard font if custom font path is not needed
    ).set_duration(clip.duration)


    # Create TextClip with wrapped text (description)
    text_clip = TextClip(
        wrapped_text,
        fontsize=text_font_size,
        color='yellow',
        font='Weaselic.ttf',  # Use a standard font if custom font path is not needed
    ).set_duration(clip.duration)
    
    heading_clip, text_clip = place_on_screen(heading_clip,text_clip,screen_height)


    # Combine VideoClip with both TextClips
    composite_clip = CompositeVideoClip([clip, heading_clip,text_clip])  

    # Write the final video to a file
    composite_clip.write_videofile("output_video.mp4", fps=24)

