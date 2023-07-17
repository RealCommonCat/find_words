import sys

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=5, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    # Print a new line when the progress bar is complete
    if iteration == total:
        print()