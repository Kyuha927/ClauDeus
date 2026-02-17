# ADR-002: WSL 파일 시스템 운영 전략

## 권장 결론
**WSL 전용 홈 디렉터리(`~/`) 내에서 프로젝트를 운영한다.**

## 결정 트리
- **성능이 최우선인가?**
    - (Yes) **WSL Home** 추천
    - (No) 다음 질문으로
- **Windows 에디터와의 실시간 동기화가 파일 시스템 이벤트 수준으로 필요한가?**
    - (Yes) **/mnt/c** (성능 저하 감수)
    - (No) **WSL Home** (vscode remote 추천)

## 비교표
| 항목 | /mnt/c (Drive Mount) | WSL Home (~/) |
| :--- | :--- | :--- |
| **성공/성능** | 낮음 (I/O 오버헤드 큼) | 높음 (ext4 네이티브 속도) |
| **운영비** | 낮음 (기존 탐색기 사용) | 보통 (네트워크 경로 접근 필요) |
| **디버깅 비용** | 높음 (chmod/chown 권한 불일치) | 낮음 (Linux 표준 권한 준수) |

## 실행 절차
1. WSL 터미널 접속: `wsl`
2. 프로젝트 복제: `git clone [URL] ~/projects/msw-vampser`
3. 환경 점검: `./dev doctor`
4. 에디터 연결: VS Code 상에서 `Open Folder` -> `\\wsl$\...` 경로 선택
5. 모든 커맨드는 WSL 터미널 상에서 수행
