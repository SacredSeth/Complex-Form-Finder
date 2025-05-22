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
    """Solves a polynomial and returns roots"""

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


# Main

how_many = num_check("how many equations: ")
print()

# loop for testing
for _ in range(how_many):

    coefficient_list = get_coefs()
    print(f"\nYour equation: {coefficient_list[2]}X^2 + {coefficient_list[1]}X + {coefficient_list[0]}")

    print()
    roots = solve_polynomial(coefficient_list)
    rect_form = simple_roots(roots)
    print(rect_form)

    print(rect_form[0][0], "\t", rect_form[1][0])
    # print(roots)

    print()
