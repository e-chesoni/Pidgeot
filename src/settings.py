# Enable project settings
class uav_simulator_settings:
    _debug = True
    _show_plots = False

    @staticmethod
    def set_debug(DEBUG):
        uav_simulator_settings._debug = DEBUG

    @staticmethod
    def set_plots(SHOW_PLOTS):
        uav_simulator_settings._show_plots = SHOW_PLOTS
    
    @staticmethod
    def get_debug_setting():
        return uav_simulator_settings._debug
    
    @staticmethod
    def get_plot_setting():
        return uav_simulator_settings._show_plots
