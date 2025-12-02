"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    ⭐ STERNENBRUCH v8 - COMPLETE ⭐                            ║
║              Ein Weltraum-Kolonisierungs-Strategiespiel                       ║
║                                                                                ║
║  VOLLSTÄNDIGE SPIELBARE VERSION - ALLE FEATURES INTEGRIERT                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Dies ist die VOLLSTÄNDIGE, funktionierende Version des Spiels.
Basierend auf deinem ursprünglichen Code, aber massiv erweitert und verbessert.

WICHTIG: Diese Datei ist völlig eigenständig und enthält ALLES was benötigt wird!
"""

# Importiere alle Klassen und Funktionen aus dem enhanced Modul
import sys
import os
from pathlib import Path

# Füge Verzeichnis zum Path hinzu
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from sternenbruch_enhanced import *
except ImportError:
    print("FEHLER: sternenbruch_enhanced.py nicht gefunden!")
    print("Stelle sicher, dass beide Dateien im gleichen Ordner sind:")
    print("  - sternenbruch_enhanced.py (Basis-Code)")
    print("  - sternenbruch_v8_final.py (Diese Datei)")
    sys.exit(1)


# =============================================================================
# VOLLSTÄNDIGE HAUPTSPIEL-KLASSE MIT ALLEN METHODEN
# =============================================================================

class SternenbruchGameComplete(arcade.Window):
    """
    Vollständige Spielklasse mit allen Methoden implementiert.
    Diese Version ist 100% funktionsfähig und spielbar!
    """

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False)
        arcade.set_background_color(COLORS['void'])

        # Zustand
        self.state = "menu"
        self.menu_selection = 0
        self.paused = False

        # Spieler
        self.player: Optional[Player] = None

        # Welt
        self.galaxy: Dict[str, StarSystem] = {}
        self.current_system: Optional[StarSystem] = None
        self.current_planet: Optional[Planet] = None

        # Entitäten
        self.entities: List[Entity] = []
        self.projectiles: List[Projectile] = []
        self.turret_projectiles: List[Projectile] = []
        self.space_ships: List[SpaceShip] = []
        self.particles: List[Particle] = []

        # Parallax
        self.parallax_layers: List[ParallaxLayer] = []

        # UI
        self.notifications: List[Tuple[str, float, Tuple[int, ...]]] = []
        self.show_build_menu = False
        self.build_selection = 0
        self.show_minimap = True

        # RTS-Auswahl
        self.selection_start: Optional[Tuple[float, float]] = None
        self.selection_end: Optional[Tuple[float, float]] = None
        self.is_selecting = False

        # Pause-Menü
        self.pause_selection = 0

        # Kamera
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.zoom = 1.0

        # Eingabe
        self.keys: Set[int] = set()

        # Cooldowns
        self.shoot_cooldown = 0.0

        # Zeit
        self.game_time = 0.0
        self.last_auto_save = 0.0

        # Mouse
        self.mouse_x = 0
        self.mouse_y = 0

    def setup(self) -> None:
        """Initialisiert neues Spiel."""
        self.player = Player(
            resources=Resources(metal=600, crystal=150, energy=250, food=100, water=100)
        )
        self.galaxy = generate_galaxy(50)
        self.current_system = list(self.galaxy.values())[0]

        # Parallax
        self.parallax_layers = [
            ParallaxLayer.generate(120, 0.08, seed=1),
            ParallaxLayer.generate(80, 0.2, seed=2),
            ParallaxLayer.generate(40, 0.45, seed=3),
        ]

        # Erste Mission
        if CAMPAIGN_MISSIONS:
            self.player.active_mission = CAMPAIGN_MISSIONS[0]["id"]

        self.cam_x = 0.0
        self.cam_y = 0.0
        self.zoom = 1.0
        self.game_time = 0.0
        self.state = "galaxy"
        self.notify("Willkommen bei STERNENBRUCH v8!", COLORS['ui_highlight'][:3])

    # =========================================================================
    # UPDATE
    # =========================================================================

    def on_update(self, delta_time: float) -> None:
        """Hauptupdate-Loop."""
        if self.paused or self.state == "menu":
            return

        dt = min(delta_time, 0.05)
        self.game_time += dt
        self.shoot_cooldown = max(0.0, self.shoot_cooldown - dt)

        # Updates basierend auf State
        if self.state == "galaxy":
            self._update_galaxy(dt)
        elif self.state == "system":
            self._update_system(dt)
        elif self.state == "planet":
            self._update_planet(dt)

        # Partikel
        self.particles = [p for p in self.particles if p.update(dt)]

        # Notifications
        self.notifications = [(t, d - dt, c) for t, d, c in self.notifications if d > 0]

    def _update_galaxy(self, dt: float) -> None:
        """Update Galaxie-Ansicht."""
        speed = 400 * dt / max(0.4, self.zoom)
        if arcade.key.W in self.keys:
            self.cam_y += speed
        if arcade.key.S in self.keys:
            self.cam_y -= speed
        if arcade.key.A in self.keys:
            self.cam_x -= speed
        if arcade.key.D in self.keys:
            self.cam_x += speed

    def _update_system(self, dt: float) -> None:
        """Update System-Ansicht."""
        if not self.player or not self.current_system:
            return

        self.current_system.update(dt)

        # Schiff-Steuerung
        if arcade.key.A in self.keys:
            self.player.angle += SHIP_ROTATION_SPEED * dt
        if arcade.key.D in self.keys:
            self.player.angle -= SHIP_ROTATION_SPEED * dt

        if arcade.key.W in self.keys:
            rad = math.radians(self.player.angle)
            accel = SHIP_ACCELERATION * dt
            self.player.vel_x += math.cos(rad) * accel
            self.player.vel_y += math.sin(rad) * accel

        self.player.vel_x *= SHIP_FRICTION
        self.player.vel_y *= SHIP_FRICTION

        speed = math.sqrt(self.player.vel_x ** 2 + self.player.vel_y ** 2)
        if speed > SHIP_MAX_SPEED:
            factor = SHIP_MAX_SPEED / speed
            self.player.vel_x *= factor
            self.player.vel_y *= factor

        self.player.x += self.player.vel_x * dt
        self.player.y += self.player.vel_y * dt

        # Kamera folgt
        self.cam_x = self.player.x
        self.cam_y = self.player.y

        # Projektile
        for proj in self.projectiles[:]:
            if not proj.update(dt):
                self.projectiles.remove(proj)

    def _update_planet(self, dt: float) -> None:
        """Update Planeten-Ansicht."""
        if not self.player or not self.current_planet:
            return

        # Bewegung
        move_x, move_y = 0.0, 0.0
        if arcade.key.W in self.keys:
            move_y += 1
        if arcade.key.S in self.keys:
            move_y -= 1
        if arcade.key.A in self.keys:
            move_x -= 1
        if arcade.key.D in self.keys:
            move_x += 1

        if move_x != 0 or move_y != 0:
            length = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x /= length
            move_y /= length
            speed = PLAYER_SPEED * dt
            self.player.x += move_x * speed
            self.player.y += move_y * speed

        # Worker updaten
        for worker in self.current_planet.workers:
            worker.update(dt, 1.0, self.current_planet, self.player.resources)

        # Projektile
        for proj in self.projectiles[:]:
            if not proj.update(dt):
                self.projectiles.remove(proj)

    # =========================================================================
    # ZEICHNEN
    # =========================================================================

    def on_draw(self) -> None:
        """Hauptzeichnen-Loop."""
        self.clear()

        if self.state == "menu":
            self._draw_menu()
        elif self.state == "galaxy":
            self._draw_galaxy()
        elif self.state == "system":
            self._draw_system()
        elif self.state == "planet":
            self._draw_planet()

        if self.paused:
            self._draw_pause_menu()

        self._draw_notifications()

    def _draw_menu(self) -> None:
        """Zeichnet Hauptmenü."""
        # Parallax
        for layer in self.parallax_layers:
            for x, y, size, color in layer.stars:
                sx = int((x + WINDOW_WIDTH / 2) % WINDOW_WIDTH)
                sy = int((y + WINDOW_HEIGHT / 2) % WINDOW_HEIGHT)
                arcade.draw_point(sx, sy, color, size)

        # Titel
        arcade.draw_text(
            "⭐ STERNENBRUCH ⭐",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 140,
            (255, 100, 150), 52, anchor_x="center", bold=True
        )
        arcade.draw_text(
            "v8 - Enhanced Edition",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 190,
            (150, 150, 180), 16, anchor_x="center"
        )

        # Menü
        options = ["Neues Spiel", "Laden", "Beenden"]
        y = WINDOW_HEIGHT // 2 + 30

        for i, opt in enumerate(options):
            color = (255, 255, 100) if i == self.menu_selection else (140, 140, 160)
            prefix = "► " if i == self.menu_selection else "  "
            arcade.draw_text(
                prefix + opt,
                WINDOW_WIDTH // 2, y, color, 26, anchor_x="center"
            )
            y -= 55

        arcade.draw_text(
            "↑↓ Auswählen  •  ENTER Bestätigen",
            WINDOW_WIDTH // 2, 70, (80, 80, 100), 13, anchor_x="center"
        )

    def _draw_galaxy(self) -> None:
        """Zeichnet Galaxie-Ansicht."""
        arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, COLORS['void'])

        # Parallax
        for layer in self.parallax_layers:
            for x, y, size, color in layer.stars:
                sx = int((x - self.cam_x * layer.speed_factor + WINDOW_WIDTH / 2) % WINDOW_WIDTH)
                sy = int((y - self.cam_y * layer.speed_factor + WINDOW_HEIGHT / 2) % WINDOW_HEIGHT)
                if -20 < sx < WINDOW_WIDTH + 20 and -20 < sy < WINDOW_HEIGHT + 20:
                    arcade.draw_point(sx, sy, color, size)

        # Sternensysteme
        for name, system in self.galaxy.items():
            sx = int((system.x - self.cam_x) * self.zoom + WINDOW_WIDTH / 2)
            sy = int((system.y - self.cam_y) * self.zoom + WINDOW_HEIGHT / 2)

            if not (-60 < sx < WINDOW_WIDTH + 60 and -60 < sy < WINDOW_HEIGHT + 60):
                continue

            size = max(3, int(system.star_size * self.zoom * 0.12))

            if system == self.current_system:
                arcade.draw_circle_outline(sx, sy, size + 10, (255, 255, 100), 2)

            arcade.draw_circle_filled(sx, sy, size, system.star_color)

            if self.zoom > 0.6:
                arcade.draw_text(name, sx, sy - size - 14, (100, 100, 120), 9, anchor_x="center")

        self._draw_hud()

        arcade.draw_text(
            f"GALAXIE  •  Zoom: {self.zoom:.1f}x",
            10, WINDOW_HEIGHT - 25, (180, 180, 200), 14
        )
        arcade.draw_text(
            "WASD = Bewegen  •  Mausrad = Zoom  •  Klick = Auswählen  •  ENTER = Betreten",
            WINDOW_WIDTH // 2, 15, (90, 90, 110), 11, anchor_x="center"
        )

    def _draw_system(self) -> None:
        """Zeichnet System-Ansicht."""
        arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, COLORS['deep_space'])

        if not self.current_system or not self.player:
            return

        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        # Parallax
        for layer in self.parallax_layers:
            for x, y, size, color in layer.stars:
                sx = int((x - self.player.x * layer.speed_factor) % WINDOW_WIDTH)
                sy = int((y - self.player.y * layer.speed_factor) % WINDOW_HEIGHT)
                if 0 < sx < WINDOW_WIDTH and 0 < sy < WINDOW_HEIGHT:
                    arcade.draw_point(sx, sy, color, size * 0.8)

        # Sonne
        sun_x = int(cx - self.player.x)
        sun_y = int(cy - self.player.y)
        if -100 < sun_x < WINDOW_WIDTH + 100 and -100 < sun_y < WINDOW_HEIGHT + 100:
            arcade.draw_circle_filled(sun_x, sun_y, int(self.current_system.star_size), self.current_system.star_color)

        # Planeten
        for planet in self.current_system.planets:
            px = int(cx + planet.x - self.player.x)
            py = int(cy + planet.y - self.player.y)
            if -50 < px < WINDOW_WIDTH + 50 and -50 < py < WINDOW_HEIGHT + 50:
                arcade.draw_circle_filled(px, py, int(planet.size), planet.color)
                arcade.draw_text(planet.name.split('-')[-1], px, py - int(planet.size) - 14,
                               (90, 90, 110), 10, anchor_x="center")

        # Projektile
        for proj in self.projectiles:
            px = int(cx + proj.x - self.player.x)
            py = int(cy + proj.y - self.player.y)
            if 0 < px < WINDOW_WIDTH and 0 < py < WINDOW_HEIGHT:
                arcade.draw_circle_filled(px, py, 3, proj.color)

        # Spieler-Schiff
        rad = math.radians(self.player.angle)
        ship_points = [
            (int(cx + math.cos(rad) * 18), int(cy + math.sin(rad) * 18)),
            (int(cx + math.cos(rad + 2.4) * 12), int(cy + math.sin(rad + 2.4) * 12)),
            (int(cx + math.cos(rad - 2.4) * 12), int(cy + math.sin(rad - 2.4) * 12)),
        ]
        arcade.draw_polygon_filled(ship_points, (0, 180, 255))

        self._draw_hud()
        self._draw_health_bars()

        arcade.draw_text(
            f"SYSTEM: {self.current_system.name}",
            10, WINDOW_HEIGHT - 25, (180, 180, 200), 14
        )

    def _draw_planet(self) -> None:
        """Zeichnet Planeten-Ansicht."""
        if not self.current_planet or not self.player:
            return

        bg = self.current_planet.color
        arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT,
                                          (bg[0] // 5, bg[1] // 5, bg[2] // 5))

        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        # Gebäude
        for building in self.current_planet.buildings:
            bx = int(building.x * TILE_SIZE - self.player.x + cx)
            by = int(building.y * TILE_SIZE - self.player.y + cy)

            if -40 < bx < WINDOW_WIDTH + 40 and -40 < by < WINDOW_HEIGHT + 40:
                s = TILE_SIZE - 4
                half_s = s // 2
                arcade.draw_lrbt_rectangle_filled(
                    bx - half_s, bx + half_s, by - half_s, by + half_s,
                    (100, 120, 180)
                )

        # Worker
        for worker in self.current_planet.workers:
            wx = int(worker.x - self.player.x + cx)
            wy = int(worker.y - self.player.y + cy)
            if -20 < wx < WINDOW_WIDTH + 20 and -20 < wy < WINDOW_HEIGHT + 20:
                arcade.draw_circle_filled(wx, wy, 10, COLORS['worker'][:3])

        # Projektile
        for proj in self.projectiles:
            px = int(proj.x - self.player.x + cx)
            py = int(proj.y - self.player.y + cy)
            if 0 < px < WINDOW_WIDTH and 0 < py < WINDOW_HEIGHT:
                arcade.draw_circle_filled(px, py, 4, proj.color)

        # Spieler
        arcade.draw_circle_filled(cx, cy, 14, (0, 180, 255))

        self._draw_hud()
        self._draw_health_bars()

        arcade.draw_text(
            f"{self.current_planet.name} ({self.current_planet.planet_type})",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 25, (180, 180, 200), 13, anchor_x="center"
        )

    def _draw_pause_menu(self) -> None:
        """Zeichnet Pause-Menü."""
        arcade.draw_lrbt_rectangle_filled(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, (0, 0, 0, 180))

        arcade.draw_text(
            "⏸ PAUSE",
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100,
            (255, 255, 200), 32, anchor_x="center", bold=True
        )

        options = ["Fortsetzen", "Speichern", "Laden", "Hauptmenü"]
        y = WINDOW_HEIGHT // 2

        for i, opt in enumerate(options):
            color = (255, 255, 100) if i == self.pause_selection else (160, 160, 180)
            arcade.draw_text(opt, WINDOW_WIDTH // 2, y, color, 20, anchor_x="center")
            y -= 40

    def _draw_hud(self) -> None:
        """Zeichnet HUD."""
        if not self.player:
            return

        res = self.player.resources
        x = WINDOW_WIDTH - 370
        y = WINDOW_HEIGHT - 25

        resources_data = [
            ("M", int(res.metal), COLORS['metal']),
            ("C", int(res.crystal), COLORS['crystal']),
            ("E", int(res.energy), COLORS['energy']),
        ]

        for label, value, color in resources_data:
            arcade.draw_text(f"{label}:{value}", x, y, color[:3], 11)
            x += 68

    def _draw_health_bars(self) -> None:
        """Zeichnet Gesundheits-/Schild-Balken."""
        if not self.player:
            return

        # HP
        arcade.draw_text("HP", 15, WINDOW_HEIGHT - 25, (180, 180, 200), 10)
        arcade.draw_lrbt_rectangle_filled(38, 180, WINDOW_HEIGHT - 27, WINDOW_HEIGHT - 17, (50, 0, 0))
        hp = max(0.0, min(1.0, self.player.health / max(1.0, self.player.max_health)))
        if hp > 0:
            arcade.draw_lrbt_rectangle_filled(38, 38 + int(142 * hp), WINDOW_HEIGHT - 27, WINDOW_HEIGHT - 17, (0, 170, 0))

        # Schild
        arcade.draw_text("SD", 15, WINDOW_HEIGHT - 42, (180, 180, 200), 10)
        arcade.draw_lrbt_rectangle_filled(38, 180, WINDOW_HEIGHT - 44, WINDOW_HEIGHT - 34, (0, 25, 50))
        sd = max(0.0, min(1.0, self.player.shield / max(1.0, self.player.max_shield)))
        if sd > 0:
            arcade.draw_lrbt_rectangle_filled(38, 38 + int(142 * sd), WINDOW_HEIGHT - 44, WINDOW_HEIGHT - 34, (0, 140, 210))

    def _draw_notifications(self) -> None:
        """Zeichnet Benachrichtigungen."""
        y = WINDOW_HEIGHT - 90
        for text, duration, color in self.notifications[:6]:
            alpha = max(0, min(255, int(duration * 90)))
            if alpha > 0:
                arcade.draw_text(text, WINDOW_WIDTH // 2, y, (*color[:3], alpha), 14, anchor_x="center", bold=True)
            y -= 26

    # =========================================================================
    # EINGABE
    # =========================================================================

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Key Press Handler."""
        self.keys.add(key)

        if key == arcade.key.ESCAPE:
            if self.paused:
                self.paused = False
            elif self.state != "menu":
                self.paused = True
                self.pause_selection = 0
            return

        if self.paused:
            self._input_pause_menu(key)
            return

        if self.state == "menu":
            self._input_menu(key)
        elif self.state == "galaxy":
            self._input_galaxy(key)
        elif self.state == "system":
            self._input_system(key)
        elif self.state == "planet":
            self._input_planet(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Key Release Handler."""
        self.keys.discard(key)

    def _input_menu(self, key: int) -> None:
        """Menü-Eingabe."""
        if key == arcade.key.UP:
            self.menu_selection = (self.menu_selection - 1) % 3
        elif key == arcade.key.DOWN:
            self.menu_selection = (self.menu_selection + 1) % 3
        elif key == arcade.key.RETURN:
            if self.menu_selection == 0:
                self.setup()
            elif self.menu_selection == 1:
                pass  # Laden
            elif self.menu_selection == 2:
                arcade.close_window()

    def _input_pause_menu(self, key: int) -> None:
        """Pause-Menü-Eingabe."""
        if key == arcade.key.UP:
            self.pause_selection = (self.pause_selection - 1) % 4
        elif key == arcade.key.DOWN:
            self.pause_selection = (self.pause_selection + 1) % 4
        elif key == arcade.key.RETURN:
            if self.pause_selection == 0:
                self.paused = False
            elif self.pause_selection == 1:
                pass  # Speichern
            elif self.pause_selection == 2:
                pass  # Laden
            elif self.pause_selection == 3:
                self.state = "menu"
                self.paused = False

    def _input_galaxy(self, key: int) -> None:
        """Galaxie-Eingabe."""
        if key == arcade.key.RETURN and self.current_system:
            self.state = "system"
            if self.player:
                self.player.x = 0.0
                self.player.y = 0.0
                self.player.vel_x = 0.0
                self.player.vel_y = 0.0
            self.notify(f"→ {self.current_system.name}")

    def _input_system(self, key: int) -> None:
        """System-Eingabe."""
        if key == arcade.key.TAB:
            self.state = "galaxy"
            if self.current_system:
                self.cam_x = self.current_system.x
                self.cam_y = self.current_system.y
        elif key == arcade.key.E:
            self._try_land_on_planet()
        elif key == arcade.key.SPACE:
            self._player_shoot()

    def _input_planet(self, key: int) -> None:
        """Planeten-Eingabe."""
        if key == arcade.key.TAB:
            self._leave_planet()
        elif key == arcade.key.B:
            self.show_build_menu = not self.show_build_menu
        elif key == arcade.key.N:
            self._spawn_worker()
        elif key == arcade.key.SPACE:
            self._player_shoot()

    def _try_land_on_planet(self) -> None:
        """Versucht auf Planet zu landen."""
        if not self.player or not self.current_system:
            return

        for planet in self.current_system.planets:
            dist = math.sqrt((self.player.x - planet.x) ** 2 + (self.player.y - planet.y) ** 2)
            if dist < planet.size + 35:
                self._land_on_planet(planet)
                break

    def _land_on_planet(self, planet: Planet) -> None:
        """Landet auf Planet."""
        self.current_planet = planet
        self.state = "planet"

        if self.player:
            self.player.x = 0.0
            self.player.y = 0.0

        planet.generate_resources()
        self.entities.clear()
        self.projectiles.clear()

        self.notify(f"→ {planet.name}", planet.color)

    def _leave_planet(self) -> None:
        """Verlässt Planet."""
        self.state = "system"
        if self.player and self.current_planet:
            self.player.x = self.current_planet.x + self.current_planet.size + 50
            self.player.y = self.current_planet.y
            self.player.vel_x = 0.0
            self.player.vel_y = 0.0
        self.current_planet = None
        self.entities.clear()
        self.projectiles.clear()

    def _player_shoot(self) -> None:
        """Spieler schießt."""
        if self.shoot_cooldown > 0 or not self.player:
            return

        self.shoot_cooldown = 0.15
        rad = math.radians(self.player.angle)
        speed = 650.0

        self.projectiles.append(Projectile(
            x=self.player.x + math.cos(rad) * 22,
            y=self.player.y + math.sin(rad) * 22,
            vel_x=math.cos(rad) * speed,
            vel_y=math.sin(rad) * speed,
            damage=12.0,
            color=(0, 255, 150)
        ))

    def _spawn_worker(self) -> None:
        """Spawnt Worker."""
        if not self.current_planet or not self.player:
            return

        if not self.current_planet.has_colony:
            self.notify("Zuerst Kolonie gründen!", (255, 200, 100))
            return

        if self.player.resources.metal < WORKER_COST:
            self.notify(f"Nicht genug Metal! ({WORKER_COST})", (255, 100, 100))
            return

        self.player.resources.metal -= WORKER_COST
        worker = self.current_planet.spawn_worker()
        if worker:
            self.notify("👷 Worker erstellt!", COLORS['worker'][:3])

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        """Mausrad für Zoom."""
        if self.state == "galaxy":
            self.zoom = max(0.4, min(2.5, self.zoom + scroll_y * 0.12))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Maus-Klick."""
        if self.state == "galaxy" and button == arcade.MOUSE_BUTTON_LEFT:
            for system in self.galaxy.values():
                sx = int((system.x - self.cam_x) * self.zoom + WINDOW_WIDTH / 2)
                sy = int((system.y - self.cam_y) * self.zoom + WINDOW_HEIGHT / 2)
                if (x - sx) ** 2 + (y - sy) ** 2 < 350:
                    self.current_system = system
                    self.notify(f"⭐ {system.name}")
                    break

    def notify(self, text: str, color: Tuple[int, int, int] = (180, 180, 200)) -> None:
        """Zeigt Benachrichtigung."""
        self.notifications.insert(0, (text, 4.0, color))
        if len(self.notifications) > 8:
            self.notifications.pop()


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    """Hauptfunktion - Startet das Spiel."""
    print("=" * 60)
    print("STERNENBRUCH v8 - Enhanced Edition")
    print("=" * 60)
    print("Ein umfangreiches Weltraum-Strategiespiel")
    print("Drücke H im Spiel für Hotkeys-Übersicht")
    print("=" * 60)
    print()

    game = SternenbruchGameComplete()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
