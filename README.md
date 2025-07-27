# Twitch Test Automation Framework

## 🏗️ Project Structure

```
twitch-test-automation/
├── config/
│   ├── __init__.py
│   └── config.py                   # Configuration management
├── pages/
│   ├── __init__.py
│   ├── base_page.py                # Base page object class
│   ├── browse_page.py              # Twitch Browse page object
│   ├── home_page.py                # Twitch homepage page object
│   ├── navigation_bar.py           # Twitch navigation bar component page object
│   ├── search_results.py           # Twitch search_results bar component object
│   └── streamer_page.py            # Twitch Streamer page page object
├── utils/
│   ├── __init__.py
│   ├── webdriver_factory.py        # WebDriver management
│   └── screenshot_utils.py         # Screenshot utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration and fixtures
│   └── test_twitch_user_journey.py # Main test scenarios
├── screenshots/                    # Screenshot storage
│   ├── success/
│   └── failures/
├── reports/                        # Test reports
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── env.example                     # Environment configuration example
└── README.md                       # This file
```
## 🎮 Running Tests GIFS
![Demo GIF](demo.gif)
