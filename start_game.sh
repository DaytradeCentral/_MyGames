#!/bin/bash
# STERNENBRUCH v8 - Starter Script

echo "=================================="
echo "  STERNENBRUCH v8 - Enhanced     "
echo "=================================="
echo ""

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    echo "Bitte installiere Python 3.8+"
    exit 1
fi

echo "✓ Python gefunden: $(python3 --version)"

# Prüfe Arcade
if ! python3 -c "import arcade" 2>/dev/null; then
    echo "⚠️  Arcade nicht installiert!"
    echo "Installiere Arcade..."
    pip install arcade
fi

echo "✓ Arcade installiert"
echo ""
echo "🚀 Starte Spiel..."
echo ""

# Starte Spiel
cd /home/user/_MyGames
python3 sternenbruch_complete.py
