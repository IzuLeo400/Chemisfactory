class Action():
    """
    The abstract class for an action preformed by an entity \n Arguments:

    1: entity -- Player or PhysicsEntity -- what is preforming the action

    2: Name -- String -- The name of the action preformed

    2: Start -- method -- ran when at the start of the action sequence

    3: Update -- method -- ran periodically while action is being preformed

    4: End -- method -- ran at the end of the action sequence 
        Arguments:
        -- interrupted -- boolean -- True if the action was interrupted
    """
    def __init__(self, entity, name='',  start=None, update=None, end=None):
        self.m_entity = entity
        self.m_name = name
        self.m_start = start
        self.m_update = update
        self.m_end = end

    def start(self):
        self.m_start()

    def update(self):
        self.m_update()

    def end(self, interrupted):
        self.m_end(interrupted)

