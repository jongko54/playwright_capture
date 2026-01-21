from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime


def capture_all_pages_with_login():
    """로그인된 Chrome 프로필을 사용해서 캡처"""

    # 타임스탬프로 폴더 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f'underthedeal_screenshots_{timestamp}'
    os.makedirs(output_dir, exist_ok=True)

    print(f"📁 저장 폴더: {output_dir}")
    print("\n⚠️  Chrome 프로필 경로를 설정해주세요!")
    print("=" * 60)

    # Chrome 프로필 경로 설정
    # Windows 예시
    user_data_dir = r"C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"

    # Mac 예시
    # user_data_dir = "/Users/YourUsername/Library/Application Support/Google/Chrome"

    # Linux 예시
    # user_data_dir = "/home/yourusername/.config/google-chrome"

    print(f"현재 설정된 경로: {user_data_dir}")
    print("\n💡 Chrome 프로필 경로 찾는 방법:")
    print("1. Chrome 주소창에 입력: chrome://version")
    print("2. '프로필 경로' 항목에서 확인")
    print("3. 경로에서 마지막 'Default' 또는 'Profile 1' 부분 제외")
    print("=" * 60)

    # 사용자 확인
    proceed = input("\n위 경로가 맞나요? 스크립트를 수정했다면 'y'를 입력하세요 (y/n): ")
    if proceed.lower() != 'y':
        print("스크립트를 수정하고 다시 실행해주세요!")
        return

    with sync_playwright() as p:
        try:
            print("\n🌐 Chrome 실행 중...")

            # 방법 1: launch_persistent_context 사용 (프로필 전체)
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,  # 화면 보이게
                channel="chrome",  # 설치된 Chrome 사용
                viewport={'width': 1920, 'height': 1080},
                # 특정 프로필 사용하려면 주석 해제하고 수정
                # args=["--profile-directory=Default"]  # 또는 Profile 1, Profile 2 등
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

        except Exception as e:
            print(f"❌ Chrome 프로필 로드 실패: {e}")
            print("\n대안: 프로필 없이 실행하고 수동으로 로그인하세요.")

            browser = p.chromium.launch(
                headless=False,
                channel="chrome"
            )
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()

            print("⏸️  잠시 후 로그인 페이지가 열립니다.")
            print("🔐 수동으로 로그인한 후 아무 키나 누르세요...")
            page.goto('https://검색할 페이지/')
            input("로그인 완료 후 Enter를 누르세요: ")

        # 캡처할 페이지 목록
        pages_to_capture = [
            {
                'name': '01',
                'url': 'https://',
                'wait': 3,
                'full_page': True
            },
            {
                'name': '02',
                'url': 'https://',
                'wait': 3,
                'full_page': True
            }
        ]

        try:
            for idx, page_info in enumerate(pages_to_capture, 1):
                print(f"\n[{idx}/{len(pages_to_capture)}] 🌐 {page_info['name']} 캡처 중...")

                # 페이지 이동
                page.goto(page_info['url'], wait_until='networkidle', timeout=30000)
                time.sleep(page_info['wait'])

                # 전체 페이지 스크린샷
                filepath = f"{output_dir}/{page_info['name']}_full.png"
                page.screenshot(path=filepath, full_page=page_info['full_page'])
                print(f"   ✅ 저장 완료: {filepath}")

                # 현재 뷰포트만 캡처
                viewport_path = f"{output_dir}/{page_info['name']}_viewport.png"
                page.screenshot(path=viewport_path, full_page=False)
                print(f"   ✅ 뷰포트 저장: {viewport_path}")

                # 스크롤 캡처
                if page_info['full_page']:
                    # 중간 지점
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
                    time.sleep(1)
                    middle_path = f"{output_dir}/{page_info['name']}_middle.png"
                    page.screenshot(path=middle_path, full_page=False)
                    print(f"   ✅ 중간 화면: {middle_path}")

                    # 하단
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(1)
                    bottom_path = f"{output_dir}/{page_info['name']}_bottom.png"
                    page.screenshot(path=bottom_path, full_page=False)
                    print(f"   ✅ 하단 화면: {bottom_path}")

            print(f"\n🎉 모든 캡처 완료!")
            print(f"📂 총 {len(pages_to_capture) * 4}개 이미지 저장됨")
            print(f"📁 위치: {os.path.abspath(output_dir)}")

        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            page.screenshot(path=f"{output_dir}/error_screenshot.png")

        finally:
            print("\n⏸️  5초 후 브라우저가 닫힙니다...")
            time.sleep(5)
            browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("로그인 프로필 사용 캡처")
    print("=" * 60)
    capture_all_pages_with_login()