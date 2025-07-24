# Functions
import math
from fractions import Fraction
import pandas as pd


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
        # simple get number
        root = num_check("root: ", float, None), 'real'

    elif form == 'rect':  # rect

        # get real and imaginary values
        real = num_check("(a+bi) enter a: ", float, None)
        imaginary = num_check("(a+bi) enter b: ", float, None)

        # make a tuple to store the values for the root
        root = real, imaginary, 'rect'

    elif form == 'polar':  # polar

        # get magnitude and angle
        magnitude = num_check("(r cis 0) enter r: ", float)

        # use the exit code function for cases when pi is needed
        theta = num_check("enter the angle (in radians, use pi for pi): ",
                          float, exit_code="pi", low=math.pi * -1, high=math.pi)
        # put use to the exit code
        if theta == "pi":
            theta = math.pi

        # set the tuple
        root = magnitude, theta, 'polar'

    else:  # exponent

        # get magnitude and angle
        magnitude = num_check("(re^(i0)) enter r: ", float)

        # use the exit code function for cases when pi is needed
        theta = num_check("enter the angle (in radians, use pi for pi): ",
                          float, exit_code="pi", low=math.pi * -1, high=math.pi)
        # put use to the exit code
        if theta == "pi":
            theta = math.pi

        # set the tuple
        root = magnitude, theta, 'exponential'

    return root


def num_check(question, datatype=int, low=0, high=None, exit_code="exit"):
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

        if test_exit == exit_code:
            return exit_code

        # try statement for checking that it is of the correct datatype
        try:
            response = datatype(test_exit)

            # Different calculations for set values of low and high
            if check == 0:
                if response >= low:  # just low
                    return response
                else:
                    print(error)

            elif check == 1:
                if low <= response <= high:  # low and high
                    return response
                else:
                    print(error)

            elif check == 2:
                if response <= high:  # just high
                    return response
                else:
                    print(error)

            else:  # no limits
                return response

        except ValueError:
            # if not correct data type, send an error
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

    # get the real value of the first root (both are the same)
    real = to_make[0][0]

    # calculate the imaginary magnitude
    imaginary = math.sqrt(to_make[0][3]) / to_make[0][5]

    # set the tuple and flip one of the imaginary values
    converted_roots = (real, imaginary, 'rect'), (real, imaginary * -1, 'rect')

    return converted_roots


def convert_roots(start_root):
    """Converts roots in real or rect form into all the other forms of roots
    these converted roots are always in the order: real, rect, polar, exponent"""

    # real roots are special when converted
    if start_root[-1] == 'real':  # real roots are in form (value, form)
        rea_form = start_root[0], 'real'
        rec_form = start_root[0], 0, 'rect' # because of no i value, rect and real identical

        # magnitude can't be negative so angle must be pi radians
        if start_root[0] < 0:
            angle = math.pi
        else:
            angle = 0

        # polar coordinates set, make sure magnitude is absolute
        pol_form = abs(start_root[0]), angle, 'polar'
        exponent_form = abs(start_root[0]), angle, 'exponential'

    elif start_root[-1] == 'rect':  # rect form converting

        # roots are imaginary not real
        rea_form = 'n/a', 'real'

        # same form
        rec_form = start_root

        # separate the real and imaginary
        imaginary = start_root[1]
        real = start_root[0]

        if imaginary == 0:
            # redefine real form if root has no imaginary component
            rea_form = real, 'real'

        # find the magnitude
        magnitude = math.sqrt((real ** 2) + (imaginary ** 2))  # pythagorean thereom

        if real == 0:  # making sure that we dont recieve an error from the atan() function

            # this angle means purely imaginary (aswell as -pi/2)
            angle = math.pi / 2

        else:

            # find the angle
            angle = math.atan(abs(imaginary / real))

        if real < 0:  # because the atan is absolute, we need to take away from a half rotation
            angle = math.pi - angle
        if imaginary < 0:  # the angle has to be between -pi and pi
            angle *= -1

        # set tuples
        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

    elif start_root[-1] == 'polar':  # convert from polar form

        # set real form to nil to start with
        rea_form = 'n/a', 'real'

        # separate magnitude and angle
        magnitude = start_root[0]
        angle = start_root[1]

        # set the polar coordinate forms
        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

        # reverse the atan function to find cartesian coordinates
        if abs(angle) < math.pi / 2:  # acute angles
            # cis = cos + i sin
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
            # used to keep angles between pi and -pi
            imaginary = magnitude * math.sin(math.pi - abs(angle))
            real = magnitude * math.cos(math.pi - abs(angle))

        if angle < 0:  # separate if statement for flipping the imaginary value
            imaginary *= -1

        # set tuple
        rec_form = real, imaginary, 'rect'

    else:  # convert from exponent form

        # set real form to nil to start with
        rea_form = 'n/a', 'real'

        # seperate magnitude and angle
        magnitude = start_root[0]
        angle = start_root[1]

        # set polar coordinate forms
        pol_form = magnitude, angle, 'polar'
        exponent_form = magnitude, angle, 'exponential'

        # reverse the atan() function
        if abs(angle) < math.pi / 2:  # acute angles
            # cis = cos + i sin
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
            # used to keep angle between pi and -pi
            imaginary = magnitude * math.sin(math.pi - abs(angle))
            real = magnitude * math.cos(math.pi - abs(angle))

        if angle < 0:  # separate if statement for flipping the imaginary value
            imaginary *= -1

        # set the tuple
        rec_form = real, imaginary, 'rect'

    # end of if statements

    return rea_form, rec_form, pol_form, exponent_form


def print_roots(list_of_roots):
    """Converts al roots into readable form and prints them"""

    # make the values mutable if they arent already
    if type(list_of_roots[0]) != tuple:
        list_of_roots = [list_of_roots]

    final_list = []

    # loop through each root
    for item in list_of_roots:

        # match the form
        match item[-1]:

            # case for real roots
            case 'real':

                # this is if the value is "n/a"
                if type(item[0]) == str:
                    final = 'n/a', 'real'

                # display simple fractions if they are simple
                elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                    final = f"{Fraction(item[0])}", 'real'

                # otherwise limit to 3 d.p.
                else:
                    final = f"{item[0]:.3f}", 'real'

            # case for rectangle roots
            case 'rect':

                # bunch of simplification
                # negative imaginary
                if item[1] < 0:

                    sign = " - "

                    # no real value
                    if item[0] == 0:
                        rel = ""
                        sign = "-"

                    # fraction real value
                    elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                        rel = Fraction(item[0])

                    # decimal real value
                    else:
                        rel = f"{item[0]:.3f}"

                    # no imaginary value
                    if item[1] == 0:
                        ima = ""
                        sign = "-"

                    # no coefficient needed
                    elif item[1] == 1:
                        ima = "i"

                    # fraction value
                    elif Fraction(item[1]) == Fraction(item[1]).limit_denominator(100):
                        ima = f"{abs(Fraction(item[1]))}i"

                    # decimal value
                    else:
                        ima = f"{abs(item[1]):.3f}i"

                    # combine variables into a string
                    final = f"{rel}{sign}{ima}", 'rect'

                else:

                    # positive imaginary
                    sign = " + "

                    # no real value
                    if item[0] == 0:
                        rel = ""
                        sign = ""

                    # fraction real value
                    elif Fraction(item[0]) == Fraction(item[0]).limit_denominator(100):
                        rel = Fraction(item[0])

                    # decimal real value (3 d.p.)
                    else:
                        rel = f"{item[0]:.3f}"

                    # no imaginary value
                    if item[1] == 0:
                        ima = ""
                        sign = ""

                    # no coefficient needed
                    elif item[1] == 1:
                        ima = "i"

                    # fraction value
                    elif Fraction(item[1]) == Fraction(item[1]).limit_denominator(100):
                        ima = f"{Fraction(item[1])}i"

                    # decimal value
                    else:
                        ima = f"{item[1]:.3f}i"

                    # combine variables into a string
                    final = f"{rel}{sign}{ima}", 'rect'

            # case for polar coordinate roots
            case 'polar':

                # put fraction in terms of pi
                simple_angle = Fraction(item[1] / math.pi)

                # check if the fraction is rational and simple
                if simple_angle == simple_angle.limit_denominator(100):

                    # confirm simplification
                    simple_angle = simple_angle.limit_denominator(100)

                    # coefficient is 0
                    if simple_angle.numerator == 0:
                        angle = "0"

                    # remove visible coefficient if magnitude is 1
                    elif simple_angle.numerator == (1 or -1):
                        # add '-' if value is -1
                        angle = f"\u03C0/{simple_angle.denominator}" if simple_angle.numerator == 1\
                            else f"-\u03C0/{simple_angle.denominator}"

                    # normal fraction
                    else:
                        # combine values into a string
                        angle = f"{simple_angle.numerator}\u03C0/{simple_angle.denominator}"

                # fraction is not simple
                else:
                    # use deimal (3 d.p.)
                    angle = f"{item[1]:.3f}"

                # just use the pi symbol if the angle is equal to pi
                if item[1] == math.pi:
                    final = f"{item[0]:.3f} cis \u03C0", 'polar'

                # otherwise use the angle
                else:
                    final = f"{item[0]:.3f} cis {angle}", 'polar'

            # case for exponential roots
            case 'exponential':

                # get fraction in terms of pi
                simple_angle = Fraction(item[1] / math.pi)

                # check for simple fraction
                if simple_angle == simple_angle.limit_denominator(100):

                    # set simple fraction
                    simple_angle = simple_angle.limit_denominator(100)

                    # coefficient value is 0
                    if simple_angle.numerator == 0:
                        angle = "0"

                    # remove visible coefficient if magnitude is 1
                    elif simple_angle.numerator == (1 or -1):
                        # add '-' if numerator is negative
                        angle = f"\u03C0/{simple_angle.denominator}" if simple_angle.numerator == 1 \
                            else f"-\u03C0/{simple_angle.denominator}"

                    # use the fraction for the angle
                    else:
                        angle = f"{simple_angle.numerator}\u03C0/{simple_angle.denominator}"

                # decimal angle (3 d.p.)
                else:
                    angle = f"{item[1]:.3f}"

                # just use the pi symbol if the angle is equal to pi
                if item[1] == math.pi:
                    final = f"{item[0]:.3f} e^(\u03C0i)", "exponential"

                # otherwise use the angle
                else:
                    final = f"{item[0]:.3f} e^({angle} i)", "exponential"

            # default (error) case
            case _:
                # mostly for debugging, shouldn't be used hopefully
                final = f"error {item}\nof type {item[-1]}\n"

        # append printable root to list
        final_list.append(final)

    # return the list of printable roots
    return final_list


def simple_equation(coefs):
    """Simplifies equations for the panda / printing"""

    # define row_header outside of inner scopes
    equation = f""

    # remove coefficients of 1
    if abs(coefs[2]) == 1:
        # add '-' if negative
        to_add = "X^2" if coefs[2] == 1 else "-X^2"
        equation += to_add

    # otherwise use the coefficient
    else:
        equation += f"{coefs[2]}X^2"

    # remove coefficients of 1
    if abs(coefs[1]) == 1:
        # add '-' if negative
        to_add = " + X" if coefs[1] == 1 else " - X"
        equation += to_add

    # no X term
    elif coefs[1] == 0:
        equation == ""

    # negative X term
    elif coefs[1] < 0:
        equation += f" - {abs(coefs[1])}X"

    # positive X term
    else:
        equation += f" + {coefs[1]}X"

    # remove constant if there is no value
    if coefs[0] == 0:
        equation += ""

    # positive constant
    elif coefs[0] > 0:
        equation += f" + {coefs[0]}"

    # negative constant
    else:
        equation += f" - {abs(coefs[0])}"

    # return the string of the row_header
    return equation


def instruct():
    """prints the instructions"""
    print("""
    This is a math tool that helps with converting
    - complex numbers
    - quadratics
    to other forms of complex numbers.
    eg. Rect form to Polar, Exponential, Real (a+bi to r cis 0, r e^(i0), real)
    or
    ax^2 + bx + c to both of it's roots

    Please choose between <e> for row_header, or <r> for roots
    to switch between the two functions.
    
    You will be asked to enter each value related to the selected form
    if you want to stop early, enter "exit" when asked for the form of root
    After providing this information,
    you will be given a table containing all the information you need. 
    """)


# Main
print("===== Complex Form Finder =====\n\n")

# ask user if they want to view instructions
instructions = string_check("would you like to see the instructions? ", ["yes", "no"])
if instructions == "yes":
    instruct()

# initialize the lists that will hold the data for the panda
row_heading_list = []
real_list = []
rect_list = []
polar_list = []
expo_list = []

# valid program modes
program_modes = ["equation", "root"]

# valid root forms
forms_list = ['real', 'rect', 'polar', 'exponential']

# holds roots to be added into the dict for panda
root_holder = []

print()
# get convert type
equa_or_root = string_check("convert from: equation | root: ", program_modes)

# how many equations the user needs to solve
how_many = num_check("how many: ", low=1)
print()

if equa_or_root == "equation":  # convert from equation

    # loop for however many equations
    for _ in range(how_many):

        # get the coefficients from the user
        coefficient_list = get_coefs()

        # simplify the row_header for printing
        row_header = simple_equation(coefficient_list)
        print(f"\nYour equation:", row_header)
        print()
        row_heading_title = "equation"

        # solve the polynomial and get the roots
        roots = solve_polynomial(coefficient_list)

        # get exact decimal values for the imaginary component
        if roots[0][-1] == 'rect':
            roots = make_convertable(roots)

        # append each root to the list
        for root in roots:
            root_holder.append(root)
            row_heading_list.append(row_header)

        # ask if user wants to continue
        cont = input("press <enter> to continue ").lower()
        if cont == "exit":
            break

    # end of loop

else:  # convert from roots

    # loop through every root
    for _ in range(how_many):

        print()
        # ask for the form of each root
        initial_form = string_check("what is the form? ", forms_list, 3)

        # get the root based off of the form
        root = get_roots(initial_form)
        print()

        # printable roots
        row_header = print_roots(root)[0][0]  # index here for just the first in the list

        # print the original
        print(row_header)

        # set the title of the row heading
        row_heading_title = "original"
        row_heading_list.append(row_header)

        # append the root to the list
        root_holder.append(root)

        # ask user if they want to continue
        cont = input("press <enter> to continue ").lower()

        # if user enters "exit" end
        if cont == "exit":
            break

    # end of loop

# add each root seperately
for root in root_holder:

    # convert the root into each form
    list_of_converted_roots = list(convert_roots(root))

    # make printable and seperate into a different variable
    real_form, rect_form, polar_form, expo_form = print_roots(list_of_converted_roots)

    # add each form to the correct list
    # (only the value, not the form because it's irrelavent)
    real_list.append(real_form[0])
    rect_list.append(rect_form[0])
    polar_list.append(polar_form[0])
    expo_list.append(expo_form[0])

# make a dict that will be used in the panda
root_dict = {
    'equation': row_heading_list,
    'real': real_list,
    'rect': rect_list,
    'polar': polar_list,
    'exponential': expo_list
}

# make the panda
root_table = pd.DataFrame(root_dict)

# make the row_header the row heading and merge the cells
root_table = root_table.set_index('equation', append=True).swaplevel(0,1)

# make it a string
root_table_string = root_table.to_string()

# print it
print(root_table_string)
