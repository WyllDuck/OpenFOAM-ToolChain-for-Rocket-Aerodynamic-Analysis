# trace generated using paraview version 5.10.0-RC1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# reset view to fit data
renderView1.ResetCamera(False)

# get active source.
casefoam = GetActiveSource()

# Properties modified on casefoam
casefoam.CaseType = 'Decomposed Case'

# get display properties
casefoamDisplay = GetDisplayProperties(casefoam, view=renderView1)

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

animationScene1.GoToLast()

# set scalar coloring
ColorBy(casefoamDisplay, ('POINTS', 'T'))

# rescale color and/or opacity maps used to include current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoamDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')

# get opacity transfer function/opacity map for 'T'
tPWF = GetOpacityTransferFunction('T')

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data
renderView1.ResetCamera(False)

# reset view to fit data
renderView1.ResetCamera(False)

# get color legend/bar for tLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)

# change scalar bar placement
tLUTColorBar.WindowLocation = 'Any Location'
tLUTColorBar.Position = [0.7976973684210525, 0.2603305785123967]
tLUTColorBar.ScalarBarLength = 0.32999999999999996

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
tLUT.ApplyPreset('Turbo', True)

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(1216, 726)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.004681204964386803, 0.08242738227786825, -19.48528044351868]
renderView1.CameraFocalPoint = [0.004681204964386803, 0.08242738227786825, 1.4999999999999996]
renderView1.CameraParallelScale = 0.10085125649965931

# save screenshot
SaveScreenshot('/home/felix/sphereCases/run/rhoCentralFoam3/images/1.png', renderView1, ImageResolution=[1216, 726], 
    # PNG options
    CompressionLevel='0')

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1216, 726)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.004681204964386803, 0.08242738227786825, -19.48528044351868]
renderView1.CameraFocalPoint = [0.004681204964386803, 0.08242738227786825, 1.4999999999999996]
renderView1.CameraParallelScale = 0.10085125649965931

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).