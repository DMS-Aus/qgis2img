import os

from collections import OrderedDict
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QDir, QFileInfo

from qgis.gui import QgsMapCanvasLayer
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsMapLayerRegistry, QgsMapSettings, QgsProject


def layer_by_id(layerid):
    return QgsMapLayerRegistry.instance().mapLayers()[layerid]


def iternodes(nodes):
    for index in xrange(nodes.length()):
        yield nodes.at(index).toElement()


class Project(object):
    def __init__(self, xmldoc):
        self.doc = xmldoc
        self._maplayers = None

    @classmethod
    def fromFile(cls, filename):
        QDir.setCurrent(os.path.dirname(filename))
        fileinfo = QFileInfo(filename)
        QgsProject.instance().read(fileinfo)
        xml = open(filename).read()
        doc = QDomDocument()
        doc.setContent(xml)
        return cls(doc)

    def _createLayer(self, node):
        type = node.attribute('type')
        if type == "vector":
            layer = QgsVectorLayer()
        elif type == "raster":
            layer = QgsRasterLayer()
        else:
            return None
        layer.readLayerXML(node)
        return layer

    def _getLayer(self, node):
        filelist = node.elementsByTagName("legendlayerfile")
        layerfile = filelist.at(0).toElement()
        layerid = layerfile.attribute('layerid')
        visible = int(layerfile.attribute('visible'))
        return layerid, bool(visible)

    def maplayers(self):
        return QgsMapLayerRegistry.instance().mapLayers().values()

    def legendlayers(self):
        legendnodes = self.doc.elementsByTagName("legendlayer")
        layers = OrderedDict()
        for elm in iternodes(legendnodes):
            layerid, visible = self._getLayer(elm)
            layers[layerid] = visible
        return layers

    def settings(self):
        """
        Return the settings that have been set for the map canvas.
        @return: A QgsMapSettings instance with the settings read from the project.
        """
        canvasnodes = self.doc.elementsByTagName("mapcanvas")
        node = canvasnodes.at(0).toElement()
        settings = QgsMapSettings()
        settings.readXML(node)
        return settings

    def visiblelayers(self):
        # Filter out only the ones we can see.
        visible = [layerid for layerid, visible in self.legendlayers().iteritems() if visible]
        return [layer_by_id(layerid) for layerid in visible]
