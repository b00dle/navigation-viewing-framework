#!/usr/bin/python

import avango
import avango.gua
import avango.script
import avango.daemon

from TUIOObjects import *

class TouchDevice(avango.script.Script):

    movement_changed = avango.SFBool()
    pos_changed = avango.SFFloat()
    cursors = avango.MFContainer()
    hands = avango.MFContainer()

    ## Default constructor.
    def __init__(self):
        self.super(TouchDevice).__init__()

        self.active_hands = {}

        self.frame_counter = 0

        self.input_changed = False

        # add touch cursors
        for i in range(0, 20):
            cursor = TUIOCursor(CursorID = i) 
            self.cursors.value.append(cursor)
            self.movement_changed.connect_from(cursor.IsMoving)
            self.pos_changed.connect_from(cursor.PosX)
            self.pos_changed.connect_from(cursor.PosY)

        # add hands (just one for now since we don't support separate views for users yet)
        for i in range(0, 4):
            hand = TUIOHand(HandID  = i)
            self.hands.value.append(hand)
            self.active_hands[hand.HandID.value] = []

        self.always_evaluate(True)


    def evaluate(self):
        self.frame_counter += 1
        self.processChange()

    def processChange(self):

        #if -1.0 == self.pos_changed.value:
        #    return

        self.input_changed = True

        # update active point list
        hands        = {}
        inputGiven   = False

        for handID in self.active_hands:
            self.active_hands[handID] = []

        for touchPoint in self.cursors.value:
            for hand in self.hands.value:
                if touchPoint.IsTouched.value and touchPoint.SessionID.value in hand.FingerSIDs.value:
                    inputGiven = True
                    self.active_hands[hand.HandID.value].append(touchPoint)
                    hands[hand.HandID.value] = hand
                    break

        if inputGiven:
            pass
        else:
            pass
