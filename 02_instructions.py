# Functions
def yes_no(question):
    """Checks for a yes or no answer"""
    ans_list = ["y", "n"]

    while 1:
        response = input(question).lower()

        if response == "":
            print("This can't be blank")
            continue

        elif response[0] not in ans_list:
            print("Please answer yes or no")
            continue

        else:
            return response[0]


def instruct():
    """prints the instructions"""
    print("""
    This is a math tool that helps with converting
    - complex numbers
    - polynomials
    to other forms of complex numbers.
    eg. Rect form to Polar form (a+bi to r cis 0)
    or
    ax^2 + bx + c to re^i0, re^i0 (both roots)
    
    Please choose between <p> for polynomial, or <c> for complex
    to switch between the two functions.
    Then enter the problem you are solving (use "^" for exponents)
    """)


# Main

# loop for testing
while 1:

    instructions = yes_no("Do you want instructions? ")

    if instructions == "y":
        instruct()
    else:
        print("Program continues")
