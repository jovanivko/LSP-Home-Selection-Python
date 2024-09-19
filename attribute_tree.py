import numpy as np
import pandas as pd

from aggregators import Aggregator, HighHardPartialDisjunction, ConjunctivePartialAbsorption
from criteria import ElementaryCriterion, QualitativeCriterion, DiscreteCriterion, ContinuousCriterion
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

class AggregationTreeNode:

    def __init__(self, node_id, name, element):
        self.element = element  # can be a suitability mapping or aggregator
        self.node_id = node_id
        self.name = name
        self.children = []
        self.weights = []

    def add_child(self, element, weight, name):
        assert not isinstance(self, ElementaryCriterion)
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

    def evaluate(self, inputs):
        if isinstance(self.element, ElementaryCriterion):
            value = inputs[self.element.name].values[0]  # Get the value for this criterion from the DataFrame
            if pd.isna(value):  # Check for NaN (missing value)
                return None
            return self.element.evaluate(value)
        else:
            # It's an aggregator, gather children evaluations, missingness-tolerant approach to data
            child_values = []
            updated_weights = []

            for child, weight in zip(self.children, self.weights):
                child_value = child.evaluate(inputs)
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
            # print(f"Normalized weights: {updated_weights}")
            # print(f"Weight sum before normalization: {weight_sum}")
            #
            # # If sum of updated weights is not 1, normalize them
            # if not np.isclose(weight_sum, 1):
            #     normalized_weights = [w / weight_sum for w in updated_weights]
            #     print(f"Weight sum after normalization: {sum(normalized_weights)}")
            # else:
            #     normalized_weights = updated_weights

            return self.element.evaluate(child_values, normalized_weights)

class TreePlotter:
    """
    Class responsible for plotting the tree diagram.
    """
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_axis_off()

    def plot_node(self, node, x, y, width, height, parent_coords=None):
        """
        Recursively plot each node and its children in the tree.
        """
        if isinstance(node.element, Aggregator):
            txt = f"{node.name}\n(ID: {node.node_id}) {node.element.name}[{node.weights}]"
        else:
            txt = f"{node.name}\n(ID: {node.node_id})"
        # Draw the rectangle for the node
        rect = Rectangle((x, y), width, height, edgecolor='black', facecolor='lightgray', lw=2)
        self.ax.add_patch(rect)
        self.ax.text(x + width / 2, y + height / 2, txt,
                     va='center', ha='center', fontsize=10)

        # Draw line from parent to current node
        if parent_coords:
            parent_x, parent_y = parent_coords
            self.ax.plot([parent_x + width / 2, x + width / 2], [parent_y, y + height], color="black", lw=2)

        # Plot children
        if node.children:
            child_width = width / len(node.children)  # Equal width for each child
            for i, child in enumerate(node.children):
                self.plot_node(child, x + i * child_width, y - height * 1.5, child_width, height, (x, y))

    def display_tree(self, root_node):
        """
        Starts the plotting process for the given tree with root_node.
        """
        # Start plotting from the root node
        self.plot_node(root_node, x=0, y=0, width=6, height=1)
        plt.show()

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

# Define some elementary criteria
discrete_criterion = DiscreteCriterion(
    name="Suitability of Neighborhood",
    description="",
    value_score_mapping={0: 0, 50: 50, 80: 100}
)

qualitative_criterion = QualitativeCriterion(
    name="Road Surface Quality",
    description="",
    value_score_mapping={"poor": 10, "average": 50, "good": 90}
)

continuous_criterion = ContinuousCriterion(
    name="Distance from public transport",
    description="",
    points=[(0, 100), (500, 80), (1000, 50), (1500, 0)]
)

# Define aggregators
aggregator1 = HighHardPartialDisjunction()
aggregator2 = ConjunctivePartialAbsorption(10, 20)

# Create the root node and add children (Discrete, Qualitative, and Continuous)
root = AggregationTreeNode(node_id="1", name="Home Suitability", element=aggregator1)

root.add_child(qualitative_criterion, weight=0.3, name="Road Surface Quality")
location_quality = root.add_child(aggregator2, weight=0.7, name="Overall Location Quality")
# Add criteria (leaves) to the respective nodes
location_quality.add_child(discrete_criterion, weight=0.6, name="Neighborhood Suitability")
location_quality.add_child(continuous_criterion, weight=0.4, name="Transport Proximity")

data = {
    "Suitability of Neighborhood": [80],  # Discrete criterion
    "Road Surface Quality": ["good"],     # Qualitative criterion
    "Distance from public transport": [600]  # Continuous criterion
}

# Convert dictionary to DataFrame
inputs = pd.DataFrame(data)

# Evaluate the tree
result = root.evaluate(inputs)
print(f"Evaluation result: {result}")

plotter = TreePlotter()
print_tree(root)
plotter.display_tree(root)