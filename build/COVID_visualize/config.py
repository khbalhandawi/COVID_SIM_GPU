'''
file that contains all configuration related methods and classes
'''

import numpy as np

class config_error(Exception):
    pass

class Configuration():
    def __init__(self, *args, **kwargs):
        #simulation variables
        self.verbose = True #whether to print infections, recoveries and fatalities to the terminal
        self.simulation_steps = 10000 #total simulation steps performed
        self.tstep = 0 #current simulation timestep
        self.save_data = False #whether to dump data at end of simulation
        self.save_pop = False #whether to save population matrix every 'save_pop_freq' timesteps
        self.save_pop_freq = 10 #population data will be saved every 'n' timesteps. Default: 10
        self.save_pop_folder = 'pop_data/' #folder to write population timestep data to
        self.endif_no_infections = True #whether to stop simulation if no infections remain
    
        #scenario flags
        self.traveling_infects = False
        self.self_isolate = False
        self.lockdown = False
        self.lockdown_percentage = 0.1 #after this proportion is infected, lock-down begins
        self.lockdown_compliance = 0.95 #fraction of the population that will obey the lockdown        

        #world variables, defines where population can and cannot roam
        self.xbounds = [0.02, 0.98]
        self.ybounds = [0.02, 0.98]
        self.n_gridpoints = 10 # resolution of 2D grid for tracking population position
        self.track_position = True
        self.track_GC = False
        self.track_R0 = False
        self.update_every_n_frame = 1
        self.update_R0_every_n_frame = 1

        #visualisation variables
        self.visualise = True #whether to visualise the simulation 
        self.visualise_every_n_frame = 1 #Frequency of plot update
        self.plot_mode = 'sir' #default or sir
        self.n_plots = 2 #number of subplots
        self.plot_last_tstep = True #plot last frame SIR
        self.trace_path = False #trace path of a single individual

        #size of the simulated world in coordinates
        self.x_plot = [0, 1] 
        self.y_plot = [0, 1]
        self.save_plot = False
        self.plot_path = 'render/' #folder where plots are saved to
        self.plot_style = 'default' #can be default, dark, ...
        self.plot_text_style = 'default' #can be default, LaTeX, ...
        self.black_white = False
        self.colorblind_mode = False
        #if colorblind is enabled, set type of colorblindness
        #available: deuteranopia, protanopia, tritanopia. defauld=deuteranopia
        self.colorblind_type = 'deuteranopia'
        self.verbose = True #output stats to console
        self.report_freq = 50; #report results every 50 frames
        self.report_status = False #output stats to console
        self.marker_size = 15 #markersize for plotting individuals

        #population variables
        self.pop_size = 2000
        self.mean_age = 45
        self.max_age = 105
        self.age_dependent_risk = True #whether risk increases with age
        self.risk_age = 55 #age where mortality risk starts increasing
        self.critical_age = 75 #age at and beyond which mortality risk reaches maximum
        self.critical_mortality_chance = 0.1 #maximum mortality risk for older age
        self.risk_increase = 'quadratic' #whether risk between risk and critical age increases 'linear' or 'quadratic'
        
        #movement variables
        #mean_speed = 0.01 # the mean speed (defined as heading * speed)
        #std_speed = 0.01 / 3 #the standard deviation of the speed parameter
        #the proportion of the population that practices social distancing, simulated
        #by them standing still
        self.proportion_distancing = 0
        self.social_distance_factor = 0.0
        self.speed = 0.01 #average speed of population
        self.max_speed = 1.0 #average speed of population
        self.dt = 0.01 #average speed of population
        
        self.wander_step_size = 0.01
        self.gravity_strength = 1
        self.wander_step_duration = 0.02
        
        self.thresh_type = 'infected'
        self.testing_threshold_on = 0.0 # number of infected
        self.social_distance_threshold_on = 0.0 # number of hospitalized
        self.social_distance_threshold_off = 0.0 # number of remaining infected people
        self.social_distance_violation = 0.0 # number of people
        self.SD_act_onset = False

        #when people have an active destination, the wander range defines the area
        #surrounding the destination they will wander upon arriving
        self.wander_range = 0.05
        self.wander_factor = 1 
        self.wander_factor_dest = 1.5 #area around destination

        #infection variables
        self.infection_range=0.01 #range surrounding sick patient that infections can take place
        self.infection_chance=0.03   #chance that an infection spreads to nearby healthy people each tick
        self.recovery_duration=(200, 500) #how many ticks it may take to recover from the illness
        self.mortality_chance=0.02 #global baseline chance of dying from the disease
        self.incubation_period=0 #number of frames the individual spreads disease unknowingly
        self.patient_Z_loc = 'random'

        #healthcare variables
        self.healthcare_capacity = 300 #capacity of the healthcare system
        self.treatment_factor = 0.5 #when in treatment, affect risk by this factor
        self.no_treatment_factor = 3 #risk increase factor to use if healthcare system is full
        #risk parameters
        self.treatment_dependent_risk = True #whether risk is affected by treatment

        #self isolation variables
        self.self_isolate_proportion = 0.6
        self.isolation_bounds = [0.02, 0.02, 0.1, 0.98]
        self.number_of_tests = 10
        
        #lockdown variables
        self.lockdown_percentage = 0.1 
        self.lockdown_vector = []
        
    def get_palette(self):
        '''returns appropriate color palette

        Uses config.plot_style to determine which palette to pick, 
        and changes palette to colorblind mode (config.colorblind_mode)
        and colorblind type (config.colorblind_type) if required.

        Palette colors are based on
        https://venngage.com/blog/color-blind-friendly-palette/
        '''

        #palette colors are: [healthy, infected, immune, dead]
        palettes = {'regular': {'default': ['#1C758A', '#CF5044', '#BBBBBB', '#444444'],
                                'dark': ['#1C758A', '#CF5044', '#BBBBBB', '#444444']},
                    'black_white': {'default': ['#000000', '#000000', '#BBBBBB', '#BBBBBB'],
                                      'dark': ['#FFFFFF', '#FFFFFF', '#6C6C6C', '#6C6C6C']},
                    'deuteranopia': {'default': ['gray', '#a50f15', '#08519c', 'black'],
                                     'dark': ['#404040', '#fcae91', '#6baed6', '#000000']},
                    'protanopia': {'default': ['gray', '#a50f15', '08519c', 'black'],
                                   'dark': ['#404040', '#fcae91', '#6baed6', '#000000']},
                    'tritanopia': {'default': ['gray', '#a50f15', '08519c', 'black'],
                                   'dark': ['#404040', '#fcae91', '#6baed6', '#000000']}
                    }

        if self.colorblind_mode:
            return palettes[self.colorblind_type.lower()][self.plot_style]
        elif self.black_white:
            return palettes['black_white'][self.plot_style]
        else:
            return palettes['regular'][self.plot_style]

    def get(self, key):
        '''gets key value from config'''
        try:
            return self.__dict__[key]
        except:
            raise config_error('key %s not present in config' %key)

    def set(self, key, value):
        '''sets key value in config'''
        self.__dict__[key] = value

    def isint(self,n):
        ''' check if string value is an int '''
        try:
            int(n)
            return True
        except:
            return False
    
    def isfloat(self,n):
        ''' check if string value is a float '''
        try:
            float(n)
            return True
        except:
            return False

    def read_from_file(self, path):
        '''reads config from filename'''
        # Read data from configuration file
        fileID = open(path,'r'); # Open file
        InputText = np.loadtxt(fileID,
                               delimiter = '\n',
                               dtype=np.str) # \n is the delimiter
        
        count = 0
        # Strips the newline character 
        for n,line in enumerate(InputText): # Read line by line
            line = InputText[n].split("=")
            key_value = None
            if len(line) > 1:
                key = line[0] # Return keys
                value = line[1] # Return value strings

                if value.isalpha():
                    if value == 'true':
                        key_value = True
                    elif value == 'false':
                        key_value = False
                    else:
                        key_value = value
                elif self.isint(value):
                        key_value = int(value)
                elif self.isfloat(value):
                        key_value = float(value)
                elif len(value.split(",")) > 1:
                    key_value = [float(i) for i in value.split(",")]

                self.set(key,key_value)

        if self.self_isolate:
            self.x_plot = [self.isolation_bounds[0] - 0.02, 1]

    def set_lockdown(self, lockdown_percentage=0.1, lockdown_compliance=0.9):
        '''sets lockdown to active'''

        self.lockdown = True

        #fraction of the population that will obey the lockdown
        self.lockdown_percentage = lockdown_percentage
        self.lockdown_vector = np.zeros((self.pop_size,))
        #lockdown vector is 1 for those not complying
        self.lockdown_vector[np.random.uniform(size=(self.pop_size,)) >= lockdown_compliance] = 1

    def set_self_isolation(self, isolation_bounds = [-0.28, 0.02, -0.02, 0.28]):
        '''sets self-isolation scenario to active'''

        self.self_isolate = True
        self.isolation_bounds = isolation_bounds
        #set roaming bounds to outside isolated area
        self.xbounds = [0.02, 0.98]
        self.ybounds = [0.02, 0.98]
        #update plot bounds everything is shown
        self.x_plot = [isolation_bounds[0] - 0.02, 1]
        self.y_plot = [0, 1]

    def set_reduced_interaction(self, speed = 0.001):
        '''sets reduced interaction scenario to active'''

        self.speed = speed

#=============================================================================
# Main execution 
if __name__ == '__main__':
    config = Configuration()
    config.read_from_file('configuration_debug.ini')