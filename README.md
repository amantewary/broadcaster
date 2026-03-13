# Broadcaster 📡

An open-source, multi-platform publishing engine. Broadcast your content to Medium, Substack, LinkedIn, and more via a single unified API.

Broadcaster is an alternative to paid tools like Ayrshare or Make.com, designed specifically for developers who want to own their publishing pipeline.

## 🚀 Features
- **Medium:** Dual-mode publishing. Supports the official API (if you have a token) OR **Session Injection** (using browser cookies) to bypass token gatekeeping.
- **Substack:** Automated drafts via the Email-to-Post gateway.
- **LinkedIn:** (Coming Soon) via OAuth2.
- **Unified Interface:** One command to rule them all.

## 🛠 Installation
```bash
git clone https://github.com/amantewary/broadcaster
cd broadcaster
pip install -e .
```

## 📖 Usage

```python
from broadcaster.core import Broadcaster

publisher = Broadcaster()

# 1. Setup your platforms

# Medium (Session Injection Mode)
# Use this if you don't have an official API token.
publisher.setup_adapter("medium", {
    "sid": "your_sid_cookie",
    "uid": "your_uid_cookie"
})

# Substack (Email-to-Post)
publisher.setup_adapter("substack", {
    "email": "your_gmail@gmail.com", 
    "password": "GMAIL_APP_PASSWORD"
})

# 2. Broadcast!
results = publisher.broadcast(
    title="The Future of AI Agents",
    content="# My Article\nThis is a test of Broadcaster.",
    substack={"target_email": "your_secret_substack_email@substack.com"}
)

print(results)
```

## 💡 Why this exists?
Paid aggregators are expensive and opaque. Broadcaster gives you a modular, extensible, and free way to build your personal brand as an AI engineer.
