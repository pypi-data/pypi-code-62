#! /usr/bin/env python

def luminance(color):
    """ Relative luminance of the color """
    unit_red = color.red / 255.0
    unit_green = color.green / 255.0
    unit_blue = color.blue / 255.0

    if unit_red <= 0.03928:
        lum_red = unit_red / 12.92
    else:
        lum_red = ((unit_red + 0.055) / 1.055) ** 2.4
    if unit_green <= 0.03928:
        lum_green = unit_green / 12.92
    else:
        lum_green = ((unit_green + 0.055) / 1.055) ** 2.4
    if unit_blue <= 0.03928:
        lum_blue = unit_blue / 12.92
    else:
        lum_blue = ((unit_blue + 0.055) / 1.055) ** 2.4
        
    return 0.2126*lum_red + 0.7152*lum_green + 0.0722*lum_blue

def contrast(bcolor, color):
    """ Contrast between two colors """
    if luminance(bcolor) > luminance(color):
        return (luminance(bcolor) + 0.05) / (luminance(color) + 0.05)
    else:
        return (luminance(color) + 0.05) / (luminance(bcolor) + 0.05)

