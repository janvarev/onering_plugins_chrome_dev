# onering_plugins_chrome_dev
OneRingTranslator plugins that works through Chrome dev connection

## Setup

1. Install **separate Chrome**, that will be controlled by plugins to get translation. For example, you can use this portable version: https://portableapps.com/apps/internet/google-chrome-portable-64 
2. Run it in dev mode. You can download `chrome_dev_controlled.bat` file and change EXE filename inside to your Chrome EXE file; 
or use cmd like `GoogleChromePortable.exe --remote-debugging-port=9222 --remote-allow-origins=*`
3. Now you get Chrome example that can be controlled by external plugin

Next:
1. Copy plugin_deepl_dev.py to your OneRingTranslator plugin folder
2. Run OneRingTranslator in usual style. Plugin must send translation phrases to controlled Chrome, and get results back.