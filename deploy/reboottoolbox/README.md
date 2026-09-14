# 리부트툴박스 운영 설정 및 복구 기록

2026-09-14 KST에 운영 서버에 적용하고 확인한 설정이다. 저장소의 이 파일들은 운영 설정의 기록이며, Git push만으로 서버의 `/etc` 설정이 바뀌지는 않는다. 새 서버의 자동 설치 스크립트로 사용하지 않는다.

서비스 주소: https://www.reboottoolbox.com/login

## 로그인 장애 원인과 조치

재부팅 후 `gunicorn.service`가 `203/EXEC`로 실패했다. 기존 `ExecStart`의 가상환경 이름 `backend-HHOJIMF`가 실제 이름 `backend-_HH0JIMF`와 달랐고, 작업 폴더도 `manage.py`가 있는 위치보다 한 단계 위였다.

실행 경로와 작업 폴더를 systemd drop-in으로 수정했다. 기존 부팅 시 자동 시작을 유지하고, 프로세스가 비정상 종료되면 5초 후 다시 시작하도록 설정했다. 기존 계정, 비밀번호 및 DB 데이터는 변경하지 않았다.

## 현재 연결 구조

- HTTP 도메인 요청은 경로를 유지해 `https://www.reboottoolbox.com`으로 308 이동한다. 인증서 갱신용 `/.well-known/acme-challenge/`는 HTTP에서 계속 제공한다.
- Nginx가 HTTPS를 처리하고 `/api/`를 `127.0.0.1:8000`의 Django/Gunicorn으로 전달한다.
- 나머지 경로는 기존 `127.0.0.1:5173`의 Node `serve -s dist -l 5173` 프로세스로 전달한다. 이번 작업에서 프런트엔드 실행 방식을 변경하거나 별도의 자동 시작 서비스를 추가하지 않았다.
- `wey_frontend/.env.production`의 `VITE_API_URL`은 `https://www.reboottoolbox.com`이다. Vite 빌드 시 반영되므로 값을 바꾼 뒤에는 반드시 다시 빌드해야 한다. 공개 프런트엔드 설정이므로 여기에 비밀번호나 비밀 키를 넣지 않는다.
- 인증서 대상은 `www.reboottoolbox.com`이다. 확인 당시 `reboottoolbox.com`에는 주소 레코드가 없었으며 DNS는 변경하지 않았다.
- 이 작업은 도메인 HTTPS 적용이다. 기존 직접 IP 접근 포트와 방화벽은 변경하지 않았다.

## 저장소 파일과 서버 적용 위치

| 저장소 파일 | 서버 적용 위치 |
| --- | --- |
| `nginx.conf` | `/etc/nginx/sites-available/reboottoolbox` |
| `gunicorn.override.conf` | `/etc/systemd/system/gunicorn.service.d/10-reboot-toolbox-recovery.conf` |
| `certbot.override.conf` | `/etc/systemd/system/certbot.service.d/10-reboot-runtime.conf` |
| `reload-nginx.sh` | `/etc/letsencrypt/renewal-hooks/deploy/reload-reboot-nginx` (실행 권한 `0755`) |

Nginx의 기존 `/etc/nginx/sites-enabled/reboottoolbox` 링크와 기본 `gunicorn.service`, `certbot.service`, `certbot.timer`를 유지한다. `.override.conf` 파일은 기존 서비스에 추가하는 설정이며 완전한 서비스 정의가 아니다.

경로는 현재 서버 기준이다. 다른 서버에서는 프로젝트 폴더, 가상환경 및 인증서 경로를 먼저 확인해야 한다. 기존 설정을 백업한 뒤 변경하고, Nginx는 `nginx -t` 성공 후 reload한다. systemd 설정을 수정한 경우 `systemctl daemon-reload` 후 해당 서비스를 재시작한다. 인증서 파일이 없는 서버에는 TLS 설정부터 적용하지 않는다.

## 인증서 자동 갱신

시스템 Certbot은 Python 환경 불일치로 실행되지 않았다. Python 3.12 기반의 별도 가상환경 `/opt/reboot-certbot`에 Certbot 5.8.0을 설치하고, 기존 `certbot.service`가 이 실행 파일을 사용하도록 수정했다.

Let's Encrypt 인증서는 webroot `/var/www/letsencrypt`로 도메인을 검증해 발급했다. 최초 발급 인증서의 만료일은 2026-12-13이며 자동 갱신 후에는 달라진다. 개인 이메일은 등록하지 않았다. 인증서와 개인 키는 서버 `/etc/letsencrypt`에서 관리하고 Git에 넣지 않는다.

기존 `certbot.timer`는 활성화되어 있다. 하루 두 번의 예약 시각에 무작위 지연을 적용해 갱신 필요 여부를 검사한다. 갱신 성공 후 deploy hook이 Nginx 설정을 검사하고 reload한다.

서버에서 상태를 확인하는 명령:

```sh
systemctl is-active nginx gunicorn certbot.timer
systemctl is-enabled gunicorn certbot.timer
systemctl list-timers certbot.timer --no-pager
systemctl show certbot.service -p Result -p ExecMainStatus
/opt/reboot-certbot/bin/certbot certificates
```

갱신 경로나 Nginx 설정을 변경한 경우 다음 명령으로 검증한다. 성공한 검증을 이유 없이 반복 실행할 필요는 없다.

```sh
/opt/reboot-certbot/bin/certbot renew --cert-name www.reboottoolbox.com --dry-run --run-deploy-hooks --no-random-sleep-on-renew
```

## 다음 프런트엔드 배포 시 확인

운영 소스는 `/var/www/RebootCommons`, 프런트엔드는 그 아래 `wey_frontend`다. 서버에 기존 미커밋 변경이 있을 수 있으므로 먼저 `git status`를 확인하고 필요한 변경만 통합한다. 운영 폴더 전체를 강제로 초기화하지 않는다.

1. `wey_frontend/.env.production`에 HTTPS API 주소가 유지되는지 확인한다.
2. 운영 중인 `dist`를 서버의 별도 백업 폴더에 보관한다.
3. `wey_frontend`에서 `npm run build -- --outDir dist-next`로 별도 폴더에 빌드한다. 빌드 성공을 확인하기 전에는 운영 파일을 교체하지 않는다.
4. 새 정적 자산을 먼저 배치한 뒤 `index.html`을 교체한다. 기존 브라우저가 이전 파일을 요청할 수 있으므로 이전 해시 자산은 전환 중 유지한다.
5. HTTPS 로그인, 기업 관리 화면 및 HTTP에서 HTTPS로의 이동을 확인한다.

프런트엔드 재배포에는 DB 초기화, 계정 재생성 또는 비밀번호 변경이 필요하지 않다.

## 적용 당시 검증 결과

- SQLite `quick_check` 통과, 기존 마스터 계정 활성화 및 관리자 권한 확인.
- Django `manage.py check` 및 WSGI import 통과.
- 로그인·프로필·기업 목록 API HTTP 200 확인.
- 실제 브라우저에서 HTTPS 마스터 로그인 후 `/companies` 화면과 기업 데이터 표시 확인.
- 외부 `curl`에서 인증서 검증 성공, HTTP 308 이동 후 HTTPS 로그인 페이지 HTTP 200 확인.
- 새 빌드의 API 주소가 HTTPS이며 이전 HTTP IP API 주소가 포함되지 않음을 확인.
- Certbot 갱신 모의 실행과 Nginx reload hook 통과, timer 활성화 확인.

전체 서버 재부팅 검증은 수행하지 않았다. 위 결과는 적용 당시 확인한 상태이며 지속적인 모니터링을 뜻하지 않는다.

## 서버 내부 백업

- 로그인 복구: `/root/reboot-toolbox-recovery/20260914-210852/` — 원래 Gunicorn 서비스, SQLite 백업, `RECOVERY.txt`.
- HTTPS 적용: `/root/reboot-toolbox-recovery/https-20260914-211433/` — 원래 Nginx 설정, 프런트엔드 환경 설정·빌드, 변경하지 않은 Django 설정 사본, `HTTPS_RECOVERY.txt`.
- `/root/reboot-toolbox-recovery/https-latest`는 위 HTTPS 백업 폴더를 가리킨다.

백업에는 DB 및 민감한 설정이 포함될 수 있으므로 서버 내부에서만 관리한다. 되돌릴 때는 해당 설정이나 프런트엔드 파일만 선택해 복원한다. 배포 이후의 사용자 데이터가 사라질 수 있으므로 설정을 되돌리기 위해 DB 백업을 덮어쓰지 않는다.
