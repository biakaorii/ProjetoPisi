import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from random import randint

# tamanho da janela
Window.size = (360, 640)
Window.resizable = False

# tela menu
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # fundo
        background = Image(
            source="fundonovo.png",
            allow_stretch=False,
            keep_ratio=True
        )
        layout.add_widget(background)

        # botão "Start"
        button1 = Button(
            text="Start",
            size_hint=(0.5, 0.1),
            pos_hint={"x": 0.25, "y": 0.4}
        )
        button1.bind(on_press=self.start_game)
        layout.add_widget(button1)

        # botão "Instruções"
        button2 = Button(
            text="Instruções",
            size_hint=(0.5, 0.1),
            pos_hint={"x": 0.25, "y": 0.2}
        )
        button2.bind(on_press=self.open_instruction)
        layout.add_widget(button2)

        self.add_widget(layout)

    def open_instruction(self, instance):
        self.manager.current = "instructions"  # vai para a tela de instruções
    def start_game(self, instance):
        game_screen = self.manager.get_screen("game")
        game_screen.reset_game()
        self.manager.current = "game"  # vai para a tela do jogo

# tela de instruções
class InstructionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # fundo
        background = Image(
            source="instrucao.png",
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(background)

        # botão "Voltar"
        button3 = Button(
            text="<--",
            size_hint=(0.15, 0.05),
            pos_hint={"x": 0.09, "y": 0.9}
        )
        button3.bind(on_press=self.go_back)
        layout.add_widget(button3)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "menu"  # volta para o menu

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # fundo da tela de game over
        background = Image(
            source="gameover.png",
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(background)

        # botão para voltar ao jogo
        button_restart = Button(
            text="<--",
            size_hint=(0.15, 0.05),
            pos_hint={"x": 0.10, "y": 0.9}
        )
        button_restart.bind(on_press=self.restart_game)
        layout.add_widget(button_restart)

        self.add_widget(layout)

    def restart_game(self, instance):
        self.manager.get_screen("game").reset_game()
        self.manager.current = "game"

class Platform(Image):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (width, height)  #  o tamanho da plataforma
        self.pos = (x, y)  # a posição da plataforma
        self.source = "New Piskel.png"

# tela do jogo
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.init_game()

    def init_game(self):
        self.game_started = False  # O jogo começa parado
        self.layout.clear_widgets()

        # fundo
        background = Image(
            source="fundonovo.png",
            allow_stretch=False,
            keep_ratio=True
        )
        self.layout.add_widget(background)

        # botão para voltar ao menu
        button4 = Button(
            text="<--",
            size_hint=(0.15, 0.05),
            pos_hint={"x": 0.09, "y": 0.9}
        )
        button4.bind(on_press=self.go_back)
        self.layout.add_widget(button4)

        # jogador
        self.player = Image(
            source="hellokitty.png",
            size_hint=(None, None),
            size=(120, 120)
        )
        # configuração das plataformas
        self.platform_speed = 1  # velocidade inicial das plataformas
        self.speed_increment = 0.6  # quanto aumenta a velocidade
        self.max_speed = 8  # velocidade máxima
        self.platform_count = 0  # contador das plataformas
        self.platforms = []

        num_platforms = 6  # quantidade das plataformas
        spacing = Window.height // (num_platforms + 1)

        for i in range(num_platforms):
            new_x = randint(10, Window.width - 180)
            new_y = i * spacing  # espaçamento fixo
            new_platform = Platform(new_x, new_y, 180, 100)
            self.platforms.append(new_platform)
            self.layout.add_widget(new_platform)

        # posição do começo na primeira plataforma
        first_platform = self.platforms[0]
        self.player.pos = (first_platform.x + (first_platform.width - self.player.width) / 2,
                            first_platform.y + first_platform.height - 60)

        self.layout.add_widget(self.player)

        # variáveis de movimento
        self.gravity = -0.6
        self.jump_force = 17
        self.velocity_y = 0  # velocidade vertical
        self.velocity_x = 0  # velocidade horizontal
        self.is_jumping = False

        # inicializa o teclado
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key_down)
            self._keyboard.bind(on_key_up=self._on_key_up)

        # inicia o loop
        Clock.schedule_interval(self.update, 1 / 60)

    def reset_game(self):
        Clock.unschedule(self.update)  # para o loop
        self.platform_speed = 1  # reinicia a velocidade das plataformas
        self.platform_count = 0  # reinicia o contador
        self.init_game()  # reinicia o jogo

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if not self.game_started:
            self.game_started = True  # só vai começar quando precionar qualquer tecla

        # controle
        if keycode[1] == "up" and not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_jumping = True  # não vai pular no ar
        elif keycode[1] == "left":  # esquerda
            self.velocity_x = -3
        elif keycode[1] == "right":  # direita
            self.velocity_x = 3

    def _on_key_up(self, keyboard, keycode):
        # para de mover horizontalmente quando a tecla é liberada
        if keycode[1] in ("left", "right","up"):
            self.velocity_x = 0

    def update(self, dt):
        if not self.game_started:
            return  # não faz nada enquanto o jogo não começar

        # a gravidade
        self.velocity_y += self.gravity
        new_y = self.player.y + self.velocity_y
        # a posição horizontal
        new_x = self.player.x + self.velocity_x

        # Posição - game over
        if new_y < 0:
            Clock.unschedule(self.update)
            self.manager.current = "gameover"  # vai para a tela de game over

        #  limite da tela
        if new_x < 0:
            new_y = 0
        elif new_x > Window.width - self.player.width:
            new_x = Window.width - self.player.width

        on_platform = False
        for platform in self.platforms:
            margin = 90  # reduz a margem do lado

            # verifica se o personagem está corretamente sobre a plataforma
            if (
                self.velocity_y < 0  # só se estiver caindo
                and self.player.y + self.velocity_y <= platform.y + platform.height - 20
                    and self.player.y + self.velocity_y + self.player.height >= platform.y
                    and self.player.y >= platform.y  #evita atravessar as plataformas
                and self.player.x + self.player.width > platform.x + margin
                and self.player.x < platform.x + platform.width - margin
            ):
                # se estiver sobre a plataforma
                new_y = platform.y + platform.height - 60  # ajusta a posição para a parte de cima da plataforma
                self.velocity_y = 1  # para a queda
                self.is_jumping = False
                on_platform = True
                break

        # movimento da tela
        self.player.y = new_y
        self.player.x = new_x

        # move todas as plataformas para baixo
        for platform in self.platforms:
            platform.y -= self.platform_speed

            # se a plataforma sair da tela, ela vai para o topo
            if platform.y < -platform.height:
                highest_platform = max(self.platforms, key=lambda p: p.y)  # encontra a mais alta
                new_y = highest_platform.y + randint(90, 270)
                platform.y = new_y
                platform.x = randint(10, Window.width - platform.width)  # novo X aleatório

                # atualiza o contador
                self.platform_count += 1
                if self.platform_count % 10 == 0:  # a cada 10 plataformas
                    self.platform_speed = min(self.platform_speed + self.speed_increment,self.max_speed)  # aumenta a velocidade

    def go_back(self, instance):
        self.manager.current = "menu"  # volta para o menu

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(InstructionsScreen(name="instructions"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm


if __name__ == "__main__":
    GameApp().run()

