from controller.DocumentosController import DocumentosController
from controller.ResultadosExcelController import ResultadosExcelController
from controller.VectorCargaController import VectorCargaController
from model.DocumentosModel import DocumentosModel
from model.MainModel import MainModel
from model.ResultadosExcelModel import ResultadosExcelModel
from model.VectorCargaModel import VectorCargaModel
from view.DocumentosView import DocumentosView
from view.MainView import MainView
from view.ResultadosExcelView import ResultadosExcelView
from view.VectorCargaView import VectorCargaView


class MainController:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view
        self.views = {}  # Registro de vistas
        self.current_view = None  # Vista actual

    def volver_a_main_view(self):
        """Método para volver a la vista principal sin recrear la vista principal."""
        if "main_view" not in self.views:
            # Crear la vista principal solo si no existe
            self.views["main_view"] = MainView(
                self.root,
                self.mostrar_vector_carga_view,
                self.mostrar_resultados_excel_view,
                self.mostrar_documentos_view
            )

        # Mostrar la vista principal
        self.show_view("main_view")

    def mostrar_vector_carga_view(self):
        """Mostrar la vista de Vector de Carga."""
        self.limpiar_main_frame()

        # Inicializa el modelo
        model = VectorCargaModel()

        # Crea la vista si no está registrada aún
        if "vector_carga_view" not in self.views:
            # Crea la nueva vista
            self.views["vector_carga_view"] = VectorCargaView(self.root)
            
            # Crea el controlador para esta vista
            controller = VectorCargaController(self, model, self.views["vector_carga_view"])
            
            # Vincula el controlador a la vista
            self.views["vector_carga_view"].set_controller(controller)
        
        # Mostrar la vista
        self.show_view("vector_carga_view")

    def mostrar_resultados_excel_view(self):
        """Mostrar la vista de Resultados Excel."""
        self.limpiar_main_frame()

        # Inicializa el modelo
        model = ResultadosExcelModel()

        # Crea la vista si no está registrada aún
        if "resultados_excel_view" not in self.views:
            # Crea la nueva vista
            self.views["resultados_excel_view"] = ResultadosExcelView(self.root)
            
            # Crea el controlador para esta vista
            controller = ResultadosExcelController(model, self.views["resultados_excel_view"])
            
            # Vincula el controlador a la vista
            self.views["resultados_excel_view"].set_controller(controller)

        # Mostrar la vista
        self.show_view("resultados_excel_view")

    def mostrar_documentos_view(self):
        """Mostrar la vista de Documentación."""
        self.limpiar_main_frame()

        # Inicializa el modelo
        model = DocumentosModel()

        # Crea la vista si no está registrada aún
        if "documentos_view" not in self.views:
            # Crea la nueva vista
            self.views["documentos_view"] = DocumentosView(self.root)
            
            # Crea el controlador para esta vista
            controller = DocumentosController(model, self.views["documentos_view"])
            
            # Vincula el controlador a la vista
            self.views["documentos_view"].set_controller(controller)

        # Mostrar la vista
        self.show_view("documentos_view")

    def show_view(self, view_name):
        """Método para mostrar una vista específica."""
        # Si ya existe una vista actual, ocultarla
        if self.current_view:
            self.current_view.hide()

        # Obtener la vista a mostrar y mostrarla
        self.current_view = self.views[view_name]
        self.current_view.show()

    def limpiar_main_frame(self):
        """Limpiar el contenido del contenedor principal antes de mostrar una nueva vista."""
        for widget in self.root.winfo_children():
            widget.destroy()
