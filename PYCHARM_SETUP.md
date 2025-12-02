# 🎮 PyCharm Setup für STERNENBRUCH v8

## ✅ Schritt-für-Schritt Anleitung

### 1. Projekt in PyCharm öffnen

**Option A: Wenn PyCharm bereits offen ist**
```
File → Open → Navigiere zu: /home/user/_MyGames/
→ OK klicken
```

**Option B: Projekt neu öffnen**
```
PyCharm starten → Open → /home/user/_MyGames/ auswählen
```

### 2. Projekt refreshen

Falls du die Dateien nicht siehst:
```
Rechtsklick auf "_MyGames" im Project Explorer
→ "Reload from Disk" oder "Synchronize"

ODER

Tastenkombination: Ctrl + Alt + Y (Windows/Linux)
                   Cmd + Alt + Y (Mac)
```

### 3. Python Interpreter einrichten

```
File → Settings → Project: _MyGames → Python Interpreter
→ Stelle sicher, dass Python 3.8+ ausgewählt ist
→ OK klicken
```

### 4. Arcade installieren

**In PyCharm Terminal** (Alt+F12):
```bash
pip install arcade
```

Oder über PyCharm Package Manager:
```
File → Settings → Project: _MyGames → Python Interpreter
→ Klick auf "+" Button
→ Suche nach "arcade"
→ "Install Package" klicken
```

### 5. Spiel starten

**Option A: Mit Run Configuration (empfohlen)**
```
Oben rechts in PyCharm solltest du jetzt "Sternenbruch v8" sehen
→ Grüner Play-Button klicken ▶️
```

**Option B: Datei direkt ausführen**
```
Öffne sternenbruch_complete.py
→ Rechtsklick → "Run 'sternenbruch_complete'"

ODER

Tastenkombination: Shift + F10
```

**Option C: Terminal**
```bash
cd /home/user/_MyGames
python3 sternenbruch_complete.py
```

**Option D: Start-Script**
```bash
./start_game.sh
```

## 📁 Projektstruktur in PyCharm

Nach dem Öffnen solltest du sehen:

```
_MyGames/
├── .git/                              (Git Repository)
├── .idea/                             (PyCharm Konfiguration)
│   └── runConfigurations/
│       └── Sternenbruch_v8.xml        (Run Config)
├── sternenbruch_enhanced.py           ⭐ Basis-Code (Teil 1)
├── sternenbruch_complete.py           ⭐ HAUPTDATEI - STARTE DIESE!
├── README.md                          📖 Hauptdokumentation
├── IMPROVEMENTS.md                    📊 Verbesserungsliste
├── PYCHARM_SETUP.md                   🔧 Diese Datei
└── start_game.sh                      🚀 Start-Script
```

## 🔧 Fehlerbehebung

### "Dateien werden nicht angezeigt"
```
1. Rechtsklick auf Projektordner → "Reload from Disk"
2. File → Invalidate Caches → "Invalidate and Restart"
3. PyCharm neu starten
```

### "Python Interpreter nicht gefunden"
```
File → Settings → Project Interpreter
→ "Show All" → "+" → "System Interpreter"
→ Python 3.8+ auswählen
```

### "Module 'arcade' not found"
```
Im Terminal:
pip install arcade

ODER pip3 install arcade
```

### "Permission denied beim Start-Script"
```bash
chmod +x start_game.sh
./start_game.sh
```

## 🎮 Spielen in PyCharm

1. **Öffne** `sternenbruch_complete.py`
2. **Klicke** den grünen ▶️ Button oben rechts
3. **Spiel startet** in neuem Fenster
4. **Drücke H** im Spiel für Hotkeys

## 💡 PyCharm Tipps

### Nützliche Shortcuts:
- **Shift + F10**: Letztes Programm erneut starten
- **Alt + F12**: Terminal öffnen
- **Ctrl + B**: Zu Definition springen
- **Ctrl + Q**: Quick Documentation
- **Shift + F6**: Rename

### Code erkunden:
- **Rechtsklick auf Klasse/Funktion** → "Go to Definition"
- **Ctrl + Klick** auf Funktionsnamen → Springt zur Definition
- **Ctrl + F**: Suche in aktueller Datei
- **Ctrl + Shift + F**: Projekt-weite Suche

## 🐛 Debug-Modus

Um das Spiel zu debuggen:
```
1. Setze Breakpoint (Klick links neben Zeilennummer)
2. Klicke Debug-Button 🐞 statt Play ▶️
3. Programm pausiert an Breakpoint
4. Untersuche Variablen im Debug-Fenster
```

## 📝 Weitere Dokumentation

- **README.md**: Vollständige Spiel-Dokumentation
- **IMPROVEMENTS.md**: Alle Verbesserungen v7 → v8
- Code-Kommentare direkt im Quellcode

## ✨ Schnellstart Zusammenfassung

```bash
# 1. In Terminal (Alt+F12 in PyCharm):
pip install arcade

# 2. Datei öffnen:
sternenbruch_complete.py

# 3. Grünen Play-Button klicken ▶️

# 4. Spielen! 🎮
```

---

**Viel Spaß beim Entwickeln und Spielen! 🚀✨**

Bei Fragen: Siehe README.md oder IMPROVEMENTS.md
