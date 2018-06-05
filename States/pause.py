import template.template as template


class Pause(template.State):
    
    def __init__(self):
        super().__init("pause")