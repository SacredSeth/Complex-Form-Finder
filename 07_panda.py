# Functions
import math
from fractions import Fraction
import pandas as pd
from prettytable import PrettyTable


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


def get_roots(form = 'rect'):
    """asks the user for the variables of a complex root
    and returns it in the correct data form for further calculations"""

    if form == 'real':  # real
        root = num_check("root: ", float, None), 'real'

    elif form == 'rect':  # rect
        real = num_check("(a+bi) enter a: ", float, None)
        imaginary = num_check("(a+bi) enter b: ", float, None)
        root = real, imaginary, 'rect'

    elif form == 'polar':  # polar
        magnitude = num_check("(r cis 0) enter r: ", float)
        theta = num_check("enter the angle (in radians, use pi for pi): ",
                          float, exit_code="pi", low=math.pi * -1, high=math.pi)
        if theta == "pi":
            theta = math.pi

        root = magnitude, theta, 'polar'

    else:  # exponent
        magnitude = num_check("(re^(i0)) enter r: ", float)
        theta = num_check("enter the angle (in radians, use pi for pi): ",
                          float, exit_code="pi", low=math.pi * -1, high=math.pi)
        if theta == "pi":
            theta = math.pi

        root = magnitude, theta, 'exponential'

    return root


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
            return exit_code

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

    # getting separate roots
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


def make_convertable(to_make):
    """Makes rect form of root provided by solve_polynomial
    into something that the convert_roots function will understand"""

    real = to_make[0][0]
    imaginary = math.sqrt(to_make[0][3]) / to_make[0][5]
    converted_roots = (real, imaginary, 'rect'), (real, imaginary * -1, 'rect')

    return converted_roots


def convert_roots(start_root):
    """Converts roots in real or rect form into all the other forms of roots
    these converted roots are always in the order: real, rect, polar, exponent"""

    # real roots are special when converted
    if start_root[-1] == 'real':  # real roots are in form (value, form)
        rea_form = start_root[0], 'real'
        rec_form = start_root[0], 0, 'rect' # because of no i value, rect and real identical

        if start_root[0] < 0:
            angle = math.pi
        else:
            angle = 0

        pol_form = abs(start_root[0]), angle, 'polar'
        exponent_form = abs(start_root[0]), angle, 'exponential'

    elif start_root[-1] == 'rect':  # rect form converting
        rea_form = 'n/a', 'real'  # roots are imaginary not real
        rec_form = start_root

        imaginary = start_root[1]
        real = start_root[0]

        if imaginary == 0:
            rea_form = real, 'real'

        magnitude = math.sqrt((real ** 2) + (imaginary ** 2))  # pythagorean thereom

        if real == 0:  # making sure that we dont recieve an error from the atan() function
            angle = math.pi / 2
        else:
            angle = math.atan(abs(imaginary / real))

        if real < 0:  # because the atan is absolute, we need to take away from a half rotation
            angle = math.pi - angle
        if imaginary < 0:  # the angle has to be between -pi and pi
            angle *= -1

        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

    elif start_root[-1] == 'polar':  # convert from polar form
        rea_form = 'n/a', 'real'

        magnitude = start_root[0]
        angle = start_root[1]

        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

        if abs(angle) < math.pi / 2:  # acute angles
            imaginary = magnitude * math.sin(abs(angle))
            real = magnitude * math.cos(abs(angle))

        elif abs(angle) == math.pi / 2:  # right angle (imaginary)
            imaginary = magnitude
            real = 0

        elif angle == math.pi or angle == 0:  # straight line (real)
            rea_form = magnitude if angle == 0 else -magnitude, 'real'  # redefine real value
            imaginary = 0
            real = magnitude if angle == 0 else -magnitude

        else:  # obtuse angles
            imaginary = magnitude * math.sin(math.pi - abs(angle))
            real = magnitude * math.cos(math.pi - abs(angle))

        if angle < 0:  # separate if statement for flipping the imaginary value
            imaginary *= -1

        rec_form = real, imaginary, 'rect'

    else:  # convert from exponent form
        rea_form = 'n/a', 'real'

        magnitude = start_root[0]
        angle = start_root[1]

        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

        if abs(angle) < math.pi / 2:  # acute angles
            imaginary = magnitude * math.sin(abs(angle))
            real = magnitude * math.cos(abs(angle))

        elif abs(angle) == math.pi / 2:  # right angle (imaginary)
            imaginary = magnitude
            real = 0

        elif angle == math.pi or angle == 0:  # straight line (real)
            rea_form = magnitude if angle == 0 else -magnitude, 'real'  # redefine real value
            imaginary = 0
            real = magnitude if angle == 0 else -magnitude

        else:  # obtuse angles
            imaginary = magnitude * math.sin(math.pi - abs(angle))
            real = magnitude * math.cos(math.pi - abs(angle))

        if angle < 0:  # separate if statement for flipping the imaginary value
            imaginary *= -1

        rec_form = real, imaginary, 'rect'

    # end of if statements

    return rea_form, rec_form, pol_form, exponent_form


def print_roots(list_of_roots):
    """Converts al roots into readable form and prints them"""

    if type(list_of_roots[0]) != tuple:
        list_of_roots = [list_of_roots]

    final_list = []

    for item in list_of_roots:

        match item[-1]:

            case 'real':

                if type(item[0]) == str:
                    final = 'n/a', 'real'
                elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                    final = f"{Fraction(item[0])}", 'real'
                else:
                    final = f"{item[0]:.3f}", 'real'

            case 'rect':

                if item[1] < 0:

                    sign = " - "

                    if item[0] == 0:
                        rel = ""
                        sign = "-"
                    elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                        rel = Fraction(item[0])
                    else:
                        rel = f"{item[0]:.3f}"

                    if item[1] == 0:
                        ima = ""
                        sign = "-"
                    elif item[1] == 1:
                        ima = "i"
                    elif Fraction(item[1]) == Fraction(item[1]).limit_denominator(100):
                        ima = f"{abs(Fraction(item[1]))}i"
                    else:
                        ima = f"{abs(item[1]):.3f}i"

                    final = f"{rel}{sign}{ima}", 'rect'

                else:

                    sign = " + "

                    if item[0] == 0:
                        rel = ""
                        sign = ""
                    elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                        rel = Fraction(item[0])
                    else:
                        rel = f"{item[0]:.3f}"

                    if item[1] == 0:
                        ima = ""
                        sign = ""
                    elif item[1] == 1:
                        ima = "i"
                    elif Fraction(item[1]) == Fraction(item[1]).limit_denominator(100):
                        ima = f"{Fraction(item[1])}i"
                    else:
                        ima = f"{item[1]:.3f}i"

                    final = f"{rel}{sign}{ima}", 'rect'

            case 'polar':

                simple_angle = Fraction(item[1] / math.pi)

                if simple_angle == simple_angle.limit_denominator(100):

                    simple_angle = simple_angle.limit_denominator(100)

                    if simple_angle.numerator == 0:
                        angle = "0"
                    elif simple_angle.numerator == (1 or -1):
                        angle = f"\u03C0/{simple_angle.denominator}" if simple_angle.numerator == 1\
                            else f"-\u03C0/{simple_angle.denominator}"
                    else:
                        angle = f"{simple_angle.numerator}\u03C0/{simple_angle.denominator}"

                else:
                    angle = f"{item[1]:.3f}"

                if item[1] == math.pi:
                    final = f"{item[0]:.3f} cis \u03C0", 'polar'
                else:
                    final = f"{item[0]:.3f} cis {angle}", 'polar'

            case 'exponential':

                simple_angle = Fraction(item[1] / math.pi)

                if simple_angle == simple_angle.limit_denominator(100):

                    simple_angle = simple_angle.limit_denominator(100)

                    if simple_angle.numerator == 0:
                        angle = "0"
                    elif simple_angle.numerator == (1 or -1):
                        angle = f"\u03C0/{simple_angle.denominator}" if simple_angle.numerator == 1 \
                            else f"-\u03C0/{simple_angle.denominator}"
                    else:
                        angle = f"{simple_angle.numerator}\u03C0/{simple_angle.denominator}"

                else:
                    angle = f"{item[1]:.3f}"

                if item[1] == math.pi:
                    final = f"{item[0]:.3f} e^(\u03C0i)", "exponential"
                else:
                    final = f"{item[0]:.3f} e^({angle} i)", "exponential"

            case _:
                final = f"error {item}\nof type {item[-1]}\n"

        final_list.append(final)

    return final_list


def simple_equation(coefs):
    """Simplifies equations for the panda / printing"""

    equation = f""

    if coefs[2] == (1 or -1):
        to_add = "X^2" if coefs[2] == 1 else "-X^2"
        equation += to_add
    else:
        equation += f"{coefs[2]}X^2"

    if coefs[1] == (1 or -1):
        to_add = " + X" if coefs[1] else " - X"
        equation += to_add
    elif coefs[1] == 0:
        equation == ""
    elif coefs[1] < 0:
        equation += f" - {abs(coefs[1])}X"
    else:
        equation += f" + {coefs[1]}X"

    if coefs[0] == 0:
        equation += ""
    elif coefs[0] > 0:
        equation += f" + {coefs[0]}"
    else:
        equation += f" - {abs(coefs[0])}"

    return equation


# Main

# get convert type
equa_or_root = string_check("convert from: equation | root: ", ["equation", "root"])

if equa_or_root == "equation":  # convert from equation

    # make lists that will hold the roots in each form
    real_list = []
    rect_list = []
    polar_list = []
    expo_list = []
    equation_list = []

    # how many equations the user needs to solve
    how_many = num_check("how many equations: ")
    print()

    # loop for however many equations
    for _ in range(how_many):

        # get the coefficients from the user
        coefficient_list = get_coefs()

        # simplify the equation for printing
        equation = simple_equation(coefficient_list)
        print(f"\nYour equation:", equation)
        print()

        # solve the polynomial and get the roots
        roots = solve_polynomial(coefficient_list)

        # get exact decimal values for the imaginary component
        if roots[0][-1] == 'rect':
            roots = make_convertable(roots)

        # add each root seperately
        for root in roots:

            # convert the root into each form
            list_of_converted_roots = convert_roots(root)

            # make printable and seperate into a different variable
            real_form, rect_form, polar_form, expo_form = print_roots(list_of_converted_roots)

            # add each form to the correct list
            # (only the value, not the form because it's irrelavent)
            real_list.append(real_form[0])
            rect_list.append(rect_form[0])
            polar_list.append(polar_form[0])
            expo_list.append(expo_form[0])

            # append the equation to the list
            equation_list.append(equation)

    # end of loop

    # make a dict that will be used in the panda
    root_dict = {
        'equation': equation_list,
        'real': real_list,
        'rect': rect_list,
        'polar': polar_list,
        'exponential': expo_list
    }

    # make the panda
    root_table = pd.DataFrame(root_dict)

    # make the equation the row heading and merge the cells
    root_table = root_table.set_index('equation', append=True).swaplevel(0,1)

    # make it a string
    root_table_string = root_table.to_string()

    # print it
    print(root_table_string)

else:  # convert from roots

    forms_list = ['real', 'rect', 'polar', 'exponential']  # valid root forms

    # ask for amount of roots
    how_many = num_check("how many roots are you converting: ")

    # initialize the lists
    root_list = []
    real_list = []
    rect_list = []
    polar_list = []
    expo_list = []

    # loop through every root
    for _ in range(how_many):

        # ask for the form of each root
        initial_form = string_check("what is the form? ", forms_list, 3)

        # get the root based off of the form
        root = get_roots(initial_form)
        print()

        # printable roots
        new_roots = print_roots(root)[0]  # index here for just the first in the list

        # append the root to the list
        root_list.append(new_roots[0])

        # convert to all forms
        list_of_converted_roots = list(convert_roots(root))
        print(list_of_converted_roots)

        # make printable
        real_form, rect_form, polar_form, expo_form = print_roots(list_of_converted_roots)

        # append each form to their respective lists
        real_list.append(real_form[0])
        rect_list.append(rect_form[0])
        polar_list.append(polar_form[0])
        expo_list.append(expo_form[0])

    # end of loop

    # make the dict for the panda
    root_dict = {
        'original': root_list,
        'real': real_list,
        'rect': rect_list,
        'polar': polar_list,
        'exponential': expo_list
    }

    # make the panda
    root_table = pd.DataFrame(root_dict)

    # remove the index
    root_table_string = root_table.to_string(index=False)

    # print it
    print("\n")
    print(root_table_string)
