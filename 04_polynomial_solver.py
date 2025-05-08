# Functions
import math


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


def find_factors(num):
    """returns the factors (+ and -) of a number"""

    if num == 0: # making sure the program doesn't send nothing if there is this factor
        return [0]

    # list of factors
    factor_list = []

    # goes through every number between 1 and num, and divides num by it to get remainder
    for f in range(1, abs(num) + 1):

        # if remainder is equal to 0, append the factor
        if num % f == 0:
            factor_list.append(f)
            factor_list.append(f * -1) # negative factor still a factor

    return factor_list


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


# Main

how_many = num_check("how many equations: ")
print()

# loop for testing
for _ in range(how_many):

    coefficient_list = get_coefs()
    print(f"\nYour equation: {coefficient_list[2]}X^2 + {coefficient_list[1]}X + {coefficient_list[0]}")

    print()
    roots = solve_polynomial(coefficient_list)
    print(roots)

    print()
