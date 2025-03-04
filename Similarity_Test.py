import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap, QBrush, QColor
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ID_MSE import compare_images as compare_id_mse
from ED_IOU import compare_images as compare_ed_iou
from DWT_SSIM import compare_images as compare_dwt_ssim
from CWT_SSIM import compare_images as compare_cwt_ssim
from skimage import io

class ImageCycler(QWidget):
    def __init__(self):
        super().__init__()

        self.image_index = 0
        self.images = self.load_images_from_directory("images/frames")
        self.setContentsMargins(96,96,96,96)

        self.layout = QVBoxLayout(self)
        self.image_layout = QHBoxLayout()

        # Layout for image 1 with label
        image_with_label_layout1 = QVBoxLayout()
        image_with_label_layout1.setSpacing(0)
        self.image_name_label1 = QLabel(self)
        self.image_name_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_name_label1.setStyleSheet("font-size: 16px; margin-bottom: 4px;")
        self.image_label1 = QLabel(self)
        self.image_label1.setFixedSize(512, 512)
        self.image_label1.setScaledContents(True)
        label1 = QLabel('Baseline/previous image', self)
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label1.setStyleSheet("font-size: 16px; margin-top: 0px;")
        image_with_label_layout1.addWidget(self.image_name_label1)
        image_with_label_layout1.addWidget(self.image_label1)
        image_with_label_layout1.addWidget(label1)

        # Layout for image 2 with label
        image_with_label_layout2 = QVBoxLayout()
        image_with_label_layout2.setSpacing(0)
        self.image_name_label2 = QLabel(self)
        self.image_name_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_name_label2.setStyleSheet("font-size: 16px; margin-bottom: 4px;")
        self.image_label2 = QLabel(self)
        self.image_label2.setFixedSize(512, 512)
        self.image_label2.setScaledContents(True)
        label2 = QLabel('Current image', self)
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setStyleSheet("font-size: 16px; margin-top: 0px;")
        image_with_label_layout2.addWidget(self.image_name_label2)
        image_with_label_layout2.addWidget(self.image_label2)
        image_with_label_layout2.addWidget(label2)

        self.image_layout.addLayout(image_with_label_layout1)
        self.image_layout.addLayout(image_with_label_layout2)

        # Button to cycle images
        self.button = QPushButton('Next Image', self)
        self.button.setFixedSize(150, 50)
        self.button.setStyleSheet("background-color: orange; font-size: 16px; font-weight: bold;")
        self.button.clicked.connect(self.cycle_images)

        self.image_layout.addWidget(self.button)

        self.layout.addLayout(self.image_layout)

        # Add a blank table below the images
        self.table = QTableWidget(4, 5, self)
        self.table.setFixedSize(842, 226)  # Set table width to 1024px and height to 256px
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(True)
        self.table.setStyleSheet("""
            QTableWidget::item { 
                border: 1px solid black;
                font-size: 48px;
            }
        """)

        # Resize cells to fit the entire table
        for row in range(4):
            self.table.setRowHeight(row, 56)  # Adjust row height to fit the table height
        for col in range(5):
            self.table.setColumnWidth(col, 168)  # Adjust column width to fit the table width

        # Set specified headers and make them 20px and bold
        headers = {
            (0, 1): "ID_MSE",
            (0, 2): "ED_IOU",
            (0, 3): "DWT_SSIM",
            (0, 4): "CWT_SSIM",
            (1, 0): "Similarity",
            (2, 0): "Threshold",
            (3, 0): "Change Key?"
        }
        for position, text in headers.items():
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            font = item.font()
            font.setPointSize(12)  # Set font size to 20px
            font.setBold(True)
            item.setFont(font)
            self.table.setItem(position[0], position[1], item)

        # Example similarity and threshold values
        similarity_values = [0.8, 0.6, 0.9, 0.7, 0.5]
        threshold_values = [0.7, 0.7, 0.7, 0.7, 0.7]

        # Set font size and color for similarity and change key cells
        for col in range(1, 5):
            similarity = similarity_values[col - 1]
            threshold = threshold_values[col - 1]

            similarity_item = QTableWidgetItem(f"{similarity * 100:.1f}%")
            change_key_item = QTableWidgetItem("Yes" if similarity < threshold else "No")

            font = similarity_item.font()
            font.setPointSize(20)
            similarity_item.setFont(font)
            change_key_item.setFont(font)

            if similarity < threshold:
                similarity_item.setForeground(QBrush(QColor("red")))
                change_key_item.setForeground(QBrush(QColor("red")))
            else:
                similarity_item.setForeground(QBrush(QColor("green")))
                change_key_item.setForeground(QBrush(QColor("green")))

            self.table.setItem(1, col, similarity_item)
            self.table.setItem(3, col, change_key_item)

        # Center the table horizontally
        table_layout = QHBoxLayout()
        table_layout.addStretch(1)
        table_layout.addWidget(self.table)
        table_layout.addStretch(1)

        self.layout.addLayout(table_layout)

        self.setLayout(self.layout)

        self.update_images()

    def load_images_from_directory(self, directory):
        # Load images from the specified directory with supported formats
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        return [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(supported_formats)]

    def update_images(self):
        pixmap1 = QPixmap(self.images[self.image_index % len(self.images)])
        pixmap2 = QPixmap(self.images[(self.image_index + 1) % len(self.images)])
        self.image_label1.setPixmap(pixmap1)
        self.image_label2.setPixmap(pixmap2)
        self.image_name_label1.setText(os.path.basename(self.images[self.image_index % len(self.images)]))
        self.image_name_label2.setText(os.path.basename(self.images[(self.image_index + 1) % len(self.images)]))

        image1 = io.imread(self.images[self.image_index % len(self.images)])
        image2 = io.imread(self.images[(self.image_index + 1) % len(self.images)])

        similarities = self.calculate_similarities(image1, image2)
        thresholds = self.get_thresholds()

        self.update_table(similarities, thresholds)

    def calculate_similarities(self, image1, image2):
        return {
            'id_mse': compare_id_mse(image1, image2) * 100,
            'ed_iou': compare_ed_iou(image1, image2) * 100,
            'dwt_ssim': compare_dwt_ssim(image1, image2) * 100,
            'cwt_ssim': compare_cwt_ssim(image1, image2) * 100,
        }

    def get_thresholds(self):
        return {
            'ID_MSE_Threshold': 95,
            'ED_IOU_Threshold': 10,
            'DWT_SSIM_Threshold': 20,
            'CWT_SSIM_Threshold': 70,
        }

    def update_table(self, similarities, thresholds):
        for i, (key, value) in enumerate(similarities.items(), start=1):
            item = QTableWidgetItem(f"{value:.2f}%")
            threshold_key = key.upper() + '_Threshold'
            font = item.font()
            font.setPointSize(24)  # Set font size to 24px
            item.setFont(font)
            threshold_item = QTableWidgetItem(f"{thresholds[threshold_key]}%")
            threshold_item.setFont(font)
            change_key_item = QTableWidgetItem("True" if value < thresholds[threshold_key] else "False")
            change_key_item.setFont(font)

            if value < thresholds[threshold_key]:
                item.setForeground(QBrush(QColor("red")))
                change_key_item.setForeground(QBrush(QColor("yellow")))
            else:
                item.setForeground(QBrush(QColor("green")))

            self.table.setItem(1, i, item)
            self.table.setItem(2, i, threshold_item)
            self.table.setItem(3, i, change_key_item)

    def cycle_images(self):
        self.image_index += 1
        self.update_images()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageCycler()
    ex.show()
    sys.exit(app.exec())