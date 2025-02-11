import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap, QBrush, QColor
from PyQt6.QtCore import Qt
from skimage import io
from Similarity_Test_Process import compare_images

class ImageCycler(QWidget):
    def __init__(self):
        super().__init__()

        self.image_index = 0
        self.images = self.load_images_from_directory("images")
        self.setContentsMargins(96, 96, 96, 96)

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
        self.layout.addLayout(self.image_layout)

        self.table = QTableWidget(4, 5, self)
        self.table.setHorizontalHeaderLabels(["", "ID_MSE", "ED_IOU", "DWT_SSIM", "CWT_SSIM"])
        self.table.setVerticalHeaderLabels(["", "Similarity", "Threshold", "Change Key?"])
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.update_images()

    def load_images_from_directory(self, directory):
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

        similarities, thresholds, change_keys = compare_images(image1, image2)

        for i, (similarity, threshold, change_key) in enumerate(zip(similarities, thresholds, change_keys)):
            self.table.setItem(1, i + 1, QTableWidgetItem(f"{similarity:.2f}%"))
            self.table.setItem(2, i + 1, QTableWidgetItem(f"{threshold}%"))
            self.table.setItem(3, i + 1, QTableWidgetItem("True" if change_key else "False"))

    def cycle_images(self):
        self.image_index += 1
        self.update_images()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageCycler()
    ex.show()
    sys.exit(app.exec())