# ওজি ইমেজ মেকার 🎨 (Python + Pillow)

> ব্লগ/গিটহাব/টুইটার শেয়ারের জন্য সুন্দর **১২০০×৬৩০ সোশ্যাল কার্ড** — টাইটেল দিন, থিম বাছুন, ছবি রেডি। **বাংলা টেক্সট সাপোর্টসহ** (Noto Sans Bengali ফন্ট বান্ডেল করা আছে)।

ওজি ইমেজ মেকার টুলগুলোতে বাংলা লিখলে ফন্ট না থাকায় টোফু (▯▯) দেখায়। এই পাইথন স্ক্রিপ্টে বাংলা ফন্ট সাথেই আছে — টাইটেল, সাবটাইটেল, ব্যাজ, ক্রেডিট সব বাংলায় লিখুন।

## ✨ Features

- ✅ **৫টা থিম**: dark · green · gold · blue · sunset — গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড
- ✅ অটো টেক্সট-র‍্যাপিং (বাংলা + ইংরেজি), ৩ লাইনের বেশি হলে "…"
- ✅ উপরে পিল-ব্যাজ + নিচে ক্রেডিট লাইন + ডেকোরেটিভ সার্কেল
- ✅ কাস্টম সাইজ (`--size 800x418`), ফোল্ডার অটো-তৈরি
- ✅ `examples/` ফোল্ডারে তৈরি করা নমুনা কার্ড দেওয়া আছে
- ✅ pytest টেস্টসুট (১৭/১৭) — সব থিম, র‍্যাপিং, সাইজ ভ্যালিডেশন

## 🚀 ব্যবহার

```bash
pip install pillow   # একবারই

python3 og_maker.py --title "বাজার হিসাব" \
  --subtitle "অফলাইনে প্রতিদিনের খরচ হিসাব — বাংলায়" \
  --badge "Day 9 of 100" --theme green --out card.png
```

নমুনা দেখুন: `examples/green.png`, `examples/gold.png`, `examples/sunset.png`

## 🧪 টেস্ট

```bash
python3 -m pytest test_og_maker.py -q   # 17 passed
```

## 🌍 গিটহাবে পুশ

```bash
git init && git add . && git commit -m "Day 12/100: OG Image Maker with Bangla font support (Python+Pillow)"
git branch -M main
git remote add origin https://github.com/iamzahirul/day-12-og-image-maker.git
git push -u origin main
```

টিপ: এই টুল দিয়েই আপনার ১০০ দিনের সব প্রজেক্টের শেয়ার-কার্ড বানিয়ে নিতে পারবেন!

## 🗺️ Roadmap (v2)

- [ ] আরো থিম + লোগো/আইকন বসানো
- [ ] ব্যাচ মোড (একটা জেসন লিস্ট থেকে অনেক কার্ড)
- [ ] ইমেজে পুরো প্যালেট কাস্টমাইজ

## 📜 ফন্ট ক্রেডিট

`assets/`-এ থাকা **Noto Sans Bengali** (SIL Open Font License) — Google/Noto Fonts থেকে। `NotoSans-Regular` (Apache-2.0) ইংরেজি ব্যাজের জন্য।

## 📜 License

MIT — Copyright (c) 2026 **Rasel (iamzahirul)**

---

*Day 12 of 100 — built in public by Rasel [@iamzahirul](https://github.com/iamzahirul)*
