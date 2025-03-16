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


# Main

# loop for testing
while 1:

    instructions = yes_no("Do you want instructions? ")

    if instructions == "y":
        print("Instructions here")
    else:
        print("Program continues")
