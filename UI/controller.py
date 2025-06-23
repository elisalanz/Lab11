import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._selectedProduct = None

    def fillDDYear(self):
        anni = range(2015, 2019)
        for anno in anni:
            self._view._ddyear.options.append(ft.dropdown.Option(anno))
        self._view.update_page()

    def fillDDColors(self):
        colors = self._model.getAllColors()
        for color in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))
        self._view.update_page()

    def handle_graph(self, e):
        self._selectedProduct = None
        if self._view._ddyear.value is None or self._view._ddcolor.value is None:
            self._view.create_alert("Selezionare anno e colore.")
            return
        anno = self._view._ddyear.value
        colore = self._view._ddcolor.value
        nNodes, nEdges = self._model.buildGraph(anno, colore)
        self.fillDDProduct()
        self._view.btn_search.disabled = False
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {nNodes} Numero di archi: {nEdges}"))
        archi_top3, nodi_ripetuti = self._model.getInfoGrafo()
        for arco in archi_top3:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {arco[0].Product_number} a {arco[1].Product_number}, peso={arco[2]["weight"]}"))
        if len(nodi_ripetuti) > 0:
            self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {nodi_ripetuti}"))
        else:
            self._view.txtOut.controls.append(ft.Text("(non ci sono nodi ripetuti)"))
        self._view.update_page()



    def fillDDProduct(self):
        self._view._ddnode.options.clear()
        prodotti = self._model.getAllProductsInGraph()
        for prodotto in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(data = prodotto, text = prodotto.Product_number, on_click = self._readDDProducts))
        self._view.update_page()

    def _readDDProducts(self, e):
        if e.control.data is None:
            self._selectedProduct = None
        else:
            self._selectedProduct = e.control.data

    def handle_search(self, e):
        source = self._selectedProduct
        if source is None:
            self._view.create_alert("Selezionare un prodotto dal menu.")
            return
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {self._model.getBestScore(source)}"))
        self._view.update_page()
