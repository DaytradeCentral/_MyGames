# 🪟 STERNENBRUCH v8 - Windows & PyCharm Installation

## 📥 SO BEKOMMST DU DAS SPIEL AUF DEINEN WINDOWS PC

### Methode 1: Download von GitHub (EMPFOHLEN)

1. **Gehe zu GitHub:**
   ```
   https://github.com/DaytradeCentral/_MyGames
   ```

2. **Wechsle zum Branch:**
   - Klicke auf "main" Dropdown
   - Wähle: `claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV`

3. **Download die ZIP:**
   - Klicke auf die Datei `sternenbruch_v8_complete.zip`
   - Klicke auf "Download" Button

4. **Oder direkter Link:**
   ```
   https://github.com/DaytradeCentral/_MyGames/blob/claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV/sternenbruch_v8_complete.zip
   ```

### Methode 2: Ganzes Repository klonen

```bash
# In Git Bash oder PowerShell:
git clone https://github.com/DaytradeCentral/_MyGames.git
cd _MyGames
git checkout claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV
```

---

## 🗂️ Installation auf Windows

### Schritt 1: ZIP entpacken

1. **Rechtsklick** auf `sternenbruch_v8_complete.zip`
2. **"Extrahieren nach..."** oder **"Extract to..."**
3. Wähle einen Ordner, z.B.:
   ```
   C:\Users\DeinName\PyCharmProjects\Sternenbruch_v8\
   ```

### Schritt 2: In PyCharm öffnen

1. **PyCharm starten**
2. **File → Open**
3. **Navigiere** zum entpackten Ordner
4. **OK** klicken

Du solltest jetzt sehen:
```
Sternenbruch_v8/
├── sternenbruch_enhanced.py
├── sternenbruch_complete.py  ⭐ HAUPTDATEI
├── README.md
├── IMPROVEMENTS.md
├── PYCHARM_SETUP.md
└── .idea/
```

---

## 🐍 Python & Arcade installieren

### Schritt 1: Python installieren (falls nicht vorhanden)

1. **Download Python 3.11:**
   ```
   https://www.python.org/downloads/
   ```

2. **Wichtig beim Installieren:**
   - ✅ Häkchen bei "Add Python to PATH"
   - ✅ "Install Now" klicken

3. **Prüfe Installation:**
   ```cmd
   python --version
   ```
   Sollte zeigen: `Python 3.11.x` oder höher

### Schritt 2: Arcade installieren

**In PyCharm Terminal** (Alt+F12) oder **Windows CMD:**

```cmd
pip install arcade
```

Oder in PyCharm:
```
File → Settings → Project: Sternenbruch_v8 → Python Interpreter
→ Klicke "+" Button
→ Suche "arcade"
→ "Install Package"
```

---

## ▶️ SPIEL STARTEN

### Option 1: In PyCharm (Einfachste)

1. **Öffne** `sternenbruch_complete.py`
2. **Rechtsklick** in der Datei
3. **"Run 'sternenbruch_complete'"**

Oder:
- **Grüner Play-Button** oben rechts ▶️
- **Shortcut:** Shift+F10

### Option 2: Windows Terminal/CMD

1. **Navigiere zum Ordner:**
   ```cmd
   cd C:\Users\DeinName\PyCharmProjects\Sternenbruch_v8
   ```

2. **Starte Spiel:**
   ```cmd
   python sternenbruch_complete.py
   ```

### Option 3: Doppelklick (nach Setup)

1. **Erstelle** `start_game.bat`:
   ```batch
   @echo off
   python sternenbruch_complete.py
   pause
   ```

2. **Doppelklick** auf `start_game.bat`

---

## 🔧 PyCharm-Konfiguration

### Run Configuration sollte automatisch erstellt werden:

**Falls nicht, manuell erstellen:**

1. **Run → Edit Configurations**
2. **"+" → Python**
3. **Name:** Sternenbruch v8
4. **Script path:** `sternenbruch_complete.py`
5. **OK**

Jetzt kannst du mit dem grünen ▶️ Button starten!

---

## 🐛 Fehlerbehebung Windows

### "Python nicht gefunden"
```cmd
# Prüfe ob Python installiert:
python --version

# Falls nicht, installiere von python.org
# Stelle sicher "Add to PATH" gewählt ist
```

### "Module 'arcade' not found"
```cmd
# Installiere Arcade:
pip install arcade

# Oder mit pip3:
pip3 install arcade
```

### "Permission denied" / Zugriffsfehler
```
→ Rechtsklick auf PyCharm
→ "Als Administrator ausführen"
```

### Spiel startet, aber schwarzer Bildschirm
```
→ Aktualisiere Grafiktreiber
→ Prüfe OpenGL 3.3+ Support
→ Versuche Intel/NVIDIA/AMD Grafiktreiber zu aktualisieren
```

### PyCharm findet Python nicht
```
File → Settings → Project Interpreter
→ "Show All"
→ "+" → "Add Local Interpreter"
→ Wähle Python.exe (z.B. C:\Python311\python.exe)
```

---

## 📁 Windows Dateistruktur

Nach der Installation solltest du haben:

```
C:\Users\DeinName\PyCharmProjects\Sternenbruch_v8\
│
├── sternenbruch_complete.py       ⭐ HAUPTDATEI (35 KB)
├── sternenbruch_enhanced.py       📦 Basis-Code (53 KB)
│
├── README.md                       📖 Spielanleitung
├── IMPROVEMENTS.md                 📊 Änderungsliste
├── PYCHARM_SETUP.md               🔧 PyCharm Setup
├── WINDOWS_SETUP.md               🪟 Diese Datei
│
├── .idea\                         🔵 PyCharm Konfiguration
│   └── runConfigurations\
│       └── Sternenbruch_v8.xml
│
└── [Nach erstem Start:]
    ├── sternenbruch_save.json     💾 Spielstand
    └── autosave.json              ⏰ Auto-Save
```

---

## ✅ Checkliste für Windows-Installation

- [ ] Python 3.8+ installiert (`python --version`)
- [ ] Arcade installiert (`pip install arcade`)
- [ ] ZIP heruntergeladen und entpackt
- [ ] Ordner in PyCharm geöffnet
- [ ] `sternenbruch_complete.py` gefunden
- [ ] Spiel läuft (grüner Play-Button)

---

## 🎮 Nach erfolgreicher Installation

**Starte das Spiel:**
```
▶️ Klicke grünen Play-Button in PyCharm
```

**Erste Schritte im Spiel:**
1. Tutorial erscheint automatisch
2. Drücke **H** für Hotkeys
3. Drücke **C** für Kampagnen

---

## 📞 Weitere Hilfe

### Dateien nicht gefunden?
**Prüfe GitHub Branch:**
- Gehe zu: https://github.com/DaytradeCentral/_MyGames
- Branch: `claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV`
- Alle Dateien sollten dort sichtbar sein

### Immer noch Probleme?
1. Prüfe ob ZIP vollständig heruntergeladen (34 KB)
2. Stelle sicher Python installiert ist
3. Installiere Arcade: `pip install arcade`
4. Prüfe Windows Firewall/Antivirus

---

## 🌐 Direkter GitHub-Link zu allen Dateien:

**Repository:**
```
https://github.com/DaytradeCentral/_MyGames
```

**Branch mit v8:**
```
https://github.com/DaytradeCentral/_MyGames/tree/claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV
```

**Einzelne Dateien downloaden:**
- [sternenbruch_complete.py](https://github.com/DaytradeCentral/_MyGames/blob/claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV/sternenbruch_complete.py)
- [README.md](https://github.com/DaytradeCentral/_MyGames/blob/claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV/README.md)
- [ZIP-Datei](https://github.com/DaytradeCentral/_MyGames/blob/claude/improve-game-features-01CKPQ41TujAeTMoP9N6TJgV/sternenbruch_v8_complete.zip)

---

**Viel Erfolg! Das Spiel läuft super auf Windows! 🚀✨**

*Bei Fragen: Siehe README.md für Spielanleitung*
