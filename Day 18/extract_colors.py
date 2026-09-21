###This code will not work in repl.it as there is no access to the colorgram package here.###
##We talk about this in the video tutorials##
import colorgram

def extract_colors():
    rgb_colors = []
    colors = colorgram.extract('image.jpg', 30)
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        new_color = (r, g, b)
        rgb_colors.append(new_color)
    return rgb_colors