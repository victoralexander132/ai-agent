import os


def is_outside_working_directory(working_directory, file_path):
    """Check if file_path is outside the working_directory"""
    if os.path.isabs(file_path):
        resolved_path = os.path.realpath(file_path)
    else:
        resolved_path = os.path.realpath(os.path.join(working_directory, file_path))
    
    real_working_directory = os.path.realpath(working_directory)
    return not os.path.commonpath([real_working_directory, resolved_path]) == real_working_directory
