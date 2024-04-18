from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="IIRAG",
    settings_files=["settings.yml", ".secret.yml"],
    merge_enabled=True,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.