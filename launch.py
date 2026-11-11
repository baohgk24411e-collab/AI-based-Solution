import os
from pathlib import Path
import sys

root=Path(__file__).resolve().parent
vendor=root/'.vendor'
if vendor.exists() and sys.version_info[:2]==(3,12):
    sys.path.insert(0,str(vendor))
os.chdir(root)
if __name__=='__main__':
    from streamlit.web import cli
    sys.argv=['streamlit','run',str(root/'app.py'),'--global.developmentMode=false','--server.address=127.0.0.1','--server.port=8501','--server.headless=true','--browser.gatherUsageStats=false']
    cli.main()
