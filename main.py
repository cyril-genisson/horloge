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
# d'un popup. En effet je viens de me rendre compte que j'avais mal
# conçu le code. La classe Clock gère l'intégralité de l'affichage
# alors que j'aurais dû la créer comme un widget urwid pour pouvoir ajouter
# de nouveaux composants comme un menu. Je reprendrais ce travail pour en avoir
# une version plus convenable. Donc à défaut, je configure une alarme dès le
# lancement du programme. Bon, c'est pas beau mais ça marche...

import time
import urwid


class Clock:
    def __init__(self, alarm=None):
        self.format = "%H:%M:%S"
        self.alarm = alarm
        self.state = {"MODE": False, "ALARM": False, "BREAK": False}
        if self.alarm:
            self.text_alarm = self.alarm[1]
            self.hour_alarm24 = f"{int(self.alarm[0][0]):02d}:{int(self.alarm[0][1]):02d}:{int(self.alarm[0][2]):02d}"
            if int(self.alarm[0][0]) < 12:
                self.hour_alarm12 = f"{int(self.alarm[0][0]):02d}:{int(self.alarm[0][1]):02d}:{int(self.alarm[0][2]):02d} AM"
            else:
                self.hour_alarm12 = f"{int(self.alarm[0][0]) % 12:02d}:{int(self.alarm[0][1]):02d}:{int(self.alarm[0][2]):02d} PM"
            self.hour_alarm_str = self.hour_alarm24
        else:
            self.hour_alarm_str = None
        self.configure_clock()
        self.palette = [("clock", "dark blue", "")]
        self.loop = urwid.MainLoop(
                self.clock,
                self.palette,
                unhandled_input=self.unhandled_input)
        self.loop.set_alarm_in(0.1, self.update)


    def update(self, loop=None, user_data=None):
        if not self.state["BREAK"]:
            self.configure_clock()
            if self.state["ALARM"]:
                loop.widget = self.clock
                loop.set_alarm_in(5, self.update)
            else:
                loop.widget = self.clock
                loop.set_alarm_in(0.1, self.update)
        else:
            loop.set_alarm_in(0.1, self.update)


    def configure_clock(self):
        text = time.strftime(self.format)
        if text == self.hour_alarm_str:
            self.state["ALARM"] = True
            text = self.text_alarm
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
        else:
            self.state["ALARM"] = False

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
                if self.alarm:
                    self.hour_alarm_str = self.hour_alarm12
            else:
                self.state["MODE"] = False
                self.format = "%H:%M:%S"
                if self.alarm:
                    self.hour_alarm_str = self.hour_alarm24

        if key in ("p", "P"):
            if not self.state["BREAK"]:
                self.state["BREAK"] = True
            else:
                self.state["BREAK"] = False


def alarm():
    if input("Do you want a alarm [y/n]: ") == 'y':
        alarm_time = input("Input time format 24h hh:mm:ss): ")
        alarm_title = input("Title [ALARM]: ")
        if not len(alarm_title):
            alarm_title = "ALARM"
        return (alarm_time.split(":"), alarm_title)
    else:
        return None


def main():
    timer = alarm()
    print(timer)
    clock = Clock(alarm=timer)
    clock.start()


if __name__ == "__main__":
    main()
