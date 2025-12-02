"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      ⭐ STERNENBRUCH v8 - ENHANCED ⭐                          ║
║                Ein Weltraum-Kolonisierungs-Strategiespiel                     ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  VERSION 8 - FEATURE-COMPLETE ENHANCED EDITION:                              ║
║  ✨ NEU: Particle-System, Tooltips, Tutorial-System                          ║
║  ✨ NEU: Achievement-System, Gebäude-Upgrades, Tech-Tree                     ║
║  ✨ NEU: Erweiterte Hotkeys, Auto-Save, Statistiken                          ║
║  ✨ NEU: Verbesserte Worker-Steuerung (Gruppen, Formationen)                 ║
║  ✨ NEU: Mehr Gebäude-Typen, interaktive Minimap                             ║
║  ✨ VERBESSERT: Performance, UI/UX, Schiffskämpfe, KI                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  STEUERUNG:                                                                   ║
║  WASD = Bewegen  |  SPACE = Schießen  |  E = Interagieren                    ║
║  B = Bauen  |  F = Forschen  |  TAB = Ansicht wechseln                       ║
║  M = Minimap  |  C = Kampagnen  |  A = Achievements                          ║
║  T = Tech-Tree  |  H = Hotkeys  |  S = Statistiken                           ║
║  ESC = Pause  |  F5 = Speichern  |  F9 = Laden                               ║
║  1-5 = Gruppen zuweisen  |  SHIFT+1-5 = Gruppe auswählen                     ║
║  Linksklick+Ziehen = Einheiten auswählen | Rechtsklick = Befehl              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import arcade
import math
import random
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
from pathlib import Path

# =============================================================================
# KONFIGURATION
# =============================================================================

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000
WINDOW_TITLE = "⭐ STERNENBRUCH v8 - Enhanced Edition ⭐"

TILE_SIZE = 32
PLAYER_SPEED = 200
PLAYER_SHIP_SPEED = 300

# Schiff-Steuerung
SHIP_ROTATION_SPEED = 200
SHIP_ACCELERATION = 450
SHIP_MAX_SPEED = 450
SHIP_FRICTION = 0.97

# Gegner-KI Parameter
ENEMY_SIGHT_RANGE = 400
ENEMY_ATTACK_RANGE = 220
ENEMY_PATROL_RANGE = 180
ENEMY_SPAWN_MIN_DIST = 450

# Fog of War
FOG_TILE_SIZE = 64
FOG_REVEAL_RADIUS = 220

# Worker
WORKER_SPEED = 90
WORKER_HARVEST_RATE = 8
WORKER_CARRY_CAPACITY = 60
WORKER_COST = 50

# Auto-Save
AUTO_SAVE_INTERVAL = 300.0  # 5 Minuten

# Farben
COLORS: Dict[str, Tuple[int, ...]] = {
    'void': (5, 5, 15),
    'deep_space': (10, 12, 25),
    'ui_bg': (15, 20, 30, 235),
    'ui_border': (70, 90, 130),
    'ui_highlight': (100, 200, 255),
    'metal': (180, 180, 200),
    'crystal': (100, 150, 255),
    'energy': (255, 255, 100),
    'food': (100, 200, 100),
    'water': (100, 180, 255),
    'shard': (255, 0, 100),
    'fog': (8, 8, 18),
    'alert': (255, 50, 50),
    'selection': (0, 255, 100),
    'worker': (200, 180, 100),
    'tooltip_bg': (25, 30, 40, 240),
    'success': (50, 255, 100),
    'warning': (255, 200, 50),
    'error': (255, 80, 80),
}


# =============================================================================
# ENUMS
# =============================================================================

class Faction(Enum):
    PLAYER = "Spieler"
    TERRAN_ALLIANCE = "Terranische Allianz"
    CRYSTAL_COLLECTIVE = "Kristall-Kollektiv"
    VOID_RAIDERS = "Void-Räuber"
    ANCIENT_ONES = "Die Alten"
    PRIMITIVE = "Primitive"


class TechLevel(Enum):
    STONE_AGE = 1
    BRONZE_AGE = 2
    IRON_AGE = 3
    INDUSTRIAL = 4
    SPACE_AGE = 5
    ADVANCED = 6


class CivBehavior(Enum):
    PEACEFUL = "Friedlich"
    DEFENSIVE = "Defensiv"
    AGGRESSIVE = "Aggressiv"
    TRADER = "Händler"
    ISOLATIONIST = "Isolationistisch"


class AIState(Enum):
    IDLE = "idle"
    PATROL = "patrol"
    ALERT = "alert"
    CHASE = "chase"
    ATTACK = "attack"
    FLEE = "flee"


class WorkerState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    HARVESTING = "harvesting"
    RETURNING = "returning"
    BUILDING = "building"


class ParticleType(Enum):
    EXPLOSION = "explosion"
    SMOKE = "smoke"
    SPARKLE = "sparkle"
    LASER_HIT = "laser_hit"
    RESOURCE = "resource"


# =============================================================================
# KONSTANTEN & DATEN
# =============================================================================

FACTION_COLORS: Dict[Faction, Tuple[int, int, int]] = {
    Faction.PLAYER: (0, 180, 255),
    Faction.TERRAN_ALLIANCE: (100, 200, 100),
    Faction.CRYSTAL_COLLECTIVE: (150, 100, 255),
    Faction.VOID_RAIDERS: (255, 80, 80),
    Faction.ANCIENT_ONES: (255, 200, 100),
    Faction.PRIMITIVE: (180, 140, 100),
}

FACTION_ATTITUDES: Dict[Faction, int] = {
    Faction.TERRAN_ALLIANCE: 50,
    Faction.CRYSTAL_COLLECTIVE: 0,
    Faction.VOID_RAIDERS: -50,
    Faction.ANCIENT_ONES: 0,
    Faction.PRIMITIVE: 20,
}

TECH_LEVEL_NAMES: Dict[TechLevel, str] = {
    TechLevel.STONE_AGE: "Steinzeit",
    TechLevel.BRONZE_AGE: "Bronzezeit",
    TechLevel.IRON_AGE: "Eisenzeit",
    TechLevel.INDUSTRIAL: "Industrie",
    TechLevel.SPACE_AGE: "Raumfahrt",
    TechLevel.ADVANCED: "Fortgeschritten",
}

PLANET_TYPES: Dict[str, Tuple[Tuple[int, int, int], Dict[str, float]]] = {
    "Terran": ((60, 120, 60), {"metal": 0.3, "water": 0.5, "food": 0.4}),
    "Desert": ((180, 150, 100), {"crystal": 0.5, "metal": 0.4}),
    "Ice": ((200, 220, 255), {"water": 0.8, "crystal": 0.3}),
    "Volcanic": ((150, 80, 50), {"metal": 0.6, "energy": 0.5}),
    "Barren": ((120, 110, 100), {"metal": 0.8}),
    "Oceanic": ((50, 100, 150), {"water": 0.9, "food": 0.3}),
    "Anomaly": ((150, 50, 150), {"shard": 1.0, "energy": 0.6}),
    "Jungle": ((40, 100, 40), {"food": 0.7, "water": 0.4}),
    "Gas Giant": ((180, 150, 200), {"energy": 0.9}),
}

# Erweiterte Gebäude mit Upgrade-Möglichkeiten
BUILDINGS: Dict[str, Tuple[str, int, int, Dict[str, int], str, int]] = {
    # name, metal_cost, crystal_cost, production, category, max_level
    "command": ("Kommandozentrale", 200, 50, {}, "colony", 3),
    "mine": ("Metallmine", 80, 0, {"metal": 2}, "production", 5),
    "crystal": ("Kristallbohrer", 100, 0, {"crystal": 1}, "production", 5),
    "solar": ("Solarpanel", 60, 20, {"energy": 3}, "production", 5),
    "farm": ("Hydroponik-Farm", 100, 30, {"food": 2}, "production", 5),
    "water": ("Wasserpumpe", 80, 10, {"water": 2}, "production", 5),
    "storage": ("Lager", 150, 50, {}, "storage", 3),
    "turret": ("Geschützturm", 200, 100, {}, "defense", 5),
    "shield": ("Schildgenerator", 300, 150, {}, "defense", 3),
    "research": ("Forschungslabor", 400, 200, {}, "research", 3),
    "barracks": ("Kaserne", 250, 80, {}, "military", 3),
    "factory": ("Fabrik", 350, 150, {}, "production", 3),
    "refinery": ("Raffinerie", 300, 100, {}, "production", 3),
    "reactor": ("Fusionsreaktor", 500, 300, {"energy": 10}, "production", 3),
    "spaceport": ("Raumhafen", 600, 400, {}, "special", 1),
}

# Erweitertes Forschungs-System mit Tech-Tree
RESEARCH: Dict[str, Tuple[str, int, int, str, List[str]]] = {
    # name, crystal_cost, time, description, prerequisites
    "mining1": ("Bergbau I", 100, 30, "Minen +50%", []),
    "mining2": ("Bergbau II", 200, 60, "Minen +100%", ["mining1"]),
    "mining3": ("Bergbau III", 400, 90, "Minen +150%", ["mining2"]),
    "solar1": ("Solarenergie I", 100, 30, "Solar +50%", []),
    "solar2": ("Solarenergie II", 250, 60, "Solar +100%", ["solar1"]),
    "weapons1": ("Waffen I", 150, 45, "Schaden +25%", []),
    "weapons2": ("Waffen II", 300, 75, "Schaden +50%", ["weapons1"]),
    "shields1": ("Schilde I", 150, 45, "Schild +50", []),
    "shields2": ("Schilde II", 300, 75, "Schild +100", ["shields1"]),
    "speed1": ("Antrieb I", 200, 60, "Speed +20%", []),
    "speed2": ("Antrieb II", 400, 90, "Speed +40%", ["speed1"]),
    "diplomacy1": ("Diplomatie", 300, 90, "Bessere Beziehungen", []),
    "scanner1": ("Scanner I", 150, 45, "Größere Sichtweite", []),
    "workers1": ("Arbeitskraft I", 200, 60, "Worker +25% Speed", []),
    "workers2": ("Arbeitskraft II", 400, 90, "Worker +50% Speed", ["workers1"]),
    "automation": ("Automatisierung", 500, 120, "Auto-Ressourcen-Sammlung", ["workers1"]),
    "quantum": ("Quanten-Tech", 1000, 180, "Alle Boni +25%", ["mining2", "solar2", "weapons2"]),
}

# Achievement-System
ACHIEVEMENTS: Dict[str, Tuple[str, str, str]] = {
    "first_colony": ("Erste Kolonie", "Gründe deine erste Kolonie", "🏠"),
    "explorer": ("Entdecker", "Besuche 5 verschiedene Sternensysteme", "🚀"),
    "researcher": ("Forscher", "Schließe 5 Forschungen ab", "🔬"),
    "warrior": ("Krieger", "Eliminiere 50 Feinde", "⚔️"),
    "diplomat": ("Diplomat", "Erreiche 75+ Beziehung mit einer Fraktion", "🤝"),
    "tycoon": ("Tycoon", "Sammle 10,000 Metal", "💰"),
    "fleet_commander": ("Flottenkommandant", "Besitze 10 Worker", "👷"),
    "master_builder": ("Meisterbauer", "Baue 50 Gebäude", "🏗️"),
    "tech_master": ("Tech-Meister", "Erforsche alle Technologien", "🎓"),
    "emperor": ("Imperator", "Gründe Kolonien in 3 Systemen", "👑"),
}

# Kampagnen-Missionen
CAMPAIGN_MISSIONS: List[Dict] = [
    {
        "id": "mission_01",
        "name": "Erste Schritte",
        "description": "Gründe deine erste Kolonie und baue grundlegende Infrastruktur.",
        "objectives": [
            {"type": "build", "building": "command", "count": 1, "desc": "Kommandozentrale bauen"},
            {"type": "build", "building": "mine", "count": 2, "desc": "2 Metallminen bauen"},
            {"type": "build", "building": "solar", "count": 1, "desc": "Solarpanel bauen"},
        ],
        "rewards": {"metal": 500, "crystal": 100, "energy": 200},
        "unlock_next": "mission_02",
        "intro_text": "Willkommen, Commander! Deine erste Aufgabe: Errichte eine funktionierende Kolonie!",
    },
    {
        "id": "mission_02",
        "name": "Workforce Expansion",
        "description": "Rekrutiere Worker und optimiere die Ressourcen-Gewinnung.",
        "objectives": [
            {"type": "workers", "count": 3, "desc": "3 Worker rekrutieren"},
            {"type": "resource", "resource": "metal", "amount": 1000, "desc": "1000 Metal sammeln"},
            {"type": "build", "building": "storage", "count": 1, "desc": "Lager bauen"},
        ],
        "rewards": {"metal": 400, "crystal": 200, "energy": 300},
        "unlock_next": "mission_03",
        "intro_text": "Exzellent! Jetzt brauchen wir eine effiziente Arbeitskraft.",
    },
    {
        "id": "mission_03",
        "name": "Verteidigungsinitiative",
        "description": "Schütze deine Kolonie vor feindlichen Angriffen.",
        "objectives": [
            {"type": "build", "building": "turret", "count": 2, "desc": "2 Geschütztürme bauen"},
            {"type": "build", "building": "shield", "count": 1, "desc": "Schildgenerator bauen"},
            {"type": "kill", "count": 10, "desc": "10 Feinde eliminieren"},
        ],
        "rewards": {"metal": 400, "crystal": 300, "shard": 2},
        "unlock_next": "mission_04",
        "intro_text": "⚠️ Feindliche Aktivitäten entdeckt! Bereite die Verteidigung vor!",
    },
    {
        "id": "mission_04",
        "name": "Forschung & Entwicklung",
        "description": "Erforsche neue Technologien für deinen Vorteil.",
        "objectives": [
            {"type": "build", "building": "research", "count": 1, "desc": "Forschungslabor bauen"},
            {"type": "research", "count": 3, "desc": "3 Technologien erforschen"},
            {"type": "resource", "resource": "crystal", "amount": 500, "desc": "500 Crystal sammeln"},
        ],
        "rewards": {"crystal": 500, "energy": 500, "shard": 3},
        "unlock_next": "mission_05",
        "intro_text": "Technologie ist der Schlüssel zum Sieg!",
    },
    {
        "id": "mission_05",
        "name": "Galaktische Expansion",
        "description": "Expandiere zu den Sternen und baue ein Imperium auf.",
        "objectives": [
            {"type": "colonies", "count": 2, "desc": "2 Kolonien gründen"},
            {"type": "systems", "count": 2, "desc": "2 verschiedene Systeme besuchen"},
            {"type": "diplomacy", "relation": 50, "desc": "50+ Beziehung mit einer Fraktion"},
        ],
        "rewards": {"metal": 1000, "crystal": 500, "shard": 5},
        "unlock_next": None,
        "intro_text": "Die finale Herausforderung: Werde zur dominanten Macht!",
    },
]

# Tutorial-Schritte
TUTORIAL_STEPS: List[Tuple[str, str, str]] = [
    ("Willkommen!", "Willkommen bei STERNENBRUCH! Dies ist ein Weltraum-Strategie-Spiel.", "galaxy"),
    ("Navigation", "Nutze WASD zum Bewegen und die Maus zum Zoomen (Galaxie-Ansicht).", "galaxy"),
    ("System betreten", "Klicke auf ein Sternensystem und drücke ENTER um es zu betreten.", "galaxy"),
    ("Raumschiff", "Nutze W für Vorwärts, A/D für Rotation. SPACE zum Schießen.", "system"),
    ("Planeten", "Fliege nah an einen Planeten und drücke E zum Landen.", "system"),
    ("Kolonie gründen", "Drücke B und baue eine Kommandozentrale um zu kolonisieren.", "planet"),
    ("Ressourcen", "Sammle Ressourcen mit E oder rekrutiere Worker mit N.", "planet"),
    ("Worker befehligen", "Ziehe ein Rechteck um Worker auszuwählen, Rechtsklick zum Befehl.", "planet"),
    ("Fortschritt", "Öffne das Kampagnen-Menü mit C für Ziele und Belohnungen.", "planet"),
]


# =============================================================================
# DATENKLASSEN
# =============================================================================

@dataclass
class Resources:
    metal: float = 0.0
    crystal: float = 0.0
    energy: float = 0.0
    food: float = 0.0
    water: float = 0.0
    shard: int = 0

    def to_dict(self) -> Dict[str, float]:
        return {
            'metal': self.metal, 'crystal': self.crystal, 'energy': self.energy,
            'food': self.food, 'water': self.water, 'shard': float(self.shard)
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'Resources':
        return cls(
            metal=d.get('metal', 0), crystal=d.get('crystal', 0),
            energy=d.get('energy', 0), food=d.get('food', 0),
            water=d.get('water', 0), shard=int(d.get('shard', 0))
        )


@dataclass
class Particle:
    """Partikel für visuelle Effekte."""
    x: float
    y: float
    vel_x: float
    vel_y: float
    color: Tuple[int, int, int, int]
    size: float
    lifetime: float
    max_lifetime: float
    particle_type: ParticleType

    def update(self, dt: float) -> bool:
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.lifetime -= dt

        # Gravity für Explosionen
        if self.particle_type == ParticleType.EXPLOSION:
            self.vel_y -= 50 * dt

        # Fade out
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            self.color = (*self.color[:3], alpha)

        return self.lifetime > 0


@dataclass
class Civilization:
    name: str
    faction: Faction
    tech_level: TechLevel
    population: int
    behavior: CivBehavior
    capital_x: float = 0.0
    capital_y: float = 0.0
    settlements: List[Tuple[float, float, str]] = field(default_factory=list)

    @property
    def military_strength(self) -> int:
        return int(self.population * self.tech_level.value * 0.1)

    @property
    def description(self) -> str:
        pop_desc = "winzige" if self.population < 100 else \
            "kleine" if self.population < 500 else \
            "mittelgroße" if self.population < 2000 else \
            "große" if self.population < 10000 else "riesige"
        return f"{pop_desc} {TECH_LEVEL_NAMES[self.tech_level]}-Zivilisation"

    def generate_settlements(self) -> None:
        self.settlements.clear()
        self.settlements.append((self.capital_x, self.capital_y, "capital"))
        num_settlements = min(10, self.population // 200)

        settlement_types = ["village", "town", "city", "outpost", "mine"]
        if self.tech_level.value >= TechLevel.INDUSTRIAL.value:
            settlement_types.extend(["factory", "base"])
        if self.tech_level.value >= TechLevel.SPACE_AGE.value:
            settlement_types.extend(["spaceport", "research"])

        for i in range(num_settlements):
            angle = (i / max(1, num_settlements)) * math.pi * 2
            dist = 200 + random.uniform(100, 400)
            x = self.capital_x + math.cos(angle) * dist
            y = self.capital_y + math.sin(angle) * dist
            stype = random.choice(settlement_types)
            self.settlements.append((x, y, stype))

    def to_dict(self) -> Dict:
        return {
            "name": self.name, "faction": self.faction.name,
            "tech_level": self.tech_level.value, "population": self.population,
            "behavior": self.behavior.value,
            "capital_x": self.capital_x, "capital_y": self.capital_y,
            "settlements": self.settlements,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'Civilization':
        civ = cls(
            name=d["name"], faction=Faction[d["faction"]],
            tech_level=TechLevel(d["tech_level"]), population=d["population"],
            behavior=CivBehavior(d["behavior"]),
            capital_x=d.get("capital_x", 0), capital_y=d.get("capital_y", 0),
        )
        civ.settlements = d.get("settlements", [])
        return civ


@dataclass
class Player:
    x: float = 0.0
    y: float = 0.0
    angle: float = 90.0
    vel_x: float = 0.0
    vel_y: float = 0.0
    health: float = 100.0
    max_health: float = 100.0
    shield: float = 50.0
    max_shield: float = 50.0
    resources: Resources = field(default_factory=Resources)
    completed_research: List[str] = field(default_factory=list)

    # Boni
    mining_bonus: float = 1.0
    solar_bonus: float = 1.0
    damage_bonus: float = 1.0
    speed_bonus: float = 1.0
    sight_bonus: float = 1.0
    worker_speed_bonus: float = 1.0

    # Diplomatie
    faction_relations: Dict[str, int] = field(default_factory=dict)

    # Fog of War
    revealed_tiles: Set[str] = field(default_factory=set)

    # Kampagne & Statistiken
    active_mission: Optional[str] = None
    completed_missions: List[str] = field(default_factory=list)
    mission_progress: Dict[str, Dict] = field(default_factory=dict)

    kills: Dict[str, int] = field(default_factory=dict)
    trades_completed: int = 0
    systems_visited: Set[str] = field(default_factory=set)
    total_metal_collected: float = 0.0
    total_crystal_collected: float = 0.0
    buildings_built: int = 0
    workers_created: int = 0

    # Achievements
    achievements: Set[str] = field(default_factory=set)

    # Tutorial
    tutorial_step: int = 0
    tutorial_completed: bool = False

    def __post_init__(self):
        if not self.faction_relations:
            self.faction_relations = {
                f.name: FACTION_ATTITUDES.get(f, 0)
                for f in Faction if f != Faction.PLAYER
            }

    def take_damage(self, amount: float) -> float:
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
                return 0.0
            amount -= self.shield
            self.shield = 0.0
        self.health = max(0.0, self.health - amount)
        return amount

    def heal(self, amount: float) -> None:
        self.health = min(self.max_health, self.health + amount)

    def recharge_shield(self, amount: float) -> None:
        self.shield = min(self.max_shield, self.shield + amount)

    def change_relation(self, faction: Faction, amount: int) -> None:
        if faction.name in self.faction_relations:
            current = self.faction_relations[faction.name]
            self.faction_relations[faction.name] = max(-100, min(100, current + amount))

    def get_relation(self, faction: Faction) -> int:
        return self.faction_relations.get(faction.name, 0)

    def get_stance(self, faction: Faction) -> str:
        rel = self.get_relation(faction)
        if rel >= 75: return "Verbündet"
        if rel >= 25: return "Freundlich"
        if rel >= -25: return "Neutral"
        if rel >= -75: return "Feindlich"
        return "Krieg"

    def reveal_area(self, center_x: float, center_y: float, radius: float) -> None:
        tile_radius = int(radius / FOG_TILE_SIZE) + 1
        center_tx = int(center_x / FOG_TILE_SIZE)
        center_ty = int(center_y / FOG_TILE_SIZE)
        for dx in range(-tile_radius, tile_radius + 1):
            for dy in range(-tile_radius, tile_radius + 1):
                if dx * dx + dy * dy <= tile_radius * tile_radius:
                    self.revealed_tiles.add(f"{center_tx + dx},{center_ty + dy}")

    def record_kill(self, faction: Faction) -> None:
        key = faction.name
        self.kills[key] = self.kills.get(key, 0) + 1

    def check_achievements(self, galaxy: Dict, workers_count: int) -> List[str]:
        """Prüft und gibt neu erreichte Achievements zurück."""
        new_achievements = []

        # Erste Kolonie
        if "first_colony" not in self.achievements:
            for system in galaxy.values():
                if any(p.owner == Faction.PLAYER for p in system.planets):
                    self.achievements.add("first_colony")
                    new_achievements.append("first_colony")
                    break

        # Entdecker
        if "explorer" not in self.achievements and len(self.systems_visited) >= 5:
            self.achievements.add("explorer")
            new_achievements.append("explorer")

        # Forscher
        if "researcher" not in self.achievements and len(self.completed_research) >= 5:
            self.achievements.add("researcher")
            new_achievements.append("researcher")

        # Krieger
        total_kills = sum(self.kills.values())
        if "warrior" not in self.achievements and total_kills >= 50:
            self.achievements.add("warrior")
            new_achievements.append("warrior")

        # Diplomat
        if "diplomat" not in self.achievements:
            for rel in self.faction_relations.values():
                if rel >= 75:
                    self.achievements.add("diplomat")
                    new_achievements.append("diplomat")
                    break

        # Tycoon
        if "tycoon" not in self.achievements and self.total_metal_collected >= 10000:
            self.achievements.add("tycoon")
            new_achievements.append("tycoon")

        # Fleet Commander
        if "fleet_commander" not in self.achievements and workers_count >= 10:
            self.achievements.add("fleet_commander")
            new_achievements.append("fleet_commander")

        # Master Builder
        if "master_builder" not in self.achievements and self.buildings_built >= 50:
            self.achievements.add("master_builder")
            new_achievements.append("master_builder")

        # Tech Master
        if "tech_master" not in self.achievements and len(self.completed_research) >= len(RESEARCH):
            self.achievements.add("tech_master")
            new_achievements.append("tech_master")

        # Imperator
        if "emperor" not in self.achievements:
            systems_with_colonies = set()
            for system in galaxy.values():
                if any(p.owner == Faction.PLAYER for p in system.planets):
                    systems_with_colonies.add(system.name)
            if len(systems_with_colonies) >= 3:
                self.achievements.add("emperor")
                new_achievements.append("emperor")

        return new_achievements


@dataclass
class Building:
    building_id: str
    x: int
    y: int
    level: int = 1
    health: float = 100.0
    active: bool = True
    current_research: Optional[str] = None
    research_progress: float = 0.0
    last_shot: float = 0.0

    @property
    def name(self) -> str:
        return BUILDINGS.get(self.building_id, ("???", 0, 0, {}, "", 1))[0]

    @property
    def max_level(self) -> int:
        return BUILDINGS.get(self.building_id, ("", 0, 0, {}, "", 1))[5]

    @property
    def production(self) -> Dict[str, int]:
        base_prod = BUILDINGS.get(self.building_id, ("", 0, 0, {}, "", 1))[3]
        # Produktion skaliert mit Level
        return {k: v * self.level for k, v in base_prod.items()}

    def get_upgrade_cost(self) -> Tuple[int, int]:
        """Gibt die Kosten für das nächste Upgrade zurück."""
        _, base_metal, base_crystal, _, _, _ = BUILDINGS.get(self.building_id, ("", 0, 0, {}, "", 1))
        # Kosten steigen exponentiell
        metal = int(base_metal * (1.5 ** self.level))
        crystal = int(base_crystal * (1.5 ** self.level))
        return metal, crystal

    def can_upgrade(self) -> bool:
        return self.level < self.max_level

    def to_dict(self) -> Dict:
        return {
            "id": self.building_id, "x": self.x, "y": self.y,
            "level": self.level, "health": self.health, "active": self.active,
            "research": self.current_research, "progress": self.research_progress
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'Building':
        b = cls(d["id"], d["x"], d["y"], d.get("level", 1))
        b.health = d.get("health", 100.0)
        b.active = d.get("active", True)
        b.current_research = d.get("research")
        b.research_progress = d.get("progress", 0.0)
        return b


@dataclass
class Worker:
    """Worker-Einheit für RTS-Mechaniken."""
    x: float
    y: float
    state: WorkerState = WorkerState.IDLE
    target_x: Optional[float] = None
    target_y: Optional[float] = None
    home_building: Optional[Building] = None
    assigned_resource: Optional[str] = None
    carrying: Dict[str, float] = field(default_factory=dict)
    carry_amount: float = 0.0
    carry_type: str = ""
    selected: bool = False
    health: float = 50.0
    max_health: float = 50.0
    harvest_timer: float = 0.0
    group: int = 0  # Gruppennummer (0-5)

    def distance_to(self, x: float, y: float) -> float:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def move_towards(self, tx: float, ty: float, speed: float, dt: float) -> bool:
        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 10:
            return True
        self.x += (dx / dist) * speed * dt
        self.y += (dy / dist) * speed * dt
        return False

    def update(self, dt: float, speed_bonus: float, planet: 'Planet', player_resources: Resources) -> Optional[str]:
        speed = WORKER_SPEED * speed_bonus

        if self.state == WorkerState.IDLE:
            pass

        elif self.state == WorkerState.MOVING:
            if self.target_x is not None and self.target_y is not None:
                if self.move_towards(self.target_x, self.target_y, speed, dt):
                    self.state = WorkerState.IDLE
                    self.target_x = None
                    self.target_y = None

        elif self.state == WorkerState.HARVESTING:
            if self.assigned_resource and self.assigned_resource in planet.resource_nodes:
                res_type, remaining = planet.resource_nodes[self.assigned_resource]
                target_parts = self.assigned_resource.split(",")
                target_x = int(target_parts[0]) * TILE_SIZE
                target_y = int(target_parts[1]) * TILE_SIZE

                if self.distance_to(target_x, target_y) > 40:
                    self.move_towards(target_x, target_y, speed, dt)
                else:
                    self.harvest_timer += dt
                    if self.harvest_timer >= 1.0:
                        self.harvest_timer = 0.0
                        harvest = min(WORKER_HARVEST_RATE, remaining, WORKER_CARRY_CAPACITY - self.carry_amount)
                        if harvest > 0:
                            self.carry_amount += harvest
                            self.carry_type = res_type
                            new_remaining = remaining - int(harvest)
                            if new_remaining <= 0:
                                del planet.resource_nodes[self.assigned_resource]
                                self.state = WorkerState.RETURNING
                            else:
                                planet.resource_nodes[self.assigned_resource] = (res_type, new_remaining)

                            if self.carry_amount >= WORKER_CARRY_CAPACITY:
                                self.state = WorkerState.RETURNING
            else:
                self.state = WorkerState.RETURNING

        elif self.state == WorkerState.RETURNING:
            if self.home_building:
                target_x = self.home_building.x * TILE_SIZE
                target_y = self.home_building.y * TILE_SIZE
            else:
                target_x, target_y = 0.0, 0.0

            if self.move_towards(target_x, target_y, speed, dt):
                if self.carry_amount > 0:
                    current = getattr(player_resources, self.carry_type, 0.0)
                    setattr(player_resources, self.carry_type, current + self.carry_amount)
                    msg = f"Worker: +{int(self.carry_amount)} {self.carry_type.title()}"
                    self.carry_amount = 0.0
                    self.carry_type = ""

                    if self.assigned_resource and self.assigned_resource in planet.resource_nodes:
                        self.state = WorkerState.HARVESTING
                    else:
                        self.state = WorkerState.IDLE
                        self.assigned_resource = None
                    return msg
                else:
                    self.state = WorkerState.IDLE

        return None

    def assign_to_resource(self, resource_key: str, home: Optional[Building] = None) -> None:
        self.assigned_resource = resource_key
        self.home_building = home
        self.state = WorkerState.HARVESTING

    def move_to(self, x: float, y: float) -> None:
        self.target_x = x
        self.target_y = y
        self.state = WorkerState.MOVING
        self.assigned_resource = None

    def to_dict(self) -> Dict:
        return {
            "x": self.x, "y": self.y, "state": self.state.value,
            "carry_amount": self.carry_amount, "carry_type": self.carry_type,
            "health": self.health, "assigned": self.assigned_resource,
            "group": self.group,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'Worker':
        w = cls(x=d["x"], y=d["y"])
        w.state = WorkerState(d.get("state", "idle"))
        w.carry_amount = d.get("carry_amount", 0.0)
        w.carry_type = d.get("carry_type", "")
        w.health = d.get("health", 50.0)
        w.assigned_resource = d.get("assigned")
        w.group = d.get("group", 0)
        return w


@dataclass
class Planet:
    name: str
    planet_type: str
    orbit_distance: float
    orbit_angle: float
    orbit_speed: float
    size: float
    danger_level: int
    owner: Optional[Faction] = None

    has_colony: bool = False
    buildings: List[Building] = field(default_factory=list)
    resource_nodes: Dict[str, Tuple[str, int]] = field(default_factory=dict)
    population: int = 0
    workers: List[Worker] = field(default_factory=list)
    civilization: Optional[Civilization] = None

    @property
    def x(self) -> float:
        return math.cos(self.orbit_angle) * self.orbit_distance

    @property
    def y(self) -> float:
        return math.sin(self.orbit_angle) * self.orbit_distance

    @property
    def color(self) -> Tuple[int, int, int]:
        return PLANET_TYPES.get(self.planet_type, ((100, 100, 100), {}))[0]

    def update_orbit(self, dt: float) -> None:
        self.orbit_angle += self.orbit_speed * dt

    def get_building_at(self, tx: int, ty: int) -> Optional[Building]:
        for b in self.buildings:
            if b.x == tx and b.y == ty:
                return b
        return None

    def add_building(self, building: Building) -> bool:
        if self.get_building_at(building.x, building.y):
            return False
        self.buildings.append(building)
        if building.building_id == "command":
            self.has_colony = True
        return True

    def get_command_center(self) -> Optional[Building]:
        for b in self.buildings:
            if b.building_id == "command":
                return b
        return None

    def spawn_worker(self) -> Optional[Worker]:
        cc = self.get_command_center()
        if cc:
            w = Worker(x=cc.x * TILE_SIZE + random.uniform(-20, 20),
                       y=cc.y * TILE_SIZE + random.uniform(-20, 20))
            w.home_building = cc
            self.workers.append(w)
            return w
        return None

    def generate_resources(self) -> None:
        if self.resource_nodes:
            return
        weights = PLANET_TYPES.get(self.planet_type, (None, {"metal": 0.5}))[1]
        for _ in range(random.randint(15, 30)):
            tx = random.randint(-50, 50)
            ty = random.randint(-50, 50)
            if abs(tx) < 5 and abs(ty) < 5:
                continue
            for res, chance in weights.items():
                if random.random() < chance:
                    self.resource_nodes[f"{tx},{ty}"] = (res, random.randint(100, 300))
                    break

    def generate_civilization(self) -> None:
        if self.civilization or self.planet_type == "Barren":
            return
        if random.random() > 0.6:
            return

        if self.owner:
            faction = self.owner
        else:
            faction = random.choice([
                Faction.TERRAN_ALLIANCE, Faction.CRYSTAL_COLLECTIVE,
                Faction.ANCIENT_ONES, Faction.PRIMITIVE
            ])

        if faction == Faction.PRIMITIVE:
            tech = random.choice([TechLevel.STONE_AGE, TechLevel.BRONZE_AGE, TechLevel.IRON_AGE])
        elif faction == Faction.ANCIENT_ONES:
            tech = random.choice([TechLevel.ADVANCED, TechLevel.SPACE_AGE])
        elif faction == Faction.CRYSTAL_COLLECTIVE:
            tech = random.choice([TechLevel.SPACE_AGE, TechLevel.ADVANCED])
        else:
            tech = random.choice(list(TechLevel))

        base_pop = 50 * tech.value
        if self.planet_type == "Terran":
            base_pop *= 3
        elif self.planet_type == "Oceanic":
            base_pop *= 2
        elif self.planet_type in ["Desert", "Ice", "Volcanic"]:
            base_pop = int(base_pop * 0.5)

        population = int(base_pop * random.uniform(0.5, 2.0))

        if faction == Faction.VOID_RAIDERS:
            behavior = CivBehavior.AGGRESSIVE
        elif faction == Faction.PRIMITIVE:
            behavior = random.choice([CivBehavior.PEACEFUL, CivBehavior.DEFENSIVE, CivBehavior.ISOLATIONIST])
        else:
            behavior = random.choice(list(CivBehavior))

        prefixes = ["Neu-", "Alt-", "Groß-", "Klein-", ""]
        suffixes = ["dorf", "stadt", "heim", "burg", "tal", "hausen", "berg"]
        civ_name = f"{random.choice(prefixes)}{self.name.split('-')[-1]}{random.choice(suffixes)}"

        capital_angle = random.uniform(0, math.pi * 2)
        capital_dist = random.uniform(300, 600)

        self.civilization = Civilization(
            name=civ_name, faction=faction, tech_level=tech, population=population,
            behavior=behavior,
            capital_x=math.cos(capital_angle) * capital_dist,
            capital_y=math.sin(capital_angle) * capital_dist,
        )
        self.civilization.generate_settlements()
        self.owner = faction

    def collect_resource(self, tx: int, ty: int, amount: int = 20) -> Tuple[str, int]:
        key = f"{tx},{ty}"
        if key in self.resource_nodes:
            res_type, remaining = self.resource_nodes[key]
            collected = min(amount, remaining)
            if collected >= remaining:
                del self.resource_nodes[key]
            else:
                self.resource_nodes[key] = (res_type, remaining - collected)
            return res_type, collected
        return "", 0

    def to_dict(self) -> Dict:
        return {
            "name": self.name, "type": self.planet_type,
            "orbit_dist": self.orbit_distance, "orbit_angle": self.orbit_angle,
            "orbit_speed": self.orbit_speed, "size": self.size,
            "danger": self.danger_level, "colony": self.has_colony,
            "owner": self.owner.name if self.owner else None,
            "population": self.population,
            "buildings": [b.to_dict() for b in self.buildings],
            "resources": self.resource_nodes,
            "workers": [w.to_dict() for w in self.workers],
            "civilization": self.civilization.to_dict() if self.civilization else None,
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'Planet':
        owner = None
        if d.get("owner"):
            try:
                owner = Faction[d["owner"]]
            except KeyError:
                pass
        p = cls(
            d["name"], d["type"], d["orbit_dist"], d["orbit_angle"],
            d["orbit_speed"], d["size"], d["danger"], owner
        )
        p.has_colony = d.get("colony", False)
        p.population = d.get("population", 0)
        p.buildings = [Building.from_dict(b) for b in d.get("buildings", [])]
        p.resource_nodes = d.get("resources", {})
        p.workers = [Worker.from_dict(w) for w in d.get("workers", [])]
        if d.get("civilization"):
            p.civilization = Civilization.from_dict(d["civilization"])
        return p


@dataclass
class StarSystem:
    name: str
    x: float
    y: float
    star_color: Tuple[int, int, int]
    star_size: float
    planets: List[Planet] = field(default_factory=list)
    controlling_faction: Optional[Faction] = None

    def update(self, dt: float) -> None:
        for p in self.planets:
            p.update_orbit(dt)

    def get_colony_count(self, faction: Optional[Faction] = None) -> int:
        if faction is None:
            return sum(1 for p in self.planets if p.has_colony)
        return sum(1 for p in self.planets if p.owner == faction)

    def to_dict(self) -> Dict:
        return {
            "name": self.name, "x": self.x, "y": self.y,
            "star_color": list(self.star_color), "star_size": self.star_size,
            "controlling": self.controlling_faction.name if self.controlling_faction else None,
            "planets": [p.to_dict() for p in self.planets],
        }

    @classmethod
    def from_dict(cls, d: Dict) -> 'StarSystem':
        ctrl = None
        if d.get("controlling"):
            try:
                ctrl = Faction[d["controlling"]]
            except KeyError:
                pass
        s = cls(d["name"], d["x"], d["y"], tuple(d["star_color"]), d["star_size"])
        s.controlling_faction = ctrl
        s.planets = [Planet.from_dict(p) for p in d.get("planets", [])]
        return s


# =============================================================================
# ENTITÄTEN
# =============================================================================

@dataclass
class Entity:
    x: float
    y: float
    health: float = 50.0
    max_health: float = 50.0
    speed: float = 80.0
    angle: float = 0.0
    faction: Faction = Faction.VOID_RAIDERS

    ai_state: AIState = AIState.IDLE
    target_x: Optional[float] = None
    target_y: Optional[float] = None
    home_x: float = 0.0
    home_y: float = 0.0
    alert_timer: float = 0.0
    patrol_timer: float = 0.0
    sight_range: float = ENEMY_SIGHT_RANGE
    attack_range: float = ENEMY_ATTACK_RANGE

    is_alerted: bool = False
    alert_display_timer: float = 0.0

    def __post_init__(self):
        self.home_x = self.x
        self.home_y = self.y

    def update_ai(self, player_x: float, player_y: float, player_relation: int, dt: float) -> None:
        dist_to_player = self.distance_to(player_x, player_y)

        if self.alert_display_timer > 0:
            self.alert_display_timer -= dt

        is_hostile = player_relation < -25

        if self.ai_state == AIState.IDLE:
            self.patrol_timer += dt
            if self.patrol_timer > 3.0:
                self.ai_state = AIState.PATROL
                self.patrol_timer = 0.0
                angle = random.uniform(0, math.pi * 2)
                self.target_x = self.home_x + math.cos(angle) * ENEMY_PATROL_RANGE
                self.target_y = self.home_y + math.sin(angle) * ENEMY_PATROL_RANGE

            if is_hostile and dist_to_player < self.sight_range:
                self.ai_state = AIState.ALERT
                self.alert_timer = 1.5
                self.is_alerted = True
                self.alert_display_timer = 2.0

        elif self.ai_state == AIState.PATROL:
            if self.target_x is not None:
                self.move_towards(self.target_x, self.target_y, dt)
                if self.distance_to(self.target_x, self.target_y) < 20:
                    self.ai_state = AIState.IDLE
                    self.target_x = None
            else:
                self.ai_state = AIState.IDLE

            if is_hostile and dist_to_player < self.sight_range:
                self.ai_state = AIState.ALERT
                self.alert_timer = 1.5
                self.is_alerted = True
                self.alert_display_timer = 2.0

        elif self.ai_state == AIState.ALERT:
            dx, dy = player_x - self.x, player_y - self.y
            self.angle = math.degrees(math.atan2(dy, dx))

            self.alert_timer -= dt
            if self.alert_timer <= 0:
                self.ai_state = AIState.CHASE

            if dist_to_player > self.sight_range * 1.5:
                self.ai_state = AIState.IDLE
                self.is_alerted = False

        elif self.ai_state == AIState.CHASE:
            self.is_alerted = True
            self.alert_display_timer = 0.5

            if dist_to_player < self.attack_range:
                self.ai_state = AIState.ATTACK
            else:
                self.move_towards(player_x, player_y, dt)

            if dist_to_player > self.sight_range * 2:
                self.ai_state = AIState.IDLE
                self.is_alerted = False

        elif self.ai_state == AIState.ATTACK:
            self.is_alerted = True
            self.alert_display_timer = 0.5

            if dist_to_player > self.attack_range * 0.8:
                self.move_towards(player_x, player_y, dt * 0.7)

            if dist_to_player > self.attack_range * 1.5:
                self.ai_state = AIState.CHASE

    def move_towards(self, tx: float, ty: float, dt: float) -> None:
        dx, dy = tx - self.x, ty - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 5:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt
            self.angle = math.degrees(math.atan2(dy, dx))

    def distance_to(self, x: float, y: float) -> float:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def take_damage(self, amount: float) -> bool:
        self.health -= amount
        if self.ai_state in [AIState.IDLE, AIState.PATROL, AIState.ALERT]:
            self.ai_state = AIState.CHASE
            self.is_alerted = True
            self.alert_display_timer = 2.0
        return self.health <= 0


@dataclass
class NPC(Entity):
    name: str = "NPC"
    npc_type: str = "trader"
    dialog: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.ai_state = AIState.IDLE

    def get_dialog(self, player_relation: int) -> str:
        if self.npc_type == "trader":
            if player_relation >= 50:
                return "Willkommen, Freund! Beste Preise für Verbündete."
            elif player_relation >= 0:
                return "Handel? Zeig mir deine Waren."
            else:
                return "Mach schnell. Ich vertraue dir nicht."
        elif self.npc_type == "diplomat":
            return "Ich spreche im Namen meines Volkes."
        elif self.npc_type == "villager":
            return "Willkommen in unserem Dorf!"
        elif self.npc_type == "guard":
            if player_relation < 0:
                return "Halt! Fremde sind hier nicht willkommen."
            return "Passieren Sie."
        return "..."


@dataclass
class Projectile:
    x: float
    y: float
    vel_x: float
    vel_y: float
    damage: float = 10.0
    lifetime: float = 2.0
    owner: str = "player"
    color: Tuple[int, int, int] = (0, 255, 100)

    def update(self, dt: float) -> bool:
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.lifetime -= dt
        return self.lifetime > 0


@dataclass
class SpaceShip(Entity):
    ship_type: str = "trader"

    def update(self, player_x: float, player_y: float, player_relation: int, dt: float) -> None:
        dist_to_player = self.distance_to(player_x, player_y)
        is_hostile = player_relation < -25 or self.faction == Faction.VOID_RAIDERS

        if self.alert_display_timer > 0:
            self.alert_display_timer -= dt

        if is_hostile and dist_to_player < 400:
            if dist_to_player < 250:
                self.is_alerted = True
                self.alert_display_timer = 0.5
                self.target_x = player_x
                self.target_y = player_y
        elif self.target_x is None or self.distance_to(self.target_x, self.target_y) < 30:
            self.target_x = random.uniform(-600, 600)
            self.target_y = random.uniform(-500, 500)
            self.is_alerted = False

        if self.target_x is not None:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 0:
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt
                target_angle = math.degrees(math.atan2(dy, dx))
                angle_diff = (target_angle - self.angle + 180) % 360 - 180
                self.angle += angle_diff * 3 * dt

    @property
    def color(self) -> Tuple[int, int, int]:
        return FACTION_COLORS.get(self.faction, (150, 150, 150))


# =============================================================================
# PARALLAX-STERNE
# =============================================================================

@dataclass
class ParallaxLayer:
    """Parallax-Hintergrund-Ebene."""
    stars: List[Tuple[float, float, float, Tuple[int, int, int]]]
    speed_factor: float

    @classmethod
    def generate(cls, count: int, speed_factor: float, seed: int = 0) -> 'ParallaxLayer':
        random.seed(seed)
        stars = []
        for _ in range(count):
            x = random.uniform(-2500, 2500)
            y = random.uniform(-2500, 2500)
            size = random.uniform(0.5, 2.5) * (1.0 - speed_factor * 0.4)
            brightness = random.randint(50, 180)
            color = (brightness, brightness, brightness + random.randint(0, 40))
            stars.append((x, y, size, color))
        random.seed()
        return cls(stars=stars, speed_factor=speed_factor)


# =============================================================================
# HILFSFUNKTIONEN - GALAXIE
# =============================================================================

def generate_galaxy(num_systems: int = 50) -> Dict[str, StarSystem]:
    """Generiert eine Galaxie mit Sternensystemen."""
    galaxy: Dict[str, StarSystem] = {}

    prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Nova", "Pulsar",
                "Vega", "Sirius", "Rigel", "Kepler", "Proxima", "Omega",
                "Tau", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]
    suffixes = ["Prime", "Major", "Minor", "I", "II", "III", "Core", "Nexus",
                "Haven", "Station", "Colony", "Outpost", "Sector"]

    star_colors: List[Tuple[int, int, int]] = [
        (255, 220, 180), (255, 180, 100), (200, 200, 255),
        (255, 100, 100), (255, 255, 200), (200, 255, 255)
    ]

    factions: List[Optional[Faction]] = [
        Faction.TERRAN_ALLIANCE, Faction.CRYSTAL_COLLECTIVE,
        Faction.VOID_RAIDERS, Faction.ANCIENT_ONES, None, None, None
    ]

    for i in range(num_systems):
        name = f"{random.choice(prefixes)}-{random.choice(suffixes)}"
        while name in galaxy:
            name = f"{random.choice(prefixes)}-{random.choice(suffixes)}-{i}"

        # Spiralgalaxie-Layout
        angle = random.uniform(0, math.pi * 4)
        dist = 70 + i * 12 + random.uniform(-35, 35)
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist * 0.7

        is_anomaly = random.random() < 0.06
        ctrl_faction = random.choice(factions) if i > 6 else None

        system = StarSystem(
            name=name, x=x, y=y,
            star_color=(200, 0, 150) if is_anomaly else random.choice(star_colors),
            star_size=random.uniform(22, 48),
            controlling_faction=ctrl_faction,
        )

        num_planets = random.randint(2, 6)
        planet_types = list(PLANET_TYPES.keys())

        for j in range(num_planets):
            ptype = "Anomaly" if is_anomaly else random.choice(planet_types[:-2])

            planet_owner = None
            if ctrl_faction and random.random() < 0.35:
                planet_owner = ctrl_faction

            planet = Planet(
                name=f"{name}-{chr(97 + j)}",
                planet_type=ptype,
                orbit_distance=65 + j * 52 + random.uniform(-8, 8),
                orbit_angle=random.uniform(0, math.pi * 2),
                orbit_speed=0.07 / (j + 1),
                size=random.uniform(14, 34),
                danger_level=random.randint(1, 3) + (2 if is_anomaly else 0),
                owner=planet_owner,
            )

            if planet_owner:
                planet.has_colony = True
                planet.population = random.randint(80, 900)

            planet.generate_civilization()
            planet.generate_resources()
            system.planets.append(planet)

        galaxy[name] = system

    return galaxy


def create_explosion_particles(x: float, y: float, count: int = 25) -> List[Particle]:
    """Erstellt Explosionspartikel."""
    particles = []
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(50, 200)
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed

        colors = [(255, 100, 0, 255), (255, 150, 0, 255), (255, 200, 0, 255), (255, 255, 100, 255)]
        color = random.choice(colors)
        size = random.uniform(2, 6)
        lifetime = random.uniform(0.3, 0.8)

        particles.append(Particle(
            x=x, y=y, vel_x=vel_x, vel_y=vel_y,
            color=color, size=size, lifetime=lifetime,
            max_lifetime=lifetime, particle_type=ParticleType.EXPLOSION
        ))
    return particles


def create_resource_particles(x: float, y: float, res_type: str, count: int = 10) -> List[Particle]:
    """Erstellt Ressourcen-Sammel-Partikel."""
    particles = []
    color_map = {
        "metal": (180, 180, 200, 255),
        "crystal": (100, 150, 255, 255),
        "energy": (255, 255, 100, 255),
        "food": (100, 200, 100, 255),
        "water": (100, 180, 255, 255),
    }
    color = color_map.get(res_type, (200, 200, 200, 255))

    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(20, 60)
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed - 30  # Nach oben

        size = random.uniform(1, 3)
        lifetime = random.uniform(0.4, 0.7)

        particles.append(Particle(
            x=x, y=y, vel_x=vel_x, vel_y=vel_y,
            color=color, size=size, lifetime=lifetime,
            max_lifetime=lifetime, particle_type=ParticleType.RESOURCE
        ))
    return particles


# =============================================================================
# HAUPTSPIEL-KLASSE (Teil 1 - Fortsetzung folgt...)
# =============================================================================
# Die Datei wird fortgesetzt in Teil 2 aufgrund der Längenbeschränkung
