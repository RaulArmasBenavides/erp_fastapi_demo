from passlib.context import CryptContext
import secrets
from app.infrastructure.schema.user_schema import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_default_users(database):  # Recibe la instancia de Database
    """Crear usuarios por defecto al iniciar la aplicación"""

    # Usamos el context manager para obtener una sesión
    with database.session() as session:
        # Verificar si ya existen usuarios
        existing_users = session.query(UserSchema).count()

        if existing_users > 0:
            print(f"✓ Ya existen {existing_users} usuarios, no se crean por defecto")
            return

        # Datos de usuarios por defecto (solo para efectos de prueba reto técnico)
        default_users = [
            {
                "email": "requester@stracon.com",
                "name": "Usuario Requester",
                "password": "Dsr1#tec",
                "role": "Requester",
                "is_active": True,
            },
            {
                "email": "admin@stracon.com",
                "name": "Admin Stracon",
                "password": "Dsr1#tec",
                "role": "Approver",
                "is_active": True,
            },
            {
                "email": "raularmasbx@gmail.com",
                "name": "Raul Armas",
                "password": "Dsr1#tec",
                "role": "Approver",
                "is_active": True,
            },
            {
                "email": "juan.lam@stracontech.com",
                "name": "Juan Lam",
                "password": "Dsr1#tec",
                "role": "Approver",
                "is_active": True,
            },
        ]

        created_count = 0
        for user_data in default_users:
            # Verificar si el usuario ya existe
            existing_user = (
                session.query(UserSchema).filter_by(email=user_data["email"]).first()
            )

            if not existing_user:
                # Crear hash de la contraseña
                password_hash = pwd_context.hash(user_data["password"])

                # Generar token de usuario (opcional)
                user_token = secrets.token_urlsafe(32)

                # Crear nuevo usuario
                new_user = UserSchema(
                    email=user_data["email"],
                    name=user_data["name"],
                    password_hash=password_hash,
                    user_token=user_token,
                    role=user_data["role"],
                    is_active=user_data["is_active"],
                    # created_at se establece automáticamente por default=datetime.utcnow
                )

                session.add(new_user)
                created_count += 1

        if created_count > 0:
            session.commit()
            print(f"✓ Creados {created_count} usuarios por defecto")
            print("  - requester@stracon.com (Rol: Requester)")
            print("  - raul.armas@stracon.com (Rol: APPROVER)")
        else:
            print("✓ No se crearon nuevos usuarios (ya existían)")
