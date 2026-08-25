from app.models.operational.organization import Organization
from app.schemas.organization import OrganizationCreate


def create(db, data: OrganizationCreate):

    organization = Organization(
        name=data.name
    )

    db.add(organization)
    db.commit()
    db.refresh(organization)

    return organization



def get_all(db):

    return db.query(Organization).all()



def get_by_id(db, organization_id):

    return (
        db.query(Organization)
        .filter(
            Organization.id == organization_id
        )
        .first()
    )
