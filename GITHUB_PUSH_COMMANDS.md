# Push to a new empty GitHub repository (Windows or Mac/Linux)

After creating a **new empty GitHub repository** in your own account, unzip this project into a folder and open the terminal inside that folder.

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git init
git branch -M main
git add .
git commit -m "Launch MallOfAmericans Etsy AI Studio"
git remote add origin https://github.com/YOUR_USERNAME/mallofamericans-etsy-studio.git
git push -u origin main
```

GitHub might prompt you to authenticate with your browser; GitHub account passwords do not work as Git HTTPS passwords. Prefer browser or credential manager sign-in. Never paste tokens into source code or commit them.

Then deploy the Python app in [Streamlit Community Cloud](https://share.streamlit.io/) using repository main branch and entrypoint `app.py`.

**If you don't want terminal commands:** On GitHub create new repository → Add file → Upload files → drag the extracted project files and folders (including `.streamlit` and `.github`) → Commit changes. Cloud deployment is still required; GitHub Pages by itself cannot run Python.
