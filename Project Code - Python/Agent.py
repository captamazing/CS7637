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

class Agent:
    attribute_list = ['shape', 'fill', 'size', 'angle', 'inside', 'above', 'overlaps', 'alignment']
    sizes_list = ['very small', 'small', 'medium', 'large', 'very large', 'huge']  # index = size value
    points_attribute = 1
    points_pattern = 2

    threshold = .985
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

    list_solutions = []

    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    def is_equal(self, im1, im2):
        val = self.get_similarity(im1, im2)
        print val
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

    def get_transform(self, figure1, figure2):
        transform = []
        # Store all attributes

        figure1_object_keys = sorted(figure1.objects.keys())
        figure2_object_keys = sorted(figure2.objects.keys())
        max_num_objects = max([len(figure1_object_keys), len(figure2_object_keys)])
        for i in range(max_num_objects):
            relationship = {}
            relationship['deleted'] = False
            relationship['added'] = False

            # Figure 1 has more objects
            if i > len(figure2_object_keys):
                relationship['deleted'] = True

            # Figure 2 has more objects
            if i > len(figure1_object_keys):
                relationship['added'] = True
                figure2_object = figure2.objects[figure2_object_keys[i]]

                for j in range(len(figure2_object.attributes)):
                    if self.attribute_list[j] in figure2_object.attributes:
                        relationship[self.attribute_list[j]] = figure2_object.attributes[self.attribute_list[j]]

            elif i < len(figure1_object_keys) and i < len(figure2_object_keys):
                figure1_object = figure1.objects[figure1_object_keys[i]]
                figure2_object = figure2.objects[figure2_object_keys[i]]

                if ('shape' in figure1_object.attributes) and ('shape' in figure2_object.attributes):
                    if figure1_object.attributes['shape'] == figure2_object.attributes['shape']:
                        relationship['shape'] = 'same'
                    else:
                        relationship['shape'] = figure1_object.attributes['shape'] + " " + figure2_object.attributes['shape']

                if ('fill' in figure1_object.attributes) and ('fill' in figure2_object.attributes):
                    if figure1_object.attributes['fill'] == figure2_object.attributes['fill']:
                        relationship['fill'] = 'same'
                    else:
                        relationship['fill'] = figure1_object.attributes['fill'] + " " + figure2_object.attributes['fill']

                if ('size' in figure1_object.attributes) and ('size' in figure2_object.attributes):
                    figure1_size_value = self.sizes_list.index(figure1_object.attributes['size'])
                    figure2_size_value = self.sizes_list.index(figure2_object.attributes['size'])
                    relationship['size'] = figure1_size_value - figure2_size_value

                if ('angle' in figure1_object.attributes) and ('angle' in figure2_object.attributes):
                    if figure1_object.attributes['angle'] == figure2_object.attributes['angle']:
                        relationship['angle'] = 'same'
                    else:
                        relationship['angle'] = figure1_object.attributes['angle'] + " " + figure2_object.attributes['angle']

                if 'inside' in figure1_object.attributes and 'inside' not in figure2_object.attributes:
                    relationship['inside'] = 'deleted'
                elif 'inside' in figure2_object.attributes and 'inside' not in figure1_object.attributes:
                    relationship['inside'] = 'created'
                elif 'inside' in figure1_object.attributes and 'inside' in figure2_object.attributes:
                    figure1_attribute_keys = sorted(figure1_object.attributes.keys())
                    figure2_attribute_keys = sorted(figure2_object.attributes.keys())

                    if figure1_attribute_keys == figure2_attribute_keys:
                        for attribute_key in figure1_attribute_keys:
                            if attribute_key == 'inside':
                                continue
                            else:
                                if (figure1_object.attributes[attribute_key] == figure2_object.attributes[attribute_key]):
                                    pass
                                else:
                                    relationship['inside'] = 'changed'
                                    break
                            relationship['inside'] = 'same'

                if ('above' in figure1_object.attributes) and ('above' in figure2_object.attributes):
                    figure1_object.attributes['above']

                if ('overlaps' in figure1_object.attributes) and ('overlaps' in figure2_object.attributes):
                    figure1_object.attributes['overlaps']

                if ('alignment' in figure1_object.attributes) and ('alignment' in figure2_object.attributes):
                    relationship['alignment'] = figure1_object.attributes['alignment'] + " " + figure2_object.attributes['alignment']

            if 'inside' in figure1_object.attributes and 'inside' not in figure2_object.attributes:
                relationship['inside'] = 'deleted'
            elif 'inside' in figure2_object.attributes and 'inside' not in figure1_object.attributes:
                relationship['inside'] = 'created'
            elif 'inside' in figure1_object.attributes and 'inside' in figure2_object.attributes:
                figure1_attribute_keys = sorted(figure1_object.attributes.keys())
                figure2_attribute_keys = sorted(figure2_object.attributes.keys())

                if figure1_attribute_keys == figure2_attribute_keys:
                    for attribute_key in figure1_attribute_keys:
                        if attribute_key == 'inside':
                            continue
                        else:
                            if (figure1_object.attributes[attribute_key] == figure2_object.attributes[attribute_key]):
                                pass
                            else:
                                relationship['inside'] = 'changed'
                                break
                        relationship['inside'] = 'same'

            transform.append(relationship)
        return transform

    def has_angle_pattern(self, angle_a_c, angle_b_sol, angle_a_b, angle_c_sol):
        if (angle_a_b == angle_c_sol) and (angle_a_c == angle_b_sol):
            return True

        if "same" in angle_a_c or "same" in angle_b_sol or "same" in angle_a_b or "same" in angle_c_sol:
            return False

        # If we made it this far, we know each angle transformation contains only numbers

        angles_a_b = angle_a_b.split(" ")
        angle_a = int(float(angles_a_b[0]))
        angle_b = int(float(angles_a_b[1]))

        angles_c_sol = angle_c_sol.split(" ")
        angle_c = int(float(angles_c_sol[0]))
        angle_sol = int(float(angles_c_sol[1]))

        symmetry_y = False
        symmetry_x = False
        # Symmetry across Y-axis
        if (((90 - angle_a == angle_b - 90) or
            (270 - angle_a == angle_b - 270))
            and
            ((90 - angle_c == angle_sol - 90) or
             (270 - angle_c == angle_sol - 270))):
            symmetry_y = True

        # Symmetry across X-axis
        if (((180 - angle_a == angle_c - 180) or
            (360 - angle_a == angle_c))
            and
            ((180 - angle_b == angle_sol - 180) or
             (360 - angle_b == angle_sol))):
            symmetry_x = True

        return symmetry_y and symmetry_x

    def has_alignment_pattern(self, alignment_a_c, alignment_b_sol, alignment_a_b, alignment_c_sol):
        if (alignment_a_b == alignment_c_sol) and (alignment_a_c == alignment_b_sol):
            return True

        alignments_a_b = alignment_a_b.split(" ")
        alignments_c_sol = alignment_c_sol.split(" ")
        alignments = [alignments_a_b[0], alignments_a_b[1], alignments_c_sol[0], alignments_c_sol[1]]
        all_unique = True
        for alignment in alignments:
            count = alignments.count(alignment)
            if count > 1:
                all_unique = False
                break
        if all_unique:
            return True

        return False

    #Merged all figures in problem + solution into a single large image
    def create_merged_image(self):
        x_orig = self.figure_a.size[0]
        y_orig = self.figure_a.size[1]
        x_new = x_orig * 3
        y_new = y_orig * 3
        merged_img = Image.new('RGB', (x_new, y_new))

        x = 0
        y = 0
        merged_img.paste(self.figure_a, (x, y))
        x += x_orig
        merged_img.paste(self.figure_b, (x, y))
        x += x_orig
        merged_img.paste(self.figure_c, (x, y))

        x = 0
        y += y_orig
        merged_img.paste(self.figure_d, (x, y))
        x += x_orig
        merged_img.paste(self.figure_e, (x, y))
        x += x_orig
        merged_img.paste(self.figure_f, (x, y))

        x = 0
        y += y_orig
        merged_img.paste(self.figure_g, (x, y))
        x += x_orig
        merged_img.paste(self.figure_h, (x, y))
        x += x_orig
        merged_img.paste(self.figure_sol, (x, y))

        return merged_img

    #Checks for vertical symmetry (across vertical axis)
    def has_vertical_symmetry(self, image):
        return self.is_equal(image, ImageOps.mirror(image))

    #Checks for horizontal symmetry (across horiontal axis)
    def has_horizontal_symmetry(self, image):
        return self.is_equal(image, ImageOps.flip(image))

    def get_solution_score(self):
        score = 0
        # Check for holistic symmetry
        eligible_for_bonus = True
        holistic_image = self.create_merged_image()
        if self.has_vertical_symmetry(holistic_image):
            score += self.points_holistic_symmetry
        else:
            eligible_for_bonus = False
        if self.has_horizontal_symmetry(holistic_image):
            score += self.points_holistic_symmetry
        else:
            eligible_for_bonus = False
        if eligible_for_bonus:
            score += self.points_bonus
            eligible_for_bonus = False
        '''
        len_a_b = len(transform_a_b)
        len_a_c = len(transform_a_c)
        len_b_sol = len(transform_b_sol)
        len_c_sol = len(transform_c_sol)

        num_objects_list = [len_a_b, len_a_c, len_b_sol, len_c_sol]
        num_objects = max(num_objects_list)
        score = 0
        for i in range(num_objects):
            if num_objects > len(transform_a_b) or num_objects > len(transform_a_c) or num_objects > len(transform_b_sol) or num_objects > len(transform_c_sol):
                continue

            vertical_relationship = transform_a_c[i]
            vertical_relationship_sol = transform_b_sol[i]

            horizontal_relationship = transform_a_b[i]
            horizontal_relationship_sol = transform_c_sol[i]

            relationship_attributes = sorted(vertical_relationship.keys())
            for j in range(len(relationship_attributes)):
                try:
                    if relationship_attributes[j] == 'alignment':
                        if self.has_alignment_pattern(vertical_relationship[relationship_attributes[j]],
                                                      vertical_relationship_sol[relationship_attributes[j]],
                                                      horizontal_relationship[relationship_attributes[j]],
                                                      horizontal_relationship_sol[relationship_attributes[j]]):
                            score += self.points_pattern

                    elif relationship_attributes[j] == 'angle':
                        if self.has_angle_pattern(vertical_relationship[relationship_attributes[j]],
                                                  vertical_relationship_sol[relationship_attributes[j]],
                                                  horizontal_relationship[relationship_attributes[j]],
                                                  horizontal_relationship_sol[relationship_attributes[j]]):
                            score += self.points_pattern
                    else:
                        if vertical_relationship[relationship_attributes[j]] == vertical_relationship_sol[relationship_attributes[j]]:
                            score += self.points_attribute
                        if horizontal_relationship[relationship_attributes[j]] == horizontal_relationship_sol[relationship_attributes[j]]:
                            score += self.points_attribute
                except KeyError:
                    pass
                    #print 'Key not found: ', relationship_attributes[j]
                except IndexError:
                    pass
                    #print 'Index out of range: ', j
        '''
        return score

    def Solve(self, problem):
        problem_name = problem.name
        answer = -1

        #Load all figures and make them black OR white (no grey!)
        self.figure_a = Image.open(problem.figures['A'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_b = Image.open(problem.figures['B'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_c = Image.open(problem.figures['C'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_d = Image.open(problem.figures['D'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_e = Image.open(problem.figures['E'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_f = Image.open(problem.figures['F'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_g = Image.open(problem.figures['G'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
        self.figure_h = Image.open(problem.figures['H'].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')

        scores = []
        problem_figure_keys = sorted(problem.figures.keys())
        num_solutions = 8
        for i in range(num_solutions):
            self.figure_sol = Image.open(problem.figures[problem_figure_keys[i]].visualFilename).convert('L').point(lambda x: 0 if x < 128 else 255, '1')
            self.create_merged_image()
            score = self.get_solution_score()
            scores.append(score)

        score_max = max(scores)

        if score_max == 0:
            answer = -1
        else:
            answer = score_max
        '''
        if scores.count(0) >= 2:
            answer = -1
        elif score_max > 0:
            answer = scores.index(score_max) + 1    # Solution number = index + 1
        else:
            answer = -1
        '''

        '''
        print problem.name
        print "Scores :", scores
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'
        '''
        return answer



