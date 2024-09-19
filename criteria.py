from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display
import textwrap

class ElementaryCriterion(ABC):
    """
    Abstract base class for an elementary criterion.
    Discrete, Qualitative, and Continuous criteria will extend this class.
    """
    def __init__(self, name, description):
        self.name = name
        self.id = ""
        self.description = description

    def display_info(self):
        """
        Displays the description and the suitability scale.
        """
        print("\n" + "-" * 80 + "\n")
        wrapped_description = self._wrap_text(f"Опис: {self.description}")
        print(f"{self.id} {self.name}\n"
              f"{wrapped_description}")
        self.display_scale()
        print("\n" + "-" * 80 + "\n")

    def display_scale(self):
        """
        Abstract method to display the scale of suitability.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @staticmethod
    def _wrap_text(text, width=80):
        """
        Wraps the text to fit within the specified width, simulating justified text in output.
        :param text: The text to wrap.
        :param width: The width of the output (default is 80 characters).
        :return: Wrapped text.
        """
        wrapper = textwrap.TextWrapper(width=width)
        return "\n".join(wrapper.wrap(text))

    @abstractmethod
    def evaluate(self, input_value):
        """
        Abstract method to be implemented by subclasses.
        This method should evaluate the criterion based on the input value.
        """
        pass

class DiscreteCriterion(ElementaryCriterion):
    """
    Discrete criterion, where the user specifies a mapping of exact values to scores.
    """
    def __init__(self, name, description, value_score_mapping):
        super().__init__(name, description)
        self.value_score_mapping = value_score_mapping
        for value, score in self.value_score_mapping.items():
            self.value_score_mapping[value] = score * 100

    def evaluate(self, input_value):
        if input_value in self.value_score_mapping:
            print(self.value_score_mapping[input_value]/100)
            return self.value_score_mapping[input_value]/100
        else:
            raise ValueError(f"Input value {input_value} is not defined in discrete values.")

    def display_scale(self):
        data = {
            'Вредност': list(self.value_score_mapping.keys()),
            'Погодност [%]': list(self.value_score_mapping.values())
        }
        df = pd.DataFrame(data)
        display(df)

    def plot_elementary_criterion(self):
        """
        Plots an elementary criterion with suitability on the Y-axis and the criterion on the X-axis.
        """
        x_values = list(self.value_score_mapping.keys())
        y_values = list(self.value_score_mapping.values())

        plt.figure(figsize=(5, 5))
        plt.plot(x_values, y_values, marker='o', color='black')
        plt.fill_between(x_values, y_values, color='lightgray', alpha=0.5)

        plt.title("Погодност vs. " + self.name)
        plt.xlabel(self.name)
        plt.ylabel("Погодност [%]")

        if min(x_values) != max(x_values):
            # Normal case where x_values differ
            plt.xticks(np.arange(min(x_values), max(x_values) + 1, (max(x_values) - min(x_values)) / 5))
        else:
            # Handle case where all x_values are the same (use a single tick)
            plt.xticks([min(x_values)])

        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        # plt.show()
        plt.savefig(self.name + "_plot.png")

class QualitativeCriterion(ElementaryCriterion):
    """
    Qualitative criterion, where the user specifies a mapping of descriptions to scores.
    """

    def __init__(self, name, description, value_score_mapping):
        """
        :param points: A list of tuples (x, y), where x is the value and y is the score.
        """
        super().__init__(name, description)
        self.value_score_mapping = value_score_mapping
        for value, score in self.value_score_mapping.items():
            self.value_score_mapping[value] = score * 100

    def display_scale(self):

        data = {
            'Вредност': list(self.value_score_mapping.keys()),
            'Погодност [%]': list(self.value_score_mapping.values())
        }
        df = pd.DataFrame(data)
        display(df)

    def evaluate(self, input_value):
        if input_value in self.value_score_mapping:
            print(self.value_score_mapping[input_value] / 100)
            return self.value_score_mapping[input_value]/100
        else:
            raise ValueError(f"Input description {input_value} is not defined in qualitative values.")

    def plot_elementary_criterion(self):
        """
        Plots an elementary criterion with suitability on the Y-axis and the criterion on the X-axis.
        Handles qualitative (text-based) criteria by labeling the x-axis with strings.
        """
        x_values = list(self.value_score_mapping.keys())
        y_values = list(self.value_score_mapping.values())

        plt.figure(figsize=(5, 5))
        plt.plot(range(len(x_values)), y_values, marker='o', color='black')
        plt.fill_between(range(len(x_values)), y_values, color='lightgray', alpha=0.5)

        plt.title("Погодност vs. " + self.name)
        plt.xlabel(self.name)
        plt.ylabel("Погодност [%]")

        # Set string labels for qualitative x-values
        plt.xticks(ticks=range(len(x_values)), labels=x_values)

        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        # plt.show()
        plt.savefig(self.name + "_plot.png")


class ContinuousCriterion(ElementaryCriterion):
    """
    Continuous criterion, where the user specifies points, and the suitability is interpolated between them.
    """
    def __init__(self, name, description, points, left=None, right=None):
        """
        :param points: A list of tuples (x, y), where x is the value and y is the score.
        """
        super().__init__(name, description)
        self.points = points
        for i in range(len(self.points)):
            self.points[i] = (self.points[i][0],self.points[i][1] * 100)

    def evaluate(self, input_value):
        x_values = [point[0] for point in self.points]
        y_values = [point[1] for point in self.points]

        if input_value < x_values[0] or input_value > x_values[-1]:
            raise ValueError(f"Input value {input_value} is out of the acceptable range [{x_values[0]}, {x_values[-1]}].")

        # Interpolate the suitability score between the points
        print(np.interp(input_value, x_values, y_values)/100)
        return np.interp(input_value, x_values, y_values)/100

    def display_scale(self):
        data = {
            'Вредност': [point[0] for point in self.points],
            'Погодност [%]': [point[1] for point in self.points]
        }
        df = pd.DataFrame(data)
        display(df)

    def plot_elementary_criterion(self):
        """
        Plots an elementary criterion with suitability on the Y-axis and the criterion on the X-axis.
        """
        x_values = [point[0] for point in self.points]
        y_values = [point[1] for point in self.points]
        plt.figure(figsize=(5, 5))
        plt.plot(x_values, y_values, marker='o', color='black')
        plt.fill_between(x_values, y_values, color='lightgray', alpha=0.5)

        plt.title("Погодност vs. "+self.name)
        plt.xlabel(self.name)
        plt.ylabel("Погодност [%]")
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, (max(x_values) - min(x_values)) / 5))
        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        # plt.show()
        plt.savefig(self.name+"_plot.png")

# Automatically determine the type of criterion based on the input data
def create_criterion(name, description, values=None, suitabilities=None, points=None):
    if points:
        # Continuous criterion if points are provided
        return ContinuousCriterion(name, description, points)
    elif values and suitabilities:
        if all(isinstance(v, str) for v in values):
            # Qualitative criterion if all values are strings
            value_score_mapping = dict(zip(values, suitabilities))
            return QualitativeCriterion(name, description, value_score_mapping)
        elif all(isinstance(v, (int, float)) for v in values):
            # Discrete criterion if all values are numbers
            value_score_mapping = dict(zip(values, suitabilities))
            return DiscreteCriterion(name, description, value_score_mapping)
        else:
            raise ValueError("Values must be either all strings (qualitative) or all numbers (discrete).")
    else:
        raise ValueError("Invalid criterion data or missing required fields.")