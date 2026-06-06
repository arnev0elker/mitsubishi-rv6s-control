def list_to_position_string(input_list):
    '''
    Converts a list of numbers into a comma-separated string formatted for the robot
    If the last 2 elements are missing 0s are added
    Example: 
    [1.23, 4.56, 7.89, 0.12, 3.45, 6.78, 7, 0] -> '(1.23,4.56,7.89,0.12,3.45,+6.78)(7,0)'
    [1.23, 4.56, 7.89] -> Error
    [1.23, 4.56, 7.89, 0.12, 3.45, 6.78] -> '(1.23,4.56,7.89,0.12,3.45,+6.78)(0,0)'
    '''
    # Check if the list has a valid length (between 6 and 8 elements)
    if len(input_list) < 6 or len(input_list) > 8:
        raise ValueError("The list must contain between 6 and 8 elements.")
    
    if len(input_list) == 7:
        input_list.append(0)  
    if len(input_list) == 6:
        input_list.extend([0, 0])

    # Split the input into two parts (first 6 elements and the rest)
    first_part = input_list[:6]
    second_part = input_list[6:]

    # Format the output as per the required structure
    first_part_str = f"({','.join(map(str, first_part))})"
    second_part_str = f"({','.join(map(str, second_part))})"

    # Combine both parts
    return first_part_str + second_part_str
    

def position_string_to_list(input_string):
    '''
    Converts a string formatted as into a list of numbers.
    
    Example:
    '(1.23,-4.56,7.89,0.12,-3.45,+6.78)(7,0)' 
    -> [1.23, -4.56, 7.89, 0.12, -3.45, 6.78, 7, 0]
    
    Example:
    '(1.23,-4.56,7.89,0.12,-3.45,+6.78)' 
    -> [1.23, -4.56, 7.89, 0.12, -3.45, 6.78]
    '''
    # Remove parentheses and split the string by ')(' into two parts
    parts = input_string.strip('()').split(')(')

    # Split the first part by commas and convert to floats
    first_part = list(map(float, parts[0].split(',')))  # First part with 6 values
    
    # If there is a second part, split it by commas and convert to integers
    if len(parts) > 1:
        second_part = list(map(int, parts[1].split(',')))  # Second part with 2 values
        return first_part + second_part
    else:
        return first_part