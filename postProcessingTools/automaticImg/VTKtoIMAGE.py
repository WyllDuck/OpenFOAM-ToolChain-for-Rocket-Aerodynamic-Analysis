#!/usr/bin/env python39

# Import necessary modules
import os
import sys
import datetime
from time import sleep

# Set the path to ParaView libraries
paraview_path = 'C:\Program Files\ParaView 5.11.1\\bin\Lib\site-packages'
sys.path.append(paraview_path)
from paraview.simple import *



def capture_screenshot(FILE_PATH, field, camera_position, view_up, parallel_scale, save_name = None):

    # use date for naming file
    if save_name is None:
        save_name = 'output_{}.png'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    sleep(1) # make sure the file name is unique

    save_name = str(field) + '_' + save_name

    # Disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()
    
    # Create an XMLPolyDataReader
    planeXZvtp = XMLPolyDataReader(registrationName='planeXZ.vtp', FileName=[FILE_PATH])
    planeXZvtp.CellArrayStatus = [field]
    
    # Set up the render view
    renderView1 = GetActiveViewOrCreate('RenderView')
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = camera_position
    renderView1.CameraFocalPoint = [camera_position[0], 0.0, 0.0]
    renderView1.CameraViewUp = view_up
    renderView1.CameraParallelScale = parallel_scale
    
    # Show the data
    planeXZvtpDisplay = Show(planeXZvtp, renderView1, 'GeometryRepresentation')
    
    # Color mapping
    ColorBy(planeXZvtpDisplay, ('CELLS', field))
    planeXZvtpDisplay.RescaleTransferFunctionToDataRange(True, False)
    planeXZvtpDisplay.SetScalarBarVisibility(renderView1, True)
    
    # Set layout size
    layout1 = GetLayout()
    layout1.SetSize(800, 600)
    
    # Save a screenshot
    save_path = '{}/{}'.format(WORK_DIR, save_name)
    SaveScreenshot(save_path, renderView1, ImageResolution=[3200, 2400], OverrideColorPalette='WhiteBackground')
    
    Disconnect()
    Connect()
    
    print(f'Screenshot saved to {save_path}')
    return save_path




def list_of_capture_screenshots (FILE_PATH, _camera_positions, _fields, _view_ups, _parallel_scales, _save_names = None):

    if _save_names is None:
        _save_names = [None] * len(_camera_positions)

    for i in range(len(_camera_positions)):
        
        fields = _fields[i]
        camera_position = _camera_positions[i]
        view_up = _view_ups[i]
        save_name = _save_names[i]
        parallel_scale = _parallel_scales[i]

        for field in fields:
            capture_screenshot(FILE_PATH, field, camera_position, view_up, parallel_scale, save_name=save_name.format(field))

    return

# This is the default screenshots that we need
def default1 (FILE_PATH):

    camera_positions = [
        [0.6223108544688549, 2.7899207451118118, 0], # all
        [0.00814209937306845, 0.028697095855665492, 0], # zoomed tip
        [1.034125040722357, 0.028697095855665492, 0], # zoomed aft
    ]

    view_ups = [
        [0, 0, -1],
        [-1, 0, 0],
        [-1, 0, 0],
    ]

    fields = [
        ['Ma', 'p', 'T', 'U', 'rho'],
        ['Ma', 'p', 'T', 'U', 'rho'],
        ['Ma', 'p', 'T', 'U', 'rho'],
    ]

    save_names = [
        'all_.png',
        'zoomed_tip.png',
        'zoomed_aft.png',
    ]

    parallel_scales = [
        0.6,
        0.060588150906668324,
        0.060588150906668324,
    ]

    list_of_capture_screenshots(FILE_PATH, camera_positions, fields, view_ups, parallel_scales, save_names)


if __name__ == '__main__':

    WORK_DIR = "D:\good\\rhoPimpleFoam\Ma0.6_AoA16_R5_rhoPimpleFoam\postProcessing\surfaces1\\551"
    FILE_PATH = '{}\\{}'.format(WORK_DIR, 'planeXZ.vtp')
        
    default1(FILE_PATH)
    print("END")
