# Placeholder for future OAuth-based admin/superuser dependency.
#
# When auth is implemented, create a `require_superuser` dependency here
# that validates the JWT token and checks for a superuser role, then apply
# it to the write endpoints (POST/PATCH/DELETE) on all game data routers:
#   teams, tournaments, matches, maps, game_stats
