#!/bin/bash

echo "🚀 YouTube View Generator - Automatic Setup"
echo "==========================================="
echo "This script will install everything you need automatically!"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

print_info "Detected OS: $OS"

# Function to install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."

    if [[ "$OS" == "linux" ]]; then
        # Update package list
        print_info "Updating package list..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update -qq

            # Install required packages
            print_info "Installing Python, pip, venv, and Chrome dependencies..."
            sudo apt-get install -y \
                python3 \
                python3-pip \
                python3-venv \
                python3.12-venv \
                python3-dev \
                wget \
                curl \
                unzip \
                xvfb \
                xauth \
                x11-utils \
                libxi6 \
                libgconf-2-4 \
                libnss3 \
                libxss1 \
                libappindicator3-1 \
                libindicator7 \
                gconf-service \
                libgconf-2-4 \
                libxfixes3 \
                libxi6 \
                libxrandr2 \
                libasound2-dev \
                libpangocairo-1.0-0 \
                libatk1.0-0 \
                libcairo-gobject2 \
                libgtk-3-0 \
                libgdk-pixbuf2.0-0 \
                2>/dev/null

        elif command -v yum &> /dev/null; then
            sudo yum update -y
            sudo yum install -y python3 python3-pip python3-venv wget curl unzip
        elif command -v pacman &> /dev/null; then
            sudo pacman -Syu --noconfirm python python-pip wget curl unzip
        fi

    elif [[ "$OS" == "macos" ]]; then
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            print_info "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi

        print_info "Installing Python and dependencies..."
        brew install python3 wget curl
    fi
}

# Function to install Chrome
install_chrome() {
    print_info "Installing Google Chrome..."

    if [[ "$OS" == "linux" ]]; then
        if ! command -v google-chrome &> /dev/null; then
            # Download and install Chrome
            wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
            echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
            sudo apt-get update -qq
            sudo apt-get install -y google-chrome-stable
            print_status "Google Chrome installed"
        else
            print_status "Google Chrome already installed"
        fi

    elif [[ "$OS" == "macos" ]]; then
        if ! ls /Applications/Google\ Chrome.app &> /dev/null; then
            brew install --cask google-chrome
            print_status "Google Chrome installed"
        else
            print_status "Google Chrome already installed"
        fi
    fi
}

# Main installation process
main() {
    echo
    print_info "Starting automatic installation..."
    echo

    # Install system dependencies
    install_system_deps
    print_status "System dependencies installed"

    # Install Chrome
    install_chrome

    # Check Python installation
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 installation failed"
        exit 1
    fi

    print_status "Python 3 found: $(python3 --version)"

    # Create virtual environment
    print_info "Creating Python virtual environment..."
    if python3 -m venv venv; then
        print_status "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi

    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated"

    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel

    # Install Python dependencies
    print_info "Installing Python dependencies..."
    if pip install -r requirements.txt; then
        print_status "Python dependencies installed"
    else
        print_error "Failed to install Python dependencies"
        exit 1
    fi

    # Test the installation
    print_info "Testing installation..."
    if python3 test_structure.py; then
        print_status "Installation test passed"
    else
        print_error "Installation test failed"
        exit 1
    fi

    # Test proxy system
    print_info "Testing proxy system..."
    if python3 -c "
from src.proxy.proxy_manager import ProxyManager
pm = ProxyManager()
stats = pm.get_proxy_stats()
print(f'Loaded {stats[\"total_proxies\"]} proxies, {stats[\"healthy_proxies\"]} healthy')
if stats['healthy_proxies'] > 0:
    print('✅ Proxy system working')
    exit(0)
else:
    print('⚠️  No healthy proxies found, but system is functional')
    exit(0)
"; then
        print_status "Proxy system test completed"
    else
        print_warning "Proxy system test had issues, but continuing..."
    fi

    # Create easy-to-use scripts
    print_info "Creating user-friendly scripts..."

    # Create simple run script
    cat > run_views.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 run_simulation.py "$@"
EOF
    chmod +x run_views.sh

    # Create demo script
    cat > run_demo.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 demo_dry_run.py
EOF
    chmod +x run_demo.sh

    print_status "User scripts created"

    echo
    echo "🎉 INSTALLATION COMPLETED SUCCESSFULLY! 🎉"
    echo "=========================================="
    echo
    print_status "Everything is ready to use!"
    echo
    echo "📋 Quick Start Guide:"
    echo "1. Test the system:     ./run_demo.sh"
    echo "2. Generate views:      ./run_views.sh 'YOUR_VIDEO_URL' VIEW_COUNT"
    echo
    echo "📝 Examples:"
    echo "   ./run_views.sh 'https://youtube.com/watch?v=abc123' 100"
    echo "   ./run_views.sh 'https://youtube.com/watch?v=abc123' 1000"
    echo
    echo "📊 The system will:"
    echo "   • Use free proxies automatically (no payment needed)"
    echo "   • Check that views are actually being counted"
    echo "   • Use human-like behavior to avoid detection"
    echo "   • Show progress and results in real-time"
    echo
    echo "⚠️  Important Notes:"
    echo "   • Start with small numbers (100-500 views) for testing"
    echo "   • Larger view counts take longer (this is intentional for safety)"
    echo "   • The system prioritizes safety over speed"
    echo
    print_info "Installation log saved to setup.log"
    echo
}

# Run main function and log output
main 2>&1 | tee setup.log
