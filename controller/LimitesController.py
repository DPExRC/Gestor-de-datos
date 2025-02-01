class LimitesController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.view.set_controller(self)


    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()