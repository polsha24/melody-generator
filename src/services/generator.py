from entities.scale import Scale
from entities.melody import Melody

class MelodyGenerator:
    """
    Генерирует мелодию на основе гаммы и параметров
    """
    def __init__(self, scale: Scale, bars: int, tempo: int):
        self.scale = scale
        self.bars = bars
        self.tempo = tempo

    def generate(self) -> Melody:
        """
        Возвращает экземпляр Melody
        """
        pass
