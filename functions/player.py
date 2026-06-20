#basic player class, for variables and functions
import arcade
import functions.settings as settings
import functions.entity as entity

class Player(entity.Entity):
    def __init__(self, x, y, scale, game=None):
        super().__init__(x, y, scale, "player.png")
        self.center_x = x
        self.center_y = y
        self.dia_icon = "assets/player_dia.png"

        self.game = game
        
        #Main Game Variables
        self.max_health = 10#max_health variable, could be changed throughout the game
        self.health = self.max_health#current health variable, starts with max health

        self.max_power = 50#max_power variable, could be changed throughout the game
        self.power = self.max_power#current power variable, starts with max power

        self.attack = 5#variable for the attack stat, could be changed throughout the game

        self.level = 1#variable for the current level, starts at 1
        self.levelup = 100#variable, level up will be reached at 100
        self.current_xp = 90#current experience points variable, starts with 50

        self.coins = 10#variable for coins, could be changed throughout the game

    #function to set the health of the player, which also updates the health label
    def set_health(self, value: int):
        self.health = max(0, min(self.max_health, value))#health is set to the value, but it can't be lower than 0 or higher than max health
        if self.game is not None:
            self.game.health_label.text = f"{self.health} / {self.max_health}"#update the health label in the game, which shows the current health and max health of the player

    #function to set the power of the player, which also updates the power label
    def set_power(self, value: int):
        self.power = max(0, min(self.max_power, value))#power is set to the value, but it can't be lower than 0 or higher than max power
        if self.game is not None:
            self.game.power_label.text = f"{self.power} / {self.max_power}"#update the power label in the game, which shows the current power and max power of the player

    #function to set the XP of the player, which also updates the level progress bar and level label
    def set_xp(self, value: int):
        self.current_xp = max(0, value)#current XP is set to the value, but it can't be lower than 0, there is no upper limit for XP, because when the player reaches the level up XP, the current XP will be reduced by the level up

        while self.current_xp >= self.levelup:#if the current XP is higher than or equal to the level up XP, the player levels up
            self.current_xp -= self.levelup
            self.level += 1#plus 1, because it must not be 0, because of division by 0. 1 isn't very visible in the progress
            print("Level up! Aktuelles Level:", self.level)

        if self.game is not None:#update the level label and progress bar
            if self.level > 0:
                progress = self.current_xp / self.levelup#progress is calculated by current XP divided by level up XP, which is then used to fill the level progress bar
            else:
                progress = 0

            progress = max(0, min(1, progress))#progress is set to the value, but it can't be lower than 0 or higher than 1, because it's used to fill the level progress bar, which is between 0 and 1
            self.game.level_label.text = f"{self.level}"#update the level label in the game, which shows the current level
            bar_width = max(1, self.game.level_panel_width - 100)#calculate the width of the level progress bar, which is the width of the level panel minus 100 pixels for padding, but it can't be lower than 1 pixel, because then the progress bar would be invisible
            self.game.level_bar_fill.width = max(1, int(bar_width * progress))#calculate the width of the filled part of the level progress bar, which is the width of the level progress bar multiplied by the progress

    #function to set the coins of the player, which also updates the coin label
    def set_coins(self, value: int):
        self.coins = max(0, value)#does not have an upper limit
        if self.game is not None:
            self.game.coins_label.text = f"{self.coins}"#update the coin label in the game, which shows the current coins of the player