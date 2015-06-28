# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.

from PIL import Image, ImageChops, ImageOps, ImageStat, ImageDraw
from Figure import Figure

class Agent:
    attribute_list = ['shape', 'fill', 'size', 'angle', 'inside', 'above', 'overlaps', 'alignment']
    sizes_list = ['very small', 'small', 'medium', 'large', 'very large', 'huge']  # index = size value
    transforms_list = ['nothing']
    points_attribute = 1
    points_pattern = 2

    threshold = .98
    points_holistic_symmetry = 5
    points_bonus = 1

    figure_a = []
    figure_b = []
    figure_c = []
    figure_d = []
    figure_e = []
    figure_f = []
    figure_g = []
    figure_h = []
    figure_sol = []
    solutions = []

    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    def is_equal(self, im1, im2):
        val = self.get_similarity(im1, im2)
        return val > self.threshold

    def get_similarity(self, im1, im2):
        max_similarity = 0
        for x_offset in range(-3, 4, 1):
            for y_offset in range(-3, 4, 1):
                diff = ImageChops.difference(ImageChops.offset(im1, x_offset, y_offset), im2)
                num_pixels = im2.size[0] * im1.size[1]
                diff_stats = ImageStat.Stat(diff)
                similarity = 1.0 - ((diff_stats.sum[0] / 255) / num_pixels)
                max_similarity = max(similarity, max_similarity)
        return max_similarity

    def get_transform(self, figure1, figure2, figure3):

        figure1.identify_objects()
        figure2.identify_objects()
        figure3.identify_objects()
        figure1.find_centroids()
        figure2.find_centroids()
        figure3.find_centroids()

        '''
        fig_diff = Figure(ImageChops.difference(figure1.image, figure2.image))
        fig_diff.identify_objects()
        fig_diff.image.show()

        # Redrawing an object to an image
        obj = figure1.objects[1]
        size = obj.size()
        im = Image.new('L', size)
        for xy in obj.area:
            print xy
            im.putpixel((xy[0] - obj.min_x, xy[1] - obj.min_y), 128)
        im.show()

        # Resizing an image
        new_im = im.resize((184, 184), Image.BILINEAR)
        new_im.show()
        im.show()
        '''

        if len(figure1.objects) == len(figure2.objects) == len(figure3.objects) == 2:
            # Check for simple shape resize
            obj1 = figure1.objects[1]
            obj2 = figure2.objects[1]
            obj3 = figure3.objects[1]

            obj1_size = obj1.size()
            obj2_size = obj2.size()
            obj3_size = obj3.size()

            if (obj3_size[0] - obj2_size[0], obj3_size[1] - obj2_size[1]) == (obj2_size[0] - obj1_size[0], obj2_size[1] - obj1_size[1]):
                resize_amount = (obj3_size[0] - obj2_size[0], obj3_size[1] - obj2_size[1])
                return ['resize', resize_amount]

        pass



    #Merged all figures in problem + solution into a single large image
    def create_merged_image(self):
        x_orig = self.figure_a.image.size[0]
        y_orig = self.figure_a.image.size[1]
        x_new = x_orig * 3
        y_new = y_orig * 3
        merged_img = Image.new('L', (x_new, y_new))

        x = 0
        y = 0
        merged_img.paste(self.figure_a.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_b.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_c.image, (x, y))

        x = 0
        y += y_orig
        merged_img.paste(self.figure_d.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_e.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_f.image, (x, y))

        x = 0
        y += y_orig
        merged_img.paste(self.figure_g.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_h.image, (x, y))
        x += x_orig
        merged_img.paste(self.figure_sol.image, (x, y))

        return merged_img

    #Checks for vertical symmetry (across vertical axis)
    def get_vertical_symmetry_measure(self, image):
        return self.get_similarity(image, ImageOps.mirror(image))

    #Checks for horizontal symmetry (across horiontal axis)
    def get_horizontal_symmetry_measure(self, image):
        return self.get_similarity(image, ImageOps.flip(image))

    def get_solution(self):
        answer = -1

        '''
        # Check for holistic symmetry
        vertical_symmetry_measures = []
        horizontal_symmetry_measures = []
        for solution in self.solutions:
            self.figure_sol = solution
            holistic_image = self.create_merged_image()
            holistic_image.show()
            vertical_symmetry_measures.append(self.get_vertical_symmetry_measure(holistic_image))
            horizontal_symmetry_measures.append(self.get_horizontal_symmetry_measure(holistic_image))
        # Check vertical
        max_measure = max(vertical_symmetry_measures)
        if max_measure > self.threshold:
            return vertical_symmetry_measures.index(max_measure) + 1
        # Check horizontal
        max_measure = max(horizontal_symmetry_measures)
        if max_measure > self.threshold:
            return horizontal_symmetry_measures.index(max_measure) + 1
        '''

        self.get_transform(self.figure_a, self.figure_b, self.figure_c)
        
        return answer

    def Solve(self, problem):
        print problem.name
        problem_name = problem.name
        answer = -1
        scores = []

        #Load all figures and make them black OR white (no grey!)
        self.figure_a = Figure(problem.figures['A'].visualFilename)
        self.figure_b = Figure(problem.figures['B'].visualFilename)
        self.figure_c = Figure(problem.figures['C'].visualFilename)
        self.figure_d = Figure(problem.figures['D'].visualFilename)
        self.figure_e = Figure(problem.figures['E'].visualFilename)
        self.figure_f = Figure(problem.figures['F'].visualFilename)
        self.figure_g = Figure(problem.figures['G'].visualFilename)
        self.figure_h = Figure(problem.figures['H'].visualFilename)

        problem_figure_keys = sorted(problem.figures.keys())
        num_solutions = 8
        for i in range(num_solutions):
            figure_sol = Figure(problem.figures[problem_figure_keys[i]].visualFilename)
            self.solutions.append(figure_sol)

        answer = self.get_solution()

        '''
        print problem.name
        print "Scores :", scores
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'
        '''
        return answer



