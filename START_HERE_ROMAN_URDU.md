# Bhai, GitHub par tool upload karne ka asaan tareeqa

1. ZIP download karke unzip karo.
2. GitHub.com pe `mallofamericans-etsy-studio` naam ki **new repository** banao.
3. ZIP ke andar wali saari files/folders repository ke main root mein upload karo, phir **Commit changes** dabao.
4. [share.streamlit.io](https://share.streamlit.io) open karo, apne GitHub account se sign in karo, **New app / Create app** par click karo.
5. Repository select karo; main file ka path `app.py` rakho; Deploy karo. Tumhe apne tool ka public ya private access URL mil jayega (Streamlit settings ke mutabiq).
6. **Optional**: Custom AI product banane ke liye Anthropic API key aur real public search ke liye Brave Search API key Streamlit ke **Secrets** mein add karo. Key GitHub files mein bilkul mat likhna.
7. Bina keys ke bhi demo product (Multi-Pet Sitter Handoff Kit) generate karke 10 JPG mockups + 2 MP4 videos + buyer files test kar sakte ho. **Lekin ye live research nahi hoga.**

**Important:** Sirf GitHub Pages par ye backend-based tool nahi chalega; GitHub code host karega aur Streamlit app run karega. GitHub par mere paas aapke account ka access available nahin hai, isliye live upload aap khud kar sakte hain ya GitHub connector connect karein.

**Cost:** Streamlit free-tier limitations apply kar sakti hain; external Anthropic aur Brave API keys alag se paid ho sakti hain.
