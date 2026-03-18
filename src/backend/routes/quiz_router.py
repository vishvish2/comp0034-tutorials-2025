from fastapi import APIRouter

from backend.core.deps import SessionDep
from backend.models.schemas import QuestionRead, ResponseRead, QuestionCreate, ResponseCreate
from backend.services.quiz_service import QuizService

router = APIRouter()

crud = QuizService()


@router.get("/questions", response_model=list[QuestionRead])
def get_questions(session: SessionDep):
    """ Returns the data for all questions

    NB: Front-end route needs to be changed from '/question' to '/questions'
    """
    questions = crud.get_questions(session)
    return questions


@router.get("/questions/{q_id}", response_model=QuestionRead)
def get_question(session: SessionDep, q_id: int):
    """ Returns the data for one questions

    NB: Front-end route needs to be changed from '/question/q_id' to '/questions/{q_id}'
    """
    question = crud.get_question(session, q_id=q_id)
    return question


@router.get("/questions/{q_id}/responses", response_model=list[ResponseRead])
def get_responses_for_question(session: SessionDep, q_id: int):
    """ Returns the data for all responses for a given question

    NB: Front-end route needs to be changed from '/question/search' to '/questions/{q_id}/responses'
    """
    responses = crud.get_responses_by_question(session, q_id)
    return responses


@router.post("/questions", response_model=QuestionRead)
def create_question(session: SessionDep, question_data: QuestionCreate):
    """ Creates a new question  """
    new_question = crud.create_question(session, question_data)
    return new_question


@router.post("/responses", response_model=ResponseRead)
def create_response(session: SessionDep, create_data: ResponseCreate):
    """ Creates a new question  """
    new_question = crud.create_response(session, create_data)
    return new_question
