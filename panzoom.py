class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PanZoom:
    def __init__(self, offsetX=0.0, offsetY=0.0, scale=1.0, minZoom=0.4, maxZoom=10.0):
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.scale = scale
        self.minZoom = minZoom
        self.maxZoom = maxZoom
        self.click = True
        self.drag = False
        self.dragStart = Point(0.0, 0.0)
        self.dragEnd = Point(0.0, 0.0)

    @property
    def OffsetX(self):
        return self.offsetX

    @OffsetX.setter
    def OffsetX(self, value):
        self.offsetX = value

    @property
    def OffsetY(self):
        return self.offsetY

    @OffsetY.setter
    def OffsetY(self, value):
        self.offsetY = value

    @property
    def Scale(self):
        return self.scale

    @Scale.setter
    def Scale(self, value):
        self.scale = min(max(self.minZoom, value), self.maxZoom)

    @property
    def MinZoom(self):
        return self.minZoom

    @MinZoom.setter
    def MinZoom(self, value):
        if value <= 0:
            raise ValueError("minZoom must be greater than 0")
        self.minZoom = value

    @property
    def MaxZoom(self):
        return self.maxZoom

    @MaxZoom.setter
    def MaxZoom(self, value):
        if value <= 0:
            raise ValueError("maxZoom must be greater than 0")
        self.maxZoom = value

    def WorldToScreenX(self, worldX):
        return (worldX - self.OffsetX) * self.Scale

    def WorldToScreenY(self, worldY):
        return (worldY - self.OffsetY) * self.Scale

    def ScreenToWorldX(self, screenX):
        return (screenX / self.Scale) + self.OffsetX

    def ScreenToWorldY(self, screenY):
        return (screenY / self.Scale) + self.OffsetY

    def MouseDown(self, mouseX, mouseY):
        self.dragStart.x = mouseX
        self.dragStart.y = mouseY
        self.drag = True

    def MouseMove(self, mouseX, mouseY):
        if self.drag:
            if self.click:
                self.click = False

            self.dragEnd.x = mouseX
            self.dragEnd.y = mouseY

            self.OffsetX -= (self.dragEnd.x - self.dragStart.x) / self.Scale
            self.OffsetY -= (self.dragEnd.y - self.dragStart.y) / self.Scale

            self.dragStart.x = self.dragEnd.x
            self.dragStart.y = self.dragEnd.y

    def MouseUp(self):
        self.drag = False

    def MouseWheel(self, mouseX, mouseY, delta):
        mouseBeforeZoomX = self.ScreenToWorldX(mouseX)
        mouseBeforeZoomY = self.ScreenToWorldY(mouseY)

        self.Scale += delta * (-0.001) * (self.Scale / 2)
        self.Scale = min(max(self.MinZoom, self.Scale), self.MaxZoom)

        mouseAfterZoomX = self.ScreenToWorldX(mouseX)
        mouseAfterZoomY = self.ScreenToWorldY(mouseY)

        self.OffsetX += (mouseBeforeZoomX - mouseAfterZoomX)
        self.OffsetY += (mouseBeforeZoomY - mouseAfterZoomY)
