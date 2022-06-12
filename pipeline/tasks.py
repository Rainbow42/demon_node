from application.celery import app


@app.task(shared=True)
def ended_time_sent_survey(survey_sending_id):
    """Когда отведенное время на прохождение отправленного опроса подойдет к концу,
    нужно поменять его статус """
    sending_survey(survey_sending_id, SendingSurveyStatus.COMPLETED)
    logger.info(f'Ended sending survey id: {survey_sending_id}')