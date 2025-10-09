# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

default:
    @echo "🛠️  Justfile commands available:"
    @echo "  just lint       → run Ruff linter"
    @echo "  just typecheck  → run Ty type checker"
    @echo "  just check      → run both lint and typecheck"

lint:
    @echo "🔍 Running Ruff..."
    ruff check .

# Run Ty type checker
typecheck:
    @echo "🧠 Running Ty..."
    ty check

# Run both in sequence
check:
    @just lint
    @just typecheck