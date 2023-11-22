import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QDoubleSpinBox, QSpinBox, QSlider
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np

def archimedean_spiral(theta, a=1, b=0):
    r = a + b * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def calculate_b_coefficient(spiral_length, num_turns):
    # Convert turns to radians
    theta = 2 * np.pi * num_turns
    
    # Calculate a coefficient using the formula
    b = (2 * spiral_length) / (theta ** 2)
    
    return b

class ArchimedeanSpiralApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_value_label = QLabel("Length: 100 cm")
        
        self.length_slider.setMinimum(0)  # Minimum value for length
        self.length_slider.setMaximum(500)
        self.length_slider.setValue(100)   # Default value for length
        self.length_slider.valueChanged.connect(self.plot_archimedean_spiral)
        self.length_slider.valueChanged.connect(lambda value: self.length_value_label.setText(f"Length:{value} cm"))

        self.a_slider = QSlider(Qt.Horizontal)
        self.a_value_label = QLabel("a: 0")
        self.a_slider.setMinimum(-50)  # Minimum value for length
        self.a_slider.setMaximum(50)
        self.a_slider.setValue(0)   # Default value for length
        self.a_slider.valueChanged.connect(self.plot_archimedean_spiral)
        self.a_slider.valueChanged.connect(lambda value: self.a_value_label.setText(f"a:{value} cm"))

        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_value_label = QLabel("Angle: 720º")
        self.angle_slider.setMaximum(1440)  # Maximum value for length
        self.angle_slider.setValue(180)   # Default value for length
        self.angle_slider.valueChanged.connect(self.plot_archimedean_spiral)
        self.angle_slider.valueChanged.connect(lambda value: self.angle_value_label.setText(f"Angle: {value}º"))
        

        self.num_dots_slider = QSlider(Qt.Horizontal)
        self.num_dots_value_label = QLabel("Number of Dots: 7")
        self.num_dots_slider.setMinimum(2)   # Minimum value for number of dots
        self.num_dots_slider.setMaximum(20)
        self.num_dots_slider.setValue(7)    # Default value for number of dots
        self.num_dots_slider.setSingleStep(1)
        self.num_dots_slider.valueChanged.connect(self.plot_archimedean_spiral)
        self.num_dots_slider.valueChanged.connect(lambda value: self.num_dots_value_label.setText(f"Number of Dots: {value}"))

        # Create figure and canvas for matplotlib.
        self.figure, self.canvas = plt.subplots(2,1, gridspec_kw={'height_ratios': [1, 4]})
        self.canvas_widget = FigureCanvas(self.figure)
        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        form_layout.addRow(self.length_value_label, self.length_slider)
        form_layout.addRow(self.num_dots_value_label, self.num_dots_slider)
        form_layout.addRow(self.angle_value_label, self.angle_slider)
        form_layout.addRow(self.a_value_label, self.a_slider)
        layout.addLayout(form_layout)
        layout.addWidget(self.canvas_widget)
        layout.setStretch(1, 3)

        self.plot_archimedean_spiral()
        

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Archimedean Spiral App')
        self.setGeometry(100, 100, 800, 600)

    def plot_archimedean_spiral(self):
        length = self.length_slider.value()
        num_dots = self.num_dots_slider.value()
        angle = self.angle_slider.value()
        a_value = self.a_slider.value()

        # Clear previous plots
        self.figure.clear()

        # Create new Axes object.
        gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1]) 
        spiral_ax = plt.subplot(gs[0], adjustable='box', aspect='equal')
        spiral_ax.grid()
        length_ax = plt.subplot(gs[1])
        
        length_ax.set_yticklabels([])
        length_ax.set_yticks([])

        self.figure.subplots_adjust(hspace=0.5)

        # Plot Archimedean Spiral
        theta = np.linspace(0, angle/180 * np.pi, 1000)
        b_value = calculate_b_coefficient(length, 2)
        x, y = archimedean_spiral(theta, a_value, b_value)
        spiral_ax.plot(x, y, label=f'Archimedean Spiral (a={b_value})')

        # Plot Dots
        dots_x, dots_y = archimedean_spiral(np.linspace(0, angle/180 * np.pi, num_dots), a_value, b_value)
        spiral_ax.scatter(dots_x, dots_y, color='red', label=f'{num_dots} dots')

        # Set plot properties
        spiral_ax.set_title('Archimedean Spiral')
        spiral_ax.set_xlabel('X-axis')
        spiral_ax.set_ylabel('Y-axis')
        # spiral_ax.legend()

        proportions = []
        for i in range(num_dots):
            proportions.append(1-(i/(num_dots-1))**2)

        proportions = np.array(proportions)
        print("Proportions:", proportions)
        length_from_origin_to_dots = proportions*length
        print("Length from origin to dots:", length_from_origin_to_dots)

        length_ax.plot(np.linspace(0, length, 2), np.zeros(2), 'b')
        length_ax.scatter(length_from_origin_to_dots, np.zeros(num_dots), color='red', label=f'{num_dots} dots')
        length_ax.set_xlabel('Length from Origin to Each Dot')

        # Redraw canvas
        self.canvas_widget.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ArchimedeanSpiralApp()
    window.show()
    sys.exit(app.exec_())
