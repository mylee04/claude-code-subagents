#!/bin/bash

# Elite Squad Agent Registry Demo Runner
# Makes it easy to run the colorful demo

echo "🚀 Starting Elite Squad Agent Registry Demo..."
echo

# Check if we're in the right directory
if [ ! -f "demo_agent_registry.py" ]; then
    echo "❌ Error: demo_agent_registry.py not found in current directory"
    echo "   Please run this script from the project root directory"
    exit 1
fi

# Check Python availability
if command -v python3 &> /dev/null; then
    python3 demo_agent_registry.py
elif command -v python &> /dev/null; then
    python demo_agent_registry.py
else
    echo "❌ Error: Python not found. Please install Python 3."
    exit 1
fi