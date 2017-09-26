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

from PIL import Image, ImageChops, ImageOps, ImageStat
from Figure import Figure
from Object import Object
import time
import copy

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
    figures = []
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

    def image_from_objects(self, size, objects):
        image = Image.new('L', size, color=255)
        for obj in objects:
            for xy in obj.area:
                try:
                    image.putpixel(xy, 0)
                except IndexError:
                    pass

        return image

    # Checks for vertical symmetry (across vertical axis)
    def get_vertical_symmetry_measure(self, image):
        return self.get_similarity(image, ImageOps.mirror(image))

    # Checks for horizontal symmetry (across horizontal axis)
    def get_horizontal_symmetry_measure(self, image):
        return self.get_similarity(image, ImageOps.flip(image))

    def has_vertical_symmetry(self, image):
        measure = self.get_vertical_symmetry_measure(image)
        return measure >= self.threshold

    # Merged all figures in problem + solution into a single, larger image
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

    def find_most_similar_solution(self, fig):
        similarity_scores = []
        for solution in self.solutions:
            similarity_scores.append(self.get_similarity(fig.image, solution.image))
        return similarity_scores.index(max(similarity_scores)) + 1

    def translate_object(self, obj, distance):
        obj_new = Object((0, 0), 0)
        obj_new.remove_pixel((0, 0))

        for xy in obj.area:
            obj_new.add_pixel((xy[0] + distance[0], xy[1] + distance[1]))

        obj_new.find_centroid()
        return obj_new

    def figure_and(self, fig1, fig2):
        im1 = fig1.image
        im2 = fig2.image
        if im1.size != im2.size:
            raise Exception('Images must be same size to AND them')
        size = im1.size
        image = Image.new('L', size, color=255)

        for x in range(size[0]):
            for y in range(size[1]):
                xy = x, y
                if im1.getpixel(xy) == im2.getpixel(xy) == 0:
                    image.putpixel(xy, 0)
        return Figure(image)

    def figure_xor(self, fig1, fig2):
        im1 = fig1.image
        im2 = fig2.image
        if im1.size != im2.size:
            raise Exception('Images must be same size to XOR them')
        size = im1.size
        image = Image.new('L', size, color=255)

        for x in range(size[0]):
            for y in range(size[1]):
                xy = x, y
                if im1.getpixel(xy) != im2.getpixel(xy):
                    image.putpixel(xy, 0)
        return Figure(image)

    def figure_add(self, fig1, fig2):
        if fig1.image.size != fig2.image.size:
            raise Exception('Figures must be same size to SUBTRACT them')

        size = fig1.image.size
        image = Image.new('L', size, color=255)

        for obj1 in fig1.objects:
            for xy in obj1.area:
                image.putpixel(xy, 0)

        for obj2 in fig2.objects:
            for xy in obj2.area:
                image.putpixel(xy, 0)

        return Figure(image)

    def figure_subtract(self, fig1, fig2):
        if fig1.image.size != fig2.image.size:
            raise Exception('Figures must be same size to SUBTRACT them')

        image = copy.deepcopy(fig1.image)

        for obj2 in fig2.objects:
            for xy in obj2.area:
                image.putpixel(xy, 255)

        return Figure(image)

    def horizontal_pass_through(self, figure1, figure2, figure3):
        im = figure1.image
        size = im.size
        im_centroid = (size[0]/2, size[1]/2)
        max_distance = size[0]/2 - 1

        for i in xrange(0, max_distance, 2):
            objects_new = []
            for obj in figure1.objects:
                # On the left side
                if obj.centroid[0] < im_centroid[0]:
                    obj_new = self.translate_object(obj, (i, 0))
                # On the right side
                else:
                    obj_new = self.translate_object(obj, (-i, 0))
                objects_new.append(obj_new)
            # end of loop

            im_new = self.image_from_objects(size, objects_new)

            # If equal, we know this is the transform
            if self.is_equal(im_new, figure2.image):
                return ['horizontal pass through']

        return ['NOT horizontal pass through']

    def get_transform(self):
        # Boolean Operators
        # Check for adding (left + middle = right)
        if self.is_equal(self.figure_add(self.figure_a, self.figure_b).image, self.figure_c.image):
            return ['add']
        # Check for subtracting (left - middle = right)
        if self.is_equal(self.figure_subtract(self.figure_a, self.figure_b).image, self.figure_c.image):
            return ['subtract']
        # Check for XOR-ing (left XOR middle = right)
        if self.is_equal(self.figure_xor(self.figure_a, self.figure_b).image, self.figure_c.image):
            return ['xor']
        # Check for and-ing (left AND middle = right)
        if self.is_equal(self.figure_and(self.figure_a, self.figure_b).image, self.figure_c.image):
            return ['and']

        '''
        # Check for resizing
        # Figures must have only one object to qualify
        if len(self.figure_a.objects) == len(self.figure_b.objects) == len(self.figure_c.objects) == 1:
            # Check for simple shape resize
            obj1 = self.figure_a.objects[0]
            obj2 = self.figure_b.objects[0]
            obj3 = self.figure_c.objects[0]

            obj1_size = obj1.size()
            obj2_size = obj2.size()
            obj3_size = obj3.size()

            xy_diff_23 = (obj3_size[0] - obj2_size[0], obj3_size[1] - obj2_size[1])
            xy_diff_12 = (obj2_size[0] - obj1_size[0], obj2_size[1] - obj1_size[1])

            if abs(xy_diff_23[0] - xy_diff_12[0]) < 3 and abs(xy_diff_23[1] - xy_diff_12[1]) < 3:
                resize_amount = ((xy_diff_23[0] + xy_diff_12[0]) / 2, (xy_diff_23[1] + xy_diff_12[1]) / 2)
                return ['resize', resize_amount]
        '''

        # Check for Add + Horizontal Slide
        # Initial fig must have 1 object and have horizontal symmetry
        if len(self.figure_a.objects) == 1 and self.has_vertical_symmetry(self.figure_a.image):
            obj_orig = self.figure_a.objects[0]
            size = self.figure_a.image.size
            width_image = size[0]
            width_obj = obj_orig.size()[0]
            max_slide_distance = (width_image / 2) - (width_obj / 2)

            for i in xrange(0, max_slide_distance, 2):
                # Slide first two objects away from each other
                obj_left = self.translate_object(obj_orig, (i, 0))
                obj_right = self.translate_object(obj_orig, (-i, 0))

                # Make new image with translated objects
                image_left_right = self.image_from_objects(size, [obj_left, obj_right])

                # Check if it is correct
                if self.is_equal(image_left_right, self.figure_b.image):
                    # Continue separating
                    for j in xrange(i, max_slide_distance, 2):
                        # Slide first two objects away from each other
                        obj_left = self.translate_object(obj_orig, (j, 0))
                        obj_right = self.translate_object(obj_orig, (-j, 0))
                        obj_center = obj_orig

                        # Draw image with third object
                        image_left_right_center = self.image_from_objects(size, [obj_left, obj_right, obj_center])
                        image_left_right = self.image_from_objects(size, [obj_left, obj_right, obj_center])

                        # Check that transformation propagates to 3rd figure
                        if self.is_equal(image_left_right_center, self.figure_c.image):
                            slide_distance = j
                            return ['add and translate', slide_distance]
                        if self.is_equal(image_left_right, self.figure_c.image):
                            slide_distance = j
                            return ['duplicate and separate', slide_distance]

                    break  # get out of outer loop


        # Check for Horizontal Pass Through
        # Must have vertical symmetry to continue
        if self.has_vertical_symmetry(self.figure_a.image):
            result = self.horizontal_pass_through(self.figure_a, self.figure_b, self.figure_c)
            if result[0] == 'horizontal pass through':
                return result

        # Check for Rotate Figures in row
        # Figures in row must be unique
        if (not self.is_equal(self.figure_a.image, self.figure_b.image)
            and not self.is_equal(self.figure_a.image, self.figure_c.image)
            and not self.is_equal(self.figure_b.image, self.figure_c.image)):

            # Check if rotating right
            if (self.is_equal(self.figure_a.image, self.figure_e.image)
                and self.is_equal(self.figure_b.image, self.figure_f.image)
                and self.is_equal(self.figure_c.image, self.figure_d.image)
                and self.is_equal(self.figure_d.image, self.figure_h.image)
                and self.is_equal(self.figure_f.image, self.figure_g.image)):
                    return ['rotate figures in row', self.figure_a]

            # Check if rotating left
            elif (self.is_equal(self.figure_a.image, self.figure_f.image)
                  and self.is_equal(self.figure_b.image, self.figure_d.image)
                  and self.is_equal(self.figure_c.image, self.figure_e.image)
                  and self.is_equal(self.figure_e.image, self.figure_g.image)
                  and self.is_equal(self.figure_f.image, self.figure_h.image)):
                    return ['rotate figures in row', self.figure_b]

            # Check for Shape Count Combination
            # Check that each figure has a unique object shape on a
            # row-by-row basis
            if ((self.figure_a.objects[0] != self.figure_b.objects[0]
                and self.figure_a.objects[0] != self.figure_c.objects[0]
                and self.figure_b.objects[0] != self.figure_c.objects[0])
                and
                (self.figure_a.objects[0] != self.figure_b.objects[0]
                and self.figure_a.objects[0] != self.figure_c.objects[0]
                and self.figure_b.objects[0] != self.figure_c.objects[0])):
                shapes = [self.figure_a.objects[0], self.figure_b.objects[0], self.figure_c.objects[0]]
                counts = [len(self.figure_a.objects), len(self.figure_b.objects), len(self.figure_c.objects)]
                combinations = []

                # Create list of combinations of shapes and shape counts
                for shape in shapes:
                    for count in counts:
                        combinations.append((shape, count))

                is_transform = True
                objects_identical = True
                for figure in self.figures:
                    shape = figure.objects[0]
                    count = len(figure.objects)

                    # Make sure objects in figure are all the same
                    for i in range(count):
                        if figure.objects[i] != figure.objects[0]:
                            objects_identical = False
                            break

                    # If all objects in figure are same
                    if objects_identical:
                        combination = shape, count

                        # If combination exists, remove from list
                        # otherwise it this proposed transform is not correct
                        if combination in combinations:
                            combinations.remove(combination)
                        else:
                            is_transform = False
                            break
                    else:
                        is_transform = False
                if is_transform:
                    print "shape count comb"
                    return ["shape count combination", combinations[0]]

        print "no transform found"
        return ['no transform found']

    def get_solution(self):
        answer = -1

        # *** REAL CODE ***
        # Check for holistic symmetry
        vertical_symmetry_measures = []
        horizontal_symmetry_measures = []
        for solution in self.solutions:
            self.figure_sol = solution
            holistic_image = self.create_merged_image()
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

        # Horizontal transforms alone have been sufficient for the practice problems encountered
        transform = self.get_transform()
        print transform[0]
        if transform[0] == 'add':
            fig_sum = self.figure_add(self.figure_g, self.figure_h)
            answer = self.find_most_similar_solution(fig_sum)

        elif transform[0] == 'subtract':
            fig_diff = self.figure_subtract(self.figure_g, self.figure_h)
            answer = self.find_most_similar_solution(fig_diff)

        elif transform[0] == 'xor':
            fig_xor = self.figure_xor(self.figure_g, self.figure_h)
            answer = self.find_most_similar_solution(fig_xor)

        elif transform[0] == 'and':
            fig_and = self.figure_and(self.figure_g, self.figure_h)
            answer = self.find_most_similar_solution(fig_and)

        elif transform[0] == 'resize':
            # if at this point, only 2 objects in figure
            # Get size of object in question and get scale factor from transform data
            obj = self.figure_h.objects[0]
            width_obj, height_obj = obj.size()
            width_trans, height_trans = transform[1]
            scale = (1 + width_trans / float(width_obj), 1 + height_trans / float(height_obj))

            im = self.figure_h.image
            width, height = im.size
            im_resized = im.resize((int(width * scale[0]), int(height * scale[1])), Image.BILINEAR)
            width_new, height_new = im_resized.size
            width_diff = width_new - width
            height_diff = height_new - height
            box = (width_diff/2, height_diff/2, width_new - width_diff/2, height_new - height_diff/2)
            fig = Figure(im_resized.crop(box))
            answer = self.find_most_similar_solution(fig)

        elif transform[0] == 'add and translate':
            translate_distance = transform[1]
            obj1 = self.figure_g.objects[0]
            size = self.figure_g.image.size

            init_l_val = 255
            obj1_new = Object((0, 0), 0)
            obj2_new = Object((0, 0), 0)
            obj1_new.remove_pixel((0, 0))
            obj2_new.remove_pixel((0, 0))

            # Slide first two objects away from each other
            for coord in obj1.area:
                obj1_new.add_pixel((coord[0] + translate_distance*2, coord[1]))
                obj2_new.add_pixel((coord[0] - translate_distance*2, coord[1]))

            # Make new image with translated objects
            image_new = Image.new('L', size, color=init_l_val)
            for xy in obj1_new.area:
                image_new.putpixel(xy, 0)
            for xy in obj2_new.area:
                image_new.putpixel(xy, 0)
            for xy in obj1.area:
                image_new.putpixel(xy, 0)

            fig = Figure(image_new)
            answer = self.find_most_similar_solution(fig)

        elif transform[0] == 'duplicate and separate':
            translate_distance = transform[1]
            objs_orig = self.figure_g.objects
            size = self.figure_g.image.size

            # Duplicate objects and separate them
            objs_left = []
            objs_right = []
            for obj in objs_orig:
                objs_left.append(self.translate_object(obj, (translate_distance[0], translate_distance[1])))
                objs_right.append(self.translate_object(obj, (-translate_distance[0], translate_distance[1])))

            # Make new image with translated objects
            image_left_right = self.image_from_objects(size, objs_left + objs_right)

            fig = Figure(image_left_right)
            answer = self.find_most_similar_solution(fig)

        elif transform[0] == 'horizontal pass through':
            size = self.figure_g.image.size
            im_centroid = (size[0]/2, size[1]/2)
            max_x = 0
            for obj in self.figure_g.objects:
                if obj.centroid[0] < im_centroid[0]:
                    if obj.max_x > max_x:
                        max_x = obj.max_x
            max_distance = int(size[0]/2)

            for i in xrange(int(max_distance/4 - 1), max_distance, 2):
                objects_new = []
                for obj in self.figure_g.objects:
                    # On the left side
                    if obj.centroid[0] < im_centroid[0]:
                        obj_new = self.translate_object(obj, (i, 0))
                    # On the right side
                    else:
                        obj_new = self.translate_object(obj, (-i, 0))
                    objects_new.append(obj_new)
                image_new = self.image_from_objects(size, objects_new)
                for solution in self.solutions:
                    if self.is_equal(image_new, solution.image):
                        answer = self.solutions.index(solution) + 1

        elif transform[0] == 'rotate figures in row':
            figure_to_match = transform[1]
            answer = self.find_most_similar_solution(figure_to_match)

        elif transform[0] == "shape count combination":
            req_shape, req_count = transform[1]

            for solution in self.solutions:
                # Check that solution meets shape/count requirements
                if len(solution.objects) == req_count and solution.objects[0] == req_shape:
                    answer = self.solutions.index(solution) + 1

        return answer

    def Solve(self, problem):
        print problem.name
        problem_name = problem.name
        answer = -1
        scores = []

        if 'Problem B' in problem_name or 'Problem C' in problem_name:
            print problem_name, 'skipped\n'
            return answer

        start_time = time.time()

        # Load all figures and make them black OR white (no grey!)
        print 'Loading figures for %s...' % problem_name
        self.figure_a = Figure(problem.figures['A'].visualFilename)
        self.figure_b = Figure(problem.figures['B'].visualFilename)
        self.figure_c = Figure(problem.figures['C'].visualFilename)
        self.figure_d = Figure(problem.figures['D'].visualFilename)
        self.figure_e = Figure(problem.figures['E'].visualFilename)
        self.figure_f = Figure(problem.figures['F'].visualFilename)
        self.figure_g = Figure(problem.figures['G'].visualFilename)
        self.figure_h = Figure(problem.figures['H'].visualFilename)

        self.figures = [self.figure_a, self.figure_b, self.figure_c,
                        self.figure_d, self.figure_e, self.figure_f,
                        self.figure_g, self.figure_h]

        print 'Identifying objects in each figure...'
        for figure in self.figures:
            figure.identify_objects()
            figure.find_centroids()

        print 'Loading all solutions and identifying the objects in each...'
        self.solutions = []
        problem_figure_keys = sorted(problem.figures.keys())
        num_solutions = 8
        for i in range(num_solutions):
            figure_sol = Figure(problem.figures[problem_figure_keys[i]].visualFilename)
            figure_sol.identify_objects()
            figure_sol.find_centroids()
            self.solutions.append(figure_sol)
        
        print 'Searching for a solution...'
        answer = self.get_solution()

        print 'Time to find solution: ', time.time() - start_time, ' seconds\n'
        return answer



