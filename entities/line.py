# Classe responsável por representar as linhas adicionadas ao canvas
class Line:
    def __init__(self, initial_pixel, final_pixel) -> None:
        self.initial_pixel = initial_pixel
        self.final_pixel = final_pixel
    