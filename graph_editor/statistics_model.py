"""Statistics Model — exposes vertex/edge counts and min/max to QML.

Read-only model, no user interactions.
"""
from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal

from ge.context import Context
from gei.graph import attachments
from gei import containers, graph


class StatisticsModel(QObject):

    changed = Signal()
    enabledChanged = Signal()

    def __init__(self, notifier, parent=None):
        super().__init__(parent)
        self._context = Context.instance()
        self._vertices_text = "-"
        self._edges_text = "-"
        self._min_max_text = "-"
        self._enabled = False

        notifier.database_did_open.connect(self._on_database_did_open)
        notifier.database_did_close.connect(self._on_database_did_close)
        notifier.state_did_change.connect(self._configure)

    # QML Properties
    def _get_vertices_text(self) -> str:
        return self._vertices_text

    verticesText = Property(str, _get_vertices_text, notify=changed)

    def _get_edges_text(self) -> str:
        return self._edges_text

    edgesText = Property(str, _get_edges_text, notify=changed)

    def _get_min_max_text(self) -> str:
        return self._min_max_text

    minMaxText = Property(str, _get_min_max_text, notify=changed)

    def _get_enabled(self) -> bool:
        return self._enabled

    enabled = Property(bool, _get_enabled, notify=enabledChanged)

    def _on_database_did_open(self):
        self._enabled = True
        self.enabledChanged.emit()

    def _on_database_did_close(self):
        self._vertices_text = "-"
        self._edges_text = "-"
        self._min_max_text = "-"
        self.changed.emit()
        self._enabled = False
        self.enabledChanged.emit()

    def _configure(self):
        attachment_getting = self._context.store.attachment_getting()
        graph_key = self._context.graph_key

        vertex_keys = containers.Set_of_Graph_VertexKey()
        edge_keys = containers.Set_of_Graph_EdgeKey()
        if opt := attachments.Graph.topology.get(attachment_getting, graph_key):
            topology = opt
            vertex_keys = topology.vertex_keys
            edge_keys = topology.edge_keys

        selected_vertex_keys = containers.Set_of_Graph_VertexKey()
        selected_edge_keys = containers.Set_of_Graph_EdgeKey()
        if opt := attachments.Graph.selection.get(attachment_getting, graph_key):
            selection = opt
            selected_vertex_keys = selection.vertex_keys
            selected_edge_keys = selection.edge_keys

        self._vertices_text = f"{len(selected_vertex_keys):03d}/{len(vertex_keys):03d}"
        self._edges_text = f"{len(selected_edge_keys):03d}/{len(edge_keys):03d}"

        values = []
        for vertex_key in vertex_keys:
            opt = attachments.Vertex.visual_attributes.get(attachment_getting, vertex_key)
            if opt:
                values.append(opt.value)

        if values:
            self._min_max_text = f"{min(values):03d}/{max(values):03d}"
        else:
            self._min_max_text = "-"

        self.changed.emit()
