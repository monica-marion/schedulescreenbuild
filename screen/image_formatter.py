from PIL import Image, ImageDraw

def crop_to_square(img_in):
    img = img_in.copy()
    img_width, img_height = img.size
    s = min(img_width, img_height)
    return img.crop(((img_width - s) // 2,
                     (img_height - s) // 2,
                     (img_width + s) // 2,
                     (img_height + s) // 2))

def convert_to_3_colors(img_in):
    img = img_in.copy()
    # Convert the image to RGB mode (if it's not already in that mode)
    img = img.convert("RGB")

    # Use the PIL image mode "P" to create a 3-color image
    # (also known as a "palette" image)
    palette = [
        0, 0, 0,
        255, 255, 255,
        255, 0, 0
    ]
    img = img.convert("P", palette=palette, colors=3)

    # Save the new image
    print(img.load()[0, 0])
    return img

def crop_to_circle(img_in, radius):
    img = img_in.copy()
    img = img.convert("RGB")
    img = crop_to_square(img)
    # Resize the image to fit inside the circle
    img.thumbnail((radius * 2, radius * 2), Image.Resampling.LANCZOS)
    print(img.size)

    # Create an alpha mask
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice((0, 0) + img.size, 0, 360, fill=255)

    # Apply the mask to the image
    img.putalpha(alpha)

    return img

def draw_semicircle(img_in, ratio, thickness):
    img = img_in.copy()

    # Create a drawing context
    draw = ImageDraw.Draw(img)
    arc_img = Image.new('RGBA', (2 * thickness + img.size[0], 2 * thickness + img.size[1]))
    arc = ImageDraw.Draw(arc_img)

    # Calculate the starting and ending angles of the semicircle
    # based on the specified ratio
    start_angle = -90
    end_angle = -90 + 360 * (ratio)

    # Calculate the coordinates of the center of the image
    center_x = img.width / 2
    center_y = img.height / 2

    # Calculate the bounding box of the semicircle
    bbox = (center_x - center_y, center_y - center_y, center_x + center_y, center_y + center_y)

    # Draw the semicircle on the image
    arc.pieslice((0, 0, arc_img.width, arc_img.height), start_angle, end_angle, fill=None, outline="red", width=thickness)
    arc_img.paste(img, (thickness, thickness), img)

    return arc_img

def get_icon(img_in, ratio):
    img = img_in.copy()
    img = img.convert("1")
    img = crop_to_circle(img, 100)
    img = draw_semicircle(img, ratio, 5)
    img = convert_to_3_colors(img)
    return img

if __name__ == "__main__":
    import notion_impl
    entries = notion_impl.get_entries()
    img = entries[0].get('image')
    if img == None:
        print("No image found for entry")
        exit(1)
    img.show()
    icon_img = get_icon(img, 0.96)
    icon_img.show()
