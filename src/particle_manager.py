from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect


class ParticleManager:
    def __init__(self):
        self.anim_group = QParallelAnimationGroup()

    def emit_particle(self, parent_widget, position):
        if self.anim_group.state() == QParallelAnimationGroup.State.Running:
            return

        particle = self.create_particle(parent_widget, position)
        self.setup_animations(particle)
        self.start_animations()
        self.setup_cleanup(particle)

    @staticmethod
    def create_particle(parent_widget, position: QPoint):
        particle = QLabel(parent_widget)
        pixmap = QPixmap('sprites/cupcake.png')
        particle.setPixmap(pixmap)
        particle.setScaledContents(True)
        particle.setFixedSize(42, 42)
        particle.move(position.x() + 4, position.y())
        particle.show()
        return particle

    def setup_animations(self, particle):
        self.setup_movement_animation(particle)
        self.setup_opacity_animation(particle)

    def setup_movement_animation(self, particle):
        animation = QPropertyAnimation(particle, b"geometry")
        animation.setDuration(1500)
        end_rect = QRect(particle.x(), particle.y() - particle.height(), 10, 10)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim_group.addAnimation(animation)

    def setup_opacity_animation(self, particle):
        opacity_effect = QGraphicsOpacityEffect(particle)
        particle.setGraphicsEffect(opacity_effect)
        opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_animation.setDuration(2000)
        opacity_animation.setStartValue(1)
        opacity_animation.setEndValue(0)
        self.anim_group.addAnimation(opacity_animation)

    def start_animations(self):
        self.anim_group.start()

    def setup_cleanup(self, particle):
        self.anim_group.finished.connect(particle.deleteLater)
