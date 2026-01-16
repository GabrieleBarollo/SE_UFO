import flet as ft
from geopy import distance


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        lista_anni = self._model.get_years()
        lista_forme = self._model.get_shapes()
        for a in lista_anni:
            self._view.dd_year.options.append(ft.dropdown.Option(a))
        for f in lista_forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(f))
        self._view.update()

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        anno = int(self._view.dd_year.value)
        shape = self._view.dd_shape.value
        info = self._model.generate_graph(anno, shape)
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"{self._model.G}"))
        for i in info:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {i[0].id}, somma pesi su archi = {i[1]}"))
        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        percorso= self._model.ricercaPercorso()
        self._view.lista_visualizzazione_2.clean()
        for i in range(0, len(percorso)-1):
            distanza = distance.geodesic((percorso[i].lat, percorso[i].lng), (percorso[i+1].lat, percorso[i+1].lng)).km
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{percorso[i].id} --> {percorso[i+1].id}: peso = {self._model.G[percorso[i]][percorso[i+1]]["peso"]} | distanza = {distanza}"))
        self._view.update()