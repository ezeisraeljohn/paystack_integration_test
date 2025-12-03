#!/bin/bash

# Paystack Integration Setup Script
# This script helps you set up the Paystack payment integration project

echo "========================================="
echo "Paystack Payment Integration Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and add your Paystack API keys"
    echo ""
    echo "To get your API keys:"
    echo "1. Sign up at https://paystack.com"
    echo "2. Go to Settings → API Keys & Webhooks"
    echo "3. Copy your test keys"
    echo "4. Edit .env file and paste your keys"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if API keys are set
source .env
if [ "$PAYSTACK_SECRET_KEY" = "sk_test_your_secret_key_here" ] || [ -z "$PAYSTACK_SECRET_KEY" ]; then
    echo "⚠️  WARNING: Paystack API keys not configured!"
    echo ""
    echo "Please update your .env file with your actual Paystack keys:"
    echo "  1. Open .env file in a text editor"
    echo "  2. Replace placeholder values with your actual keys"
    echo "  3. Save the file"
    echo ""
else
    echo "✅ Paystack API keys configured"
    echo ""
fi

# Generate documentation
echo "📄 Generating Section 1 answers document..."
python create_section1_answers.py
echo "✅ Section_1_Answers.docx created"
echo ""

echo "📄 Generating Section 2 Part 2 answers document..."
python create_section2_answers.py
echo "✅ Section_2_Part2_Answers.docx created"
echo ""

# Display next steps
echo "========================================="
echo "✨ Setup Complete!"
echo "========================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure your Paystack API keys in .env file (if not done)"
echo ""
echo "2. Start the development server:"
echo "   uvicorn main:app --reload"
echo ""
echo "3. Open your browser and visit:"
echo "   http://localhost:8000"
echo ""
echo "4. Test payment with Paystack test cards:"
echo "   Card: 4084 0840 8408 4081"
echo "   CVV: 408"
echo "   Expiry: Any future date"
echo "   PIN: 0000"
echo ""
echo "5. View transactions at:"
echo "   http://localhost:8000/transactions"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Complete project documentation"
echo "   - DEPLOYMENT.md - Deployment guide"
echo "   - Section_1_Answers.docx - Section 1 answers"
echo "   - Section_2_Part2_Answers.docx - Section 2 Part 2 answers"
echo ""
echo "🚀 Ready to deploy? Check DEPLOYMENT.md for deployment guides"
echo ""
echo "========================================="
