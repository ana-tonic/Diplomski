import math
import numpy as np
from screeninfo import get_monitors
from constants import *


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


class Detection:
    def __init__(self, mp_hands):
        self.landmarks = None
        self.mp_hands = mp_hands
        self.coords = dict()
        self.monitor = None
        self.prevMouse = 0, 0

    def getMonitorSize(self):
        for m in get_monitors():
            self.monitor = m.width, m.height

    def setLandmarks(self, landmarks):
        self.landmarks = landmarks
        self.calculateCoords()

    def calculateCoords(self):
        self.coords[WRIST] = (int(self.landmarks[self.mp_hands.HandLandmark.WRIST].x * wCam),
                              int(self.landmarks[self.mp_hands.HandLandmark.WRIST].y * hCam))
        self.coords[THUMB_CMC] = (int(self.landmarks[self.mp_hands.HandLandmark.THUMB_CMC].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.THUMB_CMC].y * hCam))
        self.coords[THUMB_MCP] = (int(self.landmarks[self.mp_hands.HandLandmark.THUMB_MCP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.THUMB_MCP].y * hCam))
        self.coords[THUMB_IP] = (int(self.landmarks[self.mp_hands.HandLandmark.THUMB_IP].x * wCam),
                                 int(self.landmarks[self.mp_hands.HandLandmark.THUMB_IP].y * hCam))
        self.coords[THUMB_TIP] = (int(self.landmarks[self.mp_hands.HandLandmark.THUMB_TIP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.THUMB_TIP].y * hCam))
        self.coords[INDEX_FINGER_DIP] = (int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].x * wCam),
                                         int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].y * hCam))
        self.coords[INDEX_FINGER_MCP] = (int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].x * wCam),
                                         int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y * hCam))
        self.coords[INDEX_FINGER_PIP] = (int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].x * wCam),
                                         int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y * hCam))
        self.coords[INDEX_FINGER_TIP] = (int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * wCam),
                                         int(self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * hCam))
        self.coords[MIDDLE_FINGER_DIP] = (int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x * wCam),
                                          int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * hCam))
        self.coords[MIDDLE_FINGER_MCP] = (int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * wCam),
                                          int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * hCam))
        self.coords[MIDDLE_FINGER_PIP] = (int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * wCam),
                                          int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * hCam))
        self.coords[MIDDLE_FINGER_TIP] = (int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * wCam),
                                          int(self.landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * hCam))
        self.coords[RING_FINGER_DIP] = (int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_DIP].x * wCam),
                                        int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_DIP].y * hCam))
        self.coords[RING_FINGER_MCP] = (int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP].x * wCam),
                                        int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_MCP].y * hCam))
        self.coords[RING_FINGER_PIP] = (int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_PIP].x * wCam),
                                        int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_PIP].y * hCam))
        self.coords[RING_FINGER_TIP] = (int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP].x * wCam),
                                        int(self.landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP].y * hCam))
        self.coords[PINKY_PIP] = (int(self.landmarks[self.mp_hands.HandLandmark.PINKY_PIP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.PINKY_PIP].y * hCam))
        self.coords[PINKY_MCP] = (int(self.landmarks[self.mp_hands.HandLandmark.PINKY_MCP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.PINKY_MCP].y * hCam))
        self.coords[PINKY_DIP] = (int(self.landmarks[self.mp_hands.HandLandmark.PINKY_DIP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.PINKY_DIP].y * hCam))
        self.coords[PINKY_TIP] = (int(self.landmarks[self.mp_hands.HandLandmark.PINKY_TIP].x * wCam),
                                  int(self.landmarks[self.mp_hands.HandLandmark.PINKY_TIP].y * hCam))
        return

    def getVolume(self):
        index_x, index_y = self.coords[INDEX_FINGER_TIP]
        thumb_x, thumb_y = self.coords[THUMB_TIP]
        indexMcp_x, indexMcp_y = self.coords[INDEX_FINGER_MCP]
        x, y = self.coords[WRIST]

        distanceThumbIndex = math.hypot(index_x - thumb_x, index_y - thumb_y)
        palmLength = math.hypot(indexMcp_x - x, indexMcp_y - y)
        return np.interp(distanceThumbIndex, (0, palmLength * 1.5), (-65, 0))

    # region gesture detection

    def isItFist(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.partialFist():
            return False
        if not self.thumbUp():
            return False
        return True

    def isItVolumeControl(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.partialFist():
            return False
        if not self.thumbOut():
            return False
        return True

    def isItScrollControl(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.pinkyRingDown():
            return False
        if not self.thumbRight():
            return False
        if self.indexUp():
            return True
        return False

    def isItCursorControl(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.pinkyRingDown():
            return False
        if not self.indexUp():
            return False
        if not self.middleUp():
            return False
        if not self.thumbOut():
            return False
        return True

    def volumeControlExit(self):
        return self.middleUp()

    def isItSlowScroll(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.isItScroll():
            return False
        if not self.thumbOut():
            return False
        return True

    def scrollUp(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.pinkyRingDown():
            return False
        if not self.middleDown():
            return False
        if not self.indexUp():
            return False
        if not self.thumbRight():
            return False
        return True

    def scrollDown(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.pinkyRingDown():
            return False
        if not self.middleUp():
            return False
        if not self.indexUp():
            return False
        if not self.thumbRight():
            return False
        return True

    def isItScroll(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.pinkyRingDown():
            return False
        if self.indexUp():
            return True
        return False

    def isItNextTrack(self):
        if not self.isHandRight():
            return False
        if not self.isIndexStraight():
            return False
        if not self.halfFistRight():
            return False
        return True

    def isItPreviousTrack(self):
        if not self.isHandLeft():
            return False
        if not self.isIndexStraight():
            return False
        if not self.halfFistLeft():
            return False
        return True

    def isItPause(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.indexUp():
            return False
        if not self.middleUp():
            return False
        if not self.ringUp():
            return False
        if not self.pinkyUp():
            return False
        if not self.thumbOut():
            return False
        return True

    def isItMute(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if not self.indexUp():
            return False
        if not self.middleUp():
            return False
        if not self.ringUp():
            return False
        if not self.pinkyUp():
            return False
        if not self.thumbRight():
            return False
        return True

    # endregion

    def getCursorPosition(self):
        x, y = self.coords.get(INDEX_FINGER_TIP)
        x2 = np.interp(x, (frameR, wCam - frameR), (0, self.monitor[0]))
        y2 = np.interp(y, (30, hCam - 200), (0, self.monitor[1]))
        prevX, prevY = self.prevMouse
        x2, y2 = prevX + (x2 - prevX) / smoothening, prevY + (y2 - prevY) / smoothening
        self.prevMouse = x2, y2
        return x2, y2

    def indexUp(self):
        index_tip, index_dip = self.coords[INDEX_FINGER_TIP], self.coords[INDEX_FINGER_DIP]
        if self.coords[INDEX_FINGER_DIP][1] - self.coords[INDEX_FINGER_TIP][1] < 10:
            return False
        if calculate_angle(self.coords[INDEX_FINGER_TIP], self.coords[INDEX_FINGER_DIP],
                           self.coords[INDEX_FINGER_PIP]) < 160:
            return False
        if calculate_angle((index_tip[0], index_tip[1] + 10), index_tip, index_dip) > 30:
            return False
        return True

    def indexDown(self):
        if self.coords[INDEX_FINGER_TIP][1] < self.coords[INDEX_FINGER_DIP][1]:
            return False
        if self.coords[INDEX_FINGER_TIP][1] < self.coords[INDEX_FINGER_MCP][1]:
            return False
        if self.coords[INDEX_FINGER_TIP][1] > self.coords[WRIST][1]:
            return False
        return True

    def middleDown(self):
        if self.coords[MIDDLE_FINGER_TIP][1] < self.coords[MIDDLE_FINGER_DIP][1]:
            return False
        if self.coords[MIDDLE_FINGER_TIP][1] < self.coords[MIDDLE_FINGER_MCP][1]:
            return False
        if self.coords[MIDDLE_FINGER_TIP][1] > self.coords[WRIST][1]:
            return False
        return True

    def pinkyRingDown(self):
        if self.coords[PINKY_TIP][1] < self.coords[PINKY_DIP][1]:
            return False
        if self.coords[RING_FINGER_TIP][1] < self.coords[RING_FINGER_DIP][1]:
            return False
        if self.coords[PINKY_TIP][1] < self.coords[PINKY_MCP][1]:
            return False
        if self.coords[RING_FINGER_TIP][1] < self.coords[RING_FINGER_MCP][1]:
            return False
        if self.coords[PINKY_TIP][1] > self.coords[WRIST][1]:
            return False
        if self.coords[RING_FINGER_TIP][1] > self.coords[WRIST][1]:
            return False
        return True

    def partialFist(self):
        if not self.pinkyRingDown():
            return False
        if not self.middleDown():
            return False
        if not self.indexDown():
            return False
        if not self.knucklesUp():
            return False
        return True

    def thumbUp(self):
        if self.coords[THUMB_TIP][1] > self.coords[INDEX_FINGER_PIP][1]:
            return False
        return True

    def thumbOut(self):
        if self.coords[THUMB_TIP][0] > self.coords[THUMB_IP][0]:
            return False
        if abs(self.coords[THUMB_TIP][1] - self.coords[THUMB_IP][1]) > 10:
            return False
        if abs(self.coords[THUMB_TIP][1] < self.coords[INDEX_FINGER_DIP][1]) > 10:
            return False
        if self.coords[THUMB_TIP][1] < self.coords[INDEX_FINGER_MCP][1]:
            return False
        return True

    def thumbRight(self):
        if self.coords[THUMB_TIP] < self.coords[THUMB_IP]:
            return False
        return True

    def middleUp(self):
        if self.coords[MIDDLE_FINGER_DIP][1] - self.coords[MIDDLE_FINGER_TIP][1] < 10:
            return False
        if calculate_angle(self.coords[MIDDLE_FINGER_TIP], self.coords[MIDDLE_FINGER_DIP],
                           self.coords[MIDDLE_FINGER_PIP]) < 170:
            return False
        return True

    def thumbRelease(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if calculate_angle(self.coords[THUMB_TIP], self.coords[THUMB_IP],
                           self.coords[THUMB_MCP]) > 170:
            return False
        if self.coords[THUMB_TIP][0] > self.coords[THUMB_IP][0]:
            return False
        return True

    def thumbClick(self):
        if not self.knucklesUp():
            return False
        if not self.palmFrontHandUp():
            return False
        if calculate_angle(self.coords[THUMB_TIP], self.coords[THUMB_IP],
                           self.coords[THUMB_MCP]) > 160:
            return False
        if self.coords[THUMB_TIP][0] < self.coords[THUMB_IP][0]:
            return False
        return True

    def isItCursorExit(self):
        index_x, index_y = self.coords[INDEX_FINGER_TIP]
        middle_x, middle_y = self.coords[MIDDLE_FINGER_TIP]
        distanceThumbIndex = math.hypot(index_x - middle_x, index_y - middle_y)

        indexMcp_x, indexMcp_y = self.coords[INDEX_FINGER_MCP]
        x, y = self.coords[WRIST]
        palmLength = math.hypot(indexMcp_x - x, indexMcp_y - y)

        if distanceThumbIndex < palmLength / 2.3:
            return False
        return True

    def isHandRight(self):
        index_mcp, middle_mcp = self.coords[INDEX_FINGER_MCP], self.coords[MIDDLE_FINGER_MCP]
        if calculate_angle((index_mcp[0], index_mcp[1] + 10), index_mcp, middle_mcp) > 45:
            return False
        if not self.indexRight():
            return False
        return True

    def test(self):
        self.knucklesUp()

    def isIndexStraight(self):
        index_tip, index_dip, index_pip, index_mcp = self.coords[INDEX_FINGER_TIP], self.coords[INDEX_FINGER_DIP], \
                                                     self.coords[INDEX_FINGER_PIP], self.coords[INDEX_FINGER_MCP]
        if calculate_angle(index_tip, index_dip, index_pip) < 160:
            return False
        if calculate_angle(index_dip, index_pip, index_mcp) < 160:
            return False
        return True

    def indexLeft(self):
        index_tip, index_dip, index_pip, index_mcp = self.coords[INDEX_FINGER_TIP][0], \
                                                     self.coords[INDEX_FINGER_DIP][0], \
                                                     self.coords[INDEX_FINGER_PIP][0], self.coords[INDEX_FINGER_MCP][0]
        if index_tip < index_dip < index_pip < index_mcp:
            return True
        return False

    def indexRight(self):
        index_tip, index_dip, index_pip, index_mcp = self.coords[INDEX_FINGER_TIP][0], self.coords[INDEX_FINGER_DIP][0], \
                                                     self.coords[INDEX_FINGER_PIP][0], self.coords[INDEX_FINGER_MCP][0]
        if index_tip > index_dip > index_pip > index_mcp:
            return True
        return False

    def isHandLeft(self):
        index_mcp, middle_mcp = self.coords[INDEX_FINGER_MCP], self.coords[MIDDLE_FINGER_MCP]
        if calculate_angle((index_mcp[0], index_mcp[1] + 10), index_mcp, middle_mcp) > 50:
            return False
        if not self.indexLeft():
            return False
        return True

    def knucklesUp(self):
        index_mcp, middle_mcp = self.coords[INDEX_FINGER_MCP], self.coords[MIDDLE_FINGER_MCP]
        angle = calculate_angle((index_mcp[0], index_mcp[1] + 10), index_mcp, middle_mcp)
        if angle < 60 or angle > 120:
            return False
        return True

    def halfFistRight(self):
        middle_tip, ring_tip, pinky_tip = self.coords[MIDDLE_FINGER_TIP][0], \
                                          self.coords[RING_FINGER_TIP][0], \
                                          self.coords[PINKY_TIP][0]
        middle_mcp, ring_mcp, pinky_mcp = self.coords[MIDDLE_FINGER_MCP][0], \
                                          self.coords[RING_FINGER_MCP][0], \
                                          self.coords[PINKY_MCP][0]

        if middle_tip > middle_mcp: return False
        if ring_tip > ring_mcp: return False
        if pinky_tip > pinky_mcp: return False
        return True

    def halfFistLeft(self):
        middle_tip, ring_tip, pinky_tip = self.coords[MIDDLE_FINGER_TIP][0], \
                                          self.coords[RING_FINGER_TIP][0], \
                                          self.coords[PINKY_TIP][0]
        middle_mcp, ring_mcp, pinky_mcp = self.coords[MIDDLE_FINGER_MCP][0], \
                                          self.coords[RING_FINGER_MCP][0], \
                                          self.coords[PINKY_MCP][0]

        if middle_tip < middle_mcp: return False
        if ring_tip < ring_mcp: return False
        if pinky_tip < pinky_mcp: return False
        return True

    def ringUp(self):
        if self.coords[RING_FINGER_DIP][1] - self.coords[RING_FINGER_TIP][1] < 10:
            return False
        if calculate_angle(self.coords[RING_FINGER_TIP], self.coords[RING_FINGER_DIP],
                           self.coords[RING_FINGER_PIP]) < 170:
            return False
        return True

    def pinkyUp(self):
        if self.coords[PINKY_DIP][1] - self.coords[PINKY_TIP][1] < 10:
            return False
        if calculate_angle(self.coords[PINKY_TIP], self.coords[PINKY_DIP],
                           self.coords[PINKY_PIP]) < 170:
            return False
        return True

    def palmFrontHandUp(self):
        if self.coords[INDEX_FINGER_MCP][0] > self.coords[PINKY_MCP][0]:
            return False
        return True
