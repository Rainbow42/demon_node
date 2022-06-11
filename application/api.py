from fastapi import APIRouter

from groups_mailing.endpoints import router as groups_mailing_router
from members.endpoints import router as members_router
from sendings.endpoints import router as sending_survey_router
from survey.endpoints import router as survey_router
from users.endpoints import router as users_router
from statistics.endpoints import router as statistics_router

router = APIRouter()
router.include_router(survey_router)
router.include_router(groups_mailing_router)
router.include_router(sending_survey_router)
router.include_router(members_router)
router.include_router(users_router)
router.include_router(statistics_router)
