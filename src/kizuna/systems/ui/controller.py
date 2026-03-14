from kizuna.core.controllers import Controller
from kizuna.rendering import DrawBatch, TextDrawable


batch = DrawBatch()


class UIController(Controller):


    def on_init(self):
        self.label = TextDrawable('Hello Kizuna!', (50, 50))

    def on_draw(self):
        self.label.on_prepare_draw(batch)
        batch.draw()
