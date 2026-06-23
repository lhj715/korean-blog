#!/usr/bin/env python3
"""
리딩맵 기출 JSON 검수기
사용법: python3 validate_exam.py <json파일>
"""

import json
import re
import sys
from pathlib import Path


def error(msg): print(f"  ❌ {msg}")
def warn(msg):  print(f"  ⚠️  {msg}")
def ok(msg):    print(f"  ✅ {msg}")


# ── 선지 품질 검수 헬퍼 ───────────────────────────────────────

# 문장을 끝맺지 않는 접속형·관형사형 어미
_TRUNCATED = re.compile(
    r'(이므로|하므로|하여|하여서|이어서|이며|하며|이고|하고|이나|이거나'
    r'|인데|하는데|이는데|에서|으로서|로서|이라서|이라|이어|이지)$'
)


def check_truncation(text: str):
    """선지가 불완전하게 끊겼으면 (True, 이유) 반환"""
    t = text.strip()
    if not t:
        return False, ''
    if t[-1] in (',', '，'):
        return True, '쉼표로 끝남'
    if _TRUNCATED.search(t):
        return True, f'접속형 어미로 끝남 (…{t[-5:]})'
    return False, ''


def check_length_variance(choices: list):
    """선지 길이 편차 이상 여부 체크 — 짧은 선지 번호 목록 반환"""
    texts = [c.get('text', '') for c in choices]
    lengths = [len(t) for t in texts]
    if not lengths or max(lengths) == 0:
        return []
    median = sorted(lengths)[len(lengths) // 2]
    threshold = max(median * 0.3, 8)   # 중앙값의 30% 또는 8자 미만
    return [
        choices[i].get('no')
        for i, l in enumerate(lengths)
        if l < threshold and l < median
    ]


def validate(path: str) -> int:
    fail = 0

    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ JSON 파싱 실패: {e}")
        return 1

    print(f"\n{'='*50}")
    print(f"검수 파일: {path}")
    print(f"{'='*50}")

    # ── 1. meta 필수 항목 ──────────────────────────────
    print("\n[1] meta")
    required_meta = ["id", "year", "exam_type", "grade", "month", "total_questions", "elective"]
    meta = data.get("meta", {})
    for f in required_meta:
        if f not in meta:
            error(f"meta.{f} 누락"); fail += 1
        else:
            ok(f"meta.{f} = {meta[f]}")

    # ── 2. sections 구조 ──────────────────────────────
    print("\n[2] sections 구조")
    sections = data.get("sections", [])
    if not sections:
        error("sections 비어 있음"); fail += 1

    all_q_numbers = []

    for sec in sections:
        sec_id = sec.get("id", "?")
        sets = sec.get("sets", [])
        print(f"\n  섹션: {sec_id} (세트 {len(sets)}개)")

        for s in sets:
            set_id = s.get("id", "?")
            q_range = s.get("q_range", [])
            passages = s.get("passages", [])
            questions = s.get("questions", [])

            print(f"\n    세트: {set_id}  문항범위={q_range}")

            # ── 3. q_range 정합성 ──────────────────────
            if len(q_range) == 2:
                expected_count = q_range[1] - q_range[0] + 1
                actual_count = len(questions)
                if actual_count != expected_count:
                    warn(f"문항 수 불일치: q_range={q_range} → {expected_count}개 예상, 실제 {actual_count}개")
                else:
                    ok(f"문항 수 일치 ({actual_count}개)")
            else:
                error("q_range 형식 오류 (2개 값 필요)"); fail += 1

            # ── 4. passages 검수 ───────────────────────
            # 화작·언매는 독립 문항이 존재해 지문이 빌 수 있음
            is_elective_sec = sec.get('id') in ('화법과작문', '언어와매체')
            if not passages:
                if is_elective_sec:
                    warn("passages 비어 있음 (선택과목 독립문항 세트, 정상)")
                else:
                    error("passages 비어 있음"); fail += 1
            for p in passages:
                pid = p.get("id") or "단일"
                paras = p.get("paragraphs", [])
                genre = p.get("genre", "없음")
                if not paras:
                    error(f"지문 [{pid}] paragraphs 비어 있음"); fail += 1
                else:
                    ok(f"지문 [{pid}] genre={genre}, 문단 {len(paras)}개")

                # markers 확인
                markers = p.get("markers", {})
                text = " ".join(paras)
                for mark in markers:
                    if mark not in text:
                        warn(f"지문 [{pid}] 표시어 '{mark}' 본문에 없음")

            # ── 5. questions 검수 ──────────────────────
            for q in questions:
                num = q.get("number")
                if num is None:
                    error("number 없는 문항"); fail += 1; continue

                all_q_numbers.append(num)
                score = q.get("score")
                choices = q.get("choices", [])
                answer = q.get("answer")
                proc_method = q.get("processing_method", "normal_text_extraction")
                confidence  = q.get("confidence", 1.0)
                needs_review = q.get("needs_review", False)
                is_special   = proc_method != "normal_text_extraction"

                prefix = f"Q{num:02d}"

                # processing_method 유효성
                valid_methods = {
                    'normal_text_extraction', 'table_choice_parser',
                    'memo_image_choice_parser', 'cropped_ocr_required'
                }
                if proc_method not in valid_methods:
                    error(f"{prefix}: 알 수 없는 processing_method='{proc_method}'"); fail += 1

                # needs_review / confidence 경고
                if needs_review:
                    warn(f"{prefix}: needs_review=True — 검토 필요")
                if confidence < 0.8:
                    warn(f"{prefix}: confidence={confidence:.2f} 낮음")
                if proc_method == 'cropped_ocr_required':
                    warn(f"{prefix}: cropped_ocr_required — OCR 처리 대기")

                # 선지 수
                if len(choices) != 5:
                    if is_special:
                        warn(f"{prefix}: 선지 수 = {len(choices)} (processing_method={proc_method})")
                    else:
                        error(f"{prefix}: 선지 수 = {len(choices)} (5개 필요)"); fail += 1
                else:
                    ok(f"{prefix}: 선지 5개")

                # 선지 번호 순서
                nos = [c.get("no") for c in choices]
                if nos != [1, 2, 3, 4, 5]:
                    if is_special and not choices:
                        pass
                    else:
                        error(f"{prefix}: 선지 번호 오류 {nos}"); fail += 1

                # 선지 내용 빈 칸
                empty = [c["no"] for c in choices if not c.get("text", "").strip()]
                if empty and not is_special:
                    warn(f"{prefix}: 선지 {empty} 내용 비어 있음")

                # ── 품질 규칙 ────────────────────────────────
                choice_fmt = q.get('choice_format', '')

                # (A) 끊긴 선지 감지 (어휘형 단답 선지 <15자는 제외)
                for c in choices:
                    t = c.get('text', '')
                    if len(t) < 15:
                        continue   # 어휘 대체형 등 단답 선지는 접속형 어미로 끝나도 정상
                    cut, reason = check_truncation(t)
                    if cut:
                        warn(f"{prefix}-{c['no']}: 선지 끊김 가능성 — {reason}")

                # (B) 길이 편차 과다
                if len(choices) == 5:
                    short = check_length_variance(choices)
                    if short:
                        warn(f"{prefix}: 선지 {short} 길이 과소 (편차 이상)")

                # (C) 특수 처리 방법인데 선지 없음 → cropped_ocr_required 후보
                if is_special and not choices:
                    warn(f"{prefix}: processing_method={proc_method}인데 choices 없음 → cropped_ocr_required 검토")

                # (D) 구조화 포맷 검수
                if choice_fmt == 'table_matching':
                    missing = [c['no'] for c in choices if not c.get('cells')]
                    if missing:
                        error(f"{prefix}: choice_format=table_matching인데 cells 없는 선지 {missing}"); fail += 1
                    else:
                        ok(f"{prefix}: table_matching cells 완비")
                if choice_fmt == 'memo_two_part':
                    missing = [c['no'] for c in choices if 'memo_note' not in c]
                    if missing:
                        error(f"{prefix}: choice_format=memo_two_part인데 memo_note 없는 선지 {missing}"); fail += 1
                    else:
                        ok(f"{prefix}: memo_two_part memo_note 완비")

                # 정답
                if answer is None:
                    warn(f"{prefix}: 정답 미입력")
                elif answer not in [1, 2, 3, 4, 5]:
                    error(f"{prefix}: 정답 = {answer} (1-5 범위 벗어남)"); fail += 1
                else:
                    ok(f"{prefix}: 정답 = {answer}")

                # 배점
                if score not in [2, 3]:
                    warn(f"{prefix}: 배점 = {score} (2점·3점 아님)")

                # passage_ref 유효성
                ref = q.get("passage_ref")
                if ref:
                    passage_ids = [p.get("id") for p in passages]
                    if ref not in passage_ids:
                        error(f"{prefix}: passage_ref='{ref}' 존재하지 않는 지문"); fail += 1

    # ── 6. 전체 문항 번호 검수 ─────────────────────────
    # 선택과목(화작/언매)은 35-45번이 두 번 나오므로 섹션 내 중복만 검사
    print("\n[3] 전체 문항 번호")
    elective_secs = {'화법과작문', '언어와매체'}
    elective_q = set()
    common_q = []
    for sec in sections:
        for s in sec.get('sets', []):
            for q in s.get('questions', []):
                if sec.get('id') in elective_secs:
                    elective_q.add(q.get('number'))
                else:
                    common_q.append(q.get('number'))

    common_q.sort()
    common_dups = [n for n in common_q if common_q.count(n) > 1]
    if common_dups:
        error(f"공통 파트 중복 문항 번호: {list(set(common_dups))}"); fail += 1
    else:
        ok(f"공통 파트 중복 없음")

    if elective_q:
        ok(f"선택과목 문항: {sorted(elective_q)} (화작·언매 공유, 중복 허용)")

    total_q = meta.get("total_questions")
    unique_q = len(set(common_q) | elective_q)
    if total_q and unique_q != total_q:
        warn(f"총 문항 수(고유): meta={total_q}, 실제={unique_q}")
    elif total_q:
        ok(f"총 문항 수(고유) 일치 ({total_q}개)")

    # ── 결과 요약 ──────────────────────────────────────
    print(f"\n{'='*50}")
    if fail == 0:
        print(f"✅ 검수 통과 (오류 0개)")
    else:
        print(f"❌ 오류 {fail}개 발견")
    print(f"{'='*50}\n")

    return fail


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 validate_exam.py <json파일>")
        sys.exit(1)
    sys.exit(validate(sys.argv[1]))
