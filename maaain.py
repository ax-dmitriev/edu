from PyQt5 import QtCore, QtGui, QtWidgets
import sys, sqlite3

class DatabaseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite — управление базой данных")
        self.resize(800, 600)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        self.db_path = "furniture_store.db"
        self.init_ui()
        self.load_database()
     
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.tabs)

        btn_layout = QtWidgets.QHBoxLayout()
        buttons = {
            "Добавить запись": self.add_record,
            "Обновить запись": self.update_record,
            "Удалить запись": self.delete_record,
        }
        for text, handler in buttons.items():
            button = QtWidgets.QPushButton(text)
            button.clicked.connect(handler)
            btn_layout.addWidget(button)
            
        self.query_box = QtWidgets.QComboBox()
        self.query_box.addItems([
            "Выберите запрос",
            "Клиенты (немецкие спальные гарнитуры, скидка >= 14%)",
            "Заказы (фамилии на В или О)"
        ])
        self.query_box.currentIndexChanged.connect(self.run_selected_query)
        btn_layout.addWidget(self.query_box)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_database(self):
        self.tabs.clear()   
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        self.tables_names = [table[0] for table in tables]

        for table in tables:
            table_name = table[0]   

            tab = QtWidgets.QWidget()
            tab_layout = QtWidgets.QVBoxLayout()
            table_widget = QtWidgets.QTableWidget()

            tab_layout.addWidget(table_widget)
            tab.setLayout(tab_layout)

            self.tabs.addTab(tab, table_name)
            self.load_table_data(table_widget, table_name)

        conn.close()

    def load_table_data(self, table_widget, table_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        table_widget.setRowCount(len(records))
        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels([col[1] for col in columns])

        for row_idx, row in enumerate(records):
            for col_idx, value in enumerate(row):
                table_widget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        table_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        conn.close()

    def get_current_table_widget(self):
        index = self.tabs.currentIndex()
        if index == -1:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет активной таблицы")
            return None, None
        
        table_name = self.tabs.tabText(index)
        tab = self.tabs.widget(index)
        table_widget = tab.findChild(QtWidgets.QTableWidget)

        return table_name, table_widget
       
    def get_data(self):
        data = {}
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for table_name in self.tables_names:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data[table_name] = columns
            
        return data
    
    def add_record(self):
        table_name, table_widget = self.get_current_table_widget()
        self.data = self.get_data()
        
        if table_name:
            dialog = RowDialog(self, "добавление записи", table_name, self.db_path, self.data, "add")
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                index = self.tabs.currentIndex()
                self.load_database()
                self.tabs.setCurrentIndex(index)

    def update_record(self):
        table_name, table_widget = self.get_current_table_widget()
        self.data = self.get_data()
        selected_items = table_widget.selectedItems()

        if table_name:
            row_data = {
                table_widget.horizontalHeaderItem(col).text(): table_widget.item(selected_items[0].row(), col).text()
                for col in range(table_widget.columnCount())
            }

            dialog = RowDialog(self, "изменение записи", table_name, self.db_path, self.data, "update", row_data)
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                index = self.tabs.currentIndex()
                self.load_database()
                self.tabs.setCurrentIndex(index)

    def delete_record(self):
        table_name, table_widget = self.get_current_table_widget()
        selected_items = table_widget.selectedItems()
        
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Удаление строки", "Выберите строку для удаления.")
            return

        selected_row = selected_items[0].row()
        conditions = {
            table_widget.horizontalHeaderItem(col).text(): table_widget.item(selected_row, col).text()
            for col in range(table_widget.columnCount())
        }

        if QtWidgets.QMessageBox.question(self, "Подтверждение", f"Удалить строку?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        ) == QtWidgets.QMessageBox.Yes:

            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                where_clause = " AND ".join(f"{col} = ?" for col in conditions)
                cursor.execute(f"DELETE FROM {table_name} WHERE {where_clause}", tuple(conditions.values()))
                    
                conn.commit()
                conn.close()

                index = self.tabs.currentIndex()
                self.load_database()
                self.tabs.setCurrentIndex(index)
                    
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка удаления", str(e))

    def run_selected_query(self):
        selected_query = self.query_box.currentText()
        
        if selected_query == "Клиенты (немецкие спальные гарнитуры, скидка >= 14%)":
            query = """
            SELECT clients.* FROM clients
            JOIN cheque ON clients.client_id = cheque.client_id
            JOIN furniture_sets ON cheque.furniture_id = furniture_sets.furniture_id
            JOIN headset_type ON furniture_sets.type_id = headset_type.type_id
            JOIN producing_country ON furniture_sets.country_id = producing_country.country_id
            WHERE headset_type.type_name = 'Офисный' AND producing_country.country_name = 'Германия' AND cheque.discount <= 14;
            """
            self.execute_query(query, "Клиенты (немецкие спальные гарнитуры, скидка >= 14%)")
        
        elif selected_query == "Заказы (фамилии на В или О)":
            query = """
            SELECT * FROM cheque
            JOIN clients ON cheque.client_id = clients.client_id
            WHERE clients.last_name LIKE 'В%' OR clients.last_name LIKE 'О%';
            """
            self.execute_query(query, "Заказы (фамилии на В или О)")
    
    def execute_query(self, query, title):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout()
        table_widget = QtWidgets.QTableWidget()
        table_widget.setRowCount(len(records))
        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels(columns)
        
        for row_idx, row in enumerate(records):
            for col_idx, value in enumerate(row):
                table_widget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        
        tab_layout.addWidget(table_widget)
        tab.setLayout(tab_layout)
        self.tabs.addTab(tab, title)
        self.tabs.setCurrentWidget(tab)
        
class RowDialog(QtWidgets.QDialog):
    def __init__(self, parent, window_title, table_name, db_path, data, mode, row_data = None):
        super().__init__(parent)
        self.setWindowTitle(f"SQLite — {window_title}")

        self.table_name = table_name
        self.db_path = db_path
        self.mode = mode
        self.data = data
        self.fields = {}

        layout = QtWidgets.QFormLayout(self)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = cursor.fetchall()
        
        for column in columns:
            field_name, is_primary = column[1], column[-1] == 1
            field = QtWidgets.QLineEdit(row_data.get(field_name, "") if row_data else "")
            field.setEnabled(not is_primary)

            if is_primary:
                self.primary_key_rec, self.primary_key_value = field_name, field.text()

            self.fields[field_name] = field
            layout.addRow(QtWidgets.QLabel(field_name), field)

        conn.close()
        
        buttons = QtWidgets.QHBoxLayout()
        ok_button = QtWidgets.QPushButton("OK")
        cancel_button = QtWidgets.QPushButton("Отмена")
        ok_button.clicked.connect(self.accept_changes)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)
    
    def accept_changes(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if self.mode == "add":
                columns, values = zip(*self.fields.items())                
                query_text = f"INSERT INTO {self.table_name} ({', '.join(columns[1:])}) VALUES ({', '.join(['?'] * (len(values) - 1))})"
                query_data = [field.text() for field in values][1:]                
                cursor.execute(query_text, query_data)

            elif self.mode == "update":
                set_clause = ", ".join([f"{key} = ?" for key in self.fields if key != self.primary_key_value])           
                query_text = [field.text() for field in self.fields.values()]     
                columns = [item.split(' = ')[0] for item in set_clause.split(', ')]
                updated_set_clause = ', '.join(f'"{col}" = "{val}"' for col, val in zip(columns[1:], query_text[1:]))
                query_update = f"UPDATE {self.table_name} SET {updated_set_clause} WHERE {self.primary_key_rec} = '{query_text[0]}'"
                cursor.execute(query_update)

            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())
