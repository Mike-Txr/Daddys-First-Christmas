import arcade
import arcade.gui

class BattleScreen:
    def __init__(self, game):
        self.game = game#variable game, to access the main game class and its attributes like health, window_width, etc.
        self.ui = arcade.gui.UIManager()
        self.root = arcade.gui.UIAnchorLayout()
        self.ui.add(self.root)

        self.current_enemy = None#variable to store the current enemy, which will be set when start_battle is called

        #debug text, not relevant
        self.title_label = arcade.gui.UILabel(text="Battle!", font_size=40, text_color=arcade.color.WHITE)
        self.root.add(self.title_label, anchor_x="center", anchor_y="center")

        #important variables for the battle logic
        self.state = "inactive" #variable to track the state of the battle screen, can be "inactive", "active", or "victory"
        self.timer = 0.0
        self.turn_delay = 1.5 #delay between turns in seconds

        #variables for the timing mechanic
        self.red_time = 1.2
        self.green_time = 0.35
        self.cue_time = 0.0
        self.green_active = False

        self.block_success = False

    def start_battle(self, enemy):
        self.current_enemy = enemy
        self.title_label.text = "Battle!"
        self.state = "player_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.block_success = False
        # später kannst du hier enemy.hp, enemy.texture usw. übernehmen

    def update(self, delta_time):
        if self.state == "inactive":
            return

        self.timer = self.timer + delta_time

        if self.state == "player_timing_attack":
            self.cue_time = self.cue_time + delta_time

            if self.cue_time >= self.red_time:
                self.green_active = True

                if self.cue_time >= self.red_time + self.green_time:
                    self.finish_attack_timing(missed=True)

        elif self.state == "enemy_turn":
            if self.timer >= self.turn_delay:
                self.start_block_timing()

        elif self.state == "enemy_timing_block":
            self.cue_time += delta_time

            if self.cue_time >= self.current_enemy["red_time"]:
                self.green_active = True

            if self.cue_time >= self.current_enemy["red_time"] + self.green_time:
                self.resolve_enemy_attack(blocked=False)

    def player_attack_pressed(self):
        if self.state == "player_turn":
            self.state = "player_timing_attack"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False

    def start_block_timing(self):
        if self.state == "enemy_turn":
            self.state = "enemy_timing_block"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False
            self.block_success = False

    def finish_attack_timing(self, missed=False):
        if self.state != "player_timing_attack":
            return

        if missed:
            damage = 2
            print("verkackt")
        else:
            damage = 10
            print("PERFECT")

        self.current_enemy["max_hp"] -= damage
        print(f"Spieler macht {damage} Schaden")

        if self.current_enemy["max_hp"] <= 0:
            self.end_battle(win=True)
            return

        self.state = "enemy_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False

    def resolve_enemy_attack(self, blocked=False):
        if self.state != "enemy_timing_block":
            return

        damage = self.current_enemy["attack"]

        if blocked or self.block_success:
            damage = max(1, int(damage * 0.3))
            print("BLOCK!")

        else:
            print("nicht geblockt")

        self.game.set_health(self.game.health - damage)
        print("Gegner macht", damage, "Schaden")

        self.state = "player_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.block_success = False


    def end_battle(self, win=False):
        print("Battle beendet:", "Sieg" if win else "Niederlage")
        self.game.set_coins(self.game.coins + self.current_enemy["coin_reward"])
        self.game.set_xp(self.game.current_xp + self.current_enemy["xp_reward"])

        self.state = "inactive"
        self.current_enemy = None
        self.game.battle = False
        self.disable()

    def enable(self):
        self.ui.enable()

    def disable(self):
        self.ui.disable()

    def draw_traffic_light(self):
        if self.state not in ("player_timing_attack", "enemy_timing_block"):
            return

        x = self.game.window_width * 0.5
        y = self.game.window_height * 0.18
        radius = 25

        if self.green_active:
            color = arcade.color.GREEN
        else:
            color = arcade.color.RED

        arcade.draw_circle_filled(x, y, radius, color)
        arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK, 3)


    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.WHITE
        )

        self.draw_traffic_light()
        self.ui.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.state == "player_turn":
                self.player_attack_pressed()

            elif self.state == "player_timing_attack":
                if self.green_active:
                    self.finish_attack_timing(missed=False)
                else:
                    print("Too early")

            elif self.state == "enemy_timing_block":
                if self.green_active:
                    self.block_success = True
                    self.resolve_enemy_attack(blocked=True)
                else:
                    print("Too early")