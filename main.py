import sys
import json
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QPushButton, QLabel, QLineEdit, 
                             QMessageBox, QSpinBox, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

class EssentialBot(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #f0f0f0; font-family: 'Arial';")
        self.setWindowTitle("Essential Bot - Lug'at O'rganuvchisi")
        self.setGeometry(100, 100, 900, 700)
        
        # Ma'lumotlarni yuklash
        with open("words.json", "r", encoding="utf-8") as file:
            self.all_words = json.load(file)
        
        # Statistika fail
        self.stats_file = "stats.json"
        self.load_stats()
        
        # Foydalanuvchi tanlagan unit
        self.current_unit = 1
        self.current_words = self.get_unit_words(1)
        self.current_word = random.choice(self.current_words)
        
        # Statistika
        self.correct_count = 0
        self.wrong_count = 0
        self.session_total = 0
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # ===== TOP PANEL: UNIT TANLASH =====
        top_panel = QHBoxLayout()
        
        unit_label = QLabel("Unit tanlang:")
        unit_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems([f"Unit {i}" for i in range(1, 31)])
        self.unit_combo.setCurrentIndex(0)
        self.unit_combo.currentIndexChanged.connect(self.on_unit_changed)
        self.unit_combo.setStyleSheet("padding: 5px; font-size: 11px;")
        
        top_panel.addWidget(unit_label)
        top_panel.addWidget(self.unit_combo)
        top_panel.addStretch()
        
        # Statistika ko'rsatkich
        stats_label = QLabel(f"✅ {self.total_correct} | ❌ {self.total_wrong}")
        stats_label.setFont(QFont("Arial", 11, QFont.Bold))
        stats_label.setStyleSheet("color: #2c3e50;")
        self.stats_label = stats_label
        top_panel.addWidget(self.stats_label)
        
        main_layout.addLayout(top_panel)
        
        # ===== PROGRESS BAR =====
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # ===== WORD DISPLAY =====
        word_panel = QVBoxLayout()
        
        word_label = QLabel("So'z:")
        word_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.word_display = QLabel(f"{self.current_word['word']}")
        self.word_display.setFont(QFont("Arial", 32, QFont.Bold))
        self.word_display.setStyleSheet("color: #3498db; padding: 20px;")
        self.word_display.setAlignment(Qt.AlignCenter)
        
        word_panel.addWidget(word_label)
        word_panel.addWidget(self.word_display)
        
        main_layout.addLayout(word_panel)
        
        # ===== INPUT FIELD =====
        meaning_label = QLabel("Ma'nosi:")
        meaning_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ma'noni kiriting...")
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.input_field.returnPressed.connect(self.check_answer)
        
        main_layout.addWidget(meaning_label)
        main_layout.addWidget(self.input_field)
        
        # ===== RESULT LABEL =====
        self.result_label = QLabel(" ")
        self.result_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("padding: 10px; border-radius: 5px;")
        main_layout.addWidget(self.result_label)
        
        # ===== BUTTONS =====
        button_layout = QHBoxLayout()
        
        check_btn = QPushButton("✅ Tasdiqlash (Enter)")
        check_btn.setFont(QFont("Arial", 11, QFont.Bold))
        check_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        check_btn.clicked.connect(self.check_answer)
        
        skip_btn = QPushButton("⏭️ O'tish")
        skip_btn.setFont(QFont("Arial", 11, QFont.Bold))
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        skip_btn.clicked.connect(self.skip_word)
        
        reset_btn = QPushButton("🔄 Qayta boshlash")
        reset_btn.setFont(QFont("Arial", 11, QFont.Bold))
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
        """)
        reset_btn.clicked.connect(self.reset_session)
        
        button_layout.addWidget(check_btn)
        button_layout.addWidget(skip_btn)
        button_layout.addWidget(reset_btn)
        
        main_layout.addLayout(button_layout)
        
        # ===== SESSION STATS =====
        stats_panel = QHBoxLayout()
        
        self.session_label = QLabel("📊 Sessiya: 0/0")
        self.session_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.session_label.setStyleSheet("color: #2c3e50;")
        
        self.accuracy_label = QLabel("Aniqlik: 0%")
        self.accuracy_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.accuracy_label.setStyleSheet("color: #2c3e50;")
        
        stats_panel.addWidget(self.session_label)
        stats_panel.addStretch()
        stats_panel.addWidget(self.accuracy_label)
        
        main_layout.addLayout(stats_panel)
        
        self.setLayout(main_layout)
        self.input_field.setFocus()
        self.show()
    
    def get_unit_words(self, unit):
        """Tanlangan unitdan so'zlarni olish"""
        return [word for word in self.all_words if word['unit'] == unit]
    
    def on_unit_changed(self):
        """Unit o'zgarganda"""
        self.current_unit = self.unit_combo.currentIndex() + 1
        self.current_words = self.get_unit_words(self.current_unit)
        self.reset_session()
    
    def check_answer(self):
        """Javobni tekshirish"""
        user_answer = self.input_field.text().strip().lower()
        
        if not user_answer:
            QMessageBox.warning(self, "Ogohlantirish", "Javob kiriting!")
            return
        
        correct_meaning = self.current_word['meaning'].lower()
        
        # Birinchi ma'noni tekshirish (verguldan avval)
        correct_first = correct_meaning.split(',')[0].strip()
        
        self.session_total += 1
        
        if user_answer == correct_first or user_answer == correct_meaning:
            self.correct_count += 1
            self.result_label.setText(f"✅ TO'G'RI! Ma'nosi: {self.current_word['meaning']}")
            self.result_label.setStyleSheet("background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px;")
        else:
            self.wrong_count += 1
            self.result_label.setText(f"❌ NOTO'G'RI! To'g'ri javob: {self.current_word['meaning']}")
            self.result_label.setStyleSheet("background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px;")
        
        self.update_stats()
        self.input_field.clear()
        
        # 1.5 soniyadan keyin keyingi so'zni ko'rsatish
        QTimer.singleShot(1500, self.next_word)
    
    def skip_word(self):
        """So'zni o'tish"""
        self.session_total += 1
        self.wrong_count += 1
        self.result_label.setText(f"⏭️ O'tdi! Ma'nosi: {self.current_word['meaning']}")
        self.result_label.setStyleSheet("background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px;")
        self.update_stats()
        self.input_field.clear()
        QTimer.singleShot(1500, self.next_word)
    
    def next_word(self):
        """Keyingi so'z"""
        self.current_word = random.choice(self.current_words)
        self.word_display.setText(self.current_word['word'])
        self.result_label.setText(" ")
        self.input_field.setFocus()
    
    def update_stats(self):
        """Statistikani yangilash"""
        self.stats_label.setText(f"✅ {self.total_correct + self.correct_count} | ❌ {self.total_wrong + self.wrong_count}")
        
        if self.session_total > 0:
            accuracy = (self.correct_count / self.session_total) * 100
            self.accuracy_label.setText(f"Aniqlik: {accuracy:.1f}%")
            self.progress_bar.setValue(int(accuracy))
        
        self.session_label.setText(f"📊 Sessiya: {self.correct_count}/{self.session_total}")
    
    def reset_session(self):
        """Sessiyani qayta boshlash"""
        self.save_stats()
        self.correct_count = 0
        self.wrong_count = 0
        self.session_total = 0
        self.result_label.setText(" ")
        self.input_field.clear()
        self.next_word()
        self.update_stats()
        self.input_field.setFocus()
    
    def load_stats(self):
        """Oldingi statistikani yuklash"""
        try:
            with open(self.stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
                self.total_correct = stats.get("total_correct", 0)
                self.total_wrong = stats.get("total_wrong", 0)
        except FileNotFoundError:
            self.total_correct = 0
            self.total_wrong = 0
    
    def save_stats(self):
        """Statistikani saqlash"""
        stats = {
            "total_correct": self.total_correct + self.correct_count,
            "total_wrong": self.total_wrong + self.wrong_count
        }
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        self.load_stats()
    
    def closeEvent(self, event):
        """Dasturni yopishda statistikani saqlash"""
        self.save_stats()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = EssentialBot()
    sys.exit(app.exec_())
