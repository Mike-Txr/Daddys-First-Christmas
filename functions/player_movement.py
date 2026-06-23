import arcade
import functions.settings as settings
import functions.key_handler as kh
import functions.collision_logic as colls

directions = {"x":0, "y":0}


def calc_movement(): #function to calculate movement of the player based on currently pressed keys
    up = arcade.key.W in kh.current_pressed
    down = arcade.key.S in kh.current_pressed
    directions["y"] = up - down #amount of pixels to move in y direction this frame

    left = arcade.key.A in kh.current_pressed
    right = arcade.key.D in kh.current_pressed
    directions["x"] = right - left #amount of pixels to move in x direction this frame

    #if the player is moving in two directions at once (eg north and east)
    #then he shouldnt be moving one pixel in each direction, because that would make his overall speed sqrt(2)
    #and it just looks weird when the player starts randomly walking faster
    #so both directions need to be multiplied by approximately sqrt(2)
    if directions["x"] * directions["y"] != 0:
        directions["x"] *= 0.71
        directions["y"] *= 0.71

    return directions

def move_player(player, directions, obstacles): #function to move the player

    if directions == {"x": 0, "y": 0}:
        player.animation_enabled = False
    else:
        player.animation_enabled = True

    player.center_x += directions["x"] #move the player in x direction
    colls.coll_check(player, obstacles, adjust_player=True) #in case he is in an obstacle, adjust his position
    
    player.center_y += directions["y"] #move the player in y direction
    colls.coll_check(player, obstacles, adjust_player=True) #in case he is in an obstacle, adjust his position

    directions_list = tuple(directions.values())
    directions_list = tuple(min(max(i, -1), 1) for i in directions_list) #clamp the values to -1, 0 or 1

    direction_dict = {
        (0, 0): player.facing, #if the player isn't moving keep the old direction

        (0, 1): "north",
        (0, -1): "south",
        (1, 0): "east",
        (-1, 0): "west",
        (1, 1): "north-east",
        (-1, 1): "north-west",
        (1, -1): "south-east",
        (-1, -1): "south-west",
    }

    player.facing = direction_dict[directions_list]
    player.update_texture()
