# TODO

## Models & CRUD
- [x] League model + CRUD API
- [x] Account model + CRUD API (Google-only auth)
- [x] Link League owner → User (ForeignKey)
- [x] Roster model + CRUD API
- [x] Player model + CRUD API (link to csf-scraper player data via sroster_id)

## League Features
- [ ] League join/leave flow (roster registration)
- [ ] League status transitions (OPEN → ACTIVE → COMPLETED)
- [ ] League settings (roster size, scoring type, trade deadlines)

## Drafting
- [ ] Draft model (linked to league)
- [ ] Draft order generation (snake, linear, auction)
- [ ] Pick/ban logic
- [ ] Draft state machine (PENDING → IN_PROGRESS → COMPLETED)

## Roster Management
- [ ] Roster model (roster ↔ player assignments)
- [ ] Add/drop players
- [ ] Trade proposals and acceptance flow
- [ ] Roster lock enforcement (during matches)

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
