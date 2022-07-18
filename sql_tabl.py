# Торгово-развлекательный / офисный центр. Служба работы с арендаторами: обработка заявок.
# Клиенты, арендаторы, помещения



import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base, sessionmaker


Base = declarative_base()


class CommonModelMixin:
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

class Place(Base, CommonModelMixin):
    __tablename__ = "places"

    name = sa.Column(sa.Unicode(255), nullable=False)
    square = sa.Column(sa.Unicode(255), nullable=False)
    price = sa.Column(sa.Unicode(255), nullable=False)


class Owner(Base, CommonModelMixin):
    __tablename__ = "owners"
    __tableargs__ = (
        sa.UniqueConstraint("passport_serial", "passport_number", "phone"),
    )

    first_name = sa.Column(sa.Unicode(255), nullable=False)
    last_name = sa.Column(sa.Unicode(255), nullable=False)
    patronymic_name = sa.Column(sa.Unicode(255), nullable=True)

    passport_serial = sa.Column(sa.String(4), nullable=False)
    passport_number = sa.Column(sa.String(6), nullable=False)
    phone = sa.Column(sa.String(11), nullable=False)


class Client(Base, CommonModelMixin):
    __tablename__ = "clients"
    __tableargs__ = (
        sa.UniqueConstraint("passport_serial", "passport_number", "phone"),
    )

    first_name = sa.Column(sa.Unicode(255), nullable=False)
    last_name = sa.Column(sa.Unicode(255), nullable=False)
    patronymic_name = sa.Column(sa.Unicode(255), nullable=True)

    passport_serial = sa.Column(sa.String(4), nullable=False)
    passport_number = sa.Column(sa.String(6), nullable=False)
    phone = sa.Column(sa.String(11), nullable=False)


class OwnerPlace(Base, CommonModelMixin):
    __tablename__ = "owners_places"
    __tableargs__ = (
        sa.UniqueConstraint("owner_id", "place_id"),
    )

    owner_id = sa.Column(sa.ForeignKey(f"{Owner.__tablename__}.id"), nullable=False)
    place_id = sa.Column(sa.ForeignKey(f"{Place.__tablename__}.id"), nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)


class ClientPlace(Base, CommonModelMixin):
    __tablename__ = "clients_places"

    client_id = sa.Column(sa.ForeignKey(f"{Client.__tablename__}.id"), nullable=False)
    place_id = sa.Column(sa.ForeignKey(f"{Place.__tablename__}.id"), nullable=False)
    owner_id = sa.Column(sa.ForeignKey(f"{Owner.__tablename__}.id"), nullable=False)
    enter_contract = sa.Column(sa.DateTime, nullable=False)
    end_contract = sa.Column(sa.DateTime, nullable=True)


class Role:
    def __init__(self, dsn: str):
        self._engine = sa.create_engine(dsn)
        Session = sessionmaker(self._engine)
        self._session = Session()
        Base.metadata.create_all(self._engine)

    def get_client(self, **filters):
        return self._session.query(Client).filter_by(**filters).first()

    def get_owner(self, **filters):
        return self._session.query(Owner).filter_by(**filters).first()

class RegistrationRole(Role):
    def register_client(self, last_name, first_name, passport_serial, passport_number,
                         phone, patronymic_name=None):
        client = Client(
            last_name=last_name,
            first_name=first_name,
            patronymic_name=patronymic_name,
            passport_serial=passport_serial,
            passport_number=passport_number,
            phone=phone
        )
        self._session.add(client)
        self._session.commit()
        return client

    def edit_client(self, client, **new_params):
        for name, value in new_params.items():
            setattr(client, name, value)
        self._session.commit()


class OwnerRole(Role):
    def get_place(self, name, square, price):
        return self._session.query(Place).filter_by(name=name, square=square, price=price).first()

    def client_place(self, client, place, owner, is_first=True):
        if is_first:
            client_place = ClientPlace(
                client_id=client.id,
                place_id=place.id,
                owner_id=owner.id,
                enter_contract=datetime.datetime.now(),
            )
            self._session.add(client_place)
        else:
            client_place = self._session.query(ClientPlace).filter_by(
                client_id=client.id,
                owner_id=owner.id,
            ).first()
            client_place.end_contract = datetime.datetime.now()
        self._session.commit()
        return client_place


class AdminRole(RegistrationRole, OwnerRole):
    def add_place(self, name, square, price):
        place = Place(name=name, square=square, price=price)
        self._session.add(place)
        self._session.commit()
        return place

    def add_owner(self, first_name, last_name, patronymic_name,
                    passport_serial, passport_number, phone):
        owner = Owner(first_name=first_name, last_name=last_name,
        patronymic_name=patronymic_name, passport_serial=passport_serial, 
        passport_number=passport_number, phone=phone
        )
        self._session.add(owner)
        self._session.commit()
        return owner

admin_role = AdminRole("sqlite:///ex_14.db")
client = admin_role.register_client(
    last_name="A",
    first_name="A",
    passport_serial="1111",
    passport_number="111111",
    phone="+7(111)111-11-11"
)
place = admin_role.add_place(
    name="P",
    square="5",
    price="10"
    ) 
owner = admin_role.add_owner(
    last_name="B",
    first_name="B",
    patronymic_name="B",
    passport_serial="2222",
    passport_number="222222",
    phone="+7(222)222-22-22"
)

client_place = admin_role.client_place(client=client, place=place, owner=owner)
print(
    f"client: {client.passport_serial}, {client.passport_number},"
    f"{client_place.enter_contract}, {client_place.end_contract}"
)

admin_role.client_place(client=client, place=place, owner=owner, is_first=False)
print(
    f"client: {client.passport_serial}, {client.passport_number},"
    f"{client_place.enter_contract}, {client_place.end_contract}"
) 

