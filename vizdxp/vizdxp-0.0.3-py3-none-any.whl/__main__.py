import sys
import streamlit.cli as stcli

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())
