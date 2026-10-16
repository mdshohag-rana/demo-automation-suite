import pytest
import allure
from pathlib import Path
from playwright.sync_api import Browser, BrowserContext, Page


# =====================================
# DIRECTORIES
# =====================================

SCREENSHOT_DIR = Path("screenshots")
VIDEO_DIR = Path("videos")
TRACE_DIR = Path("traces")

REPORT_DIR = Path("reports")
ALLURE_DIR = Path("allure-results")
PLAYWRIGHT_DIR = Path("playwright-results")


def create_directories():
    for directory in [
        SCREENSHOT_DIR,
        VIDEO_DIR,
        TRACE_DIR,
        REPORT_DIR,
        ALLURE_DIR,
        PLAYWRIGHT_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


create_directories()


# =====================================
# PYTEST CONFIGURATION file
# =====================================

def pytest_configure(config):
    create_directories()

    html_report = getattr(config.option, "htmlpath", None)

    if html_report:
        html_path = Path(html_report)

        if not html_path.is_absolute():
            html_path = Path(config.rootpath) / html_path

        html_path.parent.mkdir(parents=True, exist_ok=True)


# =====================================
# CONTEXT FIXTURE
# VIDEO + TRACE
# =====================================

@pytest.fixture(scope="function")
def context(browser: Browser, request) -> BrowserContext:
    context = browser.new_context(
        record_video_dir=str(VIDEO_DIR),
        record_video_size={
            "width": 1280,
            "height": 720,
        },
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    trace_file = TRACE_DIR / f"{request.node.name}_trace.zip"

    try:
        context.tracing.stop(path=str(trace_file))
    except Exception as e:
        print(f"Trace stop failed: {e}")

    try:
        context.close()
    except Exception as e:
        print(f"Context close failed: {e}")

    if trace_file.exists():
        allure.attach.file(
            str(trace_file),
            name="Playwright Trace",
            attachment_type=allure.attachment_type.ZIP,
        )


# =====================================
# PAGE FIXTURE
# SCREENSHOT + HTML + URL + VIDEO
# =====================================

@pytest.fixture(scope="function")
def page(context: BrowserContext, request) -> Page:
    page = context.new_page()

    yield page

    test_name = request.node.name

    screenshot_file = SCREENSHOT_DIR / f"{test_name}.png"
    html_file = SCREENSHOT_DIR / f"{test_name}.html"

    video_path = None

    try:
        if page.video:
            video_path = page.video.path()
    except Exception:
        pass

    # ==========================
    # Screenshot
    # ==========================
    try:
        page.screenshot(
            path=str(screenshot_file),
            full_page=True,
        )

        allure.attach.file(
            str(screenshot_file),
            name="Final Screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    except Exception as e:
        print(f"Screenshot failed: {e}")

    # ==========================
    # HTML Source
    # ==========================
    try:
        html = page.content()

        html_file.write_text(
            html,
            encoding="utf-8",
        )

        allure.attach.file(
            str(html_file),
            name="Page Source",
            attachment_type=allure.attachment_type.HTML,
        )

    except Exception as e:
        print(f"HTML capture failed: {e}")

    # ==========================
    # URL
    # ==========================
    try:
        allure.attach(
            page.url,
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT,
        )

    except Exception as e:
        print(f"URL attachment failed: {e}")

    # ==========================
    # Close page
    # ==========================
    try:
        page.close()
    except Exception as e:
        print(f"Page close failed: {e}")

    # ==========================
    # Attach video
    # ==========================
    try:
        if video_path and Path(video_path).exists():
            allure.attach.file(
                video_path,
                name="Test Video",
                attachment_type=allure.attachment_type.MP4,
            )
    except Exception as e:
        print(f"Video attachment failed: {e}")
