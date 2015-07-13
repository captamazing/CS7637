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
#from PIL import Image

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass



    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        attribute_list = ['shape', 'fill', 'size', 'angle', 'inside', 'above', 'overlaps', 'alignment']
        sizes_list = ['very small', 'small', 'medium', 'large', 'very large', 'huge']  # index = size value
        points_attribute = 1
        points_pattern = 2

        problem_name = problem.name
        answer = -1

        def get_transform(figure1, figure2):
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
                        if attribute_list[j] in figure2_object.attributes:
                            relationship[attribute_list[j]] = figure2_object.attributes[attribute_list[j]]

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
                        figure1_size_value = sizes_list.index(figure1_object.attributes['size'])
                        figure2_size_value = sizes_list.index(figure2_object.attributes['size'])
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

        def get_solution_score(transform_a_b, transform_a_c, transform_b_sol, transform_c_sol):
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
                            if has_alignment_pattern(vertical_relationship[relationship_attributes[j]],
                                                     vertical_relationship_sol[relationship_attributes[j]],
                                                     horizontal_relationship[relationship_attributes[j]],
                                                     horizontal_relationship_sol[relationship_attributes[j]]):
                                score += points_pattern

                        elif relationship_attributes[j] == 'angle':
                            if has_angle_pattern(vertical_relationship[relationship_attributes[j]],
                                                 vertical_relationship_sol[relationship_attributes[j]],
                                                 horizontal_relationship[relationship_attributes[j]],
                                                 horizontal_relationship_sol[relationship_attributes[j]]):
                                score += points_pattern
                        else:
                            if vertical_relationship[relationship_attributes[j]] == vertical_relationship_sol[relationship_attributes[j]]:
                                score += points_attribute
                            if horizontal_relationship[relationship_attributes[j]] == horizontal_relationship_sol[relationship_attributes[j]]:
                                score += points_attribute
                    except KeyError:
                        pass
                        #print 'Key not found: ', relationship_attributes[j]
                    except IndexError:
                        pass
                        #print 'Index out of range: ', j

            return score

        def has_alignment_pattern(alignment_a_c, alignment_b_sol, alignment_a_b, alignment_c_sol):
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

        def has_angle_pattern(angle_a_c, angle_b_sol, angle_a_b, angle_c_sol):
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

        figure_a = problem.figures['A']
        figure_b = problem.figures['B']
        figure_c = problem.figures['C']

        transform_a_b = get_transform(figure_a, figure_b)
        transform_a_c = get_transform(figure_a, figure_c)

        scores = []
        problem_figure_keys = sorted(problem.figures.keys())
        num_solutions = 6
        for i in range(num_solutions):
            figure_sol = problem.figures[problem_figure_keys[i]]
            transform_b_sol = get_transform(figure_b, figure_sol)
            transform_c_sol = get_transform(figure_c, figure_sol)

            score = get_solution_score(transform_a_b, transform_a_c, transform_b_sol, transform_c_sol)

            scores.append(score)

        score_max = max(scores)

        if scores.count(0) >= 2:
            answer = -1
        elif score_max > 0:
            answer = scores.index(score_max) + 1    # Solution number = index + 1
        else:
            answer = -1

        '''
        print problem.name
        print "Scores :", scores
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'
        '''
        return answer


