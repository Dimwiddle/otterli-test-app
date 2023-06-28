import pytest
from api.api_hub import FeedbackAPI

@pytest.fixture()
def feedback_api():
    return FeedbackAPI()


def test_quick_question_format(feedback_api: FeedbackAPI):
    question = feedback_api.get_current_question()
    assert isinstance(question['id'], int)
    assert isinstance(question['display'], bool)
    assert isinstance(question['display_from'], str)
    assert isinstance(question['display_to'], str)

@pytest.mark.skip
def test_quick_answer():
    pass

@pytest.mark.skip
def test_quick_answer_negative():
    """Pass a null value as an answer."""
    pass
