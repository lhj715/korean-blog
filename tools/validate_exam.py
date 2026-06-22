#!/usr/bin/env python3
"""
리딩맵 기출 JSON 검수기
사용법: python3 validate_exam.py <json파일>
"""

import json
import sys
from pathlib import Path


def error(msg): print(f"  ❌ {msg}")
def warn(msg):  print(f"  ⚠️  {msg}")
def ok(msg):    print(f"  ✅ {msg}")


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
            if not passages:
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
                has_image = q.get("has_image", False)

                prefix = f"Q{num:02d}"

                # 선지 수
                if len(choices) != 5:
                    error(f"{prefix}: 선지 수 = {len(choices)} (5개 필요)"); fail += 1
                else:
                    ok(f"{prefix}: 선지 5개")

                # 선지 번호 순서
                nos = [c.get("no") for c in choices]
                if nos != [1, 2, 3, 4, 5]:
                    error(f"{prefix}: 선지 번호 오류 {nos}"); fail += 1

                # 선지 내용 빈 칸
                empty = [c["no"] for c in choices if not c.get("text", "").strip()]
                if empty and not has_image:
                    warn(f"{prefix}: 선지 {empty} 내용 비어 있음")

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
    print("\n[3] 전체 문항 번호")
    all_q_numbers.sort()
    duplicates = [n for n in all_q_numbers if all_q_numbers.count(n) > 1]
    if duplicates:
        error(f"중복 문항 번호: {list(set(duplicates))}"); fail += 1
    else:
        ok(f"중복 없음")

    total_q = meta.get("total_questions")
    if total_q and len(all_q_numbers) != total_q:
        warn(f"총 문항 수: meta={total_q}, 실제={len(all_q_numbers)}")
    elif total_q:
        ok(f"총 문항 수 일치 ({total_q}개)")

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
