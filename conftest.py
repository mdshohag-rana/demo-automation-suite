import pytest
import allure
from pathlib import Path
from playwright.sync_api import Browser, BrowserContext, Page

SCREENSHOT_DIR = Path("screenshots")
VIDEO_DIR = Path("videos")
TRACE_DIR = Path("traces")
REPORT_DIR = Path("test-results")

SCREENSHOT_DIR.mkdir(exist_ok=True)
VIDEO_DIR.mkdir(exist_ok=True)
TRACE_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True, parents=True)


# =========================
# CONTEXT (VIDEO + TRACE)
# =========================
@pytest.fixture(scope="function")
def context(browser: Browser, request) -> BrowserContext:
    context = browser.new_context(
        record_video_dir=str(VIDEO_DIR),
        record_video_size={"width": 1280, "height": 720}
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield context

    # ⭐ STOP TRACE AFTER TEST
    trace_file = TRACE_DIR / f"{request.node.name}_trace.zip"
    context.tracing.stop(path=str(trace_file))

    # ⭐ CLOSE CONTEXT → THIS CREATES VIDEO FILE
    context.close()

    # ⭐ ATTACH TRACE AFTER CONTEXT CLOSE
    if trace_file.exists():
        allure.attach.file(
            str(trace_file),
            name="Playwright Trace",
            attachment_type=allure.attachment_type.ZIP
        )


# =========================
# PAGE FIXTURE (SCREENSHOT + VIDEO)
# =========================
@pytest.fixture(scope="function")
def page(context: BrowserContext, request) -> Page:
    page = context.new_page()
    yield page

    test_name = request.node.name

    # =========================
    # TAKE FINAL SCREENSHOT (ALWAYS WORKS)
    # =========================
    screenshot_file = SCREENSHOT_DIR / f"{test_name}.png"
    html_file = SCREENSHOT_DIR / f"{test_name}.html"

    try:
        page.screenshot(path=str(screenshot_file), full_page=True)

        allure.attach.file(
            str(screenshot_file),
            name="Final Screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        # Attach HTML
        html = page.content()
        html_file.write_text(html, encoding="utf-8")

        allure.attach.file(
            str(html_file),
            name="Page Source",
            attachment_type=allure.attachment_type.HTML
        )

        # Attach URL
        allure.attach(
            page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )

    except Exception as e:
        print("Screenshot failed:", e)

    # =========================
    # CLOSE PAGE
    # =========================
    try:
        video_path = page.video.path() if page.video else None
    except Exception:
        video_path = None

    page.close()

    # =========================
    # ATTACH VIDEO (NOW EXISTS!)
    # =========================
    if video_path and Path(video_path).exists():
        allure.attach.file(
            video_path,
            name="Test Video",
            attachment_type=allure.attachment_type.MP4
        )
