from domains.authentication.models.position_permission_model import PositionPermissionModel
from domains.authentication.models.permission_model import PermissionModel

def get_permissions_for_position(session, position_id: str):
    position_permissions = session.query(PositionPermissionModel).filter_by(position_id=position_id).all()

    permissions = []
    for position_permission in position_permissions:
        permission = session.query(PermissionModel).filter_by(
            permission_id=position_permission.permission_id
        ).first()

        if permission is not None:
            permissions.append(permission)

    return permissions