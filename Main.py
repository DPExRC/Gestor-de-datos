import tkinter as tk
from components.get_path_images import get_path_images

from controller.DirectoriosController import DirectoriosController
from controller.RangosController import RangosController
from controller.AjustesController import AjustesController
from controller.DocumentosController import DocumentosController
from controller.ResultadosExcelController import ResultadosExcelController
from controller.UnidadesController import UnidadesController
from controller.VectorCargaController import VectorCargaController
from controller.MainController import MainController

from model.DirectoriosModel import DirectoriosModel
from model.RangosModel import RangosModel
from model.AjustesModel import AjustesModel
from model.DocumentosModel import DocumentosModel
from model.ResultadosExcelModel import ResultadosExcelModel
from model.UnidadesModel import UnidadesModel
from model.VectorCargaModel import VectorCargaModel
from model.MainModel import MainModel

from view.DirectoriosView import DirectoriosView
from view.RangosView import RangosView
from view.AjustesView import AjustesView
from view.DocumentosView import DocumentosView
from view.ResultadosExcelView import ResultadosExcelView
from view.UnidadesView import UnidadesView
from view.VectorCargaView import VectorCargaView
from view.MainView import MainView


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("SuralisLAB")
        self.root.geometry("1200x750")  # Más ancho que alto
        #self.root.state("zoomed")  # Modo pantalla completa en Windows
        #self.root.attributes("-fullscreen", True)  # Alternativa para otros sistemas

        self.root.minsize(600, 375)  # Ancho mínimo de 1200 y alto mínimo de 750

        self.root.iconbitmap(get_path_images("Icono.ico"))

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
            self.mostrar_rangos_view,    # Primer callback
            self.mostrar_unidades_view,  # Segundo callback
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

    def registrar_vista(self, view_name, view_class, model_class, controller_class, *callbacks):
        """Registrar una vista, su modelo y controlador."""
        if view_name not in self.views:
            # Crear la vista con los callbacks recibidos
            self.views[view_name] = view_class(self.root, *callbacks)
            
            # Crear el modelo y controlador
            model = model_class()
            controller = controller_class(model, self.views[view_name], self.mostrar_main_view)
            
            # Vincular el controlador a la vista
            self.views[view_name].set_controller(controller)





    def mostrar_vector_carga_view(self):
        """Mostrar la vista de Vector de Carga."""
        self.limpiar_main_frame()
        self.registrar_vista("vector_carga_view", VectorCargaView, VectorCargaModel, VectorCargaController, self.mostrar_main_view)
        self.show_view("vector_carga_view")

    def mostrar_resultados_excel_view(self):
        """Mostrar la vista de Resultados Excel."""
        self.limpiar_main_frame()
        self.registrar_vista("resultados_excel_view", ResultadosExcelView, ResultadosExcelModel, ResultadosExcelController, self.mostrar_main_view)
        self.show_view("resultados_excel_view")

    def mostrar_documentos_view(self):
        """Mostrar la vista de Documentos."""
        self.limpiar_main_frame()
        self.registrar_vista("documentos_view", DocumentosView, DocumentosModel, DocumentosController, self.mostrar_main_view)
        self.show_view("documentos_view")

    def mostrar_ajustes_view(self):
        """Mostrar la vista de Ajustes."""
        self.limpiar_main_frame()
        self.registrar_vista(
            "ajustes_view",
            AjustesView,
            AjustesModel,
            AjustesController,
            self.mostrar_rangos_view,    # Primer callback
            self.mostrar_unidades_view,  # Segundo callback
            self.mostrar_directorios_view,
            self.mostrar_main_view     
        )
        self.show_view("ajustes_view")


    def mostrar_rangos_view(self):
        self.limpiar_main_frame()
        self.registrar_vista(
            "rangos_view",
            RangosView,
            RangosModel,
            RangosController,
            self.mostrar_ajustes_view)
        self.show_view("rangos_view")


    def mostrar_unidades_view(self):
        """Mostrar la vista de Unidades."""
        self.limpiar_main_frame()
        self.registrar_vista(
            "unidades_view",
            UnidadesView,
            UnidadesModel,
            UnidadesController,
            self.mostrar_ajustes_view  # Callback para volver a ajustes
        )
        self.show_view("unidades_view")

    def mostrar_directorios_view(self):
        """Mostrar la vista de Unidades."""
        self.limpiar_main_frame()
        self.registrar_vista(
            "directorios_view",
            DirectoriosView,
            DirectoriosModel,
            DirectoriosController,
            self.mostrar_ajustes_view  # Callback para volver a ajustes
        )
        self.show_view("directorios_view")


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