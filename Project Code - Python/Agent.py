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
        attribute_list = ['shape', 'fill', 'size', 'angle', 'inside', 'above', 'overlaps', 'angle', 'alignment']
        sizes = ['very small', 'small', 'medium', 'large', 'very large', 'huge'] # index = size value

        def get_relationship(figure1, figure2):
            '''
            figure
                objects
                    attributes
                        name
                        value

            relationship
                figures
                    objects
                        attribute changes
                            name
                            value change
            '''

            relationship = {}
            attributes1 = []
            attributes2 = []


            # Store all attributes
            for i in range(len(figure1.objects)):
                for j in range(len(figure1.objects[i].attributes)):
                    for k in range(len(attribute_list)):
                        try:
                            attribute_list[k]
                        except:
                            print attribute_list[k], ' not present'

                attributes1.append(figure1.objects[i].attributes)

            for i in range(len(figure2.objects)):
                attributes2.append(figure2.objects[i].attributes)



            return relationship

        answer = -1

        '''
        ================
           OLD CODE
        ================
        attributesA = []
        attributesB = []
        attributesC = []
        attributes1 = []
        attributes2 = []
        attributes3 = []
        attributes4 = []
        attributes5 = []
        attributes6 = []

        attributesA = problem.figures['A'].objects['a'].attributes
        attributesB = problem.figures['B'].objects['b'].attributes
        attributesC = problem.figures['C'].objects['c'].attributes

        attributes1 = problem.figures['1'].objects['d'].attributes
        attributes2 = problem.figures['2'].objects['e'].attributes
        attributes3 = problem.figures['3'].objects['f'].attributes
        attributes4 = problem.figures['4'].objects['g'].attributes
        attributes5 = problem.figures['5'].objects['h'].attributes
        attributes6 = problem.figures['6'].objects['i'].attributes
        '''

        # Comparisons to draw:
        # problem.figures['A'] to problem.figures['B']
        # problem.figures['A'] to problem.figures['C']
        # problem.figures['C'] to answer
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

        relationship_a_b = get_relationship(problem.figures['A'], problem.figures['B'])
        relationship_a_c = get_relationship(problem.figures['A'], problem.figures['C'])

        # Merge relationships
        final_transform = []

        num_matrices_in_problem = 0
        if problem.problemType == '2x2':
            num_matrices_in_problem = 3
        elif problem.problemType == '3x3':
            num_matrices_in_problem = 8

        for i in range(len(problem.figures) - num_matrices_in_problem):
            relationship_b_sol = get_relationship(problem.figures['B'], problem.figures[i + 2])
            relationship_c_sol = get_relationship(problem.figures['C'], problem.figures[i + 2])

            # Merge relationships
            sol_transform = []

            # if final_transform equals sol_transform

        print problem.name
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'

        return answer


