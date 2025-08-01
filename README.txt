Sysra Browser Lite 3.0
Sysra Browser Lite 3.0 is a lightweight, customizable web browser built with Python and PyQt5. It features tabbed browsing, built-in translation, notes, and calculator plugins — all integrated into a sleek and minimal interface.

Features
Tabbed browsing with back, forward, and reload controls

URL/search bar supporting direct URLs and DuckDuckGo search queries

Integrated Plugins:

Sysra Translate: Supports multiple languages with instant translation

Sysra Notes: Persistent note-taking tool saved locally

Sysra Calculator: Basic calculator supporting addition, subtraction, multiplication, and division

Light and Red themes for comfortable viewing

Easy tab management with closable tabs and a quick new tab button

Installation
Make sure you have Python 3.6+ installed.

Install dependencies:

bash
Kopyala
Düzenle
pip install PyQt5 PyQtWebEngine deep-translator
Clone or download the repository.

Run the main application:

bash
Kopyala
Düzenle
python sysrabrowser.py
Usage
Enter URLs or search queries directly into the address bar.

Use the plugin panel on the right to translate text, take notes, or perform calculations without leaving the browser.

Save notes locally — they persist between sessions.

Change the theme from the menu bar for a different look.

Open new tabs with the + button, close tabs by clicking the x on each tab.

File Structure
sysrabrowser.py - Main application source code

sysra_home.html - Homepage HTML file loaded on new tabs

sysra_notes.txt - Local file storing saved notes

Contributing
Contributions are welcome! Feel free to submit issues or pull requests on GitHub.

License
This project is licensed under the MIT License.

