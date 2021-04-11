import json
import re

from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.models.network.model_network_mixin import NetworkMixinModel


class GenericNetworkModel(NetworkMixinModel):
    __tablename__ = 'generic_networks'
    tags = db.Column(db.String(320), nullable=True)

    @validates('tags')
    def validate_tags(self, _, value):
        """
        Rules for tags:
        - force all tags to be lower case
        - if there is a gap add an underscore
        - no special characters
        """
        if value is not None:
            try:
                tags = json.loads(value)
                return_tags: dict = {}
                for tag in tags:
                    clean_tag: str = tag.lower()
                    clean_tag = clean_tag.replace(" ", "_")
                    clean_tag = re.sub('[^A-Za-z0-9_]+', '', clean_tag)
                    return_tags[clean_tag] = tags[tag]
                return json.dumps(return_tags)
            except ValueError:
                raise ValueError('tags needs to be a valid JSON')
        return value

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC
