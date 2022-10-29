from ctypes import cast, POINTER

import cv2
import mediapipe as mp
import pynput
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from Detecting import Detection
from constants import *


def processImage(capRead):
    ret, frame = capRead
    frame = cv2.flip(frame, 1)

    # Recolor image to RGB
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img.flags.writeable = False

    # Make detection
    results = hands.process(img)

    # Recolor back to BGR
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # cv2.rectangle(img, (100, 30), (wCam - 100, hCam - 200), (255, 0, 255), 2)

    return results, img


def volumeControl():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    det = Detection(mp_hands)

    det.getMonitorSize()

    cap = cv2.VideoCapture(0)
    mouse = pynput.mouse.Controller()
    volume = volumeControl()
    hands = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.75, max_num_hands=1)

    state = None
    stateCounter = {FIST: 0, VOLUME: 0, SCROLL: 0, SLOWSCROLL: 0,
                    CURSOR: 0, VOLUME_EXIT: 0, CURSOR_EXIT: 0, NEXT_TRACK: 0,
                    PREVIOUS_TRACK: 0, PAUSE: 0, MUTE: 0}
    actionCounter = {PRESS: 0, RELEASE: 0, ACTIVE: 0, SCROLL: 0}
    while cap.isOpened():
        resultsHands, image = processImage(cap.read())
        if resultsHands.multi_hand_landmarks is not None and resultsHands.multi_handedness[0].classification[
            0].label != "Left":
            try:
                det.setLandmarks(resultsHands.multi_hand_landmarks[0].landmark)
                match state:
                    # region FIST
                    case 1:  # FIST
                        if det.isItVolumeControl():
                            stateCounter[VOLUME] += 1
                            if stateCounter[VOLUME] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = VOLUME
                        else:
                            stateCounter[VOLUME] = stateCounter[VOLUME] - 1 if stateCounter[VOLUME] > 0 else 0

                        if det.isItScrollControl():
                            stateCounter[SCROLL] += 1
                            if stateCounter[SCROLL] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = SCROLL
                        else:
                            stateCounter[SCROLL] = stateCounter[SCROLL] - 1 if stateCounter[SCROLL] > 0 else 0

                        if det.isItCursorControl():
                            stateCounter[CURSOR] += 1
                            if stateCounter[CURSOR] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = CURSOR
                        else:
                            stateCounter[CURSOR] = stateCounter[CURSOR] - 1 if stateCounter[CURSOR] > 0 else 0

                        if det.isItNextTrack():
                            stateCounter[NEXT_TRACK] += 1
                            if stateCounter[NEXT_TRACK] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = NEXT_TRACK
                        else:
                            stateCounter[NEXT_TRACK] = stateCounter[NEXT_TRACK] - 1 \
                                if stateCounter[NEXT_TRACK] > 0 else 0

                        if det.isItPreviousTrack():
                            stateCounter[PREVIOUS_TRACK] += 1
                            if stateCounter[PREVIOUS_TRACK] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = PREVIOUS_TRACK
                        else:
                            stateCounter[PREVIOUS_TRACK] = stateCounter[PREVIOUS_TRACK] - 1 \
                                if stateCounter[PREVIOUS_TRACK] > 0 else 0

                        if det.isItPause():
                            stateCounter[PAUSE] += 1
                            if stateCounter[PAUSE] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = PAUSE
                        else:
                            stateCounter[PAUSE] = stateCounter[PAUSE] - 1 \
                                if stateCounter[PAUSE] > 0 else 0

                        if det.isItMute():
                            stateCounter[MUTE] += 1
                            if stateCounter[MUTE] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[counter] = 0
                                state = MUTE
                        else:
                            stateCounter[MUTE] = stateCounter[MUTE] - 1 \
                                if stateCounter[MUTE] > 0 else 0
                        image = cv2.putText(image, 'Fist', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                        print("FIST")
                    # endregion
                    # region VOLUME
                    case 2:  # VOLUME
                        print("volume")
                        thumb_x, thumb_y = det.coords[THUMB_TIP]
                        index_x, index_y = det.coords[INDEX_FINGER_TIP]

                        cv2.circle(image, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
                        cv2.circle(image, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)

                        cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)

                        volume.SetMasterVolumeLevel(det.getVolume(), None)

                        if det.volumeControlExit():
                            stateCounter[VOLUME_EXIT] += 1
                            if stateCounter[VOLUME_EXIT] > CONFIRMATION:
                                stateCounter[VOLUME_EXIT] = 0
                                state = "Default"
                        else:
                            stateCounter[VOLUME_EXIT] = stateCounter[VOLUME_EXIT] - 1 \
                                if stateCounter[VOLUME_EXIT] > 0 else 0
                        image = cv2.putText(image, 'Volume', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region SCROLL
                    case 3:  # SCROLL
                        print("scroll")

                        if det.scrollUp():
                            actionCounter[SCROLL] += 1
                            if actionCounter[SCROLL] > 4:
                                mouse.scroll(0, SCROLL_SPEED)
                                actionCounter[SCROLL] = 0

                        if det.scrollDown():
                            actionCounter[SCROLL] += 1
                            if actionCounter[SCROLL] > 4:
                                mouse.scroll(0, -SCROLL_SPEED)
                                actionCounter[SCROLL] = 0

                        if det.isItFist():
                            stateCounter[FIST] += 1
                            if stateCounter[FIST] > CONFIRMATION:
                                stateCounter[FIST], stateCounter[SLOWSCROLL] = 0, 0
                                state = "Default"
                        else:
                            stateCounter[FIST] = stateCounter[FIST] - 1 \
                                if stateCounter[FIST] > 0 else 0

                        if det.isItSlowScroll():
                            stateCounter[SLOWSCROLL] += 1
                            if stateCounter[SLOWSCROLL] > CONFIRMATION:
                                stateCounter[FIST], stateCounter[SLOWSCROLL] = 0, 0
                                state = SLOWSCROLL
                        else:
                            stateCounter[SLOWSCROLL] = stateCounter[SLOWSCROLL] - 1 \
                                if stateCounter[SLOWSCROLL] > 0 else 0
                        image = cv2.putText(image, 'Scroll', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region SLOWSCROLL
                    case 4:  # SLOWSCROLL
                        print("slowscroll")

                        if actionCounter[ACTIVE] == 0:

                            if det.thumbRelease():
                                actionCounter[RELEASE] += 1
                            else:
                                actionCounter[RELEASE] = 0
                            if actionCounter[RELEASE] > ACTION_CONFIRMATION:
                                actionCounter[RELEASE] = 0
                                actionCounter[ACTIVE] = 1
                                actionCounter[PRESS] = 0
                        else:
                            if det.thumbClick():
                                actionCounter[PRESS] += 1
                            else:
                                actionCounter[PRESS] = 0
                            if actionCounter[PRESS] > ACTION_CONFIRMATION:
                                actionCounter[RELEASE] = 0
                                actionCounter[ACTIVE] = 0
                                actionCounter[PRESS] = 0

                                if det.scrollUp():
                                    mouse.scroll(0, SCROLL_SPEED)

                                if det.scrollDown():
                                    mouse.scroll(0, -SCROLL_SPEED)

                        if det.isItFist():
                            stateCounter[FIST] += 1
                            if stateCounter[FIST] > CONFIRMATION:
                                stateCounter[FIST] = 0
                                state = "Default"
                        else:
                            stateCounter[FIST] = stateCounter[FIST] - 1 \
                                if stateCounter[FIST] > 0 else 0
                        image = cv2.putText(image, 'Slow scroll', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region CURSOR
                    case 5:  # CURSOR
                        print("cursor")
                        mouse.position = det.getCursorPosition()

                        if actionCounter[ACTIVE] == 0:

                            if det.thumbRelease():
                                actionCounter[RELEASE] += 1
                            else:
                                actionCounter[RELEASE] = 0
                            if actionCounter[RELEASE] > ACTION_CONFIRMATION:
                                actionCounter[RELEASE] = 0
                                actionCounter[ACTIVE] = 1
                                actionCounter[PRESS] = 0
                        else:
                            if det.thumbClick():
                                actionCounter[PRESS] += 1
                            else:
                                actionCounter[RELEASE] = 0
                            if actionCounter[PRESS] > ACTION_CONFIRMATION:
                                actionCounter[RELEASE] = 0
                                actionCounter[ACTIVE] = 0
                                actionCounter[PRESS] = 0

                                mouse.click(pynput.mouse.Button.left, 1)

                        if det.isItCursorExit():
                            stateCounter[CURSOR_EXIT] += 1
                            if stateCounter[CURSOR_EXIT] > CONFIRMATION:
                                stateCounter[CURSOR_EXIT] = 0
                                state = "Default"
                        else:
                            stateCounter[CURSOR_EXIT] = stateCounter[CURSOR_EXIT] - 1 if stateCounter[CURSOR_EXIT] > 0 \
                                else 0

                        image = cv2.putText(image, 'Cursor', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region NEXT_TRACK
                    case 6:
                        print("Next track")
                        pynput.keyboard.Controller().press(pynput.keyboard.Key.media_next)
                        pynput.keyboard.Controller().release(pynput.keyboard.Key.media_next)
                        state = "Next track"
                        image = cv2.putText(image, 'PREVIOUS_TRACK', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region PREVIOUS_TRACK
                    case 7:
                        print("Previous track")
                        pynput.keyboard.Controller().press(pynput.keyboard.Key.media_previous)
                        pynput.keyboard.Controller().release(pynput.keyboard.Key.media_previous)
                        state = "Default"
                        image = cv2.putText(image, 'Next_track', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region PLAY_PAUSE
                    case 8:
                        print("Play/pause")
                        pynput.keyboard.Controller().press(pynput.keyboard.Key.media_play_pause)
                        pynput.keyboard.Controller().release(pynput.keyboard.Key.media_play_pause)
                        state = "Default"
                        image = cv2.putText(image, 'Play/pause', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region MUTE_UNMUTE
                    case 9:
                        print("Mute/Unmute")
                        pynput.keyboard.Controller().press(pynput.keyboard.Key.media_volume_mute)
                        pynput.keyboard.Controller().release(pynput.keyboard.Key.media_volume_mute)
                        state = "Default"
                        image = cv2.putText(image, 'Mute/Unmute', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
                    # region DEFAULT
                    case _:  # DEFAULT
                        if det.isItFist():
                            stateCounter[FIST] += 1
                            if stateCounter[FIST] > CONFIRMATION:
                                for counter in stateCounter.keys():
                                    stateCounter[FIST] = 0
                                state = FIST
                        else:
                            stateCounter[FIST] = stateCounter[FIST] - 1 if stateCounter[FIST] > 0 else 0
                        # det.test()
                        print("DEFAULT")
                        image = cv2.putText(image, 'DEFAULT', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (255, 0, 255), 2, cv2.LINE_AA)
                    # endregion
            except Exception as e:
                print(e)

            # if resultsHands.multi_hand_landmarks:
            #     for num, hand in enumerate(resultsHands.multi_hand_landmarks):
            #         mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
            #                                   mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
            #                                   mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
            #                                                          circle_radius=2),
            #                                   )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
