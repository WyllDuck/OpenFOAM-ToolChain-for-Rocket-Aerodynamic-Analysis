import os, sys
from genReport import write_report
from VTKtoIMAGE import default1


def get_subfolders(paths):
    """
    Given a list of paths, returns a list of all the 1st level subfolders in each path.
    """
    subfolders = []
    for path in paths:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                subfolders.append(item_path)
    return subfolders


def execute_functions(path):
    """
    Given a list of paths, executes the genReport and VTKtoIMAGE functions on each subfolder.
    """

    window_size = 50
    solver_extensions = ['rhoCentralFoam', 'rhoPimpleFoam', 'simpleFoam', 'rhoSimpleFoam']
    REPORT = write_report(path, WINDOW_SIZE=window_size, SOLVER_EXTENSIONS=solver_extensions, show=True)
    
    # if the report is empty because no execution was found, return
    if REPORT is None:
        return    

    surface_path = os.path.join(path, 'postProcessing', 'surfaces1')
    max_subfolder = 0.0

    # loop through all the subfolders in the path and select the one with the highest number use os    
    for subfolder in os.listdir(surface_path):
        try:
            if float(subfolder) > max_subfolder:
                max_subfolder = float(subfolder)
        except ValueError:
            pass
    max_subfolder = str(max_subfolder)
    surface_path = os.path.join(surface_path, max_subfolder, 'planeXZ')

    # create folder to save the images
    save_path = os.path.join(path, 'images')
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # run the default1 function to generate the images
    default1(surface_path, save_path=save_path)

    return


# main
# read the paths as args
def main ():
    
    # read path from args
    paths = sys.argv[1:]

    EXECUTION_FOLDERS = []
    for path in paths:
        print("{}".format(path))
        subpaths = get_subfolders([path])        
        for subpath in subpaths:
            print("\t\t- {}".format(subpath))
            EXECUTION_FOLDERS.append(subpath)

    # ask for confirmation
    print("Do you want to continue? (y/n)")
    confirmation = input()
    if confirmation != 'y':
        return
    
    # execute the functions
    for path in EXECUTION_FOLDERS:
        execute_functions(path)

    return


if __name__ == "__main__":
    main()
