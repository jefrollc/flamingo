# 🦩 Flamingo

TODO

## Docker setup

TODO

## Migrations 

This uses [aerich](https://github.com/tortoise/aerich) for migrations.

```
Usage: aerich [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version      Show the version and exit.
  -c, --config TEXT  Config file.  [default: pyproject.toml]
  --app TEXT         Tortoise-ORM app name.
  -h, --help         Show this message and exit.

Commands:
  downgrade  Downgrade to specified version.
  heads      Show current available heads in migrate location.
  history    List all migrate items.
  init       Init config file and generate root migrate location.
  init-db    Generate schema and generate app migrate location.
  inspectdb  Introspects the database tables to standard output as...
  migrate    Generate migrate changes file.
  upgrade    Upgrade to specified version.
```

Helpful things to remember

```
aerich init -t database.TORTOISE_ORM

aerich init-db

# To create a migration
aerich migrate --name

# To upgrade to the most recent migration
aerich upgrade
```
