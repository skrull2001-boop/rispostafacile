# 🚀 RispostaFacile.ai

**AI-powered email response generator for Italian accountants (commercialisti)**

Generate professional email responses to client questions in 5 seconds. The accountant reviews, approves, and sends.

---

## 📁 Project Structure

```
rispostafacile/
├── main.py                    # FastAPI backend
├── templates/
│   ├── index.html            # Landing page
│   └── app.html              # Main webapp
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container config
├── Procfile                 # Heroku/Railway
├── railway.json             # Railway config
├── scrape_commercialisti.py # Lead generation tool
├── cold_email_sequence.md   # Outreach templates
├── search_guide.md          # Manual lead collection guide
└── leads_sample.csv         # CSV template for leads
```

---

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Anthropic API key

### Setup

```bash
# Clone/download the project
cd rispostafacile

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run locally
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000

---

## ☁️ Deployment

### Option 1: Railway (Recommended - Free tier available)

1. Go to [railway.app](https://railway.app)
2. Connect GitHub repo or upload files
3. Add environment variable: `ANTHROPIC_API_KEY`
4. Deploy automatically

### Option 2: Render

1. Go to [render.com](https://render.com)
2. New Web Service → Connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `ANTHROPIC_API_KEY`

### Option 3: Heroku

```bash
heroku create rispostafacile
heroku config:set ANTHROPIC_API_KEY="your-key"
git push heroku main
```

---

## 💰 Costs

### API Costs (Claude Sonnet)
- ~€0.003 per response (avg 500 input + 300 output tokens)
- 1000 responses/month = ~€3
- 30 clients × 500 responses = ~€45/month

### Hosting
- Railway free tier: 500 hours/month (enough for MVP)
- Render free tier: Spins down after inactivity
- Heroku: €7/month for always-on

---

## 📧 Go-to-Market

### Step 1: Generate Leads (3 hours)
```bash
python scrape_commercialisti.py
# Follow search_guide.md to collect 100 leads
```

### Step 2: Cold Outreach
See `cold_email_sequence.md` for:
- 3-email sequence templates
- LinkedIn messaging
- Demo call script
- Tracking spreadsheet template

### Step 3: Demo & Close
- 14-day free trial
- €149/month pricing
- Target: 1 customer per 30 cold emails

---

## 🎯 Milestones

| Week | Goal | Revenue |
|------|------|---------|
| 1 | MVP live + 90 emails sent | €0 |
| 2 | First demo calls | €0 |
| 3 | First paying customer | €149 |
| 4 | 3-5 customers | €450-750 |
| 8 | 10 customers | €1,490 |
| 12 | 20 customers | €2,980 |

---

## 🔧 Customization

### Modify AI Behavior
Edit the `SYSTEM_PROMPT` in `main.py` to:
- Change response tone
- Add specific tax knowledge
- Customize signature format

### Add Features (Future)
- [ ] User authentication
- [ ] Response history
- [ ] Email templates library
- [ ] Stripe payment integration
- [ ] Gmail/Outlook integration

---

## 📊 Analytics (Recommended)

Add these for tracking:
- **Plausible** or **Umami** (privacy-friendly analytics)
- **Hotjar** (heatmaps for landing page optimization)
- **Crisp** or **Intercom** (live chat for demos)

---

## ⚠️ Legal Notes

1. **Disclaimer**: Add clear terms that the AI is an assistant, not a replacement for professional advice
2. **GDPR**: No client data is stored by default (stateless processing)
3. **Professional liability**: The accountant reviews and approves all responses

---

## 🆘 Support

For issues or questions, open a GitHub issue.

---

## License

MIT License - Use freely for commercial purposes.
