class GeneradorController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.view.set_controller(self)


    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()
        
    def get_processed_data(self):
        headers, data = self.model.load_default_file()
        return headers, data
        pass