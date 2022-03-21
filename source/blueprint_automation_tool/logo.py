"""
File:           logo.py
Description:    test to check world edit placement in-game

Author(s):      Kevin Green
"""
from game_automation import GameAutomator

g = GameAutomator()
g.switch_to_game()

g.send_to_chat("/tp @p 0 -40 0 0 90")
BLOCK = "minecraft:blue_concrete"

y = -60

g.pos1(10, y, 11)
g.pos2(-13, y, -9)
g.send_to_chat("//set 0")

g.pos1(8, y, 9)
g.pos2(8, y, 7)
g.line(BLOCK)
g.pos1(6, y, 5)
g.line(BLOCK)
g.pos2(6, y, 4)
g.line(BLOCK)
g.pos1(4, y, 2)
g.line(BLOCK)
g.pos2(3, y, 2)
g.line(BLOCK)
g.pos1(3, y, 4)
g.line(BLOCK)
g.pos1(1, y, -1)
g.line(BLOCK)
g.pos2(-1, y, -1)
g.line(BLOCK)
g.pos1(-3, y, 2)
g.line(BLOCK)
g.pos2(-3, y, 3)
g.line(BLOCK)
g.pos2(-5, y, 2)
g.line(BLOCK)
g.pos1(-8, y, 4)
g.line(BLOCK)
g.pos2(-11, y, 7)
g.line(BLOCK)
g.pos1(-11, y, 9)
g.line(BLOCK)
g.pos2(-6, y, 9)
g.line(BLOCK)
g.pos1(-4, y, 7)
g.line(BLOCK)
g.pos2(-4, y, 6)
g.line(BLOCK)
g.pos1(-3, y, 5)
g.line(BLOCK)
g.pos2(-1, y, 7)
g.line(BLOCK)
g.pos1(0, y, 6)
g.line(BLOCK)
g.pos2(1, y, 6)
g.line(BLOCK)
g.pos1(2, y, 7)
g.line(BLOCK)
g.pos2(3, y, 6)
g.line(BLOCK)
g.pos1(5, y, 9)
g.line(BLOCK)
g.pos2(8, y, 9)
g.line(BLOCK)

g.send_to_chat("//paste")

g.pos1(10, y, 11)
g.pos2(10, y, -9)
g.line(BLOCK)
g.pos1(-13, y, -9)
g.line(BLOCK)
g.pos2(-13, y, 11)
g.line(BLOCK)
g.pos1(10, y, 11)
g.line(BLOCK)

g.send_to_chat("Done!")