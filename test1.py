
import os
from manim import *

# Set the ffmpeg path programmatically (if necessary)
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin"

class BFSVisualization(Scene):
    def construct(self):
        # Create the vertices of the graph
        vertices = {
            "A": np.array([-3, 2, 0]),
            "B": np.array([-1, 2, 0]),
            "C": np.array([1, 2, 0]),
            "D": np.array([-3, 0, 0]),
            "E": np.array([-1, 0, 0]),
            "F": np.array([1, 0, 0]),
            "G": np.array([0, -2, 0]),
        }

        # Create the edges of the graph
        edges = [
            ("A", "B"),
            ("A", "D"),
            ("B", "C"),
            ("B", "E"),
            ("D", "E"),
            ("C", "F"),
            ("E", "G"),
            ("F", "G"),
        ]

        # Create vertex circles
        vertex_mobjects = {}
        for vertex, pos in vertices.items():
            circle = Circle(radius=0.5, color=WHITE).move_to(pos)
            label = Text(vertex).move_to(pos)
            vertex_mobjects[vertex] = VGroup(circle, label)

        # Add vertices to the scene
        for vertex_mobject in vertex_mobjects.values():
            self.play(FadeIn(vertex_mobject))

        # Create and animate edges
        edge_mobjects = []
        for v1, v2 in edges:
            edge = Line(vertex_mobjects[v1].get_center(), vertex_mobjects[v2].get_center(), color=WHITE)
            edge_mobjects.append(edge)

        for edge in edge_mobjects:
            self.play(Create(edge))

        # BFS algorithm visualization
        def bfs(start_vertex):
            visited = set()
            queue = [start_vertex]
            visited.add(start_vertex)

            # Animating the search
            while queue:
                current_vertex = queue.pop(0)
                # Highlight the current vertex being explored
                self.play(vertex_mobjects[current_vertex][0].animate.set_fill(YELLOW, opacity=0.5))

                # Explore all adjacent vertices
                for v1, v2 in edges:
                    if v1 == current_vertex and v2 not in visited:
                        queue.append(v2)
                        visited.add(v2)
                        # Highlight edge and vertex
                        self.play(
                            vertex_mobjects[v2][0].animate.set_fill(BLUE, opacity=0.5),
                            vertex_mobjects[current_vertex][0].animate.set_fill(GREEN, opacity=0.5),
                        )
                    elif v2 == current_vertex and v1 not in visited:
                        queue.append(v1)
                        visited.add(v1)
                        # Highlight edge and vertex
                        self.play(
                            vertex_mobjects[v1][0].animate.set_fill(BLUE, opacity=0.5),
                            vertex_mobjects[current_vertex][0].animate.set_fill(GREEN, opacity=0.5),
                        )

        # Start BFS from node A
        bfs("A")

        # Keep the final frame visible
        self.wait(3)
