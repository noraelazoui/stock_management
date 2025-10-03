#!/bin/bash
# Build script for creating Windows installer on Linux
# This script prepares everything needed for Windows deployment

echo "=================================="
echo "Stock Management - Build Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in the correct directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}Error: main.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Installing build dependencies...${NC}"
pip install pyinstaller pillow

echo ""
echo -e "${YELLOW}Step 2: Creating icon (if needed)...${NC}"
if [ ! -f "icon.ico" ]; then
    echo "Creating default icon..."
    python3 << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple icon
img = Image.new('RGB', (256, 256), color=(33, 150, 243))
draw = ImageDraw.Draw(img)

# Draw text
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
except:
    font = ImageFont.load_default()

draw.text((40, 80), "SM", fill=(255, 255, 255), font=font)
img.save('icon.ico')
print("Icon created: icon.ico")
EOF
else
    echo "Icon already exists: icon.ico"
fi

echo ""
echo -e "${YELLOW}Step 3: Creating LICENSE.txt...${NC}"
if [ ! -f "LICENSE.txt" ]; then
    cat > LICENSE.txt << 'EOF'
Stock Management Application License

Copyright (c) 2025 Your Company

This software is provided for use by authorized clients only.
All rights reserved.

For support and updates, contact: support@yourcompany.com
EOF
    echo "LICENSE.txt created"
else
    echo "LICENSE.txt already exists"
fi

echo ""
echo -e "${YELLOW}Step 4: Building executable with PyInstaller...${NC}"
pyinstaller --clean build_config.spec

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: PyInstaller build failed!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Build completed successfully!${NC}"
echo ""
echo "Build output is in: dist/StockManagement/"
echo ""
echo -e "${YELLOW}Next Steps for Windows Deployment:${NC}"
echo "1. Download MongoDB Windows binary from: https://www.mongodb.com/try/download/community"
echo "2. Extract MongoDB files to: mongodb/"
echo "3. Install Inno Setup on Windows: https://jrsoftware.org/isinfo.php"
echo "4. Create installer scripts (see DEPLOYMENT_GUIDE.md)"
echo "5. Build the installer using Inno Setup with installer_setup.iss"
echo ""
echo "For detailed instructions, see: DEPLOYMENT_GUIDE.md"
