# TODO 프로그램 (Python CLI)

간단한 커맨드라인 TODO 프로그램입니다.

## 실행 방법

```bash
python3 todo.py --help
```

## 사용 예시

```bash
# 할 일 추가
python3 todo.py add "장보기"
python3 todo.py add "운동 30분"

# 전체 목록 보기
python3 todo.py list

# 미완료 항목만 보기
python3 todo.py list --open

# ID 1 완료 처리
python3 todo.py done 1

# ID 2 삭제
python3 todo.py delete 2

# 완료된 항목 정리
python3 todo.py clear-done
```

## 데이터 저장 위치

실행 위치 기준 `.todo.json` 파일에 저장됩니다.
