"""bancho.py's v2 apis for interacting with scores"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import status
from fastapi.param_functions import Query

from app.api.v2.common import responses
from app.api.v2.common.responses import Failure
from app.api.v2.common.responses import Success
from app.api.v2.models.scores import Score
from app.api.v2.models.players import Player
from app.repositories import scores as scores_repo
from app.repositories import matchscore as matchscores_repo
from app.api.v2.models.scores import MatchScore

router = APIRouter()


@router.get("/scores")
async def get_all_scores(
    map_md5: str | None = None,
    mods: int | None = None,
    status: int | None = None,
    mode: int | None = None,
    user_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
) -> Success[list[Score]] | Failure:
    scores = await scores_repo.fetch_many(
        map_md5=map_md5,
        mods=mods,
        status=status,
        mode=mode,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )
    total_scores = await scores_repo.fetch_count(
        map_md5=map_md5,
        mods=mods,
        status=status,
        mode=mode,
        user_id=user_id,
    )

    response = [Score.from_mapping(rec) for rec in scores]

    return responses.success(
        content=response,
        meta={
            "total": total_scores,
            "page": page,
            "page_size": page_size,
        },
    )


@router.get("/scores/{score_id}")
async def get_score(score_id: int) -> Success[Score] | Failure:
    data = await scores_repo.fetch_one(id=score_id)
    if data is None:
        return responses.failure(
            message="Score not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    response = Score.from_mapping(data)
    return responses.success(response)

@router.get("/scores/match/{match_id}")
async def get_match_score(match_id: int) -> Success[MatchScore] | Failure:
    print("Getting match score for match")
    data = await matchscores_repo.fetch_many(match_id=match_id)
    print(data)
    response = [MatchScore.from_mapping(rec) for rec in data]
    return responses.success(response)

@router.get("/scores/matches")
async def get_matches(
    map_md5: str | None = None,
    mods: int | None = None,
    status: int | None = None,
    mode: int | None = None,
    user_id: int | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),) -> Success[int] | Failure:
    data = await matchscores_repo.fetch_many(
        map_md5=map_md5,
        mods=mods,
        status=status,
        mode=mode,
        user_id=user_id,
        page=page,
        page_size=page_size,)
    total = await matchscores_repo.fetch_count(
        map_md5=map_md5,
        mods=mods,
        status=status,
        mode=mode,
        user_id=user_id,
        page=page,
        page_size=page_size,)
    response = [rec.match_id for rec in data]

    return responses.success(
        content=response,
        meta={
            "total": total,
            "page": page,
            "page_size": page_size,
        },
    )
