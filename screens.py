from config import *
from level import *
from lib.ui import *
from entities import Jugador

class PantallaMenu:
	def __init__(self, juego):
		self.juego = juego
		self.esta_cambiando_pantalla = False
		self.sonido_click = pygame.mixer.Sound('./src/audios/select.ogg')
		self.boton_sonido_cambiar = pygame.mixer.Sound('./src/audios/button_change.ogg')
		self.boton_nuevo_juego = Text('Nueva partida', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - 5 * GRID_SIZE))
		self.boton_continuar = Text('Continuar', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - 3.5 * GRID_SIZE))

		self.texts = pygame.sprite.Group(
			Text(TITLE, font=FONT_L, position=WINDOW_CENTER),
			self.boton_nuevo_juego,
			self.boton_continuar
		)
		
		if read_game('./src/save.txt')['level_number'] != 0:
			self.boton_actual = self.boton_continuar
			self.boton_nuevo_juego.image.set_alpha(255 * .3)
		else: 
			self.boton_actual = self.boton_nuevo_juego
			self.boton_continuar.image.set_alpha(255 * .3)

	def actualizar(self):
		if INPUT.down.kup or INPUT.up.kup:
			self.boton_sonido_cambiar.play()
			self.boton_actual.image.set_alpha(255 * .3)
			if self.boton_actual == self.boton_nuevo_juego:
				self.boton_actual = self.boton_continuar
			else:
				self.boton_actual = self.boton_nuevo_juego
			self.boton_actual.image.set_alpha(255)

		if INPUT.enter.kup and not self.esta_cambiando_pantalla:
			self.esta_cambiando_pantalla = True
			self.sonido_click.play()

		if self.esta_cambiando_pantalla:
			fade_in(SCREEN_FADER, 5)
			if SCREEN_FADER.get_alpha() >= 255:
				if self.boton_actual == self.boton_nuevo_juego:
					save_game({'level_number':0}, './src/save.txt')
				self.juego.screen = PantallaNivel(self.juego)
		else:
			fade_out(SCREEN_FADER, 5)

	def dibujar(self, window):
		self.texts.draw(window)


class PantallaNivel:
	def __init__(self, juego):
		self.juego = juego
		self.es_atras_menu = False
		self.es_reiniciar_nivel = False
		self.jugador = Jugador()
		self.niveles = []
		for num in range(12):
			self.niveles.append(Nivel('./src/levels/{}.tmx'.format(num), self.jugador, 'Nivel {}'.format(num+1)))
		datos = read_game('./src/save.txt')
		self.numero_nivel = 0 if datos == None else datos['level_number']
		self.niveles[self.numero_nivel].load()

	def actualizar(self):
		if INPUT.restart.kdown or not self.jugador.is_alive:
			self.es_reiniciar_nivel = True
		elif INPUT.exit.kdown:
			self.es_atras_menu = True

		if self.es_reiniciar_nivel or self.es_atras_menu or self.niveles[self.numero_nivel].is_complete:
			fade_in(SCREEN_FADER, 6)
			if SCREEN_FADER.get_alpha() >= 255:
				if self.es_reiniciar_nivel:
					self.es_reiniciar_nivel = False
				elif self.niveles[self.numero_nivel].is_complete: 
					self.numero_nivel += 1
					if self.numero_nivel >= len(self.niveles):
						save_game({'level_number':0}, './src/save.txt')
						self.juego.screen = PantallaCreditos(self.juego)
						return

				elif self.es_atras_menu:
					save_game({'level_number':self.numero_nivel}, './src/save.txt')
					self.niveles[self.numero_nivel].dispose()
					self.juego.screen = PantallaMenu(self.juego)
					return

				self.niveles[self.numero_nivel].load()
		else:
			fade_out(SCREEN_FADER, 5)

		self.niveles[self.numero_nivel].update()

	def dibujar(self, window):
		self.niveles[self.numero_nivel].draw(window)


class PantallaCreditos:
	def __init__(self, juego) -> None:
		self.juego = juego
		self.es_salida = False
		self.texts = pygame.sprite.Group(
			Text('Productor', position=(WINDOW_CENTER[0], GRID_SIZE * 2)),
			Text('Alan Jarek Cisneros Garcia', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 3.5)),

			Text('Programador', position=(WINDOW_CENTER[0], GRID_SIZE * 6)),
			Text('Luis Fernando Barrios Ramírez', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 7.5)),

			Text('Artista de personajes', position=(WINDOW_CENTER[0], GRID_SIZE * 10)),
			Text('Gerardo Ramos Chihuaqueño', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 11.5)),

			Text('QA - Progranadir', position=(WINDOW_CENTER[0], GRID_SIZE * 14)),
			Text('Ivan Hernández', font=FONT_S, position=(WINDOW_CENTER[0], GRID_SIZE * 15.5)),

			Text('[Presiona Enter para salir]', font=FONT_S, position=(WINDOW_CENTER[0], WINDOW_HEIGHT - GRID_SIZE)),
		)

	def actualizar(self):
		if INPUT.enter.kdown:
			self.es_salida = True

		if self.es_salida:
			fade_in(SCREEN_FADER, 5)
			if SCREEN_FADER.get_alpha() >= 255:
				self.juego.screen = PantallaMenu(self.juego)
		else:
			fade_out(SCREEN_FADER, 5)

	def dibujar(self, window):
		self.texts.draw(window)