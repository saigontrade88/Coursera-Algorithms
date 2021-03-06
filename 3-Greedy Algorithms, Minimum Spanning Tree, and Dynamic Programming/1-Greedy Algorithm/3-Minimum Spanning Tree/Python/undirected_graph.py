#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adjacency list representation of undirected graph.

Note that parallel edges and self-loops are not allowed.
"""

__author__ = 'Ziang Lu'

import heapq
import random
import sys
from functools import total_ordering
from typing import Dict, List

from graph_basics import AbstractGraph, AbstractVertex
from union_find import UnionFind, UnionFindObj


class IllegalArgumentError(ValueError):
    pass


@total_ordering
class Vertex(AbstractVertex, UnionFindObj):
    __slots__ = [
        '_edges', '_neighbors', '_min_cost_incident_edge', '_min_incident_cost'
    ]

    DEFAULT_MIN_INCIDENT_COST = sys.maxsize

    def __init__(self, vtx_id: int):
        """
        Constructor with parameter.
        :param vtx_id: int
        """
        AbstractVertex.__init__(self, vtx_id)
        UnionFindObj.__init__(self)
        self._edges = []
        self._neighbors = set()
        self._min_cost_incident_edge = None
        self._min_incident_cost = Vertex.DEFAULT_MIN_INCIDENT_COST

    def get_edge_with_neighbor(self, neighbor: AbstractVertex):
        """
        Returns the first edge with the given neighbor.
        :param neighbor: AbstractVertex
        :return: UndirectedEdge
        """
        # Check whether the input neighbor is None
        if not neighbor:
            raise IllegalArgumentError('The input neighbor should not be None.')

        for edge in self._edges:
            if (edge.end1 is self and edge.end2 is neighbor) or \
                    (edge.end1 is neighbor and edge.end2 is self):
                return edge
        # Not found
        return None

    @property
    def edges(self) -> list:
        """
        Accessor of edges.
        :return: list[UndirectedEdge]
        """
        return self._edges

    @property
    def min_cost_incident_edge(self):
        """
        Accessor of min_cost_incident_edge.
        :return: UndirectedEdge
        """
        return self._min_cost_incident_edge

    @property
    def min_incident_cost(self) -> float:
        """
        Accessor of min_incident_edge.
        :return: float
        """
        return self._min_incident_cost

    @property
    def obj_name(self) -> str:
        return str(self._vtx_id)

    def add_edge(self, new_edge) -> None:
        """
        Adds the given edge to this vertex.
        :param new_edge: UndirectedEdge
        :return: None
        """
        # Check whether the input edge is None
        if not new_edge:
            raise IllegalArgumentError('The edge to add should not be None.')
        # Check whether the input edge involves this vertex
        if new_edge.end1 is not self and new_edge.end2 is not self:
            raise IllegalArgumentError(
                'The edge to add should involve this vertex.'
            )
        # Find the neighbor associated with the input edge
        if new_edge.end1 is self:  # endpoint2 is the neighbor.
            neighbor = new_edge.end2
        else:  # endpoint1 is the neighbor.
            neighbor = new_edge.end1
        # Check whether the input edge already exists
        if neighbor.vtx_id in self._neighbors:
            raise IllegalArgumentError('The edge to add already exists.')

        self._edges.append(new_edge)
        self._neighbors.add(neighbor.vtx_id)

    def remove_edge(self, edge_to_remove) -> None:
        """
        Removes the given edge from this vertex.
        :param edge_to_remove: UndirectedEdge
        :return: None
        """
        # Check whether the input edge is None
        if not edge_to_remove:
            raise IllegalArgumentError('The edge to remove should not be None.')
        # Check whether the input edge involves this vertex
        if edge_to_remove.end1 is not self and edge_to_remove.end2 is not self:
            raise IllegalArgumentError(
                'The edge to remove should involve this vertex.'
            )
        # Find the neighbor associated with the input edge
        if edge_to_remove.end1 is self:  # endpoint2 is the neighbor.
            neighbor = edge_to_remove.end2
        else:  # endpoint1 is the neighbor.
            neighbor = edge_to_remove.end1
        # Check whether the input edge exists
        if neighbor.vtx_id not in self._neighbors:
            raise IllegalArgumentError("The edge to remove doesn't exist.")

        self._edges.remove(edge_to_remove)
        self._neighbors.remove(neighbor.vtx_id)

    @min_cost_incident_edge.setter
    def min_cost_incident_edge(self, min_cost_incident_edge) -> None:
        """
        Mutator of min_cost_incident_edge
        :param min_cost_incident_edge: UndirectedEdge
        :return: None
        """
        self._min_cost_incident_edge = min_cost_incident_edge

    @min_incident_cost.setter
    def min_incident_cost(self, min_incident_cost: float) -> None:
        """
        Mutator of min_incident_cost.
        :param min_incident_cost: float
        :return: None
        """
        self._min_incident_cost = min_incident_cost

    def __lt__(self, other):
        return self._min_incident_cost < other.min_incident_cost

    def __repr__(self):
        return f'Vertex #{self._vtx_id}, Its neighbors: {self._neighbors}'


@total_ordering
class UndirectedEdge(object):
    __slots__ = ['_end1', '_end2', '_cost']

    def __init__(self, end1: Vertex, end2: Vertex, cost: float):
        """
        Constructor with parameter.
        :param end1: Vertex
        :param end2: Vertex
        :param cost: float
        """
        self._end1 = end1
        self._end2 = end2
        self._cost = cost

    @property
    def end1(self) -> Vertex:
        """
        Accessor of end1.
        :return: Vertex
        """
        return self._end1

    @property
    def end2(self) -> Vertex:
        """
        Accessor of end2.
        :return: Vertex
        """
        return self._end2

    @property
    def cost(self) -> float:
        """
        Accessor of cost.
        :return: float
        """
        return self._cost

    @end1.setter
    def end1(self, end1: Vertex) -> None:
        """
        Mutator of end1.
        :param end1: Vertex
        :return: None
        """
        self._end1 = end1

    @end2.setter
    def end2(self, end2: Vertex) -> None:
        """
        Mutator of end2.
        :param end2: Vertex
        :return: None
        """
        self._end2 = end2

    def __lt__(self, other):
        return self._cost < other.cost

    def __repr__(self):
        return f'Edge between Vertex #{self._end1.vtx_id} and Vertex #{self._end2.vtx_id}'


class UndirectedGraph(AbstractGraph):
    __slots__ = []

    def __init__(self):
        """
        Default constructor.
        """
        super().__init__()

    def add_vtx(self, new_vtx_id):
        # Check whether the input vertex is repeated
        if self._find_vtx(new_vtx_id):
            raise IllegalArgumentError('The input vertex is repeated.')

        new_vtx = Vertex(new_vtx_id)
        self._vtx_list.append(new_vtx)

    def _remove_vtx(self, vtx_to_remove):
        # Remove all the edges associated with the vertex to remove
        edges_to_remove = vtx_to_remove.edges
        while len(edges_to_remove):
            self._remove_edge(edge_to_remove=edges_to_remove[0])
        # Remove the vertex
        self._vtx_list.remove(vtx_to_remove)

    def add_edge(self, end1_id, end2_id, cost):
        # Check whether the input endpoints both exist
        end1, end2 = self._find_vtx(end1_id), self._find_vtx(end2_id)
        if not end1 or not end2:
            raise IllegalArgumentError("The endpoints don't both exist.")
        # Check whether the input endpoints are the same (self-loop)
        if end1_id == end2_id:
            raise IllegalArgumentError(
                'The endpoints are the same (self-loop).'
            )

        new_edge = UndirectedEdge(end1, end2, cost)
        self._add_edge(new_edge=new_edge)

    def _add_edge(self, new_edge):
        end1, end2 = new_edge.end1, new_edge.end2
        end1.add_edge(new_edge)
        end2.add_edge(new_edge)
        self._edge_list.append(new_edge)

    def remove_edge(self, end1_id, end2_id):
        # Check whether the input endpoints both exist
        end1, end2 = self._find_vtx(end1_id), self._find_vtx(vtx_id=end2_id)
        if not end1 or not end2:
            raise IllegalArgumentError("The endpoints don't both exist.")

        # Check whether the edge to remove exists
        edge_to_remove = end1.get_edge_with_neighbor(end2)
        if not edge_to_remove:
            raise IllegalArgumentError("The edge to remove doesn't exist.")

        self._remove_edge(edge_to_remove=edge_to_remove)

    def _remove_edge(self, edge_to_remove):
        end1, end2 = edge_to_remove.end1, edge_to_remove.end2
        end1.remove_edge(edge_to_remove)
        end2.remove_edge(edge_to_remove)
        self._edge_list.remove(edge_to_remove)

    def prim_mst_straightforward(self) -> float:
        """
        Finds the minimum spanning tree (MST) in this graph using
        straightforward Prim's MST Algorithm.
        :return: float
        """
        # 1. Arbitrarily choose a source vertex s
        src_vtx = self._vtx_list[random.randint(0, len(self._vtx_list) - 1)]

        # 2. Initialize X = {s}, which contains the vertices we've spanned so
        #    far, and T = {empty}, which current spanning tree
        spanned = set()
        spanned.add(src_vtx.vtx_id)
        curr_spanning_tree = []

        # 3. Create a heap containing all the edge with one endpoint in X and
        #    the other in (V-X)
        crossing_edges = []
        for edge in src_vtx.edges:
            heapq.heappush(crossing_edges, edge)

        # 4. While X != V
        while len(spanned) < len(self._vtx_list):
            # Among all crossing edges e = (v, w) with v in X and w in (V-X),
            # pick up the cheapest crossing edge
            cheapest_crossing_edge = heapq.heappop(crossing_edges)
            # Add e to T
            curr_spanning_tree.append(cheapest_crossing_edge)
            # Add w to X
            if cheapest_crossing_edge.end1.vtx_id in spanned:  # endpoint2 is
                #  the w.
                w = cheapest_crossing_edge.end2
            else:  # endpoint1 is the w.
                w = cheapest_crossing_edge.end1
            spanned.add(w.vtx_id)

            # Update the crossing edges with w's edges if necessary
            for w_edge in w.edges:
                # Find the neighbor
                if w_edge.end1.vtx_id == w.vtx_id:  # endpoint2 is the neighbor.
                    neighbor = w_edge.end2
                else:  # endpoint1 is the neighbor.
                    neighbor = w_edge.end1
                # Check whether the neighbor of w has been spanned
                if neighbor.vtx_id not in spanned:
                    heapq.heappush(crossing_edges, w_edge)

        return sum(map(lambda x: x.cost, curr_spanning_tree))
        # Overall running time complexity: O((m + n)log m)
        # Since usually m >= n, it could be simplified to O(mlog m).

    def kruskal_mst_straightforward(self) -> float:
        """
        Finds the minimum spanning tree (MST) using straightforward Kruskal's
        MST Algorithm.
        :return: float
        """
        # 1. Sort the edges in order of increasing cost   [O(mlog m)]
        edges = sorted(self._edge_list)

        # 2. Initialize T = {empty}, which is the current spanning tree
        curr_spanning_tree = []

        # 3. For each edge e = (v, w) in the sorted edge list   [O(mn)]
        for edge in edges:
            # Check whether adding e to T causes cycles in T
            # This is equivalent to checking whether there exists a v-w path in
            # T before adding e.
            if not self._dfs_and_check_path(curr_spanning_tree, edge.end1,
                                            edge.end2):
                curr_spanning_tree.append(edge)

        return sum(map(lambda x: x.cost, curr_spanning_tree))
        # Overall running time complexity: O(mn)

    def _dfs_and_check_path(self, spanning_tree: List[UndirectedEdge],
                            v: Vertex, w: Vertex) -> bool:
        """
        Private helper function to check whether there exists a v-w path in the
        given spanning tree.
        :param spanning_tree: list[UndirectedEdge]
        :param v: Vertex
        :param w: Vertex
        :return: bool
        """
        # Create a map between vertices and its neighbors
        connections = self._construct_connections(edges=spanning_tree)
        if v.vtx_id not in connections or w.vtx_id not in connections:
            return False
        return self._dfs_and_check_path_helper(connections, curr=v, target=w)
        # Running time complexity: O(n)

    def _construct_connections(
        self, edges: List[UndirectedEdge]
    ) -> Dict[int, List[Vertex]]:
        """
        Helper function to construct the connection map from the given edges.
        :param edges: list[UndirectedEdge]
        :return: dict{int: list[Vertex]}
        """
        connections = {}
        for edge in edges:
            self._add_neighbor(connections, v=edge.end1, neighbor=edge.end2)
            self._add_neighbor(connections, v=edge.end2, neighbor=edge.end1)
        return connections
        # Running time complexity: O(n)

    def _add_neighbor(self, connections: Dict[int, List[Vertex]], v: Vertex,
                      neighbor: Vertex) -> None:
        """
        Helper function to add the given neighbor of the given vertex to the
        given connection map.
        :param connections: dict[int: list[Vertex]]
        :param v: Vertex
        :param neighbor: Vertex
        :return: None
        """
        neighbors = connections.get(v.vtx_id, [])
        neighbors.append(neighbor)
        connections[v.vtx_id] = neighbors
        # Running time complexity: O(1)

    def _dfs_and_check_path_helper(self, connections: Dict[int, List[Vertex]],
                                   curr: Vertex, target: Vertex) -> bool:
        """
        Helper function to check whether there exists a curr-target path in the
        given connection map recursively.
        :param connections: dict[int: list[Vertex]]
        :param curr: Vertex
        :param target: Vertex
        :return: bool
        """
        curr.set_as_explored()
        for neighbor in connections[curr.vtx_id]:
            if neighbor.vtx_id == target.vtx_id:
                return True
            if not neighbor.explored:
                if self._dfs_and_check_path_helper(connections, curr=neighbor,
                                                   target=target):
                    return True
        return False
        # Running time complexity: O(n)

    def kruskal_mst_improved(self) -> float:
        """
        Finds the minimum spanning tree (MST) using improved Kruskal's MST
        Algorithm.
        :return: float
        """
        # 1. Sort the edges in order of increasing cost   [O(mlog m)]
        edges = sorted(self._edge_list)

        # 2. Initialize T = {empty}, which is the current spanning tree
        curr_spanning_tree = []

        # 3. Create a Union Find of vertices
        # object -> vertex
        # group -> connected component w.r.t. the edges in T
        # Each of the vertex is on its own isolated connected component.
        union_find = UnionFind(self._vtx_list)

        # 4. For each edge e = (v, w) in the sorted edge list   [O(nlog n)]
        for edge in edges:
            # Check whether adding e to T causes cycles in T
            # This is equivalent to checking whether there exists a v-w path in
            # T before adding e.
            # This is equivalent to checking whether the leaders of v and w in
            # the UnionFind are the same.
            if edge.end1.leader is not edge.end2.leader:
                curr_spanning_tree.append(edge)
                # Fuse the two connected components to a single one
                group_name_v, group_name_w = edge.end1.leader.obj_name, \
                    edge.end2.leader.obj_name
                union_find.union(group_name_v, group_name_w)
        # Originally we would think it involves O(mn) leader updates; however,
        # we can change to a "vertex-centric" view:
        # Consider the number of leader updates for a single vertex:
        # Every time the leader of this vertex gets updated, the size of its
        # connected components at least doubles, so suppose it experiences x
        # leader updates in total, we have
        #     2^x <= n
        #     x <= log2 n
        # Thus, each vertex experiences O(log n) leader updates, leading to a
        # O(nlog n) leader updates in total.

        return sum(map(lambda x: x.cost, curr_spanning_tree))
        # Overall running time complexity: O(mlog m)

    def clustering_with_max_spacing(self, k: int) -> float:
        """
        Clusters the graph into the given number of cluster using maximum
        spacing as the objective function, which is to maximize the minimum
        distance between a pair of separated points, using Single-link
        Algorithm, which is exactly the same as Kruskal's MST Algorithm.
        :param k: int
        :return: float
        """
        # Check whether the input k is greater than 1
        if k <= 1:
            raise IllegalArgumentError(
                'The number of clusters must be greater than 1.'
            )

        edges = sorted(self._edge_list)

        # Initially, each point is in a separate cluster.
        union_find = UnionFind(self._vtx_list)

        stopped = False
        for edge in edges:
            if edge.end1.leader is not edge.end2.leader:
                if stopped:
                    return edge.cost
                # Let p, q = closest pair of separated points, which determines
                # the current spacing
                # Merge the clusters containing p and q into a single cluster
                group_name_p, group_name_q = edge.end1.leader.obj_name, \
                    edge.end2.leader.obj_name
                union_find.union(group_name_p, group_name_q)
                if union_find.num_of_groups() == k:  # Repeat until only k
                    # clusters
                    # The maximum spacing is simply the cost of the next
                    # cheapest crossing edge among different connected
                    # components.
                    stopped = True
        return 0.0  # Codes should never reach here.
        # Overall running time complexity: O(mlog m)
