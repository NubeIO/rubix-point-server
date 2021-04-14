from sqlalchemy.orm import validates

from src import db
from src.drivers.enums.drivers import Drivers
from src.models.network.model_network_mixin import NetworkMixinModel
from src.utils.model_utils import validate_json


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
                return validate_json(value)
            except ValueError:
                raise ValueError('tags needs to be a valid JSON')
        return value

    @classmethod
    def get_polymorphic_identity(cls) -> Drivers:
        return Drivers.GENERIC
