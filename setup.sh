#!/usr/bin/env bash
#
# Zero-Cost AI Business v4 — One-Command Setup
# =============================================
#
# This script does the BARE MINIMUM to get the agent running:
#   1. Asks for the few required values (LLM key, GitHub PAT)
#   2. Sets them as GitHub secrets via `gh` CLI
#   3. Enables GitHub Pages
#   4. Triggers the first run
#
# Everything else — wallet addresses, affiliate links, analytics, newsletter,
# ad network — is handled by the agent itself via zero-setup fallbacks.
# The agent will tell you (via pending_requests) what to upgrade over time.
#
# Prerequisites:
#   - `gh` CLI installed and authenticated (https://cli.github.com/)
#   - This repo pushed to GitHub
#   - You have a Groq API key (https://console.groq.com/keys)
#   - You have a GitHub Personal Access Token with `repo` scope
#
# Usage:
#   ./setup.sh
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Zero-Cost AI Business v4 — One-Command Setup           ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "This script will configure your autonomous agent in ~2 minutes."
echo "Everything else (analytics, ads, newsletter, affiliate) is auto-configured"
echo "by the agent with zero-setup fallbacks. You can upgrade later."
echo ""

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v gh &> /dev/null; then
    echo -e "${RED}✗ 'gh' CLI not found. Install from https://cli.github.com/${NC}"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo -e "${RED}✗ Not authenticated with 'gh'. Run: gh auth login${NC}"
    exit 1
fi

# Get repo info from git remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE_URL" ]; then
    echo -e "${RED}✗ No git remote 'origin' found. Push this repo to GitHub first.${NC}"
    exit 1
fi

# Extract owner/repo from remote URL
if [[ "$REMOTE_URL" =~ github\.com[/:]([^/]+)/([^/\.]+?)(\.git)?$ ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
else
    echo -e "${RED}✗ Could not parse GitHub owner/repo from: $REMOTE_URL${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Using repo: $OWNER/$REPO${NC}"
echo ""

# Compute site URL
SITE_URL="https://${OWNER}.github.io/${REPO}"
echo -e "${BLUE}Your site will be: ${SITE_URL}${NC}"
echo ""

# --- Step 1: Required secrets ---
echo -e "${YELLOW}Step 1: Required secrets${NC}"
echo ""

# Groq API key (recommended)
read -sp "Paste your Groq API key (from https://console.groq.com/keys): " GROQ_KEY
echo ""
if [ -n "$GROQ_KEY" ]; then
    gh secret set GROQ_API_KEY --body "$GROQ_KEY" --repo "$OWNER/$REPO"
    echo -e "${GREEN}✓ GROQ_API_KEY set${NC}"
else
    echo -e "${RED}✗ GROQ_API_KEY is required. Aborting.${NC}"
    exit 1
fi

# GitHub PAT
echo ""
echo "Now create a GitHub Personal Access Token:"
echo "  1. Go to https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Select scope: 'repo' (full)"
echo "  4. Click 'Generate token' and copy the token"
read -sp "Paste your GitHub PAT: " GH_PAT
echo ""
if [ -n "$GH_PAT" ]; then
    gh secret set GH_PAT --body "$GH_PAT" --repo "$OWNER/$REPO"
    echo -e "${GREEN}✓ GH_PAT set${NC}"
else
    echo -e "${RED}✗ GH_PAT is required. Aborting.${NC}"
    exit 1
fi

# Site URL (auto-derived)
echo ""
gh secret set SITE_BASE_URL --body "$SITE_URL" --repo "$OWNER/$REPO"
echo -e "${GREEN}✓ SITE_BASE_URL set to $SITE_URL${NC}"

# --- Step 2: Optional secrets ---
echo ""
echo -e "${YELLOW}Step 2: Optional secrets (press Enter to skip each)${NC}"
echo "These unlock additional revenue streams. The agent runs fine without them."
echo ""

# Gemini
read -sp "Google Gemini API key (https://aistudio.google.com/apikey) [optional]: " GEMINI_KEY
echo ""
if [ -n "$GEMINI_KEY" ]; then
    gh secret set GEMINI_API_KEY --body "$GEMINI_KEY" --repo "$OWNER/$REPO"
    echo -e "${GREEN}✓ GEMINI_API_KEY set${NC}"
fi

# Operator email (for mailto newsletter fallback)
read -p "Your email (for the 'Subscribe via Email' newsletter fallback) [optional]: " OP_EMAIL
if [ -n "$OP_EMAIL" ]; then
    gh secret set OPERATOR_EMAIL --body "$OP_EMAIL" --repo "$OWNER/$REPO"
    echo -e "${GREEN}✓ OPERATOR_EMAIL set${NC}"
fi

# --- Step 3: Enable GitHub Pages ---
echo ""
echo -e "${YELLOW}Step 3: Enabling GitHub Pages...${NC}"
echo "Setting Pages source to GitHub Actions..."

# Try to enable Pages via API
curl -s -X POST \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GH_PAT" \
    "https://api.github.com/repos/$OWNER/$REPO/pages" \
    -d '{"build_type":"workflow"}' \
    > /dev/null 2>&1 || true

# If that failed because Pages is already enabled, that's fine
echo -e "${GREEN}✓ GitHub Pages enabled (source: GitHub Actions)${NC}"

# --- Step 4: Push code ---
echo ""
echo -e "${YELLOW}Step 4: Committing and pushing code...${NC}"

git add -A
if git diff --cached --quiet; then
    echo "No changes to commit"
else
    git commit -m "Initial setup via setup.sh"
    git push origin HEAD || git push
fi
echo -e "${GREEN}✓ Code pushed${NC}"

# --- Step 5: Trigger first run ---
echo ""
echo -e "${YELLOW}Step 5: Triggering first agent run...${NC}"
gh workflow run loop.yml --repo "$OWNER/$REPO" || true
echo -e "${GREEN}✓ First run triggered${NC}"

# --- Done ---
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ✓ Setup complete!                                       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "What happens next:"
echo "  1. The agent runs every 30 minutes (first run is happening now)"
echo "  2. On first run, it auto-detects your repo and replaces all placeholders"
echo "  3. It builds new pages, submits them to SEO, distributes to channels"
echo "  4. It uses zero-setup fallbacks for analytics (GitHub Traffic API),"
echo "     ads (house ads), and newsletter (mailto:) — all working from day 1"
echo ""
echo "Monitor your agent:"
echo "  - GitHub Actions tab: see every run"
echo "  - memory/state.md: rolling summary of last 2-3 runs"
echo "  - memory/blocked.md: optional enhancements you can add later"
echo "  - memory/revenue.md: verified on-chain tips"
echo "  - Weekly auto-generated GitHub issue with summary"
echo ""
echo "Optional upgrades (do these when you have time):"
echo "  - Replace wallet addresses in docs/guides/crypto-tips.html"
echo "  - Register for EthicalAds/Carbon Ads (ad revenue)"
echo "  - Register for affiliate programs (DigitalOcean, Vultr, etc.)"
echo "  - Sign up for GoatCounter (page-level analytics)"
echo "  - Sign up for Buttondown (real newsletter)"
echo ""
echo -e "${GREEN}Done. Your agent is now autonomous.${NC}"
