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
        answer = -1
        attributesA = []
        attributesB = []
        attributesC = []
        attributes1 = []
        attributes2 = []
        attributes3 = []
        attributes4 = []
        attributes5 = []
        attributes6 = []

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
        '''
        attributesA = problem.figures['A'].objects['a'].attributes
        attributesB = problem.figures['B'].objects['b'].attributes
        attributesC = problem.figures['C'].objects['c'].attributes

        attributes1 = problem.figures['1'].objects['d'].attributes
        attributes2 = problem.figures['2'].objects['e'].attributes
        attributes3 = problem.figures['3'].objects['f'].attributes
        attributes4 = problem.figures['4'].objects['g'].attributes
        attributes5 = problem.figures['5'].objects['h'].attributes
        attributes6 = problem.figures['6'].objects['i'].attributes

        print problem.name
        print "Correct answer: ", problem.correctAnswer
        print "Answer selected: ", answer, '\n'

        return answer