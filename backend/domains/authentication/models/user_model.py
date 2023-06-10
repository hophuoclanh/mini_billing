from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'

    user_id = Column(String(36), primary_key=True)  # UUIDs are 36 characters long
    user_name = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    phone = Column(String(45), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    password = Column(String(72), nullable=False)

    def has_permission(self, session, action: str, resource: str) -> bool:
        from domains.authentication.models.user_position_model import \
            UserPositionModel  # Import here to avoid circular import
        from domains.authentication.models.position_permission_model import PositionPermissionModel
        from domains.authentication.models.permission_model import PermissionModel

        permission = session.query(PermissionModel).filter_by(
            action=action,
            resource=resource
        ).first()

        if permission is None:
            return False

        user_positions = session.query(UserPositionModel).filter_by(user_id=self.user_id).all()

        for user_position in user_positions:
            position_permission = session.query(PositionPermissionModel).filter_by(
                position_id=user_position.position_id,
                permission_id=permission.permission_id
            ).first()

            if position_permission is not None:
                return True

        return False

    def get_permissions(self, session) -> list:
        from domains.authentication.models.user_position_model import UserPositionModel
        from domains.authentication.models.position_permission_model import PositionPermissionModel
        from domains.authentication.models.permission_model import PermissionModel

        # Get all user positions
        user_positions = session.query(UserPositionModel).filter_by(user_id=self.user_id).all()

        permissions = []
        # Iterate over each user position
        for user_position in user_positions:
            # Get position permissions
            position_permissions = session.query(PositionPermissionModel).filter_by(
                position_id=user_position.position_id).all()

            # Iterate over each position permission
            for position_permission in position_permissions:
                permission = session.query(PermissionModel).filter_by(
                    permission_id=position_permission.permission_id).first()
                # Add the permission to the list
                permissions.append(permission)

        return permissions