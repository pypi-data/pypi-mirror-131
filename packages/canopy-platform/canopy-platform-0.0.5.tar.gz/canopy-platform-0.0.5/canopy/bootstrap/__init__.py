import configparser
import json
import textwrap
import time

from understory import host, web

__all__ = ["app"]

app = web.application(__name__)


def get_config():
    try:
        with open("gaea.json", "r") as fp:
            config = json.load(fp)
    except FileNotFoundError:
        config = {}
    return config


def update_config(**items):
    config = get_config()
    config.update(**items)
    with open("gaea.json", "w") as fp:
        json.dump(config, fp)


@app.control("")
class Bootsrap:
    """"""

    def get(self):
        config = get_config()
        if "registrar" in config:
            domains = host.dynadot.Client(config["registrar"]["token"]).list_domain()
        else:
            domains = []
        return app.view.index(config, domains)

    def post(self):
        form = web.form("domain", "name")
        config = get_config()
        try:
            ip_address = config["ip_address"]
        except KeyError:
            ip_address = host.spawn_machine(form.domain, config["host"]["token"])
            update_config(ip_address=ip_address)
        # dd = host.dynadot.Client(config["registrar"]["token"])
        # dd.set_dns2(form.domain, "a", ip_address)
        # host.setup_machine(ip_address)
        # while True:
        #     try:
        #         if str(web.dns.resolve(form.domain, "A")[0]) == ip_address:
        #             break
        #         else:
        #             print("waiting for DNS..")
        #     except (
        #         web.dns.NoAnswer,
        #         web.dns.NXDOMAIN,
        #         web.dns.Timeout,
        #         web.dns.NoNameservers,
        #     ):
        #         print("waiting for DNS..")
        #         time.sleep(15)
        # update_config(domain=form.domain)
        # host.setup_python(ip_address)
        # host.setup_nginx(ip_address)
        # host.generate_dhparam(ip_address)
        # host.setup_tor(ip_address)
        # host.setup_supervisor(ip_address)
        setup_canopy(ip_address, form.domain)
        return {"status": "success"}


def setup_canopy(ip_address, domain):
    ssh = host.digitalocean.get_ssh("root", ip_address)
    venv = "/root/canopy"
    # ssh(f"/root/python/bin/python3 -m venv {venv}")
    # ssh(
    #     "cat > /root/runinenv",
    #     stdin=textwrap.dedent(
    #         """\
    #         #!/usr/bin/env bash
    #         VENV=$1
    #         . ${VENV}/bin/activate
    #         shift 1
    #         exec "$@"
    #         deactivate"""
    #     ),
    # )
    # ssh("chmod +x /root/runinenv")
    # ssh(f"/root/runinenv {venv} pip install canopy-platform")

    # app = "canopy:app"
    name = "canopy"
    app_dir = "/home/gaea/apps/canopy"
    ssh(f"mkdir -p {app_dir}")

    # supervisor = configparser.ConfigParser()
    # command = (
    #     f"/root/runinenv {venv} gunicorn {app}"
    #     f" -k gevent -w 2 --bind unix:{app_dir}/app.sock"
    # )
    # supervisor[f"program:{name}"] = {
    #     "autostart": "true",
    #     "command": command,
    #     "directory": app_dir,
    #     "environment": "PYTHONUNBUFFERED=1",
    #     "stopsignal": "INT",
    #     "user": "root",
    # }

    # command = f"/root/runinenv {venv} loveliness serve"
    # supervisor[f"program:{name}-jobs"] = {
    #     "autostart": "true",
    #     "command": command,
    #     "directory": app_dir,
    #     "stopsignal": "INT",
    #     "user": "root",
    # }
    # host._write_supervisor_conf(ip_address, f"app-{name}", supervisor)

    domain_dir = f"/home/gaea/domains/{domain}"
    ssh(f"mkdir -p {domain_dir}/acme-challenge")
    ssh(
        f"cat > /root/nginx/conf/conf.d/{domain}.conf",
        stdin=f"""server {{
                      listen       80;
                      server_name  {domain};
    
                      location  /.well-known/acme-challenge/  {{
                          alias      {domain_dir}/acme-challenge/;
                          try_files  $uri  =404;
                      }}
                      location  /  {{
                          return  308  https://{domain}$request_uri;
                      }}
                  }}

                  # leave this here for cat'ing over SSH...""",
    )
    ssh("supervisorctl restart nginx")
    ssh(f"openssl genrsa 4096 > {domain_dir}/account.key")
    ssh(f"openssl genrsa 4096 > {domain_dir}/domain.key")
    ssh(
        f"openssl req -new -sha256 -key {domain_dir}/domain.key -subj "
        f"/CN={domain} > {domain_dir}/domain.csr"
    )
    ssh(
        f"/root/runinenv {venv} acme-tiny --account-key {domain_dir}/account.key "
        f"--csr {domain_dir}/domain.csr --acme-dir {domain_dir}/acme-challenge "
        f"> {domain_dir}/domain.crt"
    )
    ssh(f"rm {domain_dir}/domain.csr")
    ssh(
        f"cat > /root/nginx/conf/conf.d/{domain}.conf",
        stdin=str(host.templates.nginx_site(domain, name, host.SSL_CIPHERS)),
    )
    ssh("supervisorctl restart nginx")


@app.control("status")
class Status:
    """"""

    def get(self):
        try:
            with open("site.json") as fp:
                details = json.load(fp)
        except FileNotFoundError:
            details = {}
        return details


@app.control("host")
class Host:
    """"""

    def post(self):
        form = web.form("provider", "token")
        if form.provider == "digitalocean.com":
            c = host.digitalocean.Client(form.token)
            try:
                c.get_keys()
            except host.digitalocean.TokenError:
                return {"status": "error", "message": "bad token"}
            update_config(
                host={
                    "provider": form.provider,
                    "token": form.token,
                }
            )
            return {"status": "success"}
        return {"status": "error", "message": f"unsupported provider: {form.provider}"}


@app.control("registrar")
class Registrar:
    """"""

    def post(self):
        form = web.form("provider", "token")
        if form.provider == "dynadot.com":
            c = host.dynadot.Client(form.token)
            try:
                c.list_domain()
            except host.dynadot.TokenError:
                return {"status": "error", "message": "bad token"}
            update_config(
                registrar={
                    "provider": form.provider,
                    "token": form.token,
                }
            )
            return {"status": "success"}
        return {"status": "error", "message": f"unsupported provider: {form.provider}"}
