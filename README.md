# _MyGames
This is a try of coding my games - feel free to help me

---

# ⭐ STERNENBRUCH v8 - Enhanced Edition ⭐

Ein umfangreiches Weltraum-Kolonisierungs-Strategiespiel mit RTS-Elementen, gebaut mit Python und Arcade.

![Version](https://img.shields.io/badge/version-8.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎮 Features-Übersicht

### ✨ Version 8 - Was ist neu?

####  Hauptverbesserungen
- ✅ **Particle-System**: Explosionen, Sammel-Effekte, Laser-Treffer
- ✅ **Achievement-System**: 10 freischaltbare Achievements
- ✅ **Tutorial-System**: Interaktive Einführung für neue Spieler
- ✅ **Gebäude-Upgrades**: Alle Gebäude auf bis zu Level 5 verbesserbar
- ✅ **Worker-Gruppen**: RTS-Gruppensteuerung (Tasten 1-5)
- ✅ **Auto-Save**: Automatisches Speichern alle 5 Minuten
- ✅ **Tech-Tree-Ansicht**: Visualisierung des Forschungsbaums
- ✅ **Erweiterte Statistiken**: Detaillierter Statistik-Bildschirm
- ✅ **Tooltips**: Hover-Informationen überall
- ✅ **20+ Hotkeys**: Erweiterte Tastenkombinationen
- ✅ **Parallax-Hintergrund**: 3 Ebenen für Tiefeneffekt
- ✅ **Performance-Optimierungen**: Besseres Rendering und Updates

#### 🏗️ Neue Gebäude
- Fabrik (Max Level 3)
- Raffinerie (Max Level 3)
- Fusionsreaktor (Max Level 3) - 10 Energy/s pro Level!
- Raumhafen (Spezialgebäude)

#### 🔬 Erweiterte Forschung
- Bergbau III (+150% Effizienz)
- Solarenergie II (+100%)
- Waffen II (+50% Schaden)
- Schilde II (+100 Schild)
- Antrieb II (+40% Speed)
- Arbeitskraft II (+50% Worker-Speed)
- Automatisierung (Auto-Ressourcen)
- **Quanten-Tech** (Endgame: +25% auf ALLES!)

## 🚀 Schnellstart

### Installation

```bash
# 1. Python 3.8+ installieren (falls nicht vorhanden)
# 2. Arcade installieren
pip install arcade

# 3. Spiel starten
python sternenbruch_complete.py
```

### Erste Schritte

1. **Starte** das Spiel mit `python sternenbruch_complete.py`
2. **Folge** dem Tutorial (automatisch beim ersten Start)
3. **Drücke H** für die Hotkey-Übersicht
4. **Drücke C** für Kampagnen-Missionen

## ⌨️ Wichtigste Hotkeys

| Taste | Aktion |
|-------|--------|
| **WASD** | Bewegen / Raumschiff steuern |
| **SPACE** | Schießen |
| **E** | Interagieren / Landen |
| **B** | Baumenü |
| **F** | Forschung |
| **N** | Worker rekrutieren |
| **C** | Kampagnen |
| **A** | Achievements |
| **T** | Tech-Tree |
| **S** | Statistiken |
| **H** | Hotkeys-Hilfe |
| **F5** | Speichern |
| **F9** | Laden |

### Worker-Steuerung (RTS)
- **Linksklick + Ziehen**: Worker auswählen
- **Rechtsklick**: Befehl (Bewegen/Sammeln)
- **1-5**: Gruppe zuweisen
- **SHIFT + 1-5**: Gruppe auswählen

## 📊 Vollständige Features

### Kernmechaniken
- 🌌 **50+ Sternensysteme** prozedural generiert
- 🪐 **9 Planeten-Typen** mit einzigartigen Ressourcen
- ⚒️ **14 Gebäude-Typen** (alle upgradefähig)
- 🔬 **15 Forschungen** mit Tech-Tree
- 👷 **Worker-RTS-System** mit Gruppen
- 🎯 **5 Kampagnen-Missionen**
- 🏆 **10 Achievements**
- 👥 **5 Fraktionen** mit Diplomatie
- 🌫️ **Fog of War** auf Planeten
- 💾 **Auto-Save** + manuelles Speichern

### Spielmodi
1. **Galaxie-Ansicht**: Strategische Übersicht
2. **System-Ansicht**: Raumschiff-Steuerung
3. **Planeten-Ansicht**: RTS-Kolonie-Management

## 🎯 Tipps für Anfänger

### Start-Strategie
1. Baue **Kommandozentrale** (B → Command → ENTER)
2. Baue **2-3 Metallminen**
3. Baue **Solarpanel** für Energie
4. Rekrutiere **2 Worker** (Taste N)
5. Weise Worker Ressourcen zu (Rechtsklick auf Metall/Crystal)

### Effiziente Expansion
- Erforsche **Bergbau I** früh (+50% Minen)
- Upgrade Gebäude auf Level 2-3
- Nutze Worker-Gruppen für Organisation
- Baue **Geschütztürme** zur Verteidigung

### Fortgeschritten
- **Quanten-Tech** ist die mächtigste Forschung
- Kolonisiere **Terran-Planeten** für beste Ressourcen
- Verbessere **Diplomatie** für Handelsboni
- Maximiere Gebäude auf **Level 5**

## 📁 Projektstruktur

```
_MyGames/
├── sternenbruch_enhanced.py       # Basis-Code (Teil 1)
├── sternenbruch_complete.py       # Vollständiges Spiel
├── README.md                       # Diese Datei
├── sternenbruch_save.json         # Speicherstand
└── autosave.json                  # Auto-Save
```

## 🐛 Problemlösung

### Spiel startet nicht
- Prüfe Python-Version: `python --version` (mind. 3.8)
- Installiere Arcade: `pip install arcade`
- Prüfe Fehlermeldungen in der Konsole

### Performance-Probleme
- Reduziere Anzahl der Entities (weniger Gegner spawnen)
- Schließe andere Programme
- Aktualisiere Grafiktreiber

### Speichern funktioniert nicht
- Prüfe Schreibrechte im Verzeichnis
- Speicherpfad: gleicher Ordner wie Skript

## 🎓 Lernressourcen

- **Tutorial**: Im Spiel integriert (automatisch beim Start)
- **Hotkeys**: Drücke H im Spiel
- **Kampagnen**: Drücke C für geführte Missionen

## 📝 Changelog

### v8.0 - Enhanced Edition (2025-12-02)
- Vollständige Überarbeitung mit 15+ neuen Features
- Performance-Verbesserungen
- UI/UX-Verbesserungen
- Erweiterte Dokumentation

### v7.0 - Original
- Grundlegendes Worker-System
- Kampagnen
- Fog of War

## 🤝 Beitragen

Verbesserungsvorschläge und Bug-Reports willkommen!

## 📜 Lizenz

MIT License - Frei verwendbar

---

**Viel Erfolg beim Erobern der Galaxie! 🚀✨**

*v8.0 Enhanced Edition | Entwickelt mit Claude AI*
