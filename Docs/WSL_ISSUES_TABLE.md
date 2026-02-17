# WSL2 `/mnt/c` 이슈 정리 (README 삽입용)

> ⚠ **이 프로젝트는 WSL2 Linux 파일시스템(`~/`)에서 운영합니다.**
> Windows 드라이브(`/mnt/c`)에서 직접 작업하면 아래 문제가 발생합니다.

## 증상 → 원인 → 해결 표

| # | 증상 | 원인 | 해결 | 근거 |
|:-:|:---|:---|:---|:---|
| 1 | `npm install`이 5~10배 느림 | `/mnt/c`는 9P 프로토콜로 브릿지되어 네트워크 수준 I/O 지연 발생 | 소스와 `node_modules`를 `~/projects/` 로 이동 | [MS Docs: Comparing WSL versions](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) |
| 2 | `hot-reload`/`file watcher`가 변경 감지 못함 | Windows→Linux 간 `inotify` 이벤트가 전달되지 않음 (9P 한계) | 프로젝트를 WSL 내부에 배치하거나 polling 모드 사용 | [GitHub WSL#4739](https://github.com/microsoft/WSL/issues/4739) |
| 3 | `chmod +x` 해도 실행 권한이 안 붙음 | DrvFs는 기본적으로 Linux 권한 메타데이터를 무시 | `/etc/wsl.conf`에 `[automount] options = "metadata"` 추가 | [MS Docs: File Permissions](https://learn.microsoft.com/en-us/windows/wsl/file-permissions) |
| 4 | `git status`에 **모든 파일**이 modified 표시 | CRLF(Windows) ↔ LF(Linux) line ending 불일치 | WSL: `git config --global core.autocrlf input` | [Git Docs: autocrlf](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration) |
| 5 | `vmmem` 프로세스가 RAM 4GB+ 점유 | 교차 파일시스템 캐싱으로 WSL2 VM 메모리 팽창 | `%UserProfile%\.wslconfig`에 `memory=2GB` 제한 설정 | [MS Docs: WSL Config](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) |
| 6 | 심링크가 "Permission denied"로 실패 | Windows의 심링크 생성 권한 제한 (개발자 모드 필요) | Windows 설정 → 개발자 모드 활성화, 또는 WSL 내부에서만 심링크 사용 | [SO: WSL symlink](https://stackoverflow.com/questions/49846648) |
| 7 | 대소문자만 다른 파일 충돌 (`File.js` vs `file.js`) | NTFS의 대소문자 무시 + Linux의 대소문자 구분 차이 | 프로젝트를 ext4 (WSL 내부)에서만 관리 | [GitHub WSL#214](https://github.com/microsoft/WSL/issues/214) |

## 권장 설정 스니펫

### `/etc/wsl.conf` (WSL 내부)
```ini
[automount]
enabled = true
options = "metadata,umask=22,fmask=11"

[interop]
appendWindowsPath = false
```

### `~/.wslconfig` (Windows 측, `%UserProfile%`)
```ini
[wsl2]
memory=4GB
swap=2GB
```

### Git 설정 (WSL 내부)
```bash
git config --global core.autocrlf input
git config --global core.eol lf
```

---

> 💡 **반박 대비 키워드**: `9P protocol overhead`, `inotify cross-OS limitation`, `DrvFs metadata flag`, `NTFS case-insensitive collision`, `vmmem memory balloon`
