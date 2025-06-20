import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://alicouponkorea.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_coupons():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("❌ 요청 실패:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    coupon_cards = soup.find_all("div", class_="coupon-card")

    result = []

    for card in coupon_cards:
        # 쿠폰 코드
        code_tag = card.find("div", class_="code")
        code = code_tag.get_text(strip=True) if code_tag else None
        if not code or len(code) < 4:
            continue

        # 제목 또는 설명
        title_tag = card.find("h3") or card.find("div", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # 유효기간 추출 (정규식 사용)
        text_block = card.get_text()
        date_match = re.search(r'(\d{4}[-./]\d{2}[-./]\d{2})', text_block)
        expiry = date_match.group(1) if date_match else "Unknown"

        result.append({
            "code": code,
            "title": title,
            "region": "KR",
            "expires": expiry
        })

    return result

if __name__ == "__main__":
    coupons = extract_coupons()
    if coupons:
        with open("coupons.json", "w", encoding="utf-8") as f:
            json.dump(coupons, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(coupons)}개의 쿠폰을 coupons.json에 저장했습니다.")
    else:
        print("⚠️ 유효한 쿠폰이 없습니다.")
