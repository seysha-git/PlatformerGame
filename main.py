from game import *

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.showd_go_screen()