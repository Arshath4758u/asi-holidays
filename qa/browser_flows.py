# Browser end-to-end checks for the built features.
# Setup (Windows PowerShell, once): cd qa ; ..\backend\.venv\Scripts\python -m pip install playwright ; ..\backend\.venv\Scripts\python -m playwright install chromium
# Run with backend on :8000 and frontend dev server on :5173 already running:
#   ..\backend\.venv\Scripts\python browser_flows.py
# Note: the quote checker and enquiry forms are rate-limited per IP; restart the backend to reset.
import re
from playwright.sync_api import sync_playwright
B = "http://127.0.0.1:5173"
res = []
def rec(name, ok, detail=""):
    res.append(ok); print(("PASS " if ok else "FAIL ") + name + (" :: " + detail if detail else ""), flush=True)
def watch(pg):
    log = []
    pg.on("response", lambda r: log.append(f"{r.status} {r.request.method} {r.url.replace(B,'')}") if "/api/" in r.url else None)
    return log
ARGS = []
with sync_playwright() as p:
    br = p.chromium.launch(args=ARGS)

    # A. package enquiry form
    pg = br.new_page(); log = watch(pg)
    try:
        pg.goto(B + "/packages/sample-kerala-family", wait_until="networkidle")
        form = pg.locator("form.form").first
        form.get_by_placeholder("Your name").fill("QA Tester")
        form.get_by_placeholder("+91").fill("9876543210")
        form.locator("input[type=checkbox]").check()
        form.get_by_role("button", name="Send enquiry").click()
        pg.wait_for_url(re.compile(r".*/thank-you"), timeout=10000)
        rec("A package enquiry -> thank-you", True, " / ".join(l for l in log if "POST" in l))
    except Exception as e: rec("A package enquiry -> thank-you", False, str(e)[:160] + " | " + " / ".join(log[-2:]))
    pg.close()

    # B. contact form
    pg = br.new_page(); log = watch(pg)
    try:
        pg.goto(B + "/contact", wait_until="networkidle")
        form = pg.locator("form.form").first
        form.get_by_placeholder("Your name").fill("QA Contact")
        form.get_by_placeholder("+91").fill("9876543210")
        form.get_by_placeholder("you@example.com").fill("qa@example.com")
        form.get_by_placeholder("e.g. Kerala").fill("Ooty")
        form.get_by_placeholder("e.g. December").fill("March")
        form.get_by_placeholder("Tell us about your trip").fill("Family trip, 4 people")
        form.locator("input[type=checkbox]").check()
        form.get_by_role("button", name="Send enquiry").click()
        pg.wait_for_url(re.compile(r".*/thank-you"), timeout=10000)
        rec("B contact form -> thank-you", True, " / ".join(l for l in log if "POST" in l))
    except Exception as e: rec("B contact form -> thank-you", False, str(e)[:160] + " | " + " / ".join(log[-2:]))
    pg.close()

    # C. quiz (5 answers)
    pg = br.new_page(); log = watch(pg)
    try:
        pg.goto(B + "/quiz", wait_until="networkidle")
        for _ in range(5):
            pg.locator("button.option").first.click()
            pg.get_by_role("button", name=re.compile(r"^(Next|See my result)$")).click()
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(1500)
        body = pg.inner_text("body")
        rec("C mood quiz result", "You are" in body, " / ".join(l for l in log if "quiz" in l))
    except Exception as e: rec("C mood quiz result", False, str(e)[:160])
    pg.close()

    # D. group room: create, then vote
    pg = br.new_page(); log = watch(pg)
    try:
        pg.goto(B + "/rooms/new", wait_until="networkidle")
        pg.get_by_placeholder("e.g. Diwali holiday").fill("QA Family Trip")
        pg.locator("input[type=checkbox]").nth(0).check()
        pg.locator("input[type=checkbox]").nth(1).check()
        pg.get_by_role("button", name="Create room").click()
        pg.wait_for_url(re.compile(r".*/room/[^/]+$"), timeout=10000)
        pg.wait_for_load_state("networkidle")
        pg.get_by_placeholder("So others can see your vote").fill("Asik")
        pg.get_by_role("button", name="Vote for this").first.click()
        pg.wait_for_timeout(1500)
        rec("D group room create + vote", "Asik" in pg.inner_text("body"), " / ".join(l for l in log if "rooms" in l))
    except Exception as e: rec("D group room create + vote", False, str(e)[:160] + " | " + " / ".join(log[-2:]))
    pg.close()

    # E. quote checker
    pg = br.new_page(); log = watch(pg)
    try:
        pg.goto(B + "/check-my-quote", wait_until="networkidle")
        form = pg.locator("form.form").first
        form.get_by_label("Your name").fill("QA")
        form.get_by_placeholder("+91").fill("9876543210")
        form.get_by_placeholder(re.compile("Paste the hotels")).fill("Total 45000 INR for 4 people, hotel and flights included")
        form.locator("input[type=checkbox]").check()
        form.get_by_role("button", name="Send for review").click()
        pg.wait_for_timeout(2500)
        rec("E quote checker submits", any("POST" in l for l in log), " / ".join(l for l in log if "POST" in l) + " | " + pg.inner_text("body")[-120:].replace("\n"," "))
    except Exception as e: rec("E quote checker submits", False, str(e)[:160] + " | " + " / ".join(log[-2:]))
    pg.close()

    br.close()
print(f"\nSUMMARY {sum(res)} passed of {len(res)}")
