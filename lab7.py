import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
import math
from PIL import Image
from PIL import Image, ImageDraw
import numpy as np

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Лабораторная 7')
        
        self.main_layout = QVBoxLayout()
        
        self.open_button = QPushButton('Открыть изображение')
        self.open_button.clicked.connect(self.open_image)
        self.main_layout.addWidget(self.open_button)
        
        self.image_label = QLabel()
        self.main_layout.addWidget(self.image_label)
        
        self.plot_button = QPushButton('Создать график')
        self.plot_button.clicked.connect(self.create_plot)
        self.main_layout.addWidget(self.plot_button)
        
        self.save_button = QPushButton('Сохранить график')
        self.save_button.clicked.connect(self.save_plot)
        self.main_layout.addWidget(self.save_button)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)
        
        self.setLayout(self.main_layout)
        
        self.open_button.setStyleSheet("background-color: gray;")
        self.plot_button.setStyleSheet("background-color: gray;")
        self.save_button.setStyleSheet("background-color: gray;")
    
    def save_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', 
                                                   '', 
                                                   'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.figure.savefig(file_name)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', 
                                                   '', 
                                                   'Images (*.png *.xpm *.jpg *.bmp)')
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

    def create_plot(self):
        x = range(-10, 10)
        y = [i**3 for i in x]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        image_path = self.image_label.pixmap().toImage().save('image.png')
        img = Image.open('image.png')
        width, height = img.size

        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        draw.ellipse((0, height // 2, height // 2, height), fill=255)   
        
        img = img.convert('RGBA')
        img.putalpha(mask)
        img = img.crop((0, height // 2, height // 2, height))
            
        arr = np.array(img)
        image = OffsetImage(arr, zoom=0.5)
        ab = AnnotationBbox(image, (0, 700), frameon=False)
        ax.add_artist(ab)
            
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())