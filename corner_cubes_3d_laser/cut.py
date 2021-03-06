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

import math
import numpy
import svgwrite
from config import Config


class Cut:
    def __init__(self, iteration, cut_type):
        self.iteration = iteration
        self.length = Config.initial_cube_size * Config.iteration_multiplier ** (iteration - 1)
        self.type = cut_type
        self.id = numpy.random.randint(0, 999999999)

        self.__generate_tabs()

    def generate_bounding_box(self, drawing, starting_pos, shape_id):
        dwg = drawing.g(id=shape_id, style="font-size: 0.5")

        dwg.add(drawing.rect(
            insert=tuple(starting_pos),
            size=(str(self.length), str(self.length)),
            stroke_width=Config.stroke_thickness,
            stroke=Config.cube_color,
            fill="none"
        ))

        dwg.add(drawing.text(
            str(shape_id),
            insert=tuple(starting_pos),
        ))

        return dwg

    def generate_cut(self, drawing, starting_pos):
        self.drawing = drawing

        if self.type == "a":
            return self.__gen_cut_a(starting_pos)
        elif self.type == "b":
            return self.__gen_cut_b(starting_pos)
        elif self.type == "c":
            return self.__gen_cut_c(starting_pos)
        elif self.type == "a90":
            return self.__gen_cut_a90(starting_pos)
        elif self.type == "b90":
            return self.__gen_cut_b90(starting_pos)
        elif self.type == "c90":
            return self.__gen_cut_c90(starting_pos)
        else:
            return None

    def __generate_tabs(self):
        if math.floor(self.length) >= 3:
            self.tab_count = math.floor(self.length)

            if self.tab_count % 2 != 1:
                self.tab_count -= 1
        else:
            self.tab_count = 3

        self.tab_count = int(self.tab_count)
        self.tab_width = self.length / self.tab_count

    def __gen_cut_a(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = starting_pos + numpy.array([self.tab_width, Config.material_thickness])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Left Edge
        last_pos = starting_pos + numpy.array([Config.material_thickness, self.tab_width])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Bottom Edge
        last_pos = starting_pos + numpy.array([self.tab_width, self.length - Config.material_thickness])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Right Edge
        last_pos = starting_pos + numpy.array([self.length - Config.material_thickness, self.tab_width])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Top left corner
        last_pos = starting_pos + numpy.array([Config.material_thickness, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -(self.tab_width - Config.material_thickness)])))
        last_pos += numpy.array([0, -(self.tab_width - Config.material_thickness)])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Top right corner
        last_pos = starting_pos + numpy.array([self.length - self.tab_width, Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))
        last_pos += numpy.array([self.tab_width - Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width - Config.material_thickness])))

        # Bottom left corner
        last_pos = starting_pos + numpy.array([self.tab_width, self.length - Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([-(self.tab_width - Config.material_thickness), 0])))
        last_pos += numpy.array([-(self.tab_width - Config.material_thickness), 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -(self.tab_width - Config.material_thickness)])))

        # Bottom right corner
        last_pos = starting_pos + numpy.array([self.length - Config.material_thickness, self.length - self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width - Config.material_thickness])))
        last_pos += numpy.array([0, self.tab_width - Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([-(self.tab_width - Config.material_thickness), 0])))

        return shape

    def __gen_cut_b(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = list(starting_pos)

        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

        # Left Edge
        last_pos = list(starting_pos)

        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

        # Bottom Edge
        last_pos = list(starting_pos) + numpy.array([0, self.length])
        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

        # Right Edge
        last_pos = list(starting_pos) + numpy.array([self.length, 0])
        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

        return shape

    def __gen_cut_c(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = list(starting_pos) + numpy.array([self.tab_width, 0])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Bottom Edge
        last_pos = list(starting_pos) + numpy.array([self.tab_width, self.length])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Left Edge
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.tab_width])

        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Right Edge
        last_pos = list(starting_pos) + numpy.array([self.length - Config.material_thickness, self.tab_width])

        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Top left corner
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -self.tab_width])))
        last_pos += numpy.array([0, -self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Top right corner
        last_pos = list(starting_pos) + numpy.array([self.length - self.tab_width, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))
        last_pos += numpy.array([self.tab_width - Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))

        # Bottom left corner
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.length - self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
        last_pos += numpy.array([0, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Bottom right corner
        last_pos = list(starting_pos) + numpy.array([self.length - Config.material_thickness, self.length - self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
        last_pos += numpy.array([0, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([-(self.tab_width - Config.material_thickness), 0])))

        return shape

    def __gen_cut_a90(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = starting_pos + numpy.array([self.tab_width, Config.material_thickness])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Left Edge
        last_pos = starting_pos + numpy.array([Config.material_thickness, self.tab_width])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Bottom Edge
        last_pos = starting_pos + numpy.array([self.tab_width, self.length - Config.material_thickness])
        for i in xrange(int(math.floor((self.tab_count - 2) / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Right Edge
        last_pos = starting_pos + numpy.array([self.length - Config.material_thickness, self.tab_width])
        for i in xrange(int(math.floor((self.tab_count - 2) / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Top left corner
        last_pos = starting_pos + numpy.array([Config.material_thickness, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -(self.tab_width - Config.material_thickness)])))
        last_pos += numpy.array([0, -(self.tab_width - Config.material_thickness)])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Top right corner
        last_pos = starting_pos + numpy.array([self.length - self.tab_width, Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))
        last_pos += numpy.array([self.tab_width - Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width - Config.material_thickness])))

        # Bottom left corner
        last_pos = starting_pos + numpy.array([self.tab_width, self.length - Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([-(self.tab_width - Config.material_thickness), 0])))
        last_pos += numpy.array([-(self.tab_width - Config.material_thickness), 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -(self.tab_width - Config.material_thickness)])))

        # Bottom right cutout
        last_pos = starting_pos + numpy.array([self.length - Config.material_thickness, (self.length - self.tab_width) / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
        last_pos += numpy.array([Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width / 2])))
        last_pos += numpy.array([0, self.tab_width / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([-self.length / 2, 0])))
        last_pos += numpy.array([-self.length / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.length / 2])))
        last_pos += numpy.array([0, self.length / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([-self.tab_width / 2, 0])))
        last_pos += numpy.array([-self.tab_width / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))

        return shape

    def __gen_cut_b90(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = list(starting_pos)

        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

        # Left Edge
        last_pos = list(starting_pos)

        for i in xrange(int(math.floor(self.tab_count / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

        # Bottom Edge
        last_pos = list(starting_pos) + numpy.array([self.length, self.length])
        for i in xrange(int(math.floor(self.tab_count / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([-self.tab_width, 0])))
                last_pos += numpy.array([-self.tab_width, 0])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([-self.tab_width, 0])))
                last_pos += numpy.array([-self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

        # Right Edge
        last_pos = list(starting_pos) + numpy.array([self.length, 0])
        for i in xrange(self.tab_count):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

        # Bottom Left cutout
        last_pos = list(starting_pos) + numpy.array([0, (self.length - self.tab_width) / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
        last_pos += numpy.array([Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width / 2])))
        last_pos += numpy.array([0, self.tab_width / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([self.length / 2 - Config.material_thickness, 0])))
        last_pos += numpy.array([self.length / 2 - Config.material_thickness, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.length / 2 - Config.material_thickness])))
        last_pos += numpy.array([0, self.length / 2 - Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width / 2, 0])))
        last_pos += numpy.array([self.tab_width / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
        return shape

    def __gen_cut_c90(self, starting_pos):
        shape = self.drawing.g(id=str(self.id))

        # Top Edge
        last_pos = list(starting_pos) + numpy.array([self.tab_width, 0])
        for i in xrange(int(math.floor((self.tab_count - 2) / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Bottom Edge
        last_pos = list(starting_pos) + numpy.array([self.tab_width, self.length])
        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -Config.material_thickness])))
                last_pos += numpy.array([0, -Config.material_thickness])

                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
                last_pos += numpy.array([0, Config.material_thickness])

            else:
                shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width, 0])))
                last_pos += numpy.array([self.tab_width, 0])

        # Left Edge
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.tab_width])

        for i in xrange(self.tab_count - 2):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
                last_pos += numpy.array([0, self.tab_width])

        # Right Edge
        last_pos = list(starting_pos) + numpy.array([self.length - Config.material_thickness, self.length - self.tab_width])

        for i in xrange(int(math.floor((self.tab_count - 2) / 2))):
            if i % 2 == 0:
                shape.add(self.__gen_line(last_pos, numpy.array([Config.material_thickness, 0])))
                last_pos += numpy.array([Config.material_thickness, 0])

                shape.add(self.__gen_line(last_pos, numpy.array([0, -self.tab_width])))
                last_pos += numpy.array([0, -self.tab_width])

                shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))
                last_pos += numpy.array([-Config.material_thickness, 0])
            else:
                shape.add(self.__gen_line(last_pos, numpy.array([0, -self.tab_width])))
                last_pos += numpy.array([0, -self.tab_width])

        # Top left corner
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, -self.tab_width])))
        last_pos += numpy.array([0, -self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Top right cutout
        last_pos = list(starting_pos) + numpy.array([(self.length - self.tab_width) / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, Config.material_thickness])))
        last_pos += numpy.array([0, Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width / 2, 0])))
        last_pos += numpy.array([self.tab_width / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.length / 2 - Config.material_thickness])))
        last_pos += numpy.array([0, self.length / 2 - Config.material_thickness])

        shape.add(self.__gen_line(last_pos, numpy.array([self.length / 2, 0])))
        last_pos += numpy.array([self.length / 2, 0])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width / 2])))
        last_pos += numpy.array([0, self.tab_width / 2])

        shape.add(self.__gen_line(last_pos, numpy.array([-Config.material_thickness, 0])))

        # Bottom left corner
        last_pos = list(starting_pos) + numpy.array([Config.material_thickness, self.length - self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
        last_pos += numpy.array([0, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([self.tab_width - Config.material_thickness, 0])))

        # Bottom right corner
        last_pos = list(starting_pos) + numpy.array(
            [self.length - Config.material_thickness, self.length - self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([0, self.tab_width])))
        last_pos += numpy.array([0, self.tab_width])

        shape.add(self.__gen_line(last_pos, numpy.array([-(self.tab_width - Config.material_thickness), 0])))

        return shape

    def __gen_line(self, start_array, translation_array):
        return self.drawing.line(tuple(start_array), tuple(start_array + translation_array),
                                 stroke=Config.cube_color,
                                 stroke_width=Config.stroke_thickness)
