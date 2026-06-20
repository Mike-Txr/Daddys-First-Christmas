#manages the menu screen
import arcade
import arcade.gui

class Menu:#class for the Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        #load manager and UIBox
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        #Dimensions of the center
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        #load background and Logo
        self.background_texture = arcade.load_texture("assets/main_background.png")
        self.logo_texture = arcade.load_texture("assets/LOGO.png")

        #Arrow (realised with a spirte, which is rotated to point to the selected button)
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite("assets/arrow_black.png", scale=0.1)
        self.ui_sprites.append(self.arrow)

        #initial position of the arrow, will be updated in the draw function
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        #create buttons
        self.start_button = arcade.gui.UIFlatButton(text="Start Daddys Adventure", width=200)
        self.github_button = arcade.gui.UIFlatButton(text="View on GitHub", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        self.buttons = [self.start_button, self.github_button, self.quit_button]#list for the arrow to know which button is selected
        self.selected_index = 0#index, used to keep track of which button is selected, starts with the first button (Start)

        #events for the buttons (mouse click), which calls the activate_selected function
        @self.start_button.event("on_click")
        def _(event):
            self.selected_index = 0
            self.activate_selected()

        @self.github_button.event("on_click")
        def _(event):
            self.selected_index = 1
            self.activate_selected()
       
        @self.quit_button.event("on_click")
        def _(event):
            self.selected_index = 2
            self.activate_selected()

        #create layout of the buttons
        self.v_box.add(self.start_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.github_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.quit_button)

        #anchor layout to position the buttons in the center of the screen
        self.anchor = arcade.gui.UIAnchorLayout()

        self.back_img = arcade.gui.UIImage(
            texture=self.background_texture,
            width=self.game.window_width,
            height=self.game.window_height
        )
        self.anchor.add(self.back_img, anchor_x="center", anchor_y="center")

        self.logo_img = arcade.gui.UIImage(
            texture=self.logo_texture,
            width=905,
            height=51
        )
        self.anchor.add(self.logo_img, anchor_x="center", anchor_y="top", align_y=-100)

        self.anchor.add(self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(self.anchor)

        #text by the creators
        self.text_by = arcade.Text(
            "A Game by\n    Mike-Txr\n    FinjaAT\n    Matejastinkt",
            center_x - 600,
            center_y - 300,
            arcade.color.BLACK,
            20,
            multiline=True,
            width=300,
            anchor_x="center"
        )
    
    #Keyboard events to navigate through the buttons, which also calls the activate_selected function when the enter key is pressed
    def on_key_press(self, symbol, modifiers):
        #the corresponding keys for navigating through the buttons, W and UP for moving up, S and DOWN for moving down, ENTER and RETURN for selecting the button
        if symbol in (arcade.key.W, arcade.key.UP):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        elif symbol in (arcade.key.S, arcade.key.DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)

        elif symbol in (arcade.key.ENTER, arcade.key.RETURN):
            self.activate_selected()
    
    #function to activate the selected button and either start the game, open the github page or quit
    def activate_selected(self):
        if self.selected_index == 0:
            self.game.menu = False#disable menu, start game
            self.game.setup()

        elif self.selected_index == 1:
            import webbrowser
            webbrowser.open("https://github.com/Mike-Txr/ProjectOlex")##############################################link will probably change

        elif self.selected_index == 2:
            arcade.exit()

    #function to draw the menu screen, which is called in the main game loop when the menu variable is true
    def draw(self):
        self.manager.draw()

        #draw the arrow next to the selected button, the position is updated based on the selected_index
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                self.arrow.center_y = button.center_y

        #draw everything
        self.ui_sprites.draw()
        self.text_by.draw()
        

    #functions to enable and disable the manager, which are called in the main update function when the menu variable is true or false
    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()