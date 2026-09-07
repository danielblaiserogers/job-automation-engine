# Silence Crostini notice
echo 10 > ~/.local/share/baguette-motd 2>/dev/null || true

# Update packages and install core build tools
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget unzip ca-certificates gnupg

# Download and install VS Code
wget 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64' -O vscode.deb
sudo apt install -y ./vscode.deb
rm vscode.deb

# Configure global Git settings
git config --global user.name "Daniel Blaise Rogers"
git config --global user.email "danielblaiserogers@gmail.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input

# Set up SSH Key for GitHub if not present
if [ ! -f ~/.ssh/id_ed25519 ]; then
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    ssh-keygen -t ed25519 -C "danielblaiserogers@gmail.com" -f ~/.ssh/id_ed25519 -N ""
    chmod 600 ~/.ssh/id_ed25519
fi

# Configure ~/.bashrc for SSH Agent
if ! grep -q "Auto-start SSH Agent" ~/.bashrc; then
    cat << 'EOF' >> ~/.bashrc

# Auto-start SSH Agent
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
fi

if ! ssh-add -l > /dev/null 2>&1; then
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
EOF
fi

# Reload shell configuration
source ~/.bashrc

# Print public key to add to GitHub
echo "========================================================"
echo "COPY AND ADD THIS SSH PUBLIC KEY TO YOUR GITHUB ACCOUNT:"
echo "========================================================"
cat ~/.ssh/id_ed25519.pub
echo "========================================================"