from PIL import Image, ImageDraw, ImageFont

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        if draw.textlength(test_line, font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines

def draw_text_centered(draw, lines, position, font, max_width, padding, fill='yellow'):
    y = position[1]

    for line in lines:
        text_width = draw.textlength(line, font)
        x = position[0] + (max_width - text_width) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += font.getsize('hg')[1] + padding

def get_wrapped_text_size(draw, lines, font, padding):
    line_height = font.getsize('hg')[1]
    total_height = len(lines) * (line_height + padding) - padding
    max_line_width = max(draw.textlength(line, font) for line in lines)
    return total_height, max_line_width

def dynamically_adjust_font(draw, text, font, max_width, max_height, padding):
    lines = wrap_text(draw, text, font, max_width)
    total_height, _ = get_wrapped_text_size(draw, lines, font, padding)
    while total_height > max_height and font.size > 10:
        font = ImageFont.truetype(font.path, font.size - 1)
        lines = wrap_text(draw, text, font, max_width)
        total_height, _ = get_wrapped_text_size(draw, lines, font, padding)
    return font, lines

if __name__ == '__main__':
    # Load the image
    image = Image.open('test.png')

    # Resize the image
    to_9_by_16 = image.resize((360, 740))

    # Get resized image dimensions
    image_width, image_height = to_9_by_16.size

    # Create a drawing object
    draw = ImageDraw.Draw(to_9_by_16)

    # Add a yellow border around the image
    draw.rectangle([(0, 0), (image_width - 1, image_height - 1)], outline='yellow', width=1)

    # Define fonts
    fonts = {
        "bold": ImageFont.truetype("Roboto/Roboto-Bold.ttf", 35),
        "medium": ImageFont.truetype("Roboto/Roboto-Medium.ttf", 40),
        "light": ImageFont.truetype("Roboto/Roboto-Light.ttf", 30),
        "thin": ImageFont.truetype("Roboto/Roboto-Thin.ttf", 30)
    }

    # Titles and descriptions
    title = "Top 5 mountains in the world"
    description = "Mount Everest"
    
    padding = 5
    margin_between = 50  # Margin between title and description
    safe_margin = 10  # Margin from the image edges

    # Dynamically adjust font size and wrap text
    title_font = fonts["bold"]
    max_title_width = image_width - 2 * safe_margin
    title_max_height = (image_height - 2 * safe_margin) // 2
    title_font, title_lines = dynamically_adjust_font(draw, title, title_font, max_title_width, title_max_height, padding)

    description_font = fonts["medium"]
    max_description_width = image_width - 2 * safe_margin
    description_max_height = (image_height - 2 * safe_margin) // 2
    description_font, description_lines = dynamically_adjust_font(draw, description, description_font, max_description_width, description_max_height, padding)

    # Calculate total text height
    title_total_height, _ = get_wrapped_text_size(draw, title_lines, title_font, padding)
    description_total_height, _ = get_wrapped_text_size(draw, description_lines, description_font, padding)
    total_text_height = title_total_height + margin_between + description_total_height

    # Positioning
    if total_text_height > image_height - 2 * safe_margin:
        print("Text does not fit within the image boundaries.")
    else:
        position = (safe_margin, safe_margin + (image_height - total_text_height) // 2 - 120)

        # Draw the rectangle behind the title
        rect_x0 = safe_margin
        rect_x1 = image_width - safe_margin
        rect_y0 = position[1] - padding
        rect_y1 = rect_y0 + title_total_height + 2 * padding
        draw.rectangle([(rect_x0, rect_y0), (rect_x1, rect_y1)], fill="yellow")

        # Draw wrapped and centered title
        draw_text_centered(draw, title_lines, (safe_margin, rect_y0 + padding), title_font, rect_x1 - rect_x0, padding, fill='black')

        # Update position for description
        position = (safe_margin, rect_y1 + margin_between)

        # Draw wrapped and centered description
        draw_text_centered(draw, description_lines, position, description_font, max_description_width, padding)

    # Display the image with added text
    to_9_by_16.show()
