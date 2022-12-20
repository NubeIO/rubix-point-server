import logging

logger = logging.getLogger(__name__)


def commit(db):
    try:
        db.session.commit()
    except Exception as e:
        logger.error(f"SQL commit exception: {str(e)}")
        db.session.rollback()
        raise e
