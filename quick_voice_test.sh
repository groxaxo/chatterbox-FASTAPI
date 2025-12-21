#!/bin/bash
# Quick Voice Sample Tester
# Usage: ./quick_voice_test.sh [voice_name] [text] [language]

VOICE=${1:-aimee}
TEXT=${2:-"Hola, esta es una prueba rápida del sistema de voz."}
LANG=${3:-es}
OUTPUT="quick_test_${VOICE}_$(date +%s).mp3"

echo "🎙️  Quick Voice Test"
echo "===================="
echo "Voice: $VOICE"
echo "Text: $TEXT"
echo "Language: $LANG"
echo "Output: $OUTPUT"
echo ""

conda run -n chatterbox-fastapi python test_voice_samples.py "$VOICE" "$TEXT" "$LANG" "$OUTPUT"

if [ -f "$OUTPUT" ]; then
    echo ""
    echo "✅ Audio generated successfully!"
    echo "📁 File: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
    echo ""
    echo "🎵 Play with: mpv $OUTPUT"
fi
