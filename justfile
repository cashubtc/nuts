alias c := check
alias f := fix

default:
  @just --list

# Check style
check:
    prettier --check .

# Fix style
fix:
    prettier --check .
