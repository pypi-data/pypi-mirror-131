# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 23:04:17 2021

@author: chris
"""



import math
import cairo
from PIL import Image
from matplotlib.colors import cnames, to_rgb
#from os import remove

class krueger_gauge_circular_chart():
    
    """
    Creates Krüger Gauge Circular Charts
    insert data in dict form
    data_dict = {name:(value_length, value_width), ..}
    """
    
    def __init__(self, data_dict, height = 2000, width = 2000, background_color = (0.3, 0.3, 0.3), max_width = 80, max_length = 1.5 * math.pi, spacing = 20, radius = 200, max_value = None, transparent_background = False):
        #set settings
        self.height = height    #hieght of canvas
        self.width = width      #length of canvas
        self.center = (self.width/2, self.height/2)
        self.dict = data_dict   #datadict
        self.rings = len(self.dict)
        self.background_color = background_color    #set background color
        self.max_width = max_width                  #set maximum width of bar
        self.spacing = spacing                      #set spacing between bars
        self.max_length = max_length                #set maximum length of the bar (in radian)
        self.font_size = self.max_width / 2
        self.radius = radius                        #set the radius of the graph
        self.max_value = max_value                  #set maximum value the bar can have
        self.transparent_background = transparent_background
        
        #get a color scheme
        self.list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
                              (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188), (197, 239, 247), (190, 144, 212),
                              (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]
        
        #adjust for values between zero and one
        new_list = []
        for item in self.list_of_colors:
            r, g, b = item
            new_list.append((r/255, g/255, b/255))
        self.list_of_colors = new_list
            
        
        
        #seperate dict tuples data for easier access later
        self.length_array = []
        self.width_array = []
        self.name_list = []
        for num, (name, tuple_val) in enumerate(self.dict.items()):
            self.length_array.append(tuple_val[0])
            self.width_array.append(tuple_val[1])
            self.name_list.append(name)
        
        
        #set image
        
        #create class instances
        self.image_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height) #image surface
        self.cr = cairo.Context(self.image_surface)
        
        #draw background if it isn't transparent
        if not self.transparent_background:
            r, g, b = self.background_color
            self.cr.set_source_rgb(r,g,b)
            self.cr.rectangle(0, 0, self.width, self.height)
            self.cr.fill()
        
        
        
    def __str__(self):
        """
        prints the class instance
        """
        return f"This is a Krüger-Gauge-Chart with {self.rings} elements"
    
    
    
    def save_image_as_png(self, name = "krueger_gauge_chart.png"):
        """
        saves image as png, path can be specified under name
        """
        self.image_surface.write_to_png(name)  # Output to PNG
        
        
        
        
    def save_and_display_image(self, name = "krueger_gauge_chart.png"):
        """
        saves the image and displays it afterwards. path can be specified under name
        """
        self.image_surface.write_to_png(name)  # Output to PNG
        
        with Image.open(name) as img:
            img.show()
            
            
            

    def calculate_bars(self, starting_pos = (1000, 1000), spacing = 20):
        """
        internal use
        calculates the angles and radii of the different bars
        """
    
        #calculate radii
        return_radiuses = [self.radius]
        x, y = starting_pos
        prev_bar_width = 0
        for num, bar_width in enumerate(self.data_width_array):

           
            
            bar_width = self.max_width * bar_width #adjust relative width to max width
            return_radiuses.append(return_radiuses[-1] + bar_width/2 + prev_bar_width/2 + spacing) #bar width is drawn on both sides of radius, hence half of old and new bar width are needed for equal spacing
            prev_bar_width = bar_width
            
        return_radiuses.pop(0) #pop first element, as it is only gives the inside radius
        
        
        
        #calculate length of line
        return_angles = []
        for  length in self.data_len_array:
            return_angles.append(length*self.max_length)
            
        
            
        return return_radiuses, return_angles
        
    def add_labels(self, add_width = False, specific_labels = []):
        """
        adds names to the bar
        can add width automatically as number or can be specified manually
        """
        
        #write labels
        self.cr.set_font_size(self.font_size)
        for num, text_pos in enumerate(self.radiuses):
            if not add_width and not specific_labels:
                self.cr.move_to(self.center[0] - self.cr.text_extents(self.name_list[num])[2] - self.spacing, self.center[1] - text_pos + self.spacing - self.cr.text_extents(self.name_list[num])[3]/self.spacing)
                r, g, b = self.list_of_colors[num]
                self.cr.set_source_rgb(r, g, b)
                self.cr.show_text(self.name_list[num])
            elif not specific_labels:
                self.cr.move_to(self.center[0] - self.cr.text_extents(self.name_list[num] + " " + str(f'{self.width_array[num]:,}'))[2] - self.spacing, self.center[1] - text_pos + self.spacing - self.cr.text_extents(self.name_list[num])[3]/self.spacing)
                r, g, b = self.list_of_colors[num]
                self.cr.set_source_rgb(r, g, b)
                self.cr.show_text(self.name_list[num] + " " + str(f'{self.width_array[num]:,}'))
                
            else:
                self.cr.move_to(self.center[0] - self.cr.text_extents(str(specific_labels[num]))[2] - self.spacing, self.center[1] - text_pos + self.spacing - self.cr.text_extents(self.name_list[num])[3]/self.spacing)
                r, g, b = self.list_of_colors[num]
                self.cr.set_source_rgb(r, g, b)
                self.cr.show_text(str(specific_labels[num]))
                    

    def add_width_labels(self, labels = [], font_size = 20, extra_spacing = [], color_scheme = []):
        """
        adds labels onto the middle of the bar at the bottom of it
        the labels can be the width or specified seperately
        """
        
        self.cr.select_font_face("ToyFontFace", cairo.FONT_WEIGHT_BOLD)
        for num, (angle, radius) in enumerate(zip(self.angles, self.radiuses)):
            if extra_spacing:
                if type(extra_spacing) == int:
                    radius += extra_spacing
                elif type(extra_spacing) == list:
                    radius += extra_spacing[num]
                else:
                    raise ValueError("Extra Spacing must be an integer, or a list with extra spacing values for each bar")
                    
                    
            if not labels:
                x, y = self.center
                r, g, b = self.list_of_colors[num]
                if color_scheme:
                    r, g, b = color_scheme[num]
                self.cr.set_source_rgb(r, g, b)
                self.cr.set_font_size(font_size)
                
                text_length = self.cr.text_extents(str(self.length_array[num]))[2]
                self.cr.move_to(x - text_length / 2, y + radius)
                self.cr.show_text(str(self.length_array[num]))
            else:
                x, y = self.center
                r, g, b = self.list_of_colors[num]
                if color_scheme:
                    r, g, b = color_scheme[num] 
                self.cr.set_source_rgb(r, g, b)
                self.cr.set_font_size(font_size)
                
                text_length = self.cr.text_extents(str(labels[num]))[2]
                self.cr.move_to(x - text_length / 2, y + radius)
                self.cr.show_text(str(labels[num]))
         
            
            
    """
    OLD LABEL WIDTH IMPLEMENTATION
    Problem: letters overlay
    """

#    def add_width_labels(self, labels = [], display_at_middle = False, text_size = None, extra_spacing = None, increase_letter_distance = None):
#        
#        if text_size:
#            self.cr.set_font_size(text_size)
#        
#        for num, (angle, radius) in enumerate(zip(self.angles, self.radiuses)):
#            
#            if extra_spacing:
#                radius += extra_spacing
#           
#            #if no extra labels are passed in
#            if not labels:
#
#                x, y = self.center
#                r, g, b = self.list_of_colors[num]
#                self.cr.set_source_rgb(r, g, b)
#                self.cr.set_font_size(20)
#                #calculate start and end angle
#                text_length = self.cr.text_extents(str(self.length_array[num]))[2]
#                total_angle =  text_length / radius
#                start_angle = (3/2)* math.pi - (total_angle/2)
#                end_angle = (3/2)* math.pi + (total_angle/2)
#                spacing = np.linspace(start_angle, end_angle, len(str(self.length_array[num])))
#                
#                
#                
#                #loop over text, change angle, and print letter
#                for char_num, angle in enumerate(spacing):
#                    x_prime = x - radius * math.cos(angle)
#                    y_prime = y - radius * math.sin(angle)
#                    self.cr.move_to(x_prime, y_prime)
#                    self.cr.show_text(str(self.length_array[num])[::-1][char_num])
#                    
#            #if extra labels are passed in    
#            else:
#                x, y = self.center
#                r, g, b = self.list_of_colors[num]
#                self.cr.set_source_rgb(r, g, b)
#                self.cr.set_font_size(20)
#                #calculate start and end angle
#                text_length = self.cr.text_extents(str(labels[num]))[2]
#                total_angle =  text_length / radius
#                start_angle = (3/2)* math.pi - (total_angle/2)
#                end_angle = (3/2)* math.pi + (total_angle/2)
#                spacing = []
#                new_angle = start_angle
#                for letter in str(labels[num]):
#                    spacing.append(new_angle)
#                    new_angle += self.cr.text_extents(letter)[2] / radius
#                    
#                
#                    
#                print("New Spacing: ", len(spacing), spacing )
#                print("Old Spacing: ", len(np.linspace(start_angle, end_angle, len(str(labels[num])))), np.linspace(start_angle, end_angle, len(str(labels[num]))))
#               # spacing = np.linspace(start_angle, end_angle, len(str(labels[num])))
#                
#                
#                
#                #loop over text, change angle, and print letter
#                for char_num, angle in enumerate(spacing):
#                    x_prime = x - radius * math.cos(angle)
#                    y_prime = y - radius * math.sin(angle)
#                    if increase_letter_distance:
#                        x_prime = x - radius * math.cos(angle) - increase_letter_distance
#                    self.cr.move_to(x_prime, y_prime)
#                    self.cr.show_text(str(labels[num][::-1])[char_num])
#                    
#                
#             
                
             
                
               
            
                
            
    def add_ending_labels(self, width = 5, outside_spacing = 50, specific_labels = [], full_circle_label = False):
        """
        adds bars to the ending of the bar with their length
        """
        for num, (radius, angle) in enumerate(zip(self.radiuses, self.angles)):
            self.cr.save()
            #calculate starting point for label
            angle -= .5 * math.pi #to adjust for starting point
            x, y = self.center
            x_prime = x + radius * math.cos(angle) - width * math.cos(angle) / 2
            y_prime = y + radius * math.sin(angle) - width * math.cos(angle) / 2
            
            #get length of bar to outside
            length = self.radiuses[-1] - radius + outside_spacing
            x_prime_prime = x_prime + length * math.cos(angle)
            y_prime_prime = y_prime + length * math.sin(angle)
            
            #draw bar to outside
            self.cr.move_to(x_prime, y_prime)
            self.cr.line_to(x_prime_prime, y_prime_prime)
            self.cr.set_line_width(width)
            r, g, b = self.list_of_colors[num]
            self.cr.set_source_rgb(r, g, b)
            self.cr.stroke()
            
            #add text
            self.cr.move_to(x_prime_prime, y_prime_prime)
            self.cr.rotate(angle)
            r, g, b = self.list_of_colors[num]
            self.cr.set_source_rgb(r, g, b)
            if specific_labels:
                self.cr.show_text(str(specific_labels[num]))
            else:
                self.cr.show_text(str(self.length_array[num]))
            self.cr.restore()
            
        if full_circle_label:
            self.cr.save()
            #calculate starting point for label
            angle = - math.pi #to adjust for starting point
            x, y = self.center
            x_prime = x + (self.radius + self.spacing) * math.cos(angle)
            y_prime = y + (self.radius + self.spacing) * math.sin(angle)
            
            #get length of bar to outside
            length = self.radiuses[-1] - self.radius + outside_spacing
            x_prime_prime = x_prime + length * math.cos(angle)
            y_prime_prime = y_prime + length * math.sin(angle)
            
            #draw bar to outside
            self.cr.move_to(x_prime, y_prime)
            self.cr.line_to(x_prime_prime, y_prime_prime)
            self.cr.set_line_width(width)
            r, g, b = (0,0,0)
            self.cr.set_source_rgb(r, g, b)
            self.cr.stroke()
            
            #add text
            text_length = self.cr.text_extents(str(specific_labels[-1]))[2]
            self.cr.move_to(x_prime_prime - text_length, y_prime_prime)
            self.cr.rotate(0)
            r, g, b = (0,0,0)
            self.cr.set_source_rgb(r, g, b)
            if specific_labels:
                self.cr.show_text(str(specific_labels[-1]))
            else:
                self.cr.show_text(str(self.max_value))
            self.cr.restore()
            
            
        
    
    def draw(self):
        """
        draws the graph
        necessary before saving the graph
        """
        
        #first calculate width and angle (assuming three quarters of a cirlce as full length)
        self.data_display_dict = {}
        self.data_width_array = []
        self.data_len_array = []
        
        for name, tuple_val in self.dict.items():
            self.data_display_dict[name] = (math.pi * 0.5 * tuple_val[0] / max(self.length_array), tuple_val[1] / max(self.width_array))
            self.data_width_array.append(tuple_val[1] / max(self.width_array))
            if not self.max_value: #if max length value is provided
                self.data_len_array.append(tuple_val[0] / max(self.length_array))
            else:
                if self.max_value  < max(self.length_array):
                    raise ValueError("maximum value is smaller than the largest value")
                    
                    
                self.data_len_array.append(tuple_val[0] / self.max_value)
        
        
        self.radiuses, self.angles = self.calculate_bars(spacing = self.spacing)
        
        lighter_background_color = (self.background_color[0] * 1.3, self.background_color[1] * 1.3, self.background_color[2] * 1.3)
        for num, (radius, angle) in enumerate(zip(self.radiuses, self.angles)):
            #first draw underlying 100% mark with lighter color than background
            self.draw_circle(angle = self.max_length, radius = radius, line_width = self.data_width_array[num] * self.max_width, rgb_colors = lighter_background_color)
            #draw values in color on top
            self.draw_circle(angle = angle, radius = radius, line_width = self.data_width_array[num] * self.max_width, rgb_colors = self.list_of_colors[num])
            
            
        
    
    
    
    def draw_circle(self, radius = 200, angle = math.pi, rgb_colors = (.1, .1, .4), line_width = 50):
        """
        internal use
        draws the circular bar
        """
        x, y = self.center
        r, g, b = rgb_colors
        self.cr.arc(x, y, radius, -math.pi*.5, angle -math.pi*.5) #center posi, radius, starting and ending angle (have to add starting and ending angle together to adjust for start pos)
        self.cr.set_line_width(line_width)
        self.cr.set_source_rgb(r, g, b)
        self.cr.stroke()



    def set_colors(self, color_list):
        """
        Insert list of color names or rgb values as (r,g,b) with values between zero and one
        """
        #check for errors in size
        if len(color_list) != self.rings:
            raise ValueError(f"length of color list is {len(color_list)} for {self.rings} items")
        #check if names are given instead of rgb values
        if type(color_list[0]) == str:
            #create color list
            rgb_colors = {}
            for name, hex in cnames.items():
                rgb_colors[name] = to_rgb(hex)
            #translate name to rgb value
            rgb_translation_list = []
            for color in color_list:
                if color not in cnames:
                    raise ValueError(f"color {color} could not be found in matplotlib.colors.cnames")
                else:
                    rgb_translation_list.append(rgb_colors[color])
            self.list_of_colors = rgb_translation_list
            return
         
        #if everything is correct
        self.list_of_colors = color_list
        return
        
    def set_background_color(self, color):
        """
        sets background color
        """
        #check if color is done by name
        if type(color) == str:
            rgb_colors = {}
            for name, hex in cnames.items():
                rgb_colors[name] = to_rgb(hex)
            #translate name to rgb value
            
            
            if color not in cnames:
                raise ValueError(f"color {color} could not be found in matplotlib.colors.cnames")
            else:
                self.background_color = rgb_colors[color]
                #redraw background
                r, g, b = self.background_color
                self.cr.set_source_rgb(r,g,b)
                self.cr.rectangle(0, 0, self.width, self.height)
                self.cr.fill()
                return
            
        self.background_color = color
        #redraw background
        r, g, b = self.background_color
        self.cr.set_source_rgb(r,g,b)
        self.cr.rectangle(0, 0, self.width, self.height)
        self.cr.fill()
        return
        
    def set_spacing(self, spacing):
        """
        sets spacing between bars
        """
        if type(spacing) == int:
            self.spacing = spacing
            return
        else:
            raise ValueError("Entered Value is not an Integer")
            
    def set_max_length(self, max_length):
        """
        sets the maximum length in radian
        """
        
        if (max_length > 0) and (max_length < math.pi * 2):
            self.max_length = max_length
            return
        else:
            raise ValueError("Entered Value is not between zero and two pi")
            
    def set_radius(self, radius):
        """
        sets radius of the inside
        """
        if radius < (self.width/2):
            self.radius = radius
            return
        else:
            raise ValueError(f"Your Radius seems a bit big, the canvas width is only {self.width}")
            
            
    
    
    def insert_png_and_save_chart(self, path_to_png, chart_name = "krueger_gauge_circular_chart.png", enhance_factor = 1.):
        """
        loads a png image into the inside of the graph
        """
        #load images
        self.save_image_as_png("temp_file.png")
        background = Image.open("temp_file.png")
        foreground = Image.open(path_to_png)
        #resize inserted png
        basewidth = int(self.radius * enhance_factor)
        wpercent = (basewidth/float(foreground.size[0]))
        hsize = int((float(foreground.size[1])*float(wpercent)))
        foreground = foreground.resize((basewidth,hsize), Image.ANTIALIAS)
        #combine and save images
        background.paste(foreground, (int(self.center[0] - (basewidth/2)), int(self.center[1] - (hsize/2))), foreground)
        background.save(chart_name)
        """
        implement deletion of temporary file later
        """
        #delete temp 
#        background.close()
#        foreground.close()
#        remove("temp_file.png")
                
        
        
    def add_description_box(self, text, size = (400,400), position = (0,0), font_size = 20, background_color = (.5, .6, .1), rectangle_color = (1, .1, .1), rectangle_line_width = 20, text_spacing = 20, text_color = (0, 0, 0), line_spacing = 10):
        """
        adds a description box for better understanding
        """
        #draw outside
        self.cr.rectangle(position[0], position[1], size[0], size[1])
        r, g, b = rectangle_color
        self.cr.set_source_rgb(r, g, b)
        self.cr.fill()
        
        #draw inside
        self.cr.rectangle(position[0] + rectangle_line_width, position[1] + rectangle_line_width, size[0] - 2 * rectangle_line_width, size[1] - 2 * rectangle_line_width)
        r, g, b = background_color
        self.cr.set_source_rgb(r, g, b)
        self.cr.fill()
        
        #draw text
        for line_num, sub_text in enumerate(text.split("\n ")):
            self.cr.set_font_size(font_size)
            self.cr.move_to(position[0] + rectangle_line_width + text_spacing, position[1] + rectangle_line_width + text_spacing + self.cr.text_extents(sub_text)[3] * line_num + line_num * line_spacing)
            r, g, b = text_color
            self.cr.set_source_rgb(r, g, b)
            self.cr.show_text(sub_text)
            
       
