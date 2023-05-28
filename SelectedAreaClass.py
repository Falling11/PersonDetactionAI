class SelectedArea:
    def __init__(self, areaPoints, startTime = 0):

        self.areaPoints = areaPoints
        self.activeTime = 0
        self.passiveTime = 0
        self.startTime = startTime
        self.count = 0
        self.id = 1
