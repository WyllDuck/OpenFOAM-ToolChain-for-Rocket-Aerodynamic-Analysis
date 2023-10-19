import os, sys
import pandas as pd
import shutil
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


def execute_functions(path, generate_images=True, copy_path=None):
    """
    Given a list of paths, executes the genReport and VTKtoIMAGE functions on each subfolder.
    """

    print("=====================================================================================================")
    print("\n\n")
    print("Executing functions for {}".format(path))

    window_size = 50
    solver_extensions = ['rhoCentralFoam', 'rhoPimpleFoam', 'simpleFoam', 'rhoSimpleFoam']
    REPORT = write_report(path, WINDOW_SIZE=window_size, SOLVER_EXTENSIONS=solver_extensions, show=False)
    
    # if the report is empty because no execution was found, return
    if REPORT is None:
        return REPORT

    if generate_images:
        surface_path = os.path.join(path, 'postProcessing', 'surfaces1')
        max_subfolder_num = 0.0
        max_subfolder_str = ''

        # loop through all the subfolders in the path and select the one with the highest number use os    
        for subfolder in os.listdir(surface_path):
            try:
                if float(subfolder) > max_subfolder_num:
                    max_subfolder_num = float(subfolder)
                    max_subfolder_str = subfolder
            except ValueError:
                pass
        surface_path = os.path.join(surface_path, max_subfolder_str, 'planeXZ.vtp')

        # create folder to save the images
        save_path = os.path.join(path, 'images')
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        # run the default1 function to generate the images
        default1(surface_path, save_path=save_path)

    if copy_path is not None:
        copy_files(path, copy_path)

    return REPORT


# function that copies file to new folder when provided with workspace_path and copy_path
def copy_files(workspace_path, copy_path):
    """
    Given a list of paths, executes the genReport and VTKtoIMAGE functions on each subfolder.
    """

    print("=====================================================================================================")
    print("\n\n")
    print("Copying file from {} to {}".format(workspace_path, copy_path))

    # check if the copy_path exists
    if not os.path.exists(copy_path):
        print("Info: copy_path does not exist")
        os.mkdir(copy_path) # create the copy_path
    
    # check if the workspace_path exists
    if not os.path.exists(workspace_path):
        print("Error: workspace_path does not exist")
        return

    # origin path
    ori_path    = os.path.join(workspace_path, 'images')
    base_name   = os.path.basename(workspace_path)
    copy_path   = os.path.join(copy_path, base_name)

    # check if destination path exists and ask if it should be overwritten
    if os.path.exists(copy_path):
        print("Warning: the path '{}' already exists".format(copy_path))
        print("Do you want to overwrite it? (y/n)")
        confirmation = input()
        if confirmation != 'y':
            return
        else:
            shutil.rmtree(copy_path)

    # add images to the copy_path
    if os.path.exists(ori_path):
        shutil.copytree(ori_path, copy_path)
    else:
        print("Warning: images folder does not exist")
        os.mkdir(copy_path)

    # add residuals and forces to the copy_path
    ori_path    = os.path.join(workspace_path, 'residuals.png')
    if os.path.exists(ori_path):
        shutil.copy(ori_path, copy_path)
    else:
        print("Warning: residuals.png does not exist")
    
    ori_path    = os.path.join(workspace_path, 'forces.png')
    if os.path.exists(ori_path):
        shutil.copy(ori_path, copy_path)
    else:
        print("Warning: forces.png does not exist")

    # add the report.txt to the copy_path
    ori_path    = os.path.join(workspace_path, 'report.txt')
    if os.path.exists(ori_path):
        shutil.copy(ori_path, copy_path)
    else:
        print("Warning: report.txt does not exist")

    print("File copied successfully")
    print()

    return


# class holding all reports
class ReportContainer(object):

    def __init__(self):
        self.reports = []

    def add(self, report):
        self.reports.append(report)

    def write_csv(self, path):
        
        headers = ["OPENFOAM_WORKSPACE_DIR", "YPLUS_MIN", "YPLUS_MAX", "YPLUS_AVG", "CA_FINAL_COEFF", "CN_FINAL_COEFF", "CM_FINAL_COEFF", "CA_FINAL_COEFF_WINDOW", "CN_FINAL_COEFF_WINDOW", "CM_FINAL_COEFF_WINDOW", "WINDOW_SIZE", "TOTAL_STATUS_CODE", "EXECUTION_TIME", "NUMBER_ITERATIONS", "SOLVER_NAME", "ITERRATIONS_PER_EXECUTION_TIME", "LAST_MODIFICATION_DATE"]

        # add all HEADERS_RESIDUALS to the column names, loop through all reports
        headers_set = set()
        for report in self.reports:

            if report is None:
                print("Error: report is None\n{}".format(report["OPENFOAM_WORKSPACE_DIR"]))
                continue
            if report['HEADERS_RESIDUALS'] is None:
                print("Error: report['HEADERS_RESIDUALS'] is None\n{}".format(report["OPENFOAM_WORKSPACE_DIR"]))
                continue
            if report['LOG_LIST'] is None:
                print("Error: report['LOG_LIST'] is None\n{}".format(report["OPENFOAM_WORKSPACE_DIR"]))
                continue

            for header in report['HEADERS_RESIDUALS']:
                headers_set.add("residual_"+header)
            for header in report['LOG_LIST']:
                headers_set.add(header)

        headers_set = list(headers_set)

        """
        OTHER HEADERS:

        - OPENFOAM_WORKSPACE_DIR
        - YPLUS_MIN
        - YPLUS_MAX
        - YPLUS_AVG
        - CA_FINAL_COEFF
        - CN_FINAL_COEFF
        - CM_FINAL_COEFF
        - CA_FINAL_COEFF_WINDOW
        - CN_FINAL_COEFF_WINDOW
        - CM_FINAL_COEFF_WINDOW
        - WINDOW_SIZE
        - TOTAL_STATUS_CODE
        - EXECUTION_TIME
        - NUMBER_ITERATIONS
        - SOLVER_NAME
        - ITERRATIONS_PER_EXECUTION_TIME
        - LAST_MODIFICATION_DATE
        """

        # add the other headers
        headers += headers_set

        # create pandas dataframe with the headers and fill it with the data from the reports
        df = pd.DataFrame(columns=headers)

        i = 0
        k = 0
        while i < len(self.reports):
            report = self.reports[i]
            print("Processing report {}/{} - {}".format(i+1, len(self.reports), self.reports[i]["OPENFOAM_WORKSPACE_DIR"]))

            # create row with all the data
            row = {}
            for header in headers:
                try:
                    row[header] = report[header]
                except KeyError:
                    row[header] = None

            # add HEADER_RESIDUALS to the row
            if report['HEADERS_RESIDUALS'] is not None:
                for header in report['HEADERS_RESIDUALS']:
                    index = report['HEADERS_RESIDUALS'].index(header)
                    row["residual_"+header] = report['FINAL_RESIDUALS'][index]

            # add LOG_LIST to the row
            if report['LOG_LIST'] is not None:
                for header in report['LOG_LIST']:
                    index = report['LOG_LIST'].index(header)
                    row[header] = report['STATUS_CODE'][index]

            row["CA_FINAL_COEFF"] = report["FINAL_COEFFS"][0]
            row["CN_FINAL_COEFF"] = report["FINAL_COEFFS"][1]
            row["CM_FINAL_COEFF"] = report["FINAL_COEFFS"][2]

            row["CA_FINAL_COEFF_WINDOW"] = report["FINAL_COEFFS_WINDOW"][0]
            row["CN_FINAL_COEFF_WINDOW"] = report["FINAL_COEFFS_WINDOW"][1]
            row["CM_FINAL_COEFF_WINDOW"] = report["FINAL_COEFFS_WINDOW"][2]

            for j in range(len(report["L_EXECUTION_TIME"])):
                row["EXECUTION_TIME"] = report["L_EXECUTION_TIME"][j]
                row["NUMBER_ITERATIONS"] = report["L_NUMBER_ITERATIONS"][j]
                row["SOLVER_NAME"] = report["L_SOLVER_NAME"][j]
                row["ITERRATIONS_PER_EXECUTION_TIME"] = report["L_ITERRATIONS_PER_EXECUTION_TIME"][j]
                row["LAST_MODIFICATION_DATE"] = report["L_LAST_MODIFICATION_DATE"][j]

                # add the row to the dataframe
                df.loc[k] = row
                k += 1
            i += 1

        # write the dataframe to csv
        df.to_csv(path, index=False)
        
        return


# main
# read the paths as args
def main ():

    # get execution location in cmd
    WORK_DIR = os.getcwd()

    # instantiate the report container
    REPORTS = ReportContainer()
    
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
    
    # ask if iamges should be generated
    print("Do you want to generate images? (y/n)")
    generate_images = input()
    if generate_images == 'y':
        generate_images = True
    else:
        generate_images = False
    
    # execute the functions
    for path in EXECUTION_FOLDERS:
        REPORT = execute_functions(path, generate_images=generate_images, copy_path=os.path.join(WORK_DIR, 'reports'))
        if REPORT is not None:
            REPORTS.add(REPORT)

    print("=====================================================================================================")
    print("=====================================================================================================")

    print("Execution finished. CSV with all reports is saved in:\n {}".format(os.path.join(WORK_DIR, 'reports.csv')))

    # write csv of all reports together
    REPORTS.write_csv(os.path.join(WORK_DIR, 'reports.csv'))

    return


if __name__ == "__main__":
    main()
