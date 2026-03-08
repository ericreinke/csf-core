# TODO

## In Progress
- [ ] Fix Pydantic deprecation warning (switch `class Config` to `model_config = ConfigDict(...)`)

## Models & CRUD
- [ ] Team model + CRUD API
- [ ] Player model + CRUD API (link to csf-scraper player data via steam_id)
- [ ] User/Account model + CRUD API

## League Features
- [ ] League join/leave flow (team registration)
- [ ] League status transitions (OPEN → ACTIVE → COMPLETED)
- [ ] League settings (roster size, scoring type, trade deadlines)

## Drafting
- [ ] Draft model (linked to league)
- [ ] Draft order generation (snake, linear, auction)
- [ ] Pick/ban logic
- [ ] Draft state machine (PENDING → IN_PROGRESS → COMPLETED)

## Roster Management
- [ ] Roster model (team ↔ player assignments)
- [ ] Add/drop players
- [ ] Trade proposals and acceptance flow
- [ ] Roster lock enforcement (during matches)

## Scoring
- [ ] Scoring rules configuration per league
- [ ] Fantasy point calculation from csf-scraper game_stats
- [ ] Matchday/week scoring aggregation
- [ ] Standings/leaderboard

## Infrastructure
- [ ] Authentication (JWT or session-based)
- [ ] CORS configuration
- [ ] Environment-based config (dev/staging/prod)
- [ ] Docker setup
- [ ] CI/CD pipeline
- [ ] Logging and error handling middleware
