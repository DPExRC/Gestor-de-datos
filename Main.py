import tkinter as tk
from components.base_mostrar_view import BaseView
from components.botones import BotonBasePlace

from controller.AjustesController import AjustesController
from controller.DocumentosController import DocumentosController
from controller.ResultadosExcelController import ResultadosExcelController
from controller.VectorCargaController import VectorCargaController
from controller.MainController import MainController

from model.AjustesModel import AjustesModel
from model.DocumentosModel import DocumentosModel
from model.ResultadosExcelModel import ResultadosExcelModel
from model.VectorCargaModel import VectorCargaModel
from model.MainModel import MainModel

from view.AjustesView import AjustesView
from view.DocumentosView import DocumentosView
from view.ResultadosExcelView import ResultadosExcelView
from view.VectorCargaView import VectorCargaView
from view.MainView import MainView


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio Suralis")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Registro de vistas
        self.views = {}
        self.current_view = None

        # Crear el modelo y controlador para MainView
        self.main_model = MainModel()
        self.views["main_view"] = MainView(
            self.root,
            self.mostrar_vector_carga_view,
            self.mostrar_resultados_excel_view,
            self.mostrar_documentos_view,
            self.mostrar_ajustes_view,
        )
        self.main_controller = MainController(self.root, self.main_model, self.views["main_view"])

        # Mostrar la vista principal
        self.mostrar_main_view()

    def limpiar_main_frame(self):
        """Ocultar todas las vistas activas."""
        for view in self.views.values():
            view.hide()

    def mostrar_main_view(self):
        """Mostrar la vista principal."""
        self.limpiar_main_frame()
        self.show_view("main_view")

    def registrar_vista(self, view_name, view_class, model_class, controller_class):
        """Registrar una vista, su modelo y controlador."""
        if view_name not in self.views:
            # Crear la vista
            self.views[view_name] = view_class(self.root, self.mostrar_main_view)
            
            # Crear el modelo y controlador
            model = model_class()
            controller = controller_class(model, self.views[view_name], self.mostrar_main_view)
            
            # Vincular el controlador a la vista
            self.views[view_name].set_controller(controller)


    def mostrar_vector_carga_view(self):
        """Mostrar la vista de Vector de Carga."""
        self.limpiar_main_frame()
        self.registrar_vista("vector_carga_view", VectorCargaView, VectorCargaModel, VectorCargaController)
        self.show_view("vector_carga_view")

    def mostrar_resultados_excel_view(self):
        """Mostrar la vista de Resultados Excel."""
        self.limpiar_main_frame()
        self.registrar_vista("resultados_excel_view", ResultadosExcelView, ResultadosExcelModel, ResultadosExcelController)
        self.show_view("resultados_excel_view")

    def mostrar_documentos_view(self):
        """Mostrar la vista de Documentos."""
        self.limpiar_main_frame()
        self.registrar_vista("documentos_view", DocumentosView, DocumentosModel, DocumentosController)
        self.show_view("documentos_view")

    def mostrar_ajustes_view(self):
        """Mostrar la vista de Documentos."""
        self.limpiar_main_frame()
        self.registrar_vista("ajustes_view", AjustesView, AjustesModel, AjustesController)
        self.show_view("ajustes_view")

    def show_view(self, view_name):
        """Método para mostrar una vista específica."""
        # Ocultar la vista actual si existe
        if self.current_view:
            self.current_view.hide()

        # Obtener la vista a mostrar y actualizar current_view
        self.current_view = self.views[view_name]
        
        # Mostrar la nueva vista
        self.current_view.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()