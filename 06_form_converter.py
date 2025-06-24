# Functions
import math
from fractions import Fraction


def get_coefs():
    """Asks the user for each of the coefficients of a polynomial"""

    coefficients = []

    # list of degree coefs to ask
    degree_list = ["Constant: ", "X term: ", "X^2 term: "]

    # loop through all the quadratic terms
    for deg in degree_list:
        coef = num_check(deg, float, None)
        coefficients.append(coef)

    # make sure that x^2 value is set
    while coefficients[2] == 0:
        print("sorry - you need a value for the x^2 value")
        coefficients[2] = num_check("X^2 term: ", float, None)

    return coefficients


def num_check(question, datatype=int, low=0, high=None, exit_code="xxx"):
    """Function to make sure user inputs an integer / float that is within parameters"""

    # check if parameters are set
    if low is not None and high is None:
        ror = f" that is at least {low}"
        check = 0
    elif low is not None and high is not None:
        ror = f" that is between {low} and {high}"
        check = 1
    elif low is None and high is not None:
        ror = f" that at most {high}"
        check = 2
    else:
        ror = ""
        check = 3

    # get correct error message for data type
    if datatype == int:
        err = "Please enter an integer"
    else:
        err = "Please enter a number"

    error = err + ror

    while True:

        # tests for exit code
        test_exit = input(question).lower()

        if test_exit == exit_code or test_exit == exit_code[0]:
            return "exit"

        # try statement for checking that it is of the correct datatype
        try:
            response = datatype(test_exit)

            # Different calculations for set values of low and high
            if check == 0:
                if response >= low:
                    return response
                else:
                    print(error)

            elif check == 1:
                if low <= response <= high:
                    return response
                else:
                    print(error)

            elif check == 2:
                if response <= high:
                    return response
                else:
                    print(error)

            else:
                return response

        except ValueError:
            print(err)


def string_check(question, ans_list=None, num_letters=1):
    """Checks that the user entered the full word OR the first letter"""

    # set the default value of the list to a list
    if ans_list is None:
        ans_list = ['yes', 'no']

    # make the error message look more readable
    lis = ""
    for ite in ans_list:
        if ite != ans_list[-1]:
            lis += (ite + " / ")
        else:
            lis += ite

    # loop for authenticity
    while True:

        response = input(question).lower()

        for item in ans_list:

            # check for the entire word
            if response == item:
                return item

            # check for the first letter of the response
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from {lis}\n")


def solve_polynomial(coef_list):
    """Solves a quadratic using the quadratic formula and returns roots (imaginary and real)"""

    # simplifying coefficient values
    a = coef_list[2]
    b = coef_list[1]
    c = coef_list[0]

    # getting discriminant
    discriminant = (b ** 2) - (4 * a * c)

    # getting roots for each case of discriminant value
    # negative means imaginary roots
    if discriminant < 0:
        root_1 = b * -1 / (2 * a), " + i", "\u221a", discriminant * -1, "/", 2 * a, "rect"
        root_2 = b * -1 / (2 * a), " - i", "\u221a", discriminant * -1, "/", 2 * a, "rect"

    # discriminant == 0 means only one root
    elif discriminant == 0:
        root_1 = root_2 = b * -1 / (2 * a), "real"

    # real roots
    else:
        root_1 = ((b * -1) + math.sqrt(discriminant)) / (2 * a), "real"
        root_2 = ((b * -1) - math.sqrt(discriminant)) / (2 * a), "real"

    return root_1, root_2


def simple_roots(root_list):
    """simplifies the roots of a quadratic provided by the solve_polynomial function"""

    # getting seperate roots
    root_1, root_2 = root_list
    # root_list contains the raw ints and strings returned by the solve_polynomial function
    # root_list contains two roots, the roots are either in 'real' or 'rect' form
    # 'rect' form holds info like this: (real_num, ' +- i', 'sqrt sign', 'discriminant', '/', denominator, root type
    # 'real' form holds info like this: (real_num, root type)

    # different techniques for different kinds of roots
    if root_1[-1] == 'rect':

        # checking for sqrt(root_1[3]) being an integer
        intest_1 = math.sqrt(root_1[3])
        rem_1 = (intest_1 * 10) % 10

        if rem_1 == 0:

            # simplifying square root
            discriminant_1 = Fraction(int(math.sqrt(root_1[3])))
            denom_1 = Fraction(root_1[5])
            sign_1 = ""

            # simplify denominator (if possible)
            fraction_1 = discriminant_1 / denom_1
            fraction_1 = fraction_1.limit_denominator()
            # limit denominator method auto simplifies the fraction

        else:

            # unable to simplify square root
            sign_1 = " \u221a"  # needs the sqrt sign
            fraction_1 = f"{root_1[3]}/{root_1[5]}"
            # keep the fraction the same

        # do the same for the second root
        intest_2 = math.sqrt(root_2[3])
        rem_2 = (intest_2 * 10) % 10

        # simplifying other square root (if possible)
        if rem_2 == 0:
            discriminant_2 = Fraction(int(math.sqrt(root_2[3])))
            denom_2 = Fraction(root_2[5])
            sign_2 = ""

            # simplify denominator (if possible)
            fraction_2 = discriminant_2 / denom_2
            fraction_2 = fraction_2.limit_denominator()
            # the limit_denominator method auto simplifies the fraction

        else:

            # unable to simplify square root
            sign_2 = " \u221a"  # needs the sqrt sign
            fraction_2 = f"{root_2[3]}/{root_2[5]}"
            # keep the fraction the same

        # dont display coefficient if coefficient is 1 or 0
        # just cleans up the final simplified root so it's easier to look at
        if fraction_1 == 1:
            fraction_1 = ""
        if fraction_2 == 1:
            fraction_2 = ""

        if root_1[0] == 0:
            real_num1 = ""
        else:
            real_num1 = root_1[0]

        if root_2[0] == 0:
            real_num2 = ""
        else:
            real_num2 = root_2[0]

        # simplify the roots into one string (+ type) for printing
        sim_root_1 = f"{real_num1}{root_1[1]}{sign_1}{fraction_1}", 'rect'
        sim_root_2 = f"{real_num2}{root_2[1]}{sign_2}{fraction_2}", 'rect'

    else:  # real roots are simple
        sim_root_1 = root_1
        sim_root_2 = root_2

    return sim_root_1, sim_root_2


def convert_roots(start_roots):
    """Converts roots in real or rect form into all the other forms of roots
    these converted roots are always in the order: real, rect, polar, exponent"""

    # real roots are special when converted
    if start_roots[0][-1] == 'real':
        real_form = start_roots[0][0], start_roots[1][0], 'real'
        rect_form = start_roots[0][0], start_roots[1][0], 'rect' # because of no i value, rect and real identical

        polar_form = []
        exponent_form = []
        for root in start_roots:

            if root[0] < 0:
                # the 'r' in r cis 0 and re^i0 is always absolute
                # for real negative numbers we use pi as the angle (180 degrees)
                polar_root = f"{abs(root[0])} cis \u03C0"  # \u03C0 is the pi symbol
                expo_root = f"{abs(root[0])} e^(i\u03C0)"
            else:
                polar_root = f"{root[0]} cis 0"
                expo_root = f"{root[0]} e^(i0)"

            polar_form.append(polar_root)
            exponent_form.append(expo_root)

        polar_form.append('polar')
        exponent_form.append('exponential')

    else:  # rect form converting
        real_form = "n/a", "n/a", 'real'  # roots are imaginary not real
        simple_rect = simple_roots(start_roots)  # simplify the roots for printing
        rect_form = simple_rect[0][0], simple_rect[1][0], 'rect'

        # get the y (imaginary) and the x (real)
        # both roots will be conjuates of eachother, meaning the magnitude will be the same
        # just the imaginary part will be flipped (* -1)
        imaginary = math.sqrt(start_roots[0][3]) / start_roots[0][5]
        real = start_roots[0][0]
        print(f"i:{imaginary}\tr:{real}")

        pre_magnitude = (real ** 2) + (imaginary ** 2)  # pythagorean thereom

        if ((math.sqrt(pre_magnitude) * 10) % 10) == 0:  # simplifying the magnitude
            magnitude = math.sqrt(pre_magnitude)
        else:
            magnitude = f"\u221a{pre_magnitude}"

        if real == 0:  # making sure that we dont recieve an error from the atan() function
            angle = math.pi / 2
        else:
            angle = math.atan(abs(imaginary / real))

        if real < 0:  # because the atan is absolute, we need to take away from a half rotation
            angle = math.pi - angle
        if imaginary < 0:  # the angle has to be between -pi and pi
            angle *= -1

        simple_angle = Fraction(angle / math.pi).limit_denominator(1000)

        polar_form = (f"{magnitude} cis {simple_angle.numerator}\u03C0/{simple_angle.denominator}",
                      f"{magnitude} cis -{simple_angle.numerator}\u03C0/{simple_angle.denominator}",
                      'polar')

        exponent_form = (f"{magnitude} e^(i {simple_angle.numerator}\u03C0/{simple_angle.denominator})",
                         f"{magnitude} e^(i -{simple_angle.numerator}\u03C0/{simple_angle.denominator})",
                         'exponential')

    return real_form, rect_form, polar_form, exponent_form


# Main

how_many = num_check("how many equations: ")
print()

# loop for testing
for _ in range(how_many):

    coefficient_list = get_coefs()
    print(f"\nYour equation: {coefficient_list[2]}X^2 + {coefficient_list[1]}X + {coefficient_list[0]}")

    print()
    roots = solve_polynomial(coefficient_list)

    print(f"raw: {roots}\n")

    real_form, rect_form, polar_form, expo_form = convert_roots(roots)
    simple_form = simple_roots(roots)
    print(simple_form[0][0], "\t", simple_form[1][0])

    root_dict = {
        real_form[-1]: real_form[:-1],
        rect_form[-1]: rect_form[:-1],
        polar_form[-1]: polar_form[:-1],
        expo_form[-1]: expo_form[:-1]
    }
    print()
    for form, value in root_dict.items():
        print(f"{form} form: {value[0]}\t{value[1]}\n")
