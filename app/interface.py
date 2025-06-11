import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QLabel, QSlider
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect

# Importa a função de lógica
from app.gerador import gerar_senha

class JanelaGerador(QMainWindow):
    """
    Classe principal da janela da aplicação.
    Herda de QMainWindow para ter funcionalidades de uma janela padrão.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerador de Senhas Seguro")
        self.setFixedSize(450, 340)  # Janela com tamanho fixo

        widget_central = QWidget()
        self.layout_principal = QVBoxLayout(widget_central)
        self.layout_principal.setContentsMargins(25, 20, 25, 20)
        self.layout_principal.setSpacing(15)

        self.setCentralWidget(widget_central)

        self.initUI()
        self.aplicar_estilos()

    def initUI(self):
        """Cria e organiza todos os componentes (widgets) da interface."""
        self.label_titulo = QLabel("Gerador de Senhas Seguro")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_principal.addWidget(self.label_titulo)
        self.layout_principal.addStretch(1)

        layout_senha = QHBoxLayout()
        self.campo_senha = QLineEdit()
        self.campo_senha.setReadOnly(True)
        self.campo_senha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_senha.addWidget(self.campo_senha)

        self.botao_copiar = QPushButton("Copiar")
        self.botao_copiar.setFixedWidth(70)
        self.botao_copiar.clicked.connect(self.copiar_senha)
        layout_senha.addWidget(self.botao_copiar)
        self.layout_principal.addLayout(layout_senha)

        layout_tamanho_label = QHBoxLayout()
        label_tamanho_texto = QLabel("Tamanho da Senha:")
        self.label_tamanho_valor = QLabel("16")
        
        # Centraliza o rótulo de valor para a animação parecer correta
        self.label_tamanho_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_tamanho_label.addWidget(label_tamanho_texto)
        layout_tamanho_label.addStretch()
        layout_tamanho_label.addWidget(self.label_tamanho_valor)
        self.layout_principal.addLayout(layout_tamanho_label)
        
        self.slider_tamanho = QSlider(Qt.Orientation.Horizontal)
        self.slider_tamanho.setRange(8, 32)
        self.slider_tamanho.setValue(16)
        self.slider_tamanho.valueChanged.connect(self.atualizar_label_tamanho)
        self.layout_principal.addWidget(self.slider_tamanho)
        
        self.layout_principal.addStretch(1)

        self.botao_gerar = QPushButton("Gerar Nova Senha")
        self.botao_gerar.clicked.connect(self.gerar_nova_senha)
        self.layout_principal.addWidget(self.botao_gerar)
        
    def aplicar_estilos(self):
        """Aplica uma folha de estilos (tipo CSS) para customizar a aparência."""
        self.setStyleSheet("""
            * {
                font-family: Inter, sans-serif;
            }
            QMainWindow {
                background-color: #f8fafc;
            }
            QLabel {
                color: #334155;
                font-size: 14px;
            }
            QLabel#label_titulo {
                font-size: 22px;
                font-weight: bold;
            }
            QLabel#label_tamanho_valor {
                font-size: 14px;
                font-weight: bold;
                color: #4338ca;
                background-color: #e0e7ff;
                padding: 4px 0px; /* Padding vertical, horizontal é controlado pelo min-width */
                border-radius: 12px;
                min-width: 40px; /* Garante tamanho mínimo para o rótulo */
            }
            QLineEdit {
                background-color: white;
                color: #0f172a;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 20px;
                font-family: "Courier New";
            }
            QLineEdit:focus {
                border: 1px solid #4f46e5;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
            QPushButton:focus {
                border: 2px solid #6366f1;
            }
            QPushButton#botao_copiar {
                background-color: #eef2ff;
                color: #4338ca;
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton#botao_copiar:hover {
                background-color: #e0e7ff;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #e2e8f0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4f46e5;
                border: 2px solid white;
                width: 20px;
                height: 20px;
                margin: -8px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #4338ca;
            }
            /* Efeito "pop" no seletor ao ser pressionado */
            QSlider::handle:horizontal:pressed {
                background: #3730a3;
                width: 24px;
                height: 24px;
                margin: -10px 0;
                border-radius: 12px;
            }
        """)
        self.label_titulo.setObjectName("label_titulo")
        self.botao_gerar.setObjectName("botao_gerar")
        self.botao_copiar.setObjectName("botao_copiar")
        self.label_tamanho_valor.setObjectName("label_tamanho_valor")

    # --- Slots (Funções que respondem a sinais/eventos) ---

    def gerar_nova_senha(self):
        """Pega o valor do slider, chama a função de lógica e atualiza o campo."""
        tamanho = self.slider_tamanho.value()
        senha = gerar_senha(tamanho)
        self.campo_senha.setText(senha)

    def copiar_senha(self):
        """Copia o conteúdo do campo da senha para a área de transferência."""
        clipboard = QGuiApplication.clipboard()
        if self.campo_senha.text():
            clipboard.setText(self.campo_senha.text())
            original_text = self.botao_copiar.text()
            self.botao_copiar.setText("Copiado!")
            self.botao_copiar.setEnabled(False)
            QTimer.singleShot(1500, lambda: (
                self.botao_copiar.setText(original_text),
                self.botao_copiar.setEnabled(True)
            ))
        
    def atualizar_label_tamanho(self, valor):
        """Atualiza o label com o valor atual do slider e dispara a animação."""
        self.label_tamanho_valor.setText(str(valor))
        self.animar_label_pop()

    def animar_label_pop(self):
        """Cria uma animação de 'pop' para o label do tamanho."""
        # Configuração da animação de crescimento
        self.anim_crescer = QPropertyAnimation(self.label_tamanho_valor, b"geometry")
        self.anim_crescer.setDuration(100)
        self.anim_crescer.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Pega a geometria atual e calcula a geometria "crescida"
        geometria_atual = self.label_tamanho_valor.geometry()
        geometria_maior = QRect(geometria_atual.x() - 2, geometria_atual.y() - 2, 
                                geometria_atual.width() + 4, geometria_atual.height() + 4)
        
        self.anim_crescer.setStartValue(geometria_atual)
        self.anim_crescer.setEndValue(geometria_maior)

        # Configuração da animação de encolhimento de volta ao normal
        self.anim_encolher = QPropertyAnimation(self.label_tamanho_valor, b"geometry")
        self.anim_encolher.setDuration(150)
        self.anim_encolher.setEasingCurve(QEasingCurve.Type.OutBounce) # Efeito "quicando"
        self.anim_encolher.setStartValue(geometria_maior)
        self.anim_encolher.setEndValue(geometria_atual)

        # Encadeia as animações para que aconteçam em sequência
        self.anim_crescer.finished.connect(self.anim_encolher.start)
        
        # Inicia a animação apenas se não houver outra em andamento
        if hasattr(self, 'anim_crescer') and self.anim_crescer.state() != QPropertyAnimation.State.Running:
            self.anim_crescer.start()


# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaGerador()
    janela.show()
    sys.exit(app.exec())
