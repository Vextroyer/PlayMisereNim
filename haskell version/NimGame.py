import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QGridLayout, QMessageBox


class NimGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('NIM GAME')
        self.setGeometry(100, 100, 600, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0; /* Color de fondo */
                font-family: Arial, sans-serif; /* Fuente */
            }
            QLabel {
                color: #333; /* Color del texto de las etiquetas */
                font-size: 14px; /* Tamaño de fuente de etiquetas */
            }
            QLineEdit {
                font-size: 12px; /* Tamaño de fuente de entradas */
                height: 25px; /* Altura de entrada */
            }
            QPushButton {
                background-color: #4CAF50; /* Color de fondo de botones */
                color: white; /* Color del texto de botones */
                border: none; /* Sin borde */
                padding: 5px; /* Espaciado interno más pequeño */
                font-size: 12px; /* Tamaño de fuente de botones más pequeño */
                border-radius: 5px; /* Bordes redondeados */
            }
            QPushButton:hover {
                background-color: #45a049; /* Cambio de color al pasar el mouse */
            }
        """)

        self.nickname = self.request_nickname()  # Solicitar el apodo al iniciar el juego
        self.show_story()  # Mostrar la historia

        self.num_piles = random.randint(5, 10)
        self.piles = [random.randint(1, 39) for _ in range(self.num_piles)]

        layout = QVBoxLayout()
        grid = QGridLayout()

        self.labels = []
        self.entries = []
        self.buttons = []

        num_columns = 3  # Número de columnas que deseas (puedes cambiar esto)

        # Añadir widgets a la cuadrícula
        for i, pile in enumerate(self.piles):
            label = QLabel(f"{pile} piezas")
            label.setFont(QFont('Arial', 14))
            
            # Calcular la fila y la columna utilizando el número de columnas deseado
            row = (i // num_columns) * 3
            col = (i % num_columns) * 3
            
            grid.addWidget(label, row, col)
            self.labels.append(label)

            entry = QLineEdit()
            entry.setFixedSize(100, 25)  # Ajustar tamaño del campo de entrada
            grid.addWidget(entry, row + 1, col)
            self.entries.append(entry)

            button = QPushButton('Retirar')
            button.setFixedSize(100, 25)  # Ajustar tamaño del botón
            button.clicked.connect(lambda _, index=i: self.retire_madera(index))
            grid.addWidget(button, row + 2, col)
            self.buttons.append(button)

        self.turn_label = QLabel(f"Turno de {self.nickname}")  # Usar el apodo en el turno
        self.turn_label.setFont(QFont('Arial', 14))
        layout.addLayout(grid)
        layout.addWidget(self.turn_label)

        self.setLayout(layout)  # Establecer el layout principal

        self.current_player = 1


    def request_nickname(self):
        nickname, ok = QInputDialog.getText(self, "Introducir Nickname", "Por favor, introduce tu apodo:")
        if ok and nickname:
            return nickname
        return "Jugador"  # Apodo por defecto si no se proporciona


    def show_story(self):
        story = (
            "¡Bienvenido al Juego NIM!\n"
            "Una antigua batalla entre astutos estrategas.\n"
            "Tu objetivo es ser el último en retirar piezas "
            "de los montones que aparecen ante ti.\n"
            "Recuerda, ¡piensa con astucia y juega con estrategia!\n\n"
            "¡Que comience el juego!"
        )
        QMessageBox.information(self, "Historia del Juego", story)


    def retire_madera(self, index):
        if self.can_move():
            try:
                cantidad = int(self.entries[index].text())  # Obtener la cantidad del input
                if 1 <= cantidad <= self.piles[index]:
                    self.piles[index] -= cantidad
                    self.labels[index].setText(f"Montón {index + 1}: {self.piles[index]} piezas")

                    # Limpiar los inputs después de un movimiento exitoso
                    self.clear_inputs()

                    # Llamar para ocultar los montones vacíos
                    self.hide_empty_piles()

                    # Verificar si el jugador pierde
                    if self.check_loser(self.current_player):
                        return

                    # Cambiar turnos
                    self.current_player = 2
                    self.turn_label.setText("Turno de la máquina")
                    self.machine_move()
                else:
                    QMessageBox.warning(self, "Movimiento inválido", "Cantidad inválida o excede el montón")
            except ValueError:
                QMessageBox.warning(self, "Entrada inválida", "Por favor introduzca un número válido")


    def machine_move(self):
        if self.can_move():
            # Convierte los montones actuales en una lista de strings
            piles_as_str = list(map(str, self.piles))

            # Ejecuta el script de Haskell usando subprocess
            result = subprocess.run(
                ['runhaskell', 'haskell version/NimAI.hs'] + piles_as_str,
                capture_output=True, text=True
            )

            # Verificamos si hubo un error en la ejecución
            if result.returncode != 0:
                QMessageBox.critical(self, "Error", "Hubo un error al ejecutar la lógica de la máquina.")
                return

            # Obtener la salida como una lista de enteros (nuevo estado de los montones)
            new_piles = list(map(int, result.stdout.strip().split()))

            # Determinar el movimiento de la máquina
            movement_info = []
            for i in range(len(self.piles)):
                if new_piles[i] < self.piles[i]:  # Si la máquina retiró piezas
                    pieces_taken = self.piles[i] - new_piles[i]  # Calcular cuántas piezas se retiraron
                    movement_info.append((i, pieces_taken))  # Guardar el índice del montón y la cantidad retirada

            # Actualizar los montones y etiquetas
            for i in range(len(self.piles)):
                self.piles[i] = new_piles[i]
                self.labels[i].setText(f"Montón {i + 1}: {self.piles[i]} piezas")

            # Mostrar mensaje con el movimiento realizado por la máquina
            if movement_info:
                for pile_index, quantity_removed in movement_info:
                    QMessageBox.information(self, "Movimiento de la Máquina", 
                                            f"La máquina ha retirado {quantity_removed} pieza(s) del montón {pile_index + 1}.")

            # Llamar para ocultar los montones vacíos
            self.hide_empty_piles()

            # Verificar si la máquina pierde
            if self.check_loser(2):
                return

            # Cambiar de vuelta al jugador 1
            self.current_player = 1
            self.turn_label.setText(f"Turno de {self.nickname}")  # Usar el apodo en el turno
        else:
            self.declare_winner(2)  # La máquina pierde si no puede mover


    def hide_empty_piles(self):
        for i in range(len(self.piles)):
            if self.piles[i] == 0:
                self.labels[i].setVisible(False)  # Ocultar la etiqueta
                self.entries[i].setVisible(False)  # Ocultar el campo de entrada
                self.buttons[i].setVisible(False)  # Ocultar el botón


    def clear_inputs(self):
        for entry in self.entries:
            entry.clear()  # Limpia cada campo de entrada


    def can_move(self):
        return any(pile > 0 for pile in self.piles)


    def check_loser(self, player):
        if not self.can_move():
            winner = "Máquina" if player == 2 else f"{self.nickname}"
            self.declare_winner(winner)
            return True
        return False


    def declare_winner(self, winner):
        QMessageBox.information(self, "Fin del juego", f"¡{winner} ha ganado!")
        self.reset_game()


    def reset_game(self):
        self.num_piles = random.randint(5, 20)
        self.piles = [random.randint(1, 7) for _ in range(self.num_piles)]

        for i, pile in enumerate(self.piles):
            self.labels[i].setText(f"Montón {i+1}: {pile} piezas")
            self.entries[i].clear()

        self.current_player = 1
        self.turn_label.setText(f"{self.nickname}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NimGame()
    ex.show()
    sys.exit(app.exec_())