# TODO

## Models & CRUD
- [x] League model + CRUD API
- [x] Account model + CRUD API (Google-only auth)
- [x] Link League owner → User (ForeignKey)
- [x] Roster model + CRUD API
- [x] Player model + CRUD API
- [x] LeaguePool model + CRUD API
- [x] LeagueRegistration model + CRUD API
- [x] League join/leave flow (LeagueRegistration)
- [x] Roster model + CRUD API (Strictly bound to LeaguePool)

## Game Data (From csf-scraper)
- [x] Team model + full CRUD API (GET public, writes admin-only)
- [x] Tournament model + full CRUD API (GET public, writes admin-only)
- [x] Match model + full CRUD API (GET public, writes admin-only)
- [x] Map model + full CRUD API (GET public, writes admin-only)
- [x] GameStats model + full CRUD API (GET public + player/map filters, writes admin-only)

## Admin / Auth
- [ ] Google OAuth authentication flow
- [ ] JWT token generation & validation
- [ ] Superuser role check on game data write endpoints (POST/PATCH/DELETE)

## League Features
- [x] Automated LeaguePool assignment (configurable pool_size per league, triggered on registration close)
- [x] League status transitions (OPEN → ACTIVE → draft phase via `league_lifecycle_service`)
- [x] Time-based polling loop (`lifecycle_poller.py`) — auto-fires transitions on deadline
- [x] Manual admin override endpoints (close-registration, assign-pools, start-draft)
- [ ] League settings (scoring type, trade deadlines)
- [ ] Full draft state machine (PENDING → IN_PROGRESS → COMPLETED, pick order, etc.)

## Drafting
- [ ] Draft model (linked to league)
- [ ] Draft order generation (snake, linear, auction)
- [ ] Pick/ban logic
- [ ] Draft state machine (PENDING → IN_PROGRESS → COMPLETED)

## Roster Management
- [x] `RosterPlayer` model (Join table: Roster ↔ Player assignments)
- [x] Add/drop players (draft onto roster, drop from roster)
- [ ] Trade proposals and acceptance flow
- [ ] Roster lock enforcement (during active CS tournament matches)

## Scoring
- [ ] Scoring rules configuration per league
- [ ] Fantasy point calculation from csf-scraper game_stats
- [ ] Matchday/week scoring aggregation
- [ ] Standings/leaderboard

## Infrastructure
- [x] Logging and error handling middleware
- [ ] CORS configuration
- [ ] Environment-based config (dev/staging/prod)
- [ ] Docker setup
- [ ] CI/CD pipeline

## Cleanup
- [ ] Fix Pydantic deprecation warning (`class Config` → `model_config = ConfigDict(...)`)
