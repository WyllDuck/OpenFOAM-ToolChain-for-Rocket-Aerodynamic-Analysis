import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# read yPlus data
# returns: yPlus_min, yPlus_max, yPlus_avg
def read_yPlus (FILE_PATH):
    yPlus = pd.read_csv(FILE_PATH, sep='\t', header=None, skiprows=2).to_numpy()
    return yPlus[-1, 2], yPlus[-1, 3], yPlus[-1, 4] # min, max, average 

# read forces data
# returns: Cd, Cl, Cm
def read_forces (FILE_PATH, WINDOW_SIZE=50, save_plot=None):
    forces = pd.read_csv(FILE_PATH, sep='\t', header=None, skiprows=13).to_numpy()
    LAST = forces[-1, 1], forces[-1, 4], forces[-1, 7] # Cd, Cl, Cm

    # moving average last WINDOW_SIZE elements
    forces_WIN = forces[-WINDOW_SIZE:, :]
    Cd_WIN = np.mean(forces_WIN[:, 1])
    Cl_WIN = np.mean(forces_WIN[:, 4])
    Cm_WIN = np.mean(forces_WIN[:, 7])

    if save_plot is not None:
        plot_forces(forces[:, [1, 4, 7]], ['Cd', 'Cl', 'Cm'], save_path=save_plot)

    return LAST, [Cd_WIN, Cl_WIN, Cm_WIN], WINDOW_SIZE

# read residuals data
# returns: residuals
def read_residuals (FILE_PATH, save_plot=None):

    # read residuals with header
    residuals = pd.read_csv(FILE_PATH, sep='\t', skiprows=1)
    residuals.rename(columns=lambda x: x.replace(" ", ""), inplace=True)
    
    # find all headers with '_initial' written in them - pandas
    initial_headers = []
    for header in residuals.columns:
        if '_initial' in header:
            
            # remove '_initial' from header
            header = header.replace('_initial', '')
            
            # if header + '_solver' exists, then 
            if header + '_solver' in residuals.columns:
                
                # if is has a row entry equal to 'diagonal', then ignore
                if residuals[header + '_solver'][0] == 'diagonal':
                    print(f'ignoring {header} because it is diagonal')
                    continue
            
            else: 
                
                # if all values in column header+'_initial' are null, then ignore
                if sum(residuals[header + '_initial']) == 0:
                    print(f'ignoring {header} because all values are null')
                    continue
            
            initial_headers.append(header)

    # loop thorugh every selected header and return last value
    RET_residuals = []
    for header in initial_headers:
        RET_residuals.append(residuals[header + "_initial"].iloc[-1])

    if save_plot is not None:
        data = residuals[[s+"_initial" for s in initial_headers]].to_numpy()
        plot_residuals(data, initial_headers, save_path=save_plot)

    return RET_residuals, initial_headers


####################################################################################################

# plot residuals
# returns: None
def plot_residuals (_residuals, _headers, save_path=None):

    # plot residuals
    plt.figure(figsize=(10, 5))
    plt.plot(_residuals)
    plt.yscale('log')
    plt.ylabel('Residual')
    plt.xlabel('Iteration')
    plt.legend(_headers)

    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()

    return

# plot forces
# returns: None
def plot_forces (_forces, _headers, save_path=None):

    # plot forces
    plt.figure(figsize=(10, 5))
    plt.plot(_forces)
    plt.ylabel('Force')
    plt.xlabel('Iteration')
    plt.legend(_headers)

    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()

    return

####################################################################################################
# CHECK LOG FILES

# read log file
# returns: log_file
def read_log_file (FOLDER_PATH):

    # find all files which start with 'log.' in the folder FOLDER_PATH
    # add to list of log files
    LOG_LIST = []
    for file in os.listdir(FOLDER_PATH):
        if file.startswith('log.'):
            FILE_PATH = FOLDER_PATH + '\\' + file
            LOG_LIST.append(FILE_PATH)

    # open file and check if it ends with 'End'
    # changes status code from 0 to 1 if it does
    STATUS_CODE = [0] * len(LOG_LIST)
    
    for i in range(len(LOG_LIST)):

        log_file = open(LOG_LIST[i], 'r')
        log_lines = log_file.readlines()

        # check last 5 lines of file
        for j in range(1, 6):
            # if file has enough lines continue, else status code remains 0
            if len(log_lines) < j:
                print(f'log file {LOG_LIST[i]} has less than {j} lines')
                break

            if 'End' in log_lines[-j]:
                STATUS_CODE[i] = 1 # 1 means it ends with 'End'
        log_file.close()

    # using os remove the path from the file name
    for i in range(len(LOG_LIST)):
        LOG_LIST[i] = os.path.basename(LOG_LIST[i])

    # return STATUS_CODE list, if all elements are 1, then return 1
    if sum(STATUS_CODE) == len(STATUS_CODE):
        return 1, LOG_LIST, STATUS_CODE
    else:
        return 0, LOG_LIST, STATUS_CODE
    

# read log file solver
# returns: number of iterations, execution time, solver name, execution time per iteration
def read_log_file_solver (FOLDER_PATH, SOLVER_EXTENSIONS):

    # Look for files within the folder FOLDER_PATH which are log. files and have one of the solver externsions provided in SOLVER_EXTENSIONS
    # add to list of log files
    LOG_LIST = []
    for file in os.listdir(FOLDER_PATH):
        if file.startswith('log.'):
            if any(ext in file for ext in SOLVER_EXTENSIONS):
                FILE_PATH = FOLDER_PATH + '\\' + file
                LOG_LIST.append(FILE_PATH)

    if len(LOG_LIST) == 0:
        return None, None, None, None

    # LIST of EXECUTION_TIME, NUMBER_ITERATIONS, SOLVER_NAME, ITERRATIONS_PER_EXECUTION_TIME
    L_EXECUTION_TIME = [None] * len(LOG_LIST)
    L_NUMBER_ITERATIONS = [None] * len(LOG_LIST)
    L_SOLVER_NAME = [None] * len(LOG_LIST)
    L_ITERRATIONS_PER_EXECUTION_TIME = [None] * len(LOG_LIST)

    for i in range(len(LOG_LIST)):
    
        EXECUTION_TIME = None
        NUMBER_ITERATIONS = None
        SOLVER_NAME = None
        ITERRATIONS_PER_EXECUTION_TIME = None
        
        log_file = open(LOG_LIST[i], 'r')
        log_lines = log_file.readlines()

        # get file log name without path and extension using os library
        file_name = os.path.basename(LOG_LIST[i])
        SOLVER_NAME = file_name.split('.')[1]

        for line in log_lines[::-1]:
            if 'ExecutionTime' in line and EXECUTION_TIME is None:
                EXECUTION_TIME = line.split(' ')[2]
                # try to convert to float
                try:
                    EXECUTION_TIME = float(EXECUTION_TIME)
                except:
                    EXECUTION_TIME = None

                continue

            if 'Time' in line and NUMBER_ITERATIONS is None:
                NUMBER_ITERATIONS = line.split(' ')[2]
                # try to convert to float
                try:
                    NUMBER_ITERATIONS = float(NUMBER_ITERATIONS)
                except:
                    NUMBER_ITERATIONS = None

                continue

            if NUMBER_ITERATIONS is not None and EXECUTION_TIME is not None:
                ITERRATIONS_PER_EXECUTION_TIME = NUMBER_ITERATIONS / EXECUTION_TIME
                break
        
        L_EXECUTION_TIME[i] = EXECUTION_TIME
        L_NUMBER_ITERATIONS[i] = NUMBER_ITERATIONS
        L_SOLVER_NAME[i] = SOLVER_NAME
        L_ITERRATIONS_PER_EXECUTION_TIME[i] = ITERRATIONS_PER_EXECUTION_TIME

        log_file.close()

    return L_EXECUTION_TIME, L_NUMBER_ITERATIONS, L_SOLVER_NAME, L_ITERRATIONS_PER_EXECUTION_TIME
            

####################################################################################################

# write report based on all the information provided
# returns: standarized table
def write_report (OPENFOAM_WORKSPACE_DIR, WINDOW_SIZE=50, SOLVER_EXTENSIONS=['rhoCentralFoam', 'rhoPimpleFoam', 'simpleFoam', 'rhoSimpleFoam']):

    file_path = os.path.join(OPENFOAM_WORKSPACE_DIR, 'report.txt')

    PLOT_FORCES_PATH    = os.path.join(OPENFOAM_WORKSPACE_DIR, 'forces.svg')
    PLOT_RESIDUALS_PATH = os.path.join(OPENFOAM_WORKSPACE_DIR, 'residuals.svg')

    YPLUS_MIN, YPLUS_MAX, YPLUS_AVG = read_yPlus(OPENFOAM_WORKSPACE_DIR + '\\postProcessing\\yPlus1\\0\\yPlus.dat')
    FINAL_COEFFS, FINAL_COEFFS_WINDOW, WINDOW_SIZE = read_forces(OPENFOAM_WORKSPACE_DIR + '\\postProcessing\\forceCoeffs1\\0\\coefficient.dat', WINDOW_SIZE=WINDOW_SIZE, save_plot=PLOT_FORCES_PATH)
    FINAL_RESIDUALS, HEADERS_RESIDUALS = read_residuals(OPENFOAM_WORKSPACE_DIR + '\\postProcessing\\solverInfo1\\0\\solverInfo.dat', save_plot=PLOT_RESIDUALS_PATH)
    TOTAL_STATUS_CODE, LOG_LIST, STATUS_CODE = read_log_file(OPENFOAM_WORKSPACE_DIR)
    L_EXECUTION_TIME, L_NUMBER_ITERATIONS, L_SOLVER_NAME, L_ITERRATIONS_PER_EXECUTION_TIME = read_log_file_solver(OPENFOAM_WORKSPACE_DIR, SOLVER_EXTENSIONS=SOLVER_EXTENSIONS)

    # write report

    # write header
    report_file = open(file_path, 'w')
    report_file.write('Report\n')
    report_file.write('------\n')
    report_file.write('\n')

    # write yPlus
    report_file.write('yPlus\n')
    report_file.write('-----\n')
    report_file.write(f'min: {YPLUS_MIN}\n')
    report_file.write(f'max: {YPLUS_MAX}\n')
    report_file.write(f'avg: {YPLUS_AVG}\n')
    report_file.write('\n')

    # write forces
    report_file.write('Forces\n')
    report_file.write('------\n')
    NAMES = ['Cd', 'Cl', 'Cm']
    for i in range(len(FINAL_COEFFS)):
        report_file.write(f'{NAMES[i]}:\t {FINAL_COEFFS[i]}\n')
    report_file.write('\n')
    for i in range(len(FINAL_COEFFS_WINDOW)):
        report_file.write(f'{NAMES[i]}_WINDOW:\t {FINAL_COEFFS_WINDOW[i]}\n')
    report_file.write(f'size window:\t {WINDOW_SIZE}\n')
    report_file.write('\n')

    # write residuals
    report_file.write('Final Residuals\n')
    report_file.write('---------\n')
    for i in range(len(FINAL_RESIDUALS)):
        report_file.write(f'{HEADERS_RESIDUALS[i]}:\t {FINAL_RESIDUALS[i]}\n')
    report_file.write('\n')

    # write log files
    report_file.write('Log Files\n')
    report_file.write('---------\n')
    report_file.write(f'total status: {"SUCCESS" if TOTAL_STATUS_CODE == 1 else "FAIL"}\n')
    for i in range(len(LOG_LIST)):
        report_file.write(f'log file {LOG_LIST[i]}:\t {STATUS_CODE[i]}\n')
    report_file.write('\n')

    # write log files solver
    report_file.write('Log Files Solver\n')
    report_file.write('----------------\n')
    report_file.write(f'execution time: {L_EXECUTION_TIME}\n')
    report_file.write(f'number iterations: {L_NUMBER_ITERATIONS}\n')
    report_file.write(f'solver name: {L_SOLVER_NAME}\n')
    report_file.write(f'iterations per execution time: {L_ITERRATIONS_PER_EXECUTION_TIME}\n')
    report_file.write('\n')

    report_file.close()

    return


if __name__ == "__main__":

    OPENFOAM_WORKSPACE_DIR = '\\\\wsl.localhost\\Ubuntu\\home\\felixmarti\\openfoam-data\\sphereCases\\todo\\Ma2.3_AoA8_R1_rhoCentralFoam_WSL2'
    write_report(OPENFOAM_WORKSPACE_DIR, WINDOW_SIZE=50, SOLVER_EXTENSIONS=['rhoCentralFoam', 'rhoPimpleFoam', 'simpleFoam', 'rhoSimpleFoam'])
    