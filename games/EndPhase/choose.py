def choose(output, input_range = "none", confirm = "no"):
    """
    output: a string, usually the question
    input_range: a list of strings the input can be.
    confirm: a string that indicates if confirmation is needed
    This function lets the user picks anything, parameters include n output,
    asking the user for input and input range is if there is a certain range
    required for the input.
    """
    while True:
        _input = input(output)
        if input_range == "none" or _input in input_range:
            break
        else:
            print("**invalid input**")
    if confirm == "no":
        return _input
    while True:
        confirm = input("confirm? y/n\n")
        if confirm.lower() in ['y',"yes"]:
            return _input
        elif confirm.lower() in ['n', "no"]:
            return choose(output, input_range, confirm)
        else:
            print("**invalid input**")