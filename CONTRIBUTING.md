# Contributing to Mdundo Fraud Detection

Thank you for your interest in contributing! Here's how to get started.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone https://github.com/YOUR_USERNAME/mdundo-fraud-detection.git
cd mdundo-fraud-detection
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Local Development
```bash
# Run setup script
bash setup.sh

# Activate virtual environment
source venv/bin/activate

# Install dev dependencies
pip install pytest pytest-asyncio flake8
```

### 4. Make Your Changes

Follow these guidelines:
- Write clean, readable code
- Add comments for complex logic
- Follow PEP 8 style guide
- Test your changes locally

### 5. Test Your Changes
```bash
# Test imports
python -c "from lib.fraud_detector import MdundoFraudDetector; print('OK')"

# Run specific module
python api/functions/fraud_daily.py

# Check code style
flake8 lib/ api/
```

### 6. Commit and Push
```bash
git add .
git commit -m "Add feature: description"
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to GitHub
- Click "New Pull Request"
- Select your branch
- Describe your changes
- Submit for review

## Code Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions

### Example:
```python
def analyze_artist(self, rank: int, artist_name: str, mdundo_song: str, mdundo_url: str) -> ArtistAnalysis:
    """
    Analyze single artist for fraud indicators.
    
    Args:
        rank: Chart position (1-50)
        artist_name: Artist name to analyze
        mdundo_song: Song title from Mdundo
        mdundo_url: Mdundo profile URL
    
    Returns:
        ArtistAnalysis object with fraud score and flags
    """
    # Implementation...
```

## What to Contribute

### Bug Fixes
- Found an issue? Create an Issue first
- Reference the issue in your PR

### Features
- Check existing Issues/Discussions
- Propose feature first before implementing
- Keep scope focused

### Documentation
- README improvements
- Deployment guide clarifications
- Code comments and docstrings
- API documentation

### Performance
- Optimize database queries
- Reduce API calls
- Improve caching

## Areas for Contribution

### High Priority
- [ ] Add database persistence (PostgreSQL)
- [ ] Create web dashboard
- [ ] Add unit tests
- [ ] Email notification support
- [ ] Multi-language support

### Medium Priority
- [ ] Add rate limiting
- [ ] Implement caching layer
- [ ] Add logging service integration
- [ ] Create CLI tool
- [ ] Add Docker support

### Nice to Have
- [ ] Mobile app
- [ ] Browser extension
- [ ] Telegram bot
- [ ] Advanced analytics

## Pull Request Process

1. **Update** README.md if needed
2. **Test** your code locally
3. **Describe** what your PR does
4. **Reference** any related Issues
5. **Wait** for review and feedback
6. **Update** based on comments
7. **Merge** when approved

## Reporting Issues

### Bug Report
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior.

**Expected behavior**
What should happen.

**Actual behavior**
What actually happens.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python: [e.g. 3.11]
- Vercel deployment or local?
```

### Feature Request
```markdown
**Is your feature request related to a problem?**
Description of the problem.

**Describe the solution**
What you'd like to happen.

**Describe alternatives**
Other approaches you've considered.

**Additional context**
Any other context.
```

## Development Tips

### Local Testing with Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Run local development
vercel dev
```

### Debug Cron Locally
```bash
# Set environment variables
export SPOTIFY_TOKEN="your_token"
export SLACK_WEBHOOK="your_webhook"

# Run job
python api/functions/fraud_daily.py
```

### Database Queries
```python
# Test queries locally before deploying
python -c "
from lib.fraud_detector import MdundoFraudDetector
detector = MdundoFraudDetector(spotify_api_token='TOKEN')
# Test detection logic
"
```

## Commit Message Guidelines

```
Commit format: [TYPE] Subject (50 chars)

Types: 
- FEAT: New feature
- FIX: Bug fix
- DOCS: Documentation
- STYLE: Code style
- REFACTOR: Refactoring
- PERF: Performance
- TEST: Tests

Example:
FEAT: Add email notifications for critical alerts
- Implement EmailNotifier class
- Add email template
- Integrate with fraud detection job
```

## Review Process

### What We Look For
- ✅ Code quality and style
- ✅ Tests coverage
- ✅ Documentation
- ✅ Performance impact
- ✅ Security considerations

### Timeline
- Initial review: 2-3 days
- Feedback: 1-2 days per round
- Approval: When all issues resolved

## Recognition

We recognize contributors in:
- README contributors section
- Release notes
- Monthly newsletter

Thank you for contributing! 🎉

---

Questions? Create a GitHub Discussion or reach out to the maintainers.
