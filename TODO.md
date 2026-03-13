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
- [ ] Team model + GET API (Read-only for frontend)
- [ ] Tournament model + GET API (Read-only for frontend)
- [ ] Match model + GET API (Read-only for frontend)
- [ ] Map model + GET API (Read-only for frontend)
- [ ] GameStats model + GET API (Read-only for frontend)

## League Features
- [ ] Automated LeaguePool assignment mapping (Group users by 10)
- [ ] League status transitions (OPEN → ACTIVE → COMPLETED)
- [ ] League settings (roster size, scoring type, trade deadlines)

## Drafting
- [ ] Draft model (linked to league)
- [ ] Draft order generation (snake, linear, auction)
- [ ] Pick/ban logic
- [ ] Draft state machine (PENDING → IN_PROGRESS → COMPLETED)

## Roster Management
- [ ] `RosterPlayer` model (Join table: Roster ↔ Player assignments)
- [ ] Add/drop free agent players
- [ ] Trade proposals and acceptance flow
- [ ] Roster lock enforcement (during active CS tournament matches)

## Scoring
- [ ] Scoring rules configuration per league
- [ ] Fantasy point calculation from csf-scraper game_stats
- [ ] Matchday/week scoring aggregation
- [ ] Standings/leaderboard

## Infrastructure
- [ ] Google OAuth authentication flow
- [ ] JWT token generation & validation
- [ ] CORS configuration
- [ ] Environment-based config (dev/staging/prod)
- [ ] Docker setup
- [ ] CI/CD pipeline
- [x] Logging and error handling middleware

## Cleanup
- [ ] Fix Pydantic deprecation warning (`class Config` → `model_config = ConfigDict(...)`)
