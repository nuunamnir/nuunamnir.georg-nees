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


    def generate(self, rule=0, p=None):
        if rule == 0:
            if p is None:
                self._rule00()
            else:
                self._rule00(p=p)
        elif rule == 1:
            if p is None:
                self._rule01()
            else:
                self._rule01(p=p)



    def _rule00(self, p=8):             
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

    parser = argparse.ArgumentParser(description='Generate images following the rules of Georg Nees, published in rot 19 computer-grafik (1962).')
    parser.add_argument('output', type=str, help='the destionation to which the image is written in SVG format')
    parser.add_argument('-r', '--rule', type=int, default=0, help='the rule according to which the image is to be generated (0 = 8-ecke, 1 = 23-ecke)', choices=[0, 1])
    parser.add_argument('--width', type=int, default=64, help='the width of the generated image (default: 64)')
    parser.add_argument('--height', type=int, default=64, help='the width of the generated image (default: 64)')
    parser.add_argument('-d', '--distribution', type=str, default='uniform', help='the distribution according to which the random numbers are sampled; please note that the random number is clamped to the interval [PADDING, 1 - PADDING] (default: uniform)', choices=['uniform', 'exponential', 'normal'])
    parser.add_argument('-s', '--seed', type=int, default=2106, help='the seed for the random number generator (default: 2106)')
    parser.add_argument('-p', '--padding', type=float, default=0.1, help='the distance between the image border and the drawable area of the image as proportion of the image width and height (default:0.1)')
    parser.add_argument('-n', type=dimensions, default=(16, 16), help='the dimensions of the output, i.e., the image contains x by y subimages (default="(16,16)")')
    args = parser.parse_args()
    print(args)

    a = GenerativeArt(output_file_path=args.output, n=args.n, width=args.width, height=args.height, padding=args.padding, seed=args.seed, distribution=args.distribution)
    if args.rule == 0:
        a.generate(rule=args.rule)
    elif args.rule == 1:
        a.generate(rule=args.rule, p=23)
    else:
        raise NotImplementedError