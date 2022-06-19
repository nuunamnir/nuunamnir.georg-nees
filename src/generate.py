import numpy
import cairo


class GenerativeArt:
    def __init__(self, output_file_path='output.svg', n=(1, 1), width=128, height=128, padding=0.1, seed=2106, distribution='uniform'):
        self.n = n
        self.width = width
        self.height = height
        self.padding = padding

        rng = numpy.random.default_rng(seed)
        if distribution == 'uniform':
            self.r = rng.random
        elif distribution == 'exponential':
            self.r = lambda: rng.exponential(scale=1.)
        elif distribution == 'normal':
            self.r = lambda: rng.normal(loc=0.5, scale=0.5 / 3)
        else:
            raise NotImplementedError

        self.surface = cairo.SVGSurface(output_file_path, width * n[0], height * n[1])
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0, 0, self.width * self.n[0], self.height * self.n[1])
        self.context.fill()
        self.context.set_source_rgb(0, 0, 0)


    def generate(self, rule=0, **kwargs):
        if rule == 0:
            self._rule00(**{k:v for k, v in kwargs.items() if v is not None})
        elif rule == 1:
            self._rule01(**{k:v for k, v in kwargs.items() if v is not None})
        elif rule == 2:
            self._rule02(**{k:v for k, v in kwargs.items() if v is not None})
        elif rule == 3:
            self._rule03(**{k:v for k, v in kwargs.items() if v is not None})
        elif rule == 4:
            self._rule04(**{k:v for k, v in kwargs.items() if v is not None})
        else:
            raise NotImplementedError



    def _rule00(self, p=8): 
        # 8-ecke            
        for i in range(self.n[0]):
            offset_x = i * self.width
            for j in range(self.n[1]):
                offset_y = j * self.height
                start_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                start_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                self.context.move_to(start_x + offset_x, start_y + offset_y)
                for _ in range(p - 1):
                    self.context.line_to(self.width * min(1 - self.padding, max(self.padding, self.r())) + offset_x, self.height * min(1 - self.padding, max(self.padding, self.r())) + offset_y)
                self.context.line_to(start_x + offset_x, start_y + offset_y)
                self.context.stroke()


    def _rule01(self, p=23): 
        # 23-ecke
        if p < 3:
            raise ValueError('p must be at least 3')            
        for i in range(self.n[0]):
            offset_x = i * self.width
            for j in range(self.n[1]):
                orientation = numpy.random.randint(2)
                offset_y = j * self.height
                start_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                start_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                current_x = last_x = start_x
                current_y = last_y = start_y
                self.context.move_to(start_x + offset_x, start_y + offset_y)
                for k in range(p - 2):
                    if k % 2 == orientation:
                        current_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                        self.context.line_to(last_x + offset_x, current_y + offset_y)
                    else:
                        current_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                        self.context.line_to(current_x + offset_x, last_y + offset_y)
                    last_x = current_x
                    last_y = current_y
                if (p - 3) % 2 == 1 - orientation:
                    self.context.line_to(last_x + offset_x, start_y + offset_y)
                else:
                    self.context.line_to(start_x + offset_x, last_y + offset_y)
                self.context.line_to(start_x + offset_x, start_y + offset_y)
                self.context.stroke()


    def _rule02(self, p=2048, l=0.1, mode='line'):
        # achsenparalleler irrweg
        if mode == 'line':
            for i in range(self.n[0]):
                offset_x = i * self.width
                for j in range(self.n[1]):
                    orientation = numpy.random.randint(2)
                    offset_y = j * self.height
                    start_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                    start_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                    current_x = last_x = start_x
                    current_y = last_y = start_y
                    self.context.move_to(start_x + offset_x, start_y + offset_y)
                    for k in range(p):
                        if k % 2 == orientation:
                            current_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                            while abs(current_y - last_y) > l * self.height:
                                current_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                            self.context.line_to(last_x + offset_x, current_y + offset_y)
                        else:
                            current_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                            while abs(current_x - last_x) > l * self.width:
                                current_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                            self.context.line_to(current_x + offset_x, last_y + offset_y)
                        last_x = current_x
                        last_y = current_y
                    self.context.stroke()
        elif mode == 'rectangle':
            for i in range(self.n[0]):
                offset_x = i * self.width
                for j in range(self.n[1]):
                    offset_y = j * self.height
                    for _ in range(p):
                        start_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                        start_y = self.height * min(1 - self.padding, max(self.padding, self.r()))

                        end_x = self.width * min(1 - self.padding, max(self.padding, self.r()))
                        while abs(end_x - start_x) > l * self.width:
                            end_x = self.width * min(1 - self.padding, max(self.padding, self.r()))

                        end_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
                        while abs(end_y - start_y) > l * self.height:
                            end_y = self.height * min(1 - self.padding, max(self.padding, self.r()))
        
                        if start_x > end_x:
                            start_x, end_x = end_x, start_x
                        if start_y > end_y:
                            start_y, end_y = end_y, start_y
                        self.context.rectangle(start_x + offset_x, start_y + offset_y, end_x - start_x, end_y - start_y)
                        self.context.stroke()

        else:
            raise NotImplementedError


    def _rule03(self, p=48, a=60, r=60, w=0.3, l=0.3):
        # andreaskreuz
        max_radius = (min(self.width, self.height)) / 2
        for i in range(self.n[0]):
                offset_x = i * self.width
                for j in range(self.n[1]):
                    offset_y = j * self.height
                    for _ in range(p):
                        for offset_r in [0, r]:
                            current_r = 0
                            while current_r < max_radius * (l / 2):
                                current_r = max_radius * min(1 - self.padding, max(self.padding, self.r()))
                            current_a = (offset_r + a + (180 / 2 * w) * (max(0, min(1, self.r())) - 0.5)) * (numpy.pi / 180)
                            start_x = current_r * numpy.cos(current_a)
                            start_y = current_r * numpy.sin(current_a)
                            self.context.move_to(start_x + offset_x + self.width / 2, start_y + offset_y + self.height / 2)
                            current_a = (offset_r + a + 180 + ((180 / 2 * w) * (max(0, min(1, self.r())) - 0.5))) * (numpy.pi / 180)
                            end_x = current_r * numpy.cos(current_a)
                            end_y = current_r * numpy.sin(current_a)
                            self.context.line_to(end_x + offset_x + self.width / 2, end_y + offset_y + self.height / 2)
                            self.context.stroke()
    

    def _rule04(self, p=64):
        # gardine
        for i in range(self.n[0]):
                offset_x = i * self.width
                for j in range(self.n[1]):
                    offset_y = j * self.height
                    for _ in range(p):
                        y = (self.height * (min(1 - self.padding, max(self.padding, self.r())) - 0.5))
                        self.context.save()
                        self.context.translate(0, offset_y + self.height * (0.5 - self.padding))
                        self.context.move_to(offset_x + self.padding * self.width, offset_y + self.height / 2 - abs(y))
                        self.context.line_to(offset_x + self.width - self.padding * self.width, offset_y + self.height / 2 - abs(y))
                        self.context.stroke()
                        self.context.restore()
                    for _ in range(p):
                        y = (self.height * (min(1 - self.padding, max(self.padding, self.r())) - 0.5))
                        self.context.save()
                        self.context.translate(0, offset_y - self.height * 0.5)
                        self.context.move_to(offset_x + self.padding * self.width, offset_y + self.height / 2 + abs(y) + self.height * self.padding)
                        self.context.line_to(offset_x + self.width - self.padding * self.width, offset_y + self.height / 2 + abs(y) + self.height * self.padding)
                        self.context.stroke()
                        self.context.restore()


    def __del__(self):
        self.surface.flush()
        self.surface.finish()


if __name__ == '__main__':
    import argparse

    def dimensions(s):
        try:
            return tuple(map(int, s.lstrip('(').rstrip(')').split(',')))
        except:
            raise argparse.ArgumentTypeError('dimensions must be given separated by commas and enclosed in brackets, e.g.: "(16,16)"')
    
    
    def rule_parameters(s):
        try:
            parameters = s.split(',')
            r = dict()
            if not len(s):
                return r
            for parameter in parameters:
                name, value = parameter.split('=')
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        value = str(value)
                r[name] = value
            return r
        except:
            raise argparse.ArgumentTypeError('rule parameters must be given separated by commas, e.g.: l=0.1,mode=rectangle')


    parser = argparse.ArgumentParser(description='Generate images following the rules of Georg Nees, published in rot 19 computer-grafik (1962).')
    parser.add_argument('output', type=str, help='the destination to which the image is written in SVG format')
    parser.add_argument('-r', '--rule', type=int, default=0, help='the rule according to which the image is to be generated (0 = 8-ecke, 1 = 23-ecke, 2 = achesenparalleler irrweg, 3 = andreaskreuz, 4 = gardine)', choices=[0, 1, 2, 3, 4])
    parser.add_argument('--width', type=int, default=64, help='the width of the generated image (default: 64)')
    parser.add_argument('--height', type=int, default=64, help='the width of the generated image (default: 64)')
    parser.add_argument('-d', '--distribution', type=str, default='uniform', help='the distribution according to which the random numbers are sampled; please note that the random number is clamped to the interval [PADDING, 1 - PADDING] (default: uniform)', choices=['uniform', 'exponential', 'normal'])
    parser.add_argument('-s', '--seed', type=int, default=2106, help='the seed for the random number generator (default: 2106)')
    parser.add_argument('-p', '--padding', type=float, default=0.1, help='the distance between the image border and the drawable area of the image as proportion of the image width and height (default:0.1)')
    parser.add_argument('-n', type=dimensions, default=(16, 16), help='the dimensions of the output, i.e., the image contains x by y subimages (default="(16,16)")')
    parser.add_argument('-x', '--parameters', type=rule_parameters, default='', help='additional parameters that are rule specific, in the shape parameter1=x,parameter2=y,parameterN=z (default="")')
    args = parser.parse_args()

    a = GenerativeArt(output_file_path=args.output, n=args.n, width=args.width, height=args.height, padding=args.padding, seed=args.seed, distribution=args.distribution)
    a.generate(rule=args.rule, **{k:v for k, v in args.parameters.items()})