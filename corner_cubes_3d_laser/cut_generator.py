# Program by Ankur Gupta
# www.github.com/agupta231
# Jan 2017
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Imports
import svgwrite
from svgwrite import inch

# Set up parameters
material_thickness = 0.8
initial_cube_size = 10
iteration_multiplier = 0.5
iterations = 3
cutting_bed_width = 18
cutting_bed_height = 10

bounding_box_color = "yellow"
cube_color = "black"
stroke = 0.5

# Create svg bounds box
drawing = svgwrite.Drawing(filename="test.svg")
drawing.add(drawing.rect(insert=(0, 0),
                         size=(str(cutting_bed_width) + "in", str(cutting_bed_height) + "in"),
                         stroke_width=0.5,
                         stroke="black",
                         fill="none"))

drawing.save()
