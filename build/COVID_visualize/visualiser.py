'''
contains all methods for visualisation tasks
'''

import matplotlib.pyplot as plt
import matplotlib.lines as mlines #for legend actors
import matplotlib.patches as patches #for boundaries
import matplotlib as mpl
# from matplotlib.transforms import TransformedBbox, Affine2D
import numpy as np

from environment import build_hospital
from utils import check_folder

def set_style(Config):
    '''sets the plot style
    
    '''
    if Config.plot_style.lower() == 'dark':
        mpl.style.use('plot_styles/dark.mplstyle')
    
    if Config.plot_text_style == 'LaTeX':
        mpl.rc('text', usetex = True)
        mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}',
                                               r'\usepackage{amssymb}']
        mpl.rcParams['font.family'] = 'serif'
    else:
        mpl.rc('text', usetex = False)

def build_fig(Config, figsize=(10,5)):
    set_style(Config)

    if not Config.self_isolate:
        fig = plt.figure(figsize=(10,5))
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[5,5])
    elif Config.self_isolate:
        fig = plt.figure(figsize=(12,5))
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=[7,5])

    ax1 = fig.add_subplot(spec[0,0])
    # plt.title('infection simulation')
    plt.xlim(Config.xbounds[0], Config.xbounds[1])
    plt.ylim(Config.ybounds[0], Config.ybounds[1])

    lower_corner = (Config.xbounds[0],Config.ybounds[0])
    width = Config.xbounds[1] - Config.xbounds[0]
    height = Config.ybounds[1] - Config.ybounds[0]

    # Draw boundary of world
    if Config.plot_style.lower() == 'dark':
        bound_color = 'w'
    elif Config.plot_style.lower() == 'default':
        bound_color = 'k'
        
    rect = patches.Rectangle(lower_corner, width, height, linewidth=1, edgecolor=bound_color, facecolor='none', fill='None', hatch=None)
    # Add the patch to the Axes
    ax1.add_patch(rect)

    if Config.self_isolate and Config.isolation_bounds != None:
        build_hospital(Config.isolation_bounds[0], Config.isolation_bounds[2],
                       Config.isolation_bounds[1], Config.isolation_bounds[3], ax1, 
                       bound_color, addcross = False)

    ax1.axis('off')

    # SIR graph
    ax2 = fig.add_subplot(spec[0,1])
    # ax2.set_title('number of infected')
    #ax2.set_xlim(0, simulation_steps)
    ax2.set_ylim(0, Config.pop_size)

    ax2.set_xlabel('Time (days)', fontsize = 14)
    ax2.set_ylabel('Population size', fontsize = 14)

    #get color palettes
    palette = Config.get_palette()

    # Legend actors
    # a1 = mlines.Line2D([], [], color=palette[1], marker='', markersize=5, linestyle=':')
    # a2 = mlines.Line2D([], [], color=palette[1], marker='', markersize=5, linestyle='-')
    # a3 = mlines.Line2D([], [], color=palette[3], marker='', markersize=5, linestyle='-')
    # a4 = mlines.Line2D([], [], color=palette[0], marker='', markersize=5, linestyle='-')
    # a5 = mlines.Line2D([], [], color=palette[2], marker='', markersize=5, linestyle='-')
    # Legend actors type 2
    a1 = mlines.Line2D([], [], color=palette[1], marker='', markersize=5, linestyle=':')
    a2 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[1], fill='None', hatch=None)
    a3 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[0], fill='None', hatch=None)
    a4 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[2], fill='None', hatch=None)
    a5 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[3], fill='None', hatch=None)

    handles, labels = [[a1,a2,a3,a4,a5], ['healthcare capacity','infectious','susceptible','recovered','fatalities']]
    fig.legend(handles, labels, loc='upper center', ncol=5, fontsize = 10)

    # Get tight figure bbox
    tight_bbox_raw = fig.get_tightbbox(fig.canvas.get_renderer())
    # tight_bbox = TransformedBbox(tight_bbox_raw, Affine2D().scale(1./fig.dpi))

    #if 

    return fig, spec, ax1, ax2, tight_bbox_raw

def build_fig_scatter(Config, figsize=(5,5)):
    set_style(Config)

    if not Config.self_isolate:
        fig = plt.figure(figsize=(5,5))
    elif Config.self_isolate:
        fig = plt.figure(figsize=(7,5))

    ax1 = fig.gca()
    # plt.title('infection simulation')
    plt.xlim(Config.xbounds[0], Config.xbounds[1])
    plt.ylim(Config.ybounds[0], Config.ybounds[1])

    lower_corner = (Config.xbounds[0],Config.ybounds[0])
    width = Config.xbounds[1] - Config.xbounds[0]
    height = Config.ybounds[1] - Config.ybounds[0]

    # Draw boundary of world
    if Config.plot_style.lower() == 'dark':
        bound_color = 'w'
    elif Config.plot_style.lower() == 'default':
        bound_color = 'k'
        
    rect = patches.Rectangle(lower_corner, width, height, linewidth=1, edgecolor=bound_color, facecolor='none', fill='None', hatch=None)
    # Add the patch to the Axes
    ax1.add_patch(rect)

    if Config.self_isolate and Config.isolation_bounds != None:
        build_hospital(Config.isolation_bounds[0], Config.isolation_bounds[2],
                       Config.isolation_bounds[1], Config.isolation_bounds[3], ax1, 
                       bound_color, addcross = False)

    ax1.axis('off')

    #get color palettes
    palette = Config.get_palette()

    if not Config.black_white: # for colored mode
        
        marker_type = ['.'] * 4
        marker_sizes = [Config.marker_size] * 4
        # Legend actors
        # a1 = mlines.Line2D([], [], color=palette[1], marker='', markersize=5, linestyle=':')
        # a2 = mlines.Line2D([], [], color=palette[1], marker='', markersize=5, linestyle='-')
        # a3 = mlines.Line2D([], [], color=palette[3], marker='', markersize=5, linestyle='-')
        # a4 = mlines.Line2D([], [], color=palette[0], marker='', markersize=5, linestyle='-')
        # a5 = mlines.Line2D([], [], color=palette[2], marker='', markersize=5, linestyle='-')
        # Legend actors type 2
        a2 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[1], fill='None', hatch=None)
        a3 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[0], fill='None', hatch=None)
        a4 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[2], fill='None', hatch=None)
        a5 = patches.Rectangle((20,20), 20, 20, linewidth=1, edgecolor='none', facecolor=palette[3], fill='None', hatch=None)
    else:

        marker_type = ['o','d','o','x']
        marker_sizes = [3,5,3,5]
        line_widths = [1,1,1,5]

        # Legend actors type 3
        a2 = mlines.Line2D([], [], color=palette[1], marker=marker_type[1], markersize=marker_sizes[1], linestyle='', linewidth=line_widths[1])
        a3 = mlines.Line2D([], [], color=palette[0], marker=marker_type[0], markersize=marker_sizes[0], linestyle='', linewidth=line_widths[0])
        a4 = mlines.Line2D([], [], color=palette[2], marker=marker_type[2], markersize=marker_sizes[2], linestyle='', linewidth=line_widths[2])
        a5 = mlines.Line2D([], [], color=palette[3], marker=marker_type[3], markersize=marker_sizes[3], linestyle='', linewidth=line_widths[3])

    handles, labels = [[a2,a3,a4,a5], ['infectious','susceptible','recovered','fatalities']]
    fig.legend(handles, labels, loc='upper center', ncol=4, fontsize = 10)

    # Get tight figure bbox
    tight_bbox_raw = fig.get_tightbbox(fig.canvas.get_renderer())
    # tight_bbox = TransformedBbox(tight_bbox_raw, Affine2D().scale(1./fig.dpi))

    #if 

    return fig, ax1, tight_bbox_raw

def build_fig_SIRonly(Config, figsize=(5,4)):
    set_style(Config)
    if Config.black_white:
        fig = plt.figure(figsize=(5.5,4))
    else:
        fig = plt.figure(figsize=(5,4))

    spec = fig.add_gridspec(ncols=1, nrows=1)

    ax1 = fig.add_subplot(spec[0,0])
    #ax2.set_xlim(0, simulation_steps)
    ax1.set_ylim(0, Config.pop_size + 100)

    ax1.set_xlabel('Time (days)', fontsize = 14)
    ax1.set_ylabel('Population size', fontsize = 14)

    #get color palettes
    palette = Config.get_palette()
    
    if Config.black_white: # create legend if black and white mode selected
        # Legend actors
        a1 = mlines.Line2D([], [], color=palette[2], marker='', linewidth=2, linestyle='-')
        a2 = mlines.Line2D([], [], color=palette[0], marker='', linewidth=1, linestyle='-.')
        a3 = mlines.Line2D([], [], color=palette[0], marker='', linewidth=1, linestyle='--')
        a4 = mlines.Line2D([], [], color=palette[0], marker='', linewidth=1, linestyle='--', dashes=(5,2,20,2) )
        a5 = mlines.Line2D([], [], color=palette[0], marker='', linewidth=1, linestyle=':')

        handles, labels = [[a1,a2,a3,a4,a5], ['healthcare capacity','susceptible','infectious','recovered','fatalities']]
        leg = fig.legend(handles, labels, loc='upper center', ncol=3, fontsize = 10)
        
        return fig, spec, ax1, leg
    else:
        return fig, spec, ax1

def build_fig_time_series(Config, label, figsize=(5,4)):
    set_style(Config)
    fig = plt.figure(figsize=(5,4))
    spec = fig.add_gridspec(ncols=1, nrows=1)

    ax1 = fig.add_subplot(spec[0,0])

    ax1.set_xlabel('Time (days)', fontsize = 14)
    ax1.set_ylabel(label, fontsize = 14)
    
    # handles, labels = [[a1,a2,a3,a4,a5], ['healthcare capacity','infectious','susceptible','recovered','fatalities']]
    # fig.legend(handles, labels, loc='upper center', ncol=5, fontsize = 10)

    #if 

    return fig, ax1

def draw_tstep(Config, population, pop_tracker, frame,
               fig, spec, ax1, ax2, tight_bbox = None):
    #construct plot and visualise

    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()

    # option 2, remove all lines and collections
    for artist in ax1.lines + ax1.collections + ax1.texts:
        artist.remove()
    for artist in ax2.lines + ax2.collections:
        artist.remove()

    ax1.set_xlim(Config.x_plot[0], Config.x_plot[1])
    ax1.set_ylim(Config.y_plot[0], Config.y_plot[1])
        
    #plot population segments
    healthy = population[population[:,6] == 0][:,1:3]
    ax1.scatter(healthy[:,0], healthy[:,1], color=palette[0], s = Config.marker_size, label='susceptible', zorder = 2)
    
    infected = population[population[:,6] == 1][:,1:3]
    ax1.scatter(infected[:,0], infected[:,1], color=palette[1], s = Config.marker_size, label='infectious', zorder = 2)

    immune = population[population[:,6] == 2][:,1:3]
    ax1.scatter(immune[:,0], immune[:,1], color=palette[2], s = Config.marker_size, label='recovered', zorder = 2)
    
    fatalities = population[population[:,6] == 3][:,1:3]
    ax1.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], s = Config.marker_size, label='fatalities', zorder = 2)

    # Trace path of random individual
    if Config.trace_path:
        grid_coords = pop_tracker.grid_coords
        ground_covered = pop_tracker.ground_covered[0,:]

        for grid in grid_coords[ground_covered > 0]:
            rect = patches.Rectangle(grid[:2], grid[2] - grid[0], grid[3] - grid[1], linewidth=1, edgecolor='r', facecolor='none', fill='None', hatch=None)
            # Add the patch to the Axes
            ax1.add_patch(rect)

    #add text descriptors
    ax1.text(Config.xbounds[0], 
             Config.ybounds[1] + ((Config.ybounds[1] - Config.ybounds[0]) / 100), 
             'timestep: %i, total: %i, susceptible: %i infectious: %i recovered: %i fatalities: %i' %(frame,
                                                                                                    len(population),
                                                                                                    len(healthy), 
                                                                                                    len(infected), 
                                                                                                    len(immune), 
                                                                                                    len(fatalities)),
                fontsize=6)

    x_data = np.arange(frame+1) / 10 # time vector for plot
    if Config.treatment_dependent_risk:
        infected_arr = np.asarray(pop_tracker.infectious)
        indices = np.argwhere(infected_arr >= Config.healthcare_capacity)

        a1 = ax2.plot(x_data, [Config.healthcare_capacity for x in range(len(pop_tracker.infectious))], 
                 'r:', label='healthcare capacity')

    if Config.plot_mode.lower() == 'default':
        ax2.plot(pop_tracker.infectious, color=palette[1])
        ax2.plot(pop_tracker.fatalities, color=palette[3], label='fatalities')
    elif Config.plot_mode.lower() == 'sir':
        
        I = pop_tracker.infectious
        S = np.add(I, pop_tracker.susceptible)
        Rr = np.add(S, pop_tracker.recovered) 
        Rf = np.add(Rr, pop_tracker.fatalities) 

        # ax2.plot(I, color=palette[1], label='infectious')
        # ax2.plot(S, color=palette[0], label='susceptible')
        # ax2.plot(Rr, color=palette[2], label='recovered')
        # ax2.plot(Rf, color=palette[3], label='fatalities')
        
        # Filled plot
        ax2.fill_between(x_data, [0.0]*(frame+1), I, color=palette[1]) #infectious
        ax2.fill_between(x_data, I, S, color=palette[0]) #healthy
        ax2.fill_between(x_data, S, Rr, color=palette[2]) #recovered
        ax2.fill_between(x_data, Rr, Rf, color=palette[3]) #dead

    else:
        raise ValueError('incorrect plot_style specified, use \'sir\' or \'default\'')

    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        
        if Config.plot_style == 'default':
            bg_color = 'w'
        elif Config.plot_style == 'dark':
            bg_color = "#121111"

        try:
            fig.savefig('%s/%i.pdf' %(Config.plot_path, frame), dpi=300, facecolor=bg_color, bbox_inches=tight_bbox)
        except:
            check_folder(Config.plot_path)
            fig.savefig('%s/%i.pdf' %(Config.plot_path, frame), dpi=300, facecolor=bg_color, bbox_inches=tight_bbox)

def draw_tstep_scatter(Config, population, pop_tracker, frame,
                       fig, ax1, tight_bbox = None):
    #construct plot and visualise

    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()

    if Config.black_white:
        marker_type = ['o','d','o','x']
        marker_sizes = [3,5,3,25]
        line_widths = [1,1,1,2]
    else:
        marker_type = ['.'] * 4
        marker_sizes = [Config.marker_size] * 4
        line_widths = [1,1,1,1]

    # option 2, remove all lines and collections
    for artist in ax1.lines + ax1.collections + ax1.texts:
        artist.remove()

    ax1.set_xlim(Config.x_plot[0], Config.x_plot[1])
    ax1.set_ylim(Config.y_plot[0], Config.y_plot[1])
        
    #plot population segments
    healthy = population[population[:,6] == 0][:,1:3]
    ax1.scatter(healthy[:,0], healthy[:,1], color=palette[0], marker = marker_type[0], s = marker_sizes[0], linewidth = line_widths[0], label='susceptible', zorder = 2)
    
    infected = population[population[:,6] == 1][:,1:3]
    ax1.scatter(infected[:,0], infected[:,1], color=palette[1], marker = marker_type[1], s = marker_sizes[1], linewidth = line_widths[1], label='infectious', zorder = 2)

    immune = population[population[:,6] == 2][:,1:3]
    ax1.scatter(immune[:,0], immune[:,1], color=palette[2], marker = marker_type[2], s = marker_sizes[2], linewidth = line_widths[2], label='recovered', zorder = 2)
    
    fatalities = population[population[:,6] == 3][:,1:3]
    ax1.scatter(fatalities[:,0], fatalities[:,1], color=palette[3], marker = marker_type[3], s = marker_sizes[3], linewidth = line_widths[3], label='fatalities', zorder = 2)

    # Trace path of random individual
    if Config.trace_path:
        grid_coords = pop_tracker.grid_coords
        if pop_tracker.ground_covered.ndim > 1:
            ground_covered = pop_tracker.ground_covered[0,:]
        elif pop_tracker.ground_covered.ndim == 1:
            ground_covered = pop_tracker.ground_covered

        for grid in grid_coords[ground_covered == 1]:
            rect = patches.Rectangle(grid[:2], grid[2] - grid[0], grid[3] - grid[1], linewidth=1, edgecolor='r', facecolor='none', fill='None', hatch=None)
            # Add the patch to the Axes
            ax1.add_patch(rect)

    #add text descriptors
    ax1.text(Config.xbounds[0], 
             Config.ybounds[1] + ((Config.ybounds[1] - Config.ybounds[0]) / 100), 
             'timestep: %i, total: %i, susceptible: %i infectious: %i recovered: %i fatalities: %i' %(frame,
                                                                                                    len(population),
                                                                                                    len(healthy), 
                                                                                                    len(infected), 
                                                                                                    len(immune), 
                                                                                                    len(fatalities)),
                fontsize=6)


    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        
        if Config.plot_style == 'default':
            bg_color = 'w'
        elif Config.plot_style == 'dark':
            bg_color = "#121111"

        try:
            fig.savefig('%s/%i.pdf' %(Config.plot_path, frame), dpi=300, facecolor=bg_color, bbox_inches=tight_bbox)
        except:
            check_folder(Config.plot_path)
            fig.savefig('%s/%i.pdf' %(Config.plot_path, frame), dpi=300, facecolor=bg_color, bbox_inches=tight_bbox)

def draw_SIRonly(Config, fig, ax1, leg=None, pop_tracker=None, data=None):

    #construct plot and visualise

    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()

    # option 2, remove all lines and collections
    for artist in ax1.lines + ax1.collections + ax1.texts:
        artist.remove()

    ax1.set_ylim(0, Config.pop_size + 200)

    if pop_tracker is not None:
        S = pop_tracker.susceptible
        I = pop_tracker.infectious
        R = pop_tracker.recovered
        F = pop_tracker.fatalities
    elif data is not None:
        S = data[:,1]
        I = data[:,2]
        R = data[:,3]
        F = data[:,4]

    x_data = np.arange(len(I)) / 10 # time vector for plot
    if Config.treatment_dependent_risk:
        infected_arr = np.asarray(I)
        indices = np.argwhere(infected_arr >= Config.healthcare_capacity)

    if Config.plot_mode.lower() == 'default':
        ax1.plot(x_data, I, color=palette[1])
        ax1.plot(x_data, F, color=palette[3], label='fatalities')

    elif Config.plot_mode.lower() == 'sir':

        if Config.black_white:
            ax1.plot(x_data, S, color=palette[0], label='susceptible', linestyle='-.', linewidth=1)
            ax1.plot(x_data, I, color=palette[0], label='infectious', linestyle='--', linewidth=1)
            ax1.plot(x_data, R, color=palette[0], label='recovered', linestyle='--', dashes=(5,2,20,2), linewidth=1)
            ax1.plot(x_data, F, color=palette[0], label='fatalities', linestyle=':', linewidth=1)

            ax1.plot(x_data, [Config.healthcare_capacity for x in range(len(I))], 
                     color=palette[2], label='healthcare capacity', linestyle='-', linewidth=2)

        elif not Config.black_white:
            ax1.plot(x_data, S, color=palette[0], label='susceptible')
            ax1.plot(x_data, I, color=palette[1], label='infectious')
            ax1.plot(x_data, R, color=palette[2], label='recovered')
            ax1.plot(x_data, F, color=palette[3], label='fatalities')

            ax1.plot(x_data, [Config.healthcare_capacity for x in range(len(I))], 
                     color=palette[1], linestyle='--', label='healthcare capacity')
    else:
        raise ValueError('incorrect plot_style specified, use \'sir\' or \'default\'')
    
    if not Config.black_white:
        ax1.legend(loc = 'best', fontsize = 10)
    elif Config.black_white:
        # # Get the bounding box of the original legend
        # bb = leg.get_bbox_to_anchor().inverse_transformed(ax1.transAxes)

        # # Change to location of the legend. 
        # yOffset = 0.2
        # xOffset = 0.0
        # bb.x0 += yOffset
        # bb.x1 += xOffset
        # leg.set_bbox_to_anchor(bb, transform = ax1.transAxes)
        pass

    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        
        if Config.plot_style == 'default':
            bg_color = 'w'
        elif Config.plot_style == 'dark':
            bg_color = "#121111"

        try:
            fig.savefig('%s/SIRF_plot.pdf' %(Config.plot_path), dpi=1000, facecolor=bg_color, bbox_inches='tight')
        except:
            check_folder(Config.plot_path)
            fig.savefig('%s/SIRF_plot.pdf' %(Config.plot_path), dpi=1000, facecolor=bg_color, bbox_inches='tight')

def draw_time_series(Config, time, data, label, fig, ax1, line_label=None, threshold=None, threshold_label=None):

    #construct plot and visualise

    #set plot style
    set_style(Config)

    #get color palettes
    palette = Config.get_palette()

    # option 2, remove all lines and collections
    for artist in ax1.lines + ax1.collections + ax1.texts:
        artist.remove()

    ax1.plot(time / 10, data, label=line_label)
    
    if (line_label is not None) and (threshold is not None) and (threshold_label is not None):
        ax1.plot(time / 10, [threshold for x in range(len(data))], 
                 'r:', label=threshold_label)

    ax1.legend(loc = 'best', fontsize = 10)

    plt.draw()
    plt.pause(0.0001)

    if Config.save_plot:
        
        if Config.plot_style == 'default':
            bg_color = 'w'
        elif Config.plot_style == 'dark':
            bg_color = "#121111"

        try:
            fig.savefig('%s/%s_plot.pdf' %(Config.plot_path, label), dpi=100, facecolor=bg_color, bbox_inches='tight')
        except:
            check_folder(Config.plot_path)
            fig.savefig('%s/%s_plot.pdf' %(Config.plot_path, label), dpi=100, facecolor=bg_color, bbox_inches='tight')