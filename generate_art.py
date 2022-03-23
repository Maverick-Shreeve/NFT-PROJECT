
from PIL import Image, ImageChops, ImageDraw # pip installed pillow

import random

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return(
        int(start_color[0] * recip + end_color[0] * factor), # turned into ints because the multiplaction turns it into a float
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor),
    )

def generate_art(path: str):  # the path argument lets me generate multiple images at once
    print("Art is happening")
    image_size_px = 128
    padding_px = 8 # means 8% 
    image_bg_color = (0, 0, 0) # produces a black BG
    start_color = random_color()
    end_color = random_color()   
    image = Image.new("RGB", size = (image_size_px, image_size_px),color = (image_bg_color)) 
   
   #drawing on the empty pic
    draw= ImageDraw.Draw(image)
    points = []

    #generate the points
    for i in range(9):  # 9 is the amount of lines it draws
        random_point = (
            random.randint(padding_px, image_size_px - padding_px),
            random.randint(padding_px, image_size_px - padding_px), # - padding makes sure the lines arent on the edges of the picture
        )
        points.append(random_point)

        # draw a bounds box for the image
        
        min_x = min([p[0] for p in points])
        max_x = max([p[0] for p in points])
        min_y = min([p[1] for p in points])
        max_y = max([p[1] for p in points])
        draw.rectangle((min_x, min_y, max_x, max_y), outline = (200, 0, 0))
        #comment off this line ^^^ if you dont want the outer boxes for the drawing
        
        #center the drawing
        delta_x = min_x - (image_size_px - max_x)
        delta_y = min_y - (image_size_px - max_y)

        for i, point in enumerate(points):
            points[i] = (point[0]- delta_x // 2, point[1] - delta_y // 2)

       


    # draw the points (connects the points to make weird shapes)
    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):  # enumarate helps iterate through points
        
        # overlaying canvases for the lines on the drawing
        overlay_image = Image.new("RGB", size = (image_size_px, image_size_px),color = (image_bg_color))
        overlay_draw = ImageDraw.Draw(overlay_image)
        p1 = point
        
        if i == len(points) - 1: #checks if it is at he end of the list
            p2 = points[0]
        else:
            p2 = points [i + 1] # continues by 1 through list till it gets till last point

        line_xy = (p1, p2)
        color_factor =  i /n_points # gets a number betwwn 1 and 0 for our factor
        line_color = interpolate(start_color, end_color, color_factor)
        thickness +=1  # image progressively get thicker lines
        overlay_draw.line(line_xy, fill = line_color, width = thickness)
        image = ImageChops.add(image, overlay_image)  # ImageChops lets the images stack on eachother, letting the colors blend nicely


    image.save(path)

if __name__ == "__main__":
    for i in range (10):
        generate_art(f"test_image{i}.png")