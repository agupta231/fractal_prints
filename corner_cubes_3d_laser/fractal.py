# Program by Ankur Gupta
# www.github.com/agupta231
# Feb 2017
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

import svgwrite
import numpy
import glob
import os
from cut import Cut
from config import Config


class Fractal:
    def __init__(self):
        self.shape_queue = []
        self.bounds_array = []

    def generate_plans(self):
        self.populate_cut_queue()

        while len(self.shape_queue) != 0:
            drawing, name = self.create_canvas()

            drawing.add(drawing.rect(insert=(0, 0),
                                     size=(str(Config.cutting_bed_width), str(Config.cutting_bed_height)),
                                     stroke_width=Config.stroke_thickness,
                                     stroke=Config.bounding_box_color,
                                     fill="none"))

            self.bounds_array = []
            self.gen_shape_positions(drawing, numpy.array([0.0, 0.0]))

            drawing.save()
            print name + " - completed"

    def populate_cut_queue(self):
        for current_iteration in xrange(1, Config.iterations + 1):
            for i in xrange(7 ** (current_iteration - 1)):
                self.shape_queue.append(Cut(current_iteration, "a"))
                self.shape_queue.append(Cut(current_iteration, "b"))
                self.shape_queue.append(Cut(current_iteration, "c"))

                if current_iteration == 1:
                    self.shape_queue.append(Cut(current_iteration, "a"))
                    self.shape_queue.append(Cut(current_iteration, "b"))
                    self.shape_queue.append(Cut(current_iteration, "c"))

                else:
                    self.shape_queue.append(Cut(current_iteration, "a90"))
                    self.shape_queue.append(Cut(current_iteration, "b90"))
                    self.shape_queue.append(Cut(current_iteration, "c90"))

    def create_canvas(self):
        filename = "plans/plan_" + str(len(glob.glob(os.getcwd() + "/plans/*"))) + ".svg"
        return svgwrite.Drawing(filename=filename), filename

    def gen_shape_positions(self, drawing, starting_pos):
        horizontal_distance = Config.cutting_bed_width - starting_pos[0]
        vertical_distance = Config.cutting_bed_height - starting_pos[1]

        for i in xrange(len(self.bounds_array)):
            horizontal_delta = self.bounds_array[i][0][0] - starting_pos[0]

            if 0 <= horizontal_delta < horizontal_distance:
                if self.bounds_array[i][0][1] < starting_pos[1] < self.bounds_array[i][1][1]:
                    horizontal_distance = horizontal_delta

                elif self.bounds_array[i][0][1] == starting_pos[1] and self.bounds_array[i][0][0] == starting_pos[0]:
                    return

        for i in xrange(len(self.bounds_array)):
            vertical_delta = self.bounds_array[i][0][1] - starting_pos[1]

            if 0 <= vertical_delta < vertical_distance:
                if self.bounds_array[i][0][0] < starting_pos[0] < self.bounds_array[i][1][0]:
                    if vertical_delta == 0:
                        return
                    else:
                        vertical_distance = vertical_delta
                        break

        if horizontal_distance < vertical_distance:
            bounding_distance = horizontal_distance
        else:
            bounding_distance = vertical_distance

        for i in xrange(len(self.shape_queue)):
            if self.shape_queue[i].length <= bounding_distance:
                drawing.add(self.shape_queue[i].generate_cut(drawing, starting_pos))

                self.bounds_array.append([starting_pos, starting_pos + numpy.array([self.shape_queue[i].length, self.shape_queue[i].length])])

                right_box_pos = starting_pos + numpy.array([self.shape_queue[i].length, 0])
                bottom_box_pos = starting_pos + numpy.array([0, self.shape_queue[i].length])

                del self.shape_queue[i]

                self.gen_shape_positions(drawing, right_box_pos)
                self.gen_shape_positions(drawing, bottom_box_pos)

                return

fractal = Fractal()
fractal.generate_plans()
