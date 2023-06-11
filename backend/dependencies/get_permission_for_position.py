from backend.domains.authentication.models.position_model import PositionModel
from backend.domains.authentication.models.position_permission_model import PositionPermissionModel
from backend.domains.authentication.models.permission_model import PermissionModel

def get_permissions_for_role(session, role: str):
    positions = session.query(PositionModel).filter_by(role=role).all()

    permissions = []
    for position in positions:
        position_permissions = session.query(PositionPermissionModel).filter_by(
            position_id=position.position_id
        ).all()

        for position_permission in position_permissions:
            permission = session.query(PermissionModel).filter_by(
                permission_id=position_permission.permission_id
            ).first()

            if permission is not None:
                permissions.append(permission)

    return permissions
