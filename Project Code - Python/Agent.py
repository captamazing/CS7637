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

                if i > len(figure2_object_keys):
                    relationship['deleted'] = True

                if i > len(figure1_object_keys):
                    relationship['added'] = True
                    figure2_object = figure2.objects[figure2_object_keys[i]]

                    for j in range(len(figure2_object.attributes)):
                        if attribute_list[j] in figure2_object.attributes:
                            relationship[attribute_list[j]] = figure2_object.attributes[attribute_list[j]]

                elif i < len(figure1_object_keys) and i < len(figure2_object_keys):
                    try:
                        figure1_object = figure1.objects[figure1_object_keys[i]]
                        figure2_object = figure2.objects[figure2_object_keys[i]]
                    except IndexError:
                        print 'index: ', i
                        print 'figure1 keys: ', figure1_object_keys
                        print 'figure1: ', figure1_object
                        print 'figure2 keys: ', figure2_object_keys
                        print 'figure2: ', figure2_object

                    if ('shape' in figure1_object.attributes) and ('shape' in figure2_object.attributes):
                        if figure1_object.attributes['shape'] == figure2_object.attributes['shape']:
                            relationship['shape'] = 'same'
                        else:
                            relationship['shape'] = figure1_object.attributes['shape'] + " " + figure2_object.attributes['shape']

                    if ('fill' in figure1_object.attributes) and ('fill' in figure2_object.attributes):
                        if figure1_object.attributes['fill'] == figure2_object.attributes['fill']:
                            relationship['fill'] = 'same'
                        else:
                            relationship['fill'] = figure1_object.attributes['fill'] + " " + figure1_object.attributes['fill']

                    if ('size' in figure1_object.attributes) and ('size' in figure2_object.attributes):
                        figure1_size_value = sizes_list.index(figure1_object.attributes['size'])
                        figure2_size_value = sizes_list.index(figure2_object.attributes['size'])
                        relationship['size'] = figure1_size_value - figure2_size_value

                    if ('angle' in figure1_object.attributes) and ('angle' in figure2_object.attributes):
                        figure1_angle = int(float(figure1_object.attributes['angle']))
                        figure2_angle = int(float(figure2_object.attributes['angle']))
                        relationship['angle'] = figure1_angle - figure2_angle

                    if ('inside' in figure1_object.attributes) and ('inside' in figure2_object.attributes):
                        figure1_object.attributes['inside']

                    if ('above' in figure1_object.attributes) and ('above' in figure2_object.attributes):
                        figure1_object.attributes['above']

                    if ('overlaps' in figure1_object.attributes) and ('overlaps' in figure2_object.attributes):
                        figure1_object.attributes['overlaps']

                    if ('alignment' in figure1_object.attributes) and ('alignment' in figure2_object.attributes):
                        figure1_object.attributes['alignment']

                transform.append(relationship)
            return transform

        def get_solution_score(transform_a_b, transform_a_c, transform_b_sol, transform_c_sol):

            num_relationships = len(transform_a_b)  # All relationships should have the same number of objects
            score = 0
            for i in range(num_relationships):
                vertical_relationship = transform_a_b[i]
                vertical_relationship_sol = transform_c_sol[i]

                horizontal_relationship = transform_a_c[i]
                horizontal_relationship_sol = transform_b_sol[i]

                relationship_attributes = sorted(vertical_relationship.keys())
                for j in range(len(relationship_attributes)):
                    try:
                        if vertical_relationship[relationship_attributes[j]] == vertical_relationship_sol[relationship_attributes[j]]:
                            score += 1
                        if horizontal_relationship[relationship_attributes[j]] == horizontal_relationship_sol[relationship_attributes[j]]:
                            score += 1
                    except KeyError:
                        print 'Key not found: ', relationship_attributes[j]
                    except IndexError:
                        print 'Index out of range: ', j

            return score
        '''
        -Compare A to B
        -Compare A to C
        -Establish attribute changes for each comparison

        -Compare C to 1, 2, 3, 4, 5, and 6
        -Compare B to 1, 2, 3, 4, 5, and 6
        -Choose answer such that attribute changes from A to B are same as C to x
                             and attribute changes from A to C are same as B to x

        ======================================================
        -Create relationship between figure A and B
        -Create relationship between figure A and C
        -Create common relationship/transform

        -For each solution:
            -Create relationship between figure B and solution
            -Create relationship between figure C and solution
            -Create common relationship/transform
            -Compare to relationship/transform found above
        '''

        transform_a_b = get_transform(problem.figures['A'], problem.figures['B'])
        transform_a_c = get_transform(problem.figures['A'], problem.figures['C'])

        # Used for indexing
        num_matrices_in_problem = 0
        if problem.problemType == '2x2':
            num_matrices_in_problem = 3
        elif problem.problemType == '3x3':
            num_matrices_in_problem = 8

        scores = []
        problem_figure_keys = sorted(problem.figures.keys())
        num_solutions = 6
        for i in range(num_solutions):
            transform_b_sol = get_transform(problem.figures['B'], problem.figures[problem_figure_keys[i]])
            transform_c_sol = get_transform(problem.figures['C'], problem.figures[problem_figure_keys[i]])

            score = get_solution_score(transform_a_b, transform_a_c, transform_b_sol, transform_c_sol)

            scores.append(score)

        answer = scores.index(max(scores)) + 1      # Solution number = index + 1
        print problem.name
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'

        return answer


