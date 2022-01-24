import math

import math_utils


class NodeClusters:
    class Cluster:
        def __init__(self, node):
            self.pos = math_utils.Point(math.floor(node.position().x()), math.floor(node.position().y()))
            self.nodes = [node]

        def exists(self, node):
            return math.floor(node.position().x()) == self.pos.x() and \
                   math.floor(node.position().y()) == self.pos.y()

    def __init__(self):
        self.clusters = []

    def getNodes(self, node):
        for cluster in self.clusters:
            if cluster.exists(node):
                return cluster.nodes
        return []

    def addNode(self, node):
        for cluster in self.clusters:
            if cluster.exists(node):
                cluster.nodes.append(node)
                return
        self.clusters.append(self.Cluster(node))
