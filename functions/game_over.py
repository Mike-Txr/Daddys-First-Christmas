#manages the game over screen
import arcade
import arcade.gui

class GameOver:#class for the Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        #load manager and UIBox
        self.manager = arcade.gui.UIManager()#contains all the UI elements, which are drawn in the draw function, can be enabled and disabled
        self.v_box = arcade.gui.UIBoxLayout()#v_box is used to arrange the buttons vertically, which is added to the manager in the draw function

        #Dimensions of the center (for easier use in the draw function)
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        #Arrow (realised with a sprite, which is rotated to point to the selected button)
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite("assets/arrow.png", scale=0.1)
        self.ui_sprites.append(self.arrow)

        #initial position of the arrow, will be updated in the draw function
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        #create all the buttons
        self.restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        self.buttons = [self.restart_button, self.quit_button]#list for the arrow to know which button is selected
        self.selected_index = 0#index, used to keep track of which button is selected, starts with the first button (Restart)

        #events for the buttons (mouse click), which calls the activate_selected function (basically just sets the self.selected_index to the corresponding button and calls the activate_selected function)
        @self.restart_button.event("on_click")
        def _(event):
            self.selected_index = 0
            self.activate_selected()
       
        @self.quit_button.event("on_click")
        def _(event):
            self.selected_index = 1
            self.activate_selected()

        #create layout of the buttons
        self.v_box.add(self.restart_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.quit_button)

        #anchor layout to position the buttons in the center of the screen
        self.anchor = arcade.gui.UIAnchorLayout()
        self.anchor.add(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
        self.manager.add(self.anchor)

        #insert Game over text
        self.text_gameover = arcade.Text(
            "GAME OVER",
            center_x,
            center_y + 150,
            arcade.color.BLACK,
            60,
            anchor_x="center"
        )

    #Keyboard events to navigate through the buttons, is called in the main game loop when the game over screen is active
    def on_key_press(self, symbol, modifiers):
        #the corresponding keys for navigating through the buttons, W and UP for moving up, S and DOWN for moving down, ENTER and RETURN for selecting the button
        if symbol in (arcade.key.W, arcade.key.UP):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        elif symbol in (arcade.key.S, arcade.key.DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)

        elif symbol in (arcade.key.ENTER, arcade.key.RETURN):
            self.activate_selected()
    
    #function to activate the selected button and either resatart or quit
    def activate_selected(self):
        if self.selected_index == 0:
            self.game.game_over = False#close game over screen
            self.game.setup()#call setup = always equals restart

        elif self.selected_index == 1:
            arcade.exit()#close game

    #function to draw the game over screen, which is called in the main game loop when the game over screen is active
    def draw(self):
        #draw rectangle over the whole screen
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.RED[:3] + (200,)
        )

        #draw the arrow next to the selected button, the position is updated based on the selected_index
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                self.arrow.center_y = button.center_y

        #draw everything
        self.ui_sprites.draw()
        self.text_gameover.draw()
        self.manager.draw()

    #functions to enable and disable the manager, which are called in the main update function when the menu variable is true or false
    #very important, because the manager handles the events for the buttons, which are only needed when the menu is active    
    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()