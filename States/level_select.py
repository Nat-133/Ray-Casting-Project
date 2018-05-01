import template.template as template


class LevelSelect(template.State):
    
    def __init__(self, screen):
        super().__init__(screen, "levelSelect")
