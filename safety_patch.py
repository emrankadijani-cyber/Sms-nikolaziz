from pathlib import Path
root=Path("app/src/main/java/ir/niko/sms")
p=root/"sms/SendService.kt"
s=p.read_text()
s=s.replace('if (fails >= 3) autoStop("۳ خطای متوالی؛ برای رعایت محدودیت‌های اپراتور ارسال متوقف شد")','if (fails >= 1) autoStop("خطای ارسال ثبت شد؛ صف برای بررسی متوقف شد")')
s=s.replace('var done = 0\n            while (true)', 'var done = 0\n            val maxPerRun = 20 // conservative per-session safeguard, not an operator-approved quota\n            while (true)')
s=s.replace('if (SendState.shouldHalt()) break\n                val row', 'if (SendState.shouldHalt()) break\n                if (done >= maxPerRun) {\n                    SendState.pauseRequested = true\n                    break\n                }\n                val row')
s=s.replace('delayInterruptible(maxOf(1, prefs.delaySec) * 1000L)', 'delayInterruptible(maxOf(15, prefs.delaySec) * 1000L)')
p.write_text(s)
p=root/"data/Prefs.kt"
s=p.read_text().replace('p.getInt("delaySec", 3)','p.getInt("delaySec", 15)').replace('p.getInt("batchSize", 20)','p.getInt("batchSize", 10)').replace('p.getInt("batchPauseSec", 60)','p.getInt("batchPauseSec", 300)')
p.write_text(s)
p=root/"ui/SettingsFragment.kt"
s=p.read_text().replace('?: 3).coerceIn(1, 3600)','?: 15).coerceIn(15, 3600)').replace('?: 20).coerceIn(1, 500)','?: 10).coerceIn(1, 20)').replace('?: 60).coerceIn(0, 3600)','?: 300).coerceIn(300, 3600)')
p.write_text(s)
print("Safety patch applied")
