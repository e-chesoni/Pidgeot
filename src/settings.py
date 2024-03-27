# Enable project settings
class uav_simulator_settings:
    _debug = True
    _show_plots = False
    _deflect_delta_down = True
    _apply_stall_model = True

    @staticmethod
    def set_debug(DEBUG):
        uav_simulator_settings._debug = DEBUG

    @staticmethod
    def set_plots(SHOW_PLOTS):
        uav_simulator_settings._show_plots = SHOW_PLOTS

    @staticmethod
    def set_apply_stall_model(APPLY_STALL_MODEL):
        uav_simulator_settings._apply_stall_model = APPLY_STALL_MODEL
    
    @staticmethod
    def set_delta_deflection_down(DEFLECT_DELTA_DOWN):
        uav_simulator_settings._deflect_delta_down = DEFLECT_DELTA_DOWN
    
    @staticmethod
    def get_debug_setting():
        return uav_simulator_settings._debug
    
    @staticmethod
    def get_plot_setting():
        return uav_simulator_settings._show_plots
    
    @staticmethod
    def get_apply_stall_model():
        return uav_simulator_settings._apply_stall_model
    
    @staticmethod
    def get_delta_deflection_down():
        return uav_simulator_settings._deflect_delta_down
