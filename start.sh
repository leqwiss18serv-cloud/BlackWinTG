#!/bin/bash

echo "🎰 Black Win Bot - Quick Start Script"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "Please edit .env file with your credentials:"
    echo "  - BOT_TOKEN (from @BotFather)"
    echo "  - SUPABASE_URL (from Supabase dashboard)"
    echo "  - SUPABASE_KEY (from Supabase dashboard)"
    echo "  - OWNER_ID (your Telegram ID)"
    echo ""
    echo "Run this script again after editing .env"
    exit 1
fi

echo "✅ Found .env file"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo "✅ Python 3 is installed"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "Please install pip"
    exit 1
fi

echo "✅ pip is installed"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Check if database is set up
echo "📊 Database Setup Check"
echo "----------------------"
echo "Have you set up the Supabase database?"
echo "1. Go to your Supabase project"
echo "2. Run the SQL from SETUP.md or DATABASE.md"
echo "3. Verify all tables are created"
echo ""
read -p "Is database ready? (y/n): " db_ready

if [ "$db_ready" != "y" ]; then
    echo ""
    echo "Please set up the database first!"
    echo "Follow instructions in SETUP.md"
    exit 1
fi

echo ""
echo "🚀 Starting Black Win Bot..."
echo "=============================="
echo ""
python3 main.py
