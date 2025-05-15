import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import Graph, Node, CreateGraph_1, CreateGraph_2, LoadGraphFromFile
from path import Path
from network import FindShortestPath
from airSpace import AirSpace  # Asegúrate de tener airSpace.py con la clase AirSpace
import os

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.graph = Graph()
        self.selected_node = None

        self.mode = None  # Modo actual de interacción
        self.temp_data = {}  # Datos temporales según el modo

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.btn_example1 = tk.Button(self.frame, text="Load Example 1", command=self.load_example1)
        self.btn_example1.pack(pady=2)

        self.btn_example2 = tk.Button(self.frame, text="Load Example 2", command=self.load_example2)
        self.btn_example2.pack(pady=2)

        self.btn_load_file = tk.Button(self.frame, text="Load From File", command=self.load_from_file)
        self.btn_load_file.pack(pady=2)

        # Nuevo botón para cargar airspace desde diálogo de archivo
        self.btn_load_airspace = tk.Button(self.frame, text="Load Airspace From File", command=self.load_airspace_from_file)
        self.btn_load_airspace.pack(pady=2)

        self.btn_select_node = tk.Button(self.frame, text="Select Node", command=self.select_node)
        self.btn_select_node.pack(pady=2)

        self.btn_add_node = tk.Button(self.frame, text="Add Node", command=self.prepare_add_node)
        self.btn_add_node.pack(pady=2)

        self.btn_add_segment = tk.Button(self.frame, text="Add Segment", command=self.prepare_add_segment)
        self.btn_add_segment.pack(pady=2)

        self.btn_delete_node = tk.Button(self.frame, text="Delete Node", command=self.delete_node)
        self.btn_delete_node.pack(pady=2)

        self.btn_new_graph = tk.Button(self.frame, text="New Graph", command=self.new_graph)
        self.btn_new_graph.pack(pady=2)

        self.btn_save = tk.Button(self.frame, text="Save Graph", command=self.save_graph)
        self.btn_save.pack(pady=2)

        self.btn_reachability = tk.Button(self.frame, text="Show Reachability", command=self.show_reachability)
        self.btn_reachability.pack(pady=2)

        self.btn_shortest_path = tk.Button(self.frame, text="Shortest Path", command=self.shortest_path)
        self.btn_shortest_path.pack(pady=2)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

    def draw_graph(self, highlight_node=None, path=None, only_path=False):
        self.ax.clear()

        if path and only_path:
            # Mostrar solo los segmentos del camino
            for i in range(len(path.nodes) - 1):
                n1, n2 = path.nodes[i], path.nodes[i + 1]
                self.ax.plot([n1.x, n2.x], [n1.y, n2.y], color='orange', linewidth=2)
        else:
            # Mostrar todos los segmentos
            for segment in self.graph.segments:
                x1, y1 = segment.origin.x, segment.origin.y
                x2, y2 = segment.destination.x, segment.destination.y
                self.ax.plot([x1, x2], [y1, y2], color='black')

                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                dx = x2 - x1
                dy = y2 - y1
                fraction = 0.15
                start_x = mid_x - dx * fraction
                start_y = mid_y - dy * fraction
                end_x = mid_x + dx * fraction
                end_y = mid_y + dy * fraction

                self.ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                                 arrowprops=dict(arrowstyle='->', color='black', linewidth=1.5))

        # Mostrar todos los nodos
        for node in self.graph.nodes:
            color = 'red'
            if highlight_node == node:
                color = 'green'
            elif highlight_node and node in highlight_node.neighbors:
                color = 'blue'
            self.ax.scatter(node.x, node.y, color=color, s=100)
            self.ax.text(node.x, node.y, node.name, fontsize=10, ha='right')

        self.ax.set_title("Graph Viewer")
        self.ax.set_xlim(self.ax.get_xlim())  # mantener zoom actual
        self.ax.set_ylim(self.ax.get_ylim())
        self.canvas.draw()

    def prepare_add_node(self):
        name = simpledialog.askstring("Add Node", "Enter node name:")
        if name:
            self.mode = "add_node"
            self.temp_data = {"name": name}
            messagebox.showinfo("Add Node", "Click on the canvas to place the node.")

    def prepare_add_segment(self):
        name = simpledialog.askstring("Add Segment", "Enter segment name:")
        if name:
            self.mode = "add_segment"
            self.temp_data = {"name": name, "nodes": []}
            messagebox.showinfo("Add Segment", "Click two nodes to create the segment (origin then destination).")

    def on_canvas_click(self, event):
        if not event.inaxes:
            return

        if self.mode == "add_node":
            name = self.temp_data["name"]
            x, y = event.xdata, event.ydata
            self.graph.AddNode(Node(name, x, y))
            self.mode = None
            self.temp_data = {}
            self.draw_graph()

        elif self.mode == "add_segment":
            clicked_node = self.graph.GetClosest(event.xdata, event.ydata)
            self.temp_data["nodes"].append(clicked_node)
            if len(self.temp_data["nodes"]) == 2:
                name = self.temp_data["name"]
                origin = self.temp_data["nodes"][0].name
                destination = self.temp_data["nodes"][1].name
                if self.graph.AddSegment(name, origin, destination):
                    self.draw_graph()
                else:
                    messagebox.showerror("Error", "Failed to add segment.")
                self.mode = None
                self.temp_data = {}

        else:
            closest = self.graph.GetClosest(event.xdata, event.ydata)
            self.draw_graph(highlight_node=closest)

    def load_example1(self):
        self.graph = CreateGraph_1()
        self.draw_graph()

    def load_example2(self):
        self.graph = CreateGraph_2()
        self.draw_graph()

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.graph = LoadGraphFromFile(path)
            self.draw_graph()

    def load_airspace_from_file(self):
        path_nav = filedialog.askopenfilename(
            title="Select navigation points file (_nav.txt)",
            filetypes=[("Nav files", "*_nav.txt")]
        )
        if not path_nav:
            return  # Cancelled dialog

        base_dir = os.path.dirname(path_nav)
        base_name = os.path.basename(path_nav)
        if not base_name.endswith("_nav.txt"):
            messagebox.showerror("Error", "El archivo seleccionado no es un archivo '_nav.txt'")
            return
        prefix = base_name[:-8]  # Remove '_nav.txt'

        path_seg = os.path.join(base_dir, f"{prefix}_seg.txt")
        path_aer = os.path.join(base_dir, f"{prefix}_aer.txt")

        airspace = AirSpace()
        try:
            airspace.load_navpoints(path_nav)
            airspace.load_segments(path_seg)
            airspace.load_airports(path_aer)
        except Exception as e:
            messagebox.showerror("Error loading airspace", str(e))
            return

        self.graph = Graph()
        for np in airspace.nav_points.values():
            node = Node(np.name, np.longitude, np.latitude)
            node.number = np.number
            self.graph.AddNode(node)
        for seg in airspace.nav_segments:
            origin_node = next((n for n in self.graph.nodes if getattr(n, 'number', None) == seg.origin_number), None)
            dest_node = next((n for n in self.graph.nodes if getattr(n, 'number', None) == seg.destination_number), None)
            if origin_node and dest_node:
                name = f"{origin_node.name}->{dest_node.name}"
                self.graph.AddSegment(name, origin_node.name, dest_node.name)

        self.draw_graph()

    def select_node(self):
        name = simpledialog.askstring("Select Node", "Enter node name:")
        if name:
            node = next((n for n in self.graph.nodes if n.name == name), None)
            if node:
                self.draw_graph(highlight_node=node)
            else:
                messagebox.showerror("Error", "Node not found")

    def delete_node(self):
        name = simpledialog.askstring("Delete Node", "Enter node name to delete:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if node:
            self.graph.nodes.remove(node)
            self.graph.segments = [s for s in self.graph.segments if s.origin != node and s.destination != node]
            self.draw_graph()
        else:
            messagebox.showerror("Error", "Node not found")

    def new_graph(self):
        self.graph = Graph()
        self.draw_graph()

    def save_graph(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w') as file:
                for node in self.graph.nodes:
                    file.write(f"{node.name},{node.x},{node.y}\n")
                for segment in self.graph.segments:
                    file.write(f"{segment.name},{segment.origin.name},{segment.destination.name}\n")
            messagebox.showinfo("Saved", "Graph saved successfully!")

    def show_reachability(self):
        name = simpledialog.askstring("Reachability", "Enter node name:")
        node = next((n for n in self.graph.nodes if n.name == name), None)
        if not node:
            messagebox.showerror("Error", "Node not found")
            return

        # Filtrar los segmentos salientes desde el nodo seleccionado
        reachable_segments = [
            s for s in self.graph.segments if s.origin == node
        ]

        self.ax.clear()

        # Dibujar solo los segmentos salientes
        for segment in reachable_segments:
            x1, y1 = segment.origin.x, segment.origin.y
            x2, y2 = segment.destination.x, segment.destination.y
            self.ax.plot([x1, x2], [y1, y2], color='blue', linewidth=2)

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            dx = x2 - x1
            dy = y2 - y1
            fraction = 0.15
            start_x = mid_x - dx * fraction
            start_y = mid_y - dy * fraction
            end_x = mid_x + dx * fraction
            end_y = mid_y + dy * fraction

            self.ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                             arrowprops=dict(arrowstyle='->', color='blue', linewidth=1.5))

        # Dibujar todos los nodos
        for n in self.graph.nodes:
            color = 'green' if n == node else 'blue' if n in node.neighbors else 'red'
            self.ax.scatter(n.x, n.y, color=color, s=100)
            self.ax.text(n.x, n.y, n.name, fontsize=10, ha='right')

        self.ax.set_title(f"Reachability from {node.name}")
        self.ax.set_xlim(self.ax.get_xlim())  # mantener zoom
        self.ax.set_ylim(self.ax.get_ylim())
        self.canvas.draw()

    def shortest_path(self):
        start_name = simpledialog.askstring("Shortest Path", "Enter origin node:")
        end_name = simpledialog.askstring("Shortest Path", "Enter destination node:")
        origin = next((n for n in self.graph.nodes if n.name == start_name), None)
        dest = next((n for n in self.graph.nodes if n.name == end_name), None)
        if origin and dest:
            path = FindShortestPath(self.graph, origin, dest)
            if path:
                self.draw_graph(path=path, only_path=True)  # 🔥 solo muestra el camino más corto
            else:
                messagebox.showinfo("Result", "No path found")
        else:
            messagebox.showerror("Error", "Invalid nodes")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()



