# Functions
def get_coefs(degree="quadratic"):
    """Asks the user for each of the coefficients of a polynomial based on a degree"""

    coefficients = []

    degree_list = ["Constant: ", "X term: ", "X^2 term: "]

    # loop through all the quadratic terms
    for deg in degree_list:
        coef = num_check(deg, float, None)
        coefficients.append(coef)

    # if cubic, ask for the X^3 term
    if degree == "cubic":
        cube = num_check("X^3 term: ", float, None)
        coefficients.append(cube)

    return coefficients


def num_check(question, datatype=int, low=0, high=None, exit_code="xxx"):
    """ Function to make sure user inputs an integer / float that is within parameters """

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


# Main
quadratic = get_coefs()
print(quadratic)
print("\n\n")

cubic = get_coefs("cubic")
print(cubic)

