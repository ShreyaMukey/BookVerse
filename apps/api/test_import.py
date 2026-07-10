import importlib
mods = [
  "bookverse.config",
  "bookverse.db",
  "bookverse.main",
  "bookverse.models",
  "bookverse.routers.health",
  "bookverse.routers.books",
  "bookverse.routers.authors",
  "bookverse.routers.search",
]
for m in mods:
    importlib.import_module(m)
    print("ok", m)
