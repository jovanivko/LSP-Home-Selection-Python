import numpy as np
import pandas as pd
from aggregators import Aggregator
from criteria import ElementaryCriterion
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


class AggregationTreeNode:

    def __init__(self, node_id, name, element):
        self.element = element  # can be a suitability mapping or aggregator
        self.node_id = node_id
        self.name = name
        self.children = []
        self.weights = []

    @staticmethod
    def evaluate_aggregation_tree(root, inputs):
        scores = []
        for input_data in inputs:
            scores.append(float(root.evaluate(input_data)))
        return scores

    def add_child(self, element, weight=0, name=""):
        if isinstance(element, ElementaryCriterion):
            element.id = self.node_id + f" {len(self.children)+1}"
            node = AggregationTreeNode(element.id, element.name, element)
        elif isinstance(element, Aggregator):
            node = AggregationTreeNode(self.node_id + f" {len(self.children) + 1}", name, element)
        else:
            raise TypeError("You can only add ElementaryCriterion or Aggregator types to the tree!")

        self.children.append(node)
        self.weights.append(weight)
        if isinstance(node.element, Aggregator):
            return node

    def evaluate(self, input_data):
        if isinstance(self.element, ElementaryCriterion):
            value = input_data[self.element.name] # Get the value for this criterion from the DataFrame
            if pd.isna(value):  # Check for NaN (missing value)
                return None
            return self.element.evaluate(value)
        else:
            # It's an aggregator, gather children evaluations, missingness-tolerant approach to data
            child_values = []
            updated_weights = []

            for child, weight in zip(self.children, self.weights):
                child_value = child.evaluate(input_data)
                if child_value is None:
                    # Calculate missingness tolerance
                    calculated_tolerance = 1 - 2 * weight

                    # Adjust tolerance to the 0, 0.5, or 1 levels
                    if calculated_tolerance < 0.25:
                        tolerance = 0
                    elif calculated_tolerance > 0.75:
                        tolerance = 1
                    else:
                        tolerance = 0.5

                    # Apply missingness tolerance logic
                    if tolerance == 0:
                        child_values.append(0)
                        updated_weights.append(weight)
                    elif tolerance == 0.5:
                        # Add placeholder, we'll calculate the arithmetic mean of others later
                        child_values.append(None)
                        updated_weights.append(weight)
                    else:  # tolerance == 1
                        # Skip this child and redistribute its weight among the others
                        continue
                else:
                    child_values.append(child_value)
                    updated_weights.append(weight)

            # Handle the None (0.5 tolerance) cases
            if None in child_values:
                valid_values = [v for v in child_values if v is not None]
                mean_value = np.mean(valid_values) if valid_values else 0
                child_values = [mean_value if v is None else v for v in child_values]

            # Normalize weights after redistributing for removed nodes
            weight_sum = sum(updated_weights)
            if weight_sum != 1:
                normalized_weights = [w / weight_sum for w in updated_weights]
            else:
                normalized_weights = updated_weights
            return self.element.evaluate(child_values, normalized_weights)

class TreePlotter:
    """
    Class for plotting a tree diagram with consistent node widths, proper vertical distribution,
    and parent-child connections drawn correctly.
    """

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(18, 18))  # Increased figure size for better readability
        self.ax.set_axis_off()
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    def build_level_lists(self, node, level=0, levels=None):
        """
        Traverse the tree and build a list of nodes for each level.
        """
        if levels is None:
            levels = {}

        if level not in levels:
            levels[level] = []

        # Append node to its level
        levels[level].append(node)

        # Recursively process the children
        for child in node.children:
            self.build_level_lists(child, level + 1, levels)

        return levels

    def distribute_vertically(self, nodes, total_height):
        """
        Distribute the nodes vertically for a given level.
        """
        count = len(nodes)
        spacing = total_height / count  # Even spacing for nodes at level
        return [spacing * i for i in range(count)]  # Y-coordinates for each node

    def plot_levels(self, levels, total_height):
        """
        Plot all nodes level by level and store their positions for later line connection.
        """
        node_positions = {}
        width = 12.5
        height = 3
        x_spacing = width * 1.25

        # Center the root node
        root_y_centered = total_height / 2 - height / 2

        # Iterate through each level and plot nodes
        for level, nodes in levels.items():
            y_positions = self.distribute_vertically(nodes, total_height)
            if level == 0:  # Center the root node explicitly
                y_positions = [root_y_centered]
            node_positions[level] = []
            for i, node in enumerate(nodes):
                x = level * x_spacing
                y = y_positions[i]
                node_positions[level].append((x, y))  # Store node's position

                # Plot the node
                self.plot_node(node, x, y, width, height)

        return node_positions

    def plot_node(self, node, x, y, width, height):
        """
        Plot a single node and display the text inside it.
        """
        if isinstance(node.element, Aggregator):
            txt = f"{node.name}\n(ID: {node.node_id})\n{node.element.name}[{node.weights}]"
        else:
            txt = f"{node.name}\n(ID: {node.node_id})"


        rect = Rectangle((x, y), width, height, edgecolor='black', facecolor='lightgray', lw=2)
        self.ax.add_patch(rect)
        self.ax.text(x + width / 2, y + height / 2, txt, va='center', ha='center',  fontsize=10, fontweight='bold', wrap=True)

    def connect_nodes(self, node_positions, levels):
        """
        Draw lines connecting parent and child nodes based on their stored positions.
        """
        for level, nodes in levels.items():
            if level == len(levels) - 1:  # Skip the last level (no children)
                break
            for i, node in enumerate(nodes):
                # Get the position of the current node
                parent_x, parent_y = node_positions[level][i]
                # Get children positions by iterating over the children of the parent node
                for child in node.children:
                    child_index = levels[level + 1].index(child)  # Find the index of the child in the next level
                    child_x, child_y = node_positions[level + 1][child_index]
                    # Draw line from parent to child
                    self.ax.plot([parent_x + 12.5, child_x], [parent_y + 1.5, child_y + 1.5], color="black", lw=2)

    def display_tree(self, root_node, output_file="tree.png"):
        """
        Main function to plot the tree and save the output to a PNG file.
        """
        # Build the list of nodes for each level
        levels = self.build_level_lists(root_node)

        # Calculate the total height for the plot based on the number of nodes
        max_level_count = max([len(nodes) for nodes in levels.values()])
        total_height = max_level_count * 4  # Adjust based on the level with the most nodes

        # Plot the nodes level by level and remember their positions
        node_positions = self.plot_levels(levels, total_height)

        # Connect the nodes using lines
        self.connect_nodes(node_positions, levels)

        # Save the figure as a high-resolution PNG file
        plt.savefig(output_file, dpi=300)


def print_tree(node, prefix=""):
    """
    Recursively prints the tree structure in the console.
    """
    # Print the current node
    print(f"{prefix}├── [{node.name}]")

    # Print all the children of the current node
    for i, child in enumerate(node.children):
        # If it's the last child, print └ instead of ├
        if i == len(node.children) - 1:
            print_tree(child, prefix + "    ")
        else:
            print_tree(child, prefix + "│   ")

# # Define some elementary criteria
# discrete_criterion = DiscreteCriterion(
#     name="Suitability of Neighborhood",
#     description="",
#     value_score_mapping={0: 0, 50: 50, 80: 100}
# )
#
# qualitative_criterion = QualitativeCriterion(
#     name="Road Surface Quality",
#     description="",
#     value_score_mapping={"poor": 10, "average": 50, "good": 90}
# )
#
# continuous_criterion = ContinuousCriterion(
#     name="Distance from public transport",
#     description="",
#     points=[(0, 100), (500, 80), (1000, 50), (1500, 0)]
# )
#
# # Define aggregators
# aggregator1 = HighHardPartialDisjunction()
# aggregator2 = ConjunctivePartialAbsorption(10, 20)
#
# # Create the root node and add children (Discrete, Qualitative, and Continuous)
# root = AggregationTreeNode(node_id="1", name="Home Suitability", element=aggregator1)
#
# root.add_child(qualitative_criterion, weight=0.3, name="Road Surface Quality")
# location_quality = root.add_child(aggregator2, weight=0.7, name="Overall Location Quality")
# # Add criteria (leaves) to the respective nodes
# location_quality.add_child(discrete_criterion, weight=0.6, name="Neighborhood Suitability")
# location_quality.add_child(continuous_criterion, weight=0.4, name="Transport Proximity")
#
# data = {
#     "Suitability of Neighborhood": [80],  # Discrete criterion
#     "Road Surface Quality": ["good"],     # Qualitative criterion
#     "Distance from public transport": [600]  # Continuous criterion
# }
#
# # Convert dictionary to DataFrame
# inputs = pd.DataFrame(data)
#
# # Evaluate the tree
# result = root.evaluate(inputs)
# print(f"Evaluation result: {result}")
#
# plotter = TreePlotter()
# print_tree(root)
# plotter.display_tree(root)