#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Project: Clock
# Filename: main.py
# Created: 28/11/2023
#
# Licence: GPLv3
#
# Author: Cyril GENISSON
#
#
# Description: Pour ce projet d'horloge j'ai essayé d'utiliser
# la librairie urwid pour avoir une gestion du terminal
# de type Curses. Je ne suis pas très satisfait du résultat,
# cette librairie semble être parfaite pour se projet mais je
# n'est pas encore réussi à en comprendre toutes ses subtilités.
# Néanmoins ce travail aura eu le mérite de me la faire découvrir.
#
# Les touches claviers pour gérer l'horloge
# q : quitter le programme
# p : mettre en pause l'horloge 
# m : passer du mode 24h au mode 12h (AM/PM) 
#
# je n'ai pas eu le temps de concevoir l'alarme avec l'affichage
# du pop-up. En effet je viens de me rendre compte que j'avais mal
# conçu le code. La classe Clock gère l'intégralité de l'affichage
# alors que j'aurais dû la créer comme un widget urwid pour pouvoir ajouter
# de nouveaux composants comme un menu. Je reprendrais ce travail pour en avoir
# une version beaucoup convenable.

import time
import urwid


class Clock:
    def __init__(self):
        self.format = "%H:%M:%S"
        self.configure_clock()
        self.state = {"MODE": False, "ALARM": False, "BREAK": False}
        self.palette = [("clock", "dark blue", "")]
        self.loop = urwid.MainLoop(
                self.clock,
                self.palette,
                unhandled_input=self.unhandled_input)
        self.loop.set_alarm_in(0.1, self.update)
        self.hours = ('00', '01', '02', '03', '04', '05',
                      '06', '07', '08', '09', '10', '11',
                      '12', '13', '14', '15', '16', '17',
                      '18', '19', '20', '21', '22', '23')
        self.minutes = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09'
                        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                        '50', '51', '52', '53', '54', '55', '56', '57', '58', '59')
        self.seconds = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09'
                        '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
                        '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
                        '50', '51', '52', '53', '54', '55', '56', '57', '58', '59')

    def update(self, loop=None, user_data=None):
        if not self.state["BREAK"]:
            self.configure_clock()
            loop.widget = self.clock
            loop.set_alarm_in(0.1, self.update)
        else:
            loop.set_alarm_in(0.1, self.update)

    def configure_clock(self):
        text = time.strftime(self.format)
        font = urwid.font.HalfBlock7x7Font()
        self.text_clock = urwid.BigText(text, font)
        self.clock = urwid.Filler(
                urwid.AttrMap(
                    urwid.Padding(
                        self.text_clock,
                        "center",
                        width="clip"
                        ), "clock"
                    ), "middle"
                )

    def start(self):
        self.loop.run()

    def unhandled_input(self, key):
        if key in ("q", "Q"):
            raise urwid.ExitMainLoop()
        if key in ("m", "M"):
            if not self.state["MODE"]:
                self.state["MODE"] = True
                self.format = "%I:%M:%S %p"
            else:
                self.state["MODE"] = False
                self.format = "%H:%M:%S"
        if key in ("p", "P"):
            if not self.state["BREAK"]:
                self.state["BREAK"] = True
            else:
                self.state["BREAK"] = False


def main():
    clock = Clock()
    clock.start()


if __name__ == "__main__":
    main()
