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
        wrapped_description = self._wrap_text(self.description)
        print(f"{self.id} {self.name}"
              f"Description:\n{wrapped_description}")
        self.display_scale()

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

    def evaluate(self, input_value):
        if input_value in self.value_score_mapping:
            print(self.value_score_mapping[input_value]/100)
            return self.value_score_mapping[input_value]/100
        else:
            raise ValueError(f"Input value {input_value} is not defined in discrete values.")

    def display_scale(self):
        data = {
            'Value': list(self.value_score_mapping.keys()),
            'Suitability [%]': list(self.value_score_mapping.values())
        }
        df = pd.DataFrame(data)
        display(df)

    def plot_elementary_criterion(self):
        """
        Plots an elementary criterion with suitability on the Y-axis and the criterion on the X-axis.
        """
        x_values = self.value_score_mapping.keys()
        y_values = self.value_score_mapping.values()
        plt.figure(figsize=(5, 5))
        plt.plot(x_values, y_values, marker='o', color='black')
        plt.fill_between(x_values, y_values, color='lightgray', alpha=0.5)

        plt.title("Suitability vs. "+self.name)
        plt.xlabel(self.name)
        plt.ylabel("Suitability [%]")
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, (max(x_values) - min(x_values)) // 5))
        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        plt.show()

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

    def display_scale(self):

        data = {
            'Value': list(self.value_score_mapping.keys()),
            'Suitability [%]': list(self.value_score_mapping.values())
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
        """
        x_values = self.value_score_mapping.keys()
        y_values = self.value_score_mapping.values()
        plt.figure(figsize=(5, 5))
        plt.plot(x_values, y_values, marker='o', color='black')
        plt.fill_between(x_values, y_values, color='lightgray', alpha=0.5)

        plt.title("Suitability vs. "+self.name)
        plt.xlabel(self.name)
        plt.ylabel("Suitability [%]")
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, (max(x_values) - min(x_values)) // 5))
        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        plt.show()

class ContinuousCriterion(ElementaryCriterion):
    """
    Continuous criterion, where the user specifies points, and the suitability is interpolated between them.
    """
    def __init__(self, name, description, points):
        """
        :param points: A list of tuples (x, y), where x is the value and y is the score.
        """
        super().__init__(name, description)
        self.points = points

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
            'Value': [point[0] for point in self.points],
            'Suitability [%]': [point[1] for point in self.points]
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

        plt.title("Suitability vs. "+self.name)
        plt.xlabel(self.name)
        plt.ylabel("Suitability [%]")
        plt.xticks(np.arange(min(x_values), max(x_values) + 1, (max(x_values) - min(x_values)) // 5))
        plt.yticks(np.arange(0, 101, 20))
        plt.grid(True)
        plt.show()

# Automatically determine the type of criterion based on the input data
def create_criterion(description, values, suitability):
    if all(isinstance(v, str) for v in values):
        # Qualitative criterion if all values are strings
        value_score_mapping = dict(zip(values, suitability))
        return QualitativeCriterion("",description, value_score_mapping)
    elif isinstance(values, list) and isinstance(suitability, list):
        if len(values) == len(suitability):
            # Discrete or Continuous criterion based on numeric values
            points = list(zip(values, suitability))
            return ContinuousCriterion("", description, points)
        else:
            raise ValueError("Values and suitability lists must be of the same length.")
    else:
        raise ValueError("Invalid criterion data.")

criteria = [
    {
        "id": 1111,
        "description": "The distance from train stations is measured in meters. All distances below 400 meters are considered excellent and acceptable. Similarly, all distances of 1000 meters or more are considered unacceptable.",
        "values": [400, 1000],
        "suitability": [100, 0]
    },
    {
        "id": 1112,
        "description": "The distance from bus stations is measured in meters. Bus stations are expected to be closer than train stations. All distances below 50 meters are considered excellent.",
        "values": [50, 700],
        "suitability": [100, 0]
    },
    {
        "id": 112,
        "description": "The distance from local food stores is measured in meters. The criterion assumes walking distances are acceptable. All distances below 100 meters are excellent.",
        "values": [100, 400, 600],
        "suitability": [100, 50, 0]
    },
    {
        "id": 121,
        "description": "The distance from parks is measured in meters. Parks are highly desirable for this kind of stakeholder. The ideal location would be immediately next to a park.",
        "values": [0, 3500],
        "suitability": [100, 0]
    },
    {
        "id": 122,
        "description": "The average distance from local restaurants (measured in meters). Living too close to a restaurant brings noise and pollution. Proximity to restaurants is highly desirable within walking distance.",
        "values": [0, 500, 900],
        "suitability": [40, 100, 0]
    },
    {
        "id": 123,
        "description": "The distance from the public library is measured in meters. The closer the library, the more desirable for frequent visits.",
        "values": [0, 3000],
        "suitability": [100, 0]
    },
    {
        "id": 123,
        "description": "The distance from train stations is measured in meters. All distances below 400 meters are considered excellent and acceptable. Similarly, all distances of 1000 meters or more are considered unacceptable.",
        "values": [400, 1000],
        "suitability": [100, 0]
    },
    {
        "id": 123,
        "description": "The quality of road surface leading to the house. Descriptions can include 'poor', 'average', and 'good'.",
        "values": ["poor", "average", "good"],
        "suitability": [20, 60, 90]
    },
    {
        "id": 123,
        "description": "The distance from local food stores is measured in meters. The criterion assumes walking distances are acceptable. All distances below 100 meters are excellent.",
        "values": [100, 400, 600],
        "suitability": [100, 50, 0]
    }
]

for criterion in criteria:
    description = criterion['description']
    values = criterion['values']
    suitability = criterion['suitability']

    # Automatically create the appropriate criterion type
    criterion_instance = create_criterion(description, values, suitability)
    criterion_instance.display_info()

    print("\n" + "-" * 80 + "\n")