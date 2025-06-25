import tomli

with open("/opt/jbond/jbond.toml", "rb") as cfg:
    config = tomli.load(cfg)