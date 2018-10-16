# -*- coding: utf-8 -*-
import sys, os, pyglet, time, datetime
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np
from mod import DrawLine, DrawStim

# Get display informations
use_scr = 0
config = Config(sample_buffers=1, samples=4) # configuration for anti-aliasing
platform = pyglet.window.get_platform()
display = platform.get_default_display()      
screens = display.get_screens()
win = pyglet.window.Window()
win.set_config = config
#win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen = True, screen = screens[use_scr])
#win.set_exclusive_mouse() # Exclude mouse pointer
key = pyglet.window.key
batch = pyglet.graphics.Batch()

#------------------------------------------------------------------------
rept = 3 # Input repeat counts
data = pd.read_csv("hoch.csv") # Load the condition file
distract_x = -1 # presentation distract grid on right when positive number
line_width = 3 # circles' line size
d = 5 # disparity
#------------------------------------------------------------------------

# Load variable conditions
header = data.columns # Store variance name
ind = data.shape[0] # Store number of csv file's index
dat = pd.DataFrame()
list_a = [] # Create null list to store experimental variance
list_b = []
iso = 6.8
deg1 = 42.8 # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = 30.0 # 42 arcmin = 30 pix
cntx = screens[use_scr].width/2 #Store center of screen about x positon
cnty = screens[use_scr].height/4 #Store center of screen about y position
draw_objects = [] # 描画対象リスト
draw_batches = []
trial = False # Routine status to be exitable or not
tcs = [] # Store transients per trials
trial_starts = [] # Store time when trial starts
kud_list = [] # Store durations of key pressed
cdt = [] #Store sum(kud), cumulative reaction time on a trial.

# Load sound resource
p_sound = pyglet.resource.media("button57.mp3", streaming = False)
beep_sound = pyglet.resource.media("p01.mp3", streaming = False)

#--------------------------------------- 

r = 50
pi = np.pi

# A getting key response function
class key_resp(object):
    def on_key_press(self, symbol, modifiers):
        global tc, trial
        if trial == True and symbol == key.SPACE:
            kd.append(time.time())
            tc = tc + 1
        if trial == False and symbol == key.B:
            trial = True
            p_sound.play()
            pyglet.app.exit()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()
    def on_key_release(self, symbol, modifiers):
        global tc
        if trial == True and symbol == key.SPACE:
            ku.append(time.time())
            tc = tc + 1
resp_handler = key_resp()

# Set up polygons for presentation area
bsl = DrawStim.Quad(deg1*5, deg1*5, cntx - deg1*iso, cnty, 1.0, 1.0, 1.0)
bsr = DrawStim.Quad(deg1*5, deg1*5, cntx + deg1*iso, cnty, 1.0, 1.0, 1.0)
lfixv = DrawStim.Quad(3, 8, cntx - deg1*iso, cnty, 0.0,0.0,1.0)
lfixw = DrawStim.Quad(8, 3, cntx - deg1*iso, cnty, 0.0,0.0,1.0)
rfixv = DrawStim.Quad(3, 8, cntx + deg1*iso, cnty, 0.0,0.0,1.0)
rfixw = DrawStim.Quad(8, 3, cntx + deg1*iso, cnty, 0.0,0.0,1.0)

circler = DrawStim.Circle(cntx + deg1*iso+d, cnty, 3, 50, 120)
circlel = DrawStim.Circle(cntx - deg1*iso-d, cnty, 3, 50, 120)
lerge_circler = DrawStim.Circle(cntx + deg1*iso, cnty, 3, 100, 120)
lerge_circlel = DrawStim.Circle(cntx - deg1*iso, cnty, 3, 100, 120)

# Display fixation
def fixer():
    draw_objects.append(bsl)
    draw_objects.append(bsr)
    draw_objects.append(lfixv)
    draw_objects.append(lfixw)
    draw_objects.append(rfixv)
    draw_objects.append(rfixw)

# display stimlus
def stimli(dt):
    draw_objects.append(inner)
    draw_objects.append(outer)
    draw_objects.append(circler)
    draw_objects.append(lerge_circler)
    draw_objects.append(circlel)
    draw_objects.append(lerge_circlel)
    draw_objects.append(lfixv)
    draw_objects.append(lfixw)
    draw_objects.append(rfixv)
    draw_objects.append(rfixw)

# A ending trial function
def end_routine(dt):
    global trial
    trial = False
    beep_sound.play()
    fixer()

@win.event
def on_draw():
    # Refresh window
    win.clear()
    # 描画対象のオブジェクトを描画する
    for draw_object in draw_objects:
        draw_object.draw()

# Event handler handlers
def set_handler(dt):
    win.push_handlers(resp_handler)
def remove_handler(dt):
    win.remove_handlers(resp_handler)

# Remove all components
def delete(dt):
    del draw_objects[:]
    p_sound.play()
    # Check the experiment continue or break
    if i == dl - 1:
        pyglet.app.exit()

# Store the start time
start = time.time()

fixer()

#----------------- start loop -----------------------------
# Get variables per trial from csv
for j in range(rept):
    camp = data.take(np.random.permutation(ind))
    dat = pd.concat([dat, camp], axis=0, ignore_index=True)
dat = dat.values
dl = dat.shape[0]
for i in range(dl):
    tc = 0 #Count transients
    ku = deque([]) #Store unix time when key up
    kd = deque([]) #Store unix time when key down
    kud = [] # Differences between kd and ku
    da = dat[i]
    cola = da[0] # Store variance of index [i], column 0
    colb = da[1] # Store variance of index [i], column 1
    list_a.append(cola)
    list_b.append(colb)
    print(2*round(r/line_width))   
    # Set up polygon for stimulus
    inner = DrawStim.cLine(cntx - deg1*iso - d, cnty, -cola, line_width, 2*round(r/line_width), line_width, r, 0)
    outer = DrawStim.cLine(cntx - deg1*iso - d, cnty, cola, line_width, 2*round(r/line_width), line_width, r, 180)
    
    # Scheduling flow
    pyglet.clock.schedule_once(remove_handler, 0.0)
    pyglet.clock.schedule_once(stimli, 1.0)
    pyglet.clock.schedule_once(set_handler, 1.0)
    pyglet.clock.schedule_once(remove_handler, 31.0)
    pyglet.clock.schedule_once(delete, 31.0)
    pyglet.clock.schedule_once(end_routine, 61.0)
    pyglet.clock.schedule_once(set_handler, 61.0)
    
    trial_start = time.time()
    
    pyglet.app.run()
    
    trial_end = time.time()
    
    # Get results
    ku.append(trial_start + 31.0)
    while len(kd) > 0:
        kud.append(ku.popleft() - kd.popleft() + 0) # list up key_press_duration
    kud_list.append(str(kud))
    cdt.append(sum(kud))
    tcs.append(tc)
    trial_starts.append(trial_start)
    print("--------------------------------------------------")
    print("trial_start:"  + str(trial_start))
    print("trial_end:" + str(trial_end))
    print("key_pressed:"  + str(kud))
    print("transient counts:"  + str(tc))
    print("cdt:"  + str(sum(kud)))
    print("condition" + str(da))
    print("-------------------------------------------------- ")
#-------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({header.base[0]:list_a, # Store variance_A conditions
                        header.base[1]:list_b, # Store variance_B conditions
                        "transient_counts":tcs, # Store transient_counts
                        "cdt":cdt, # Store cdt(target values) and input number of trials
                        "traial_start":trial_starts,
                        "key_press_list":kud_list}) # Store the key_press_duration list
#index = range(ind*rept)
results.to_csv(path_or_buf="./data/" + str(daten) + ".csv", index=False) # Output experimental data

# Output following to shell, check this experiment
print(u"開始日時: " + str(start))
print(u"終了日時: " + str(end_time))  
print(u"経過時間: " + str(end_time - start))
