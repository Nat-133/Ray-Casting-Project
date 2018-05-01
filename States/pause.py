import template.template as template


class Pause(template.State):
    
    def __init__(self, screen):
        super().__init(screen, "pause")