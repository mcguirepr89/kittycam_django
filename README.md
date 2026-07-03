# KittyCam Django

KittyCam Django is the web application component of the KittyCam project. It provides an authenticated dashboard for viewing an IP camera stream and monitoring the status of the camera infrastructure. While it is fully functional as a standalone Django application, it is designed to be used alongside the companion **kittycam_docker** repository, which provides a secure deployment of go2rtc, Tailscale, and Caddy.

The project emphasizes a secure-by-default architecture intended for self-hosted environments. Rather than exposing an IP camera or its RTSP stream directly to the Internet, the recommended deployment isolates the camera behind multiple layers of authentication and network segmentation while still providing convenient remote access through a modern web interface.

---

# Project Goals

KittyCam was designed with the following principles in mind:

* Provide a clean, responsive dashboard for viewing a camera stream.
* Require user authentication before granting access.
* Minimize the attack surface exposed to the public Internet.
* Separate application code from mutable application data.
* Follow established Linux deployment conventions.
* Encourage deployment as a dedicated system service rather than under a personal user account.
* Remain portable across Linux distributions while being developed and tested primarily on Debian.

Although development and testing have been performed on Raspberry Pi hardware running Debian, neither is a requirement. Any modern Linux system capable of running Python, Django, and a reverse proxy should be suitable.

---

# Architecture

This repository intentionally focuses on the web application itself.

<img width="1774" height="887" alt="KittyCam_Architecture" src="https://github.com/user-attachments/assets/9b5fb949-f1f5-4a3e-8dd9-39d4adff5ef2" />

When deployed using the companion **kittycam_docker** repository, go2rtc is reachable only through a private Tailscale network. Django never communicates directly with the camera itself; instead, it embeds the WebRTC stream provided by go2rtc.

This separation of responsibilities allows each component to remain relatively simple while reducing the amount of infrastructure exposed to the public Internet.

---

# Security Philosophy

One of the primary goals of KittyCam is to make unauthorized access to the camera as difficult as reasonably possible.

Many consumer IP cameras encourage deployments where:

* the camera has unrestricted Internet access,
* the RTSP stream is available on the local network,
* reverse proxies expose the video stream directly,
* authentication is minimal or absent.

KittyCam intentionally recommends a different approach.

The recommended architecture:

* keeps the camera isolated from the Internet whenever possible,
* exposes only the Django application through the reverse proxy,
* stores application secrets outside the source repository,
* runs the application as an unprivileged system account,
* stores mutable application data outside the application directory,
* limits access to the video infrastructure through Tailscale.

The companion Docker repository expands on these decisions in greater detail, including the Tailscale network topology and the deployment of go2rtc.

The goal is not to claim absolute security—no system can—but rather to significantly reduce the opportunities available to an attacker by minimizing exposed services and following the principle of least privilege.

---

# Recommended Directory Layout

The project intentionally separates executable code from configuration, application data, and logs.

```
/srv/kittycam/
├── app/
└── venv/

/etc/kittycam/
└── .env

/var/lib/kittycam/
├── db.sqlite3
├── media/
└── static/

/var/log/kittycam/
```

This organization closely follows the Linux Filesystem Hierarchy Standard (FHS).

| Directory            | Purpose                        |
| -------------------- | ------------------------------ |
| `/srv/kittycam/app`  | Django application source code |
| `/srv/kittycam/venv` | Python virtual environment     |
| `/etc/kittycam`      | Configuration and secrets      |
| `/var/lib/kittycam`  | Mutable application data       |
| `/var/log/kittycam`  | Application logs               |

Separating these concerns makes upgrades, backups, and system administration considerably simpler while preventing accidental modification of application code by runtime processes.

---

# Dedicated Service Account

Rather than running Django under a personal login account, KittyCam recommends creating a dedicated system account.

Example:

```bash
sudo useradd \
    --system \
    --home /srv/kittycam \
    --shell /usr/sbin/nologin \
    kittycam
```

Create the required directories:

```bash
sudo mkdir -p /srv/kittycam
sudo mkdir -p /etc/kittycam
sudo mkdir -p /var/lib/kittycam
sudo mkdir -p /var/log/kittycam

sudo chown -R kittycam:kittycam \
    /srv/kittycam \
    /var/lib/kittycam \
    /var/log/kittycam
```

Running as a dedicated service account limits the privileges available to the application and keeps ownership of application files independent from any particular administrator.

---

# Configuration

Application configuration is provided through environment variables.

A sample configuration is included as:

```
.env.example
```

Production deployments are expected to store the actual configuration outside the repository:

```
/etc/kittycam/.env
```

This file typically contains values such as:

* `SECRET_KEY`
* `DEBUG`
* `ALLOWED_HOSTS`
* `CSRF_TRUSTED_ORIGINS`

Secrets should never be committed to version control.

---

# Running as a systemd Service

KittyCam is intended to run as a standard Linux system service.

Example:

```ini
[Unit]
Description=KittyCam Django
After=network.target

[Service]
Type=simple
User=kittycam
Group=kittycam

WorkingDirectory=/srv/kittycam/app

Environment=DJANGO_SETTINGS_MODULE=config.settings.production

ExecStart=/srv/kittycam/venv/bin/gunicorn \
    config.wsgi:application \
    --bind 127.0.0.1:7000

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Most deployments only need to adjust:

* `WorkingDirectory`
* `ExecStart`
* listening address and port
* service user

---

# Reverse Proxy

KittyCam expects to be deployed behind a reverse proxy.

Although any capable reverse proxy may be used, development has been performed using **Caddy** because it offers:

* straightforward configuration,
* automatic HTTPS,
* automatic certificate renewal,
* excellent support for self-hosted applications.

Nginx, Apache, Traefik, or similar software can be substituted without requiring changes to the Django application itself.

---

# Relationship to the Docker Repository

This repository contains only the Django application.

The companion **kittycam_docker** repository contains the recommended deployment of:

* go2rtc
* Tailscale
* Caddy
* supporting configuration files

The Django application does not require those components in order to function, but they represent the recommended deployment architecture for users seeking a secure self-hosted camera system.

---

# Development

Clone the repository, create a virtual environment, install the dependencies, and apply migrations.

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

A development `.env` file can be created from the included `.env.example`.

---

# Contribution

Contributions that improve security, documentation, portability, or maintainability are especially welcome. The project's primary objective is to provide a simple, well-documented, and security-conscious reference implementation for self-hosted IP camera deployments.

---

# License

This project is released under the terms of the license included in this repository.
