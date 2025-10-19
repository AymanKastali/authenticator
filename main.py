import uvicorn

from delivery.db.in_memory.user_repository import get_in_memory_repository
from delivery.web.fastapi.app import create_app
from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress

app = create_app()
user_repo = get_in_memory_repository()

user = User.register_local(
    EmailAddress("alice@example.com"), "strongpassword123"
)
user_repo.save(user)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
