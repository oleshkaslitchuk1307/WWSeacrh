import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from domain.models.view_models.user_vm import UserUpdate, UserResponse
from bl.jwt_bl import get_current_user
from domain.interfaces.service_interfaces import IUserService

class UserController:
    def __init__(self, user_service: IUserService):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/me", self.get_me, methods=["GET"], response_model=UserResponse)
        self.router.add_api_route("/me", self.update_me, methods=["PUT"])
        self.router.add_api_route("/me/avatar", self.upload_avatar, methods=["POST"])
        self.router.add_api_route("/search", self.search_users, methods=["GET"])
        self.router.add_api_route("/friends", self.get_friends, methods=["GET"])
        self.router.add_api_route("/friends/{friend_id}", self.add_friend, methods=["POST"])
        self.router.add_api_route("/friends/{friend_id}/accept", self.accept_friend, methods=["POST"])
        self.router.add_api_route("/friends/{friend_id}/reject", self.reject_friend, methods=["POST"])
        self.router.add_api_route("/friends/{friend_id}", self.remove_friend, methods=["DELETE"])
        self.router.add_api_route("/{user_id}", self.get_user, methods=["GET"], response_model=UserResponse)
        self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"])
        self.router.add_api_route("/{user_id}", self.delete_user, methods=["DELETE"])

    def get_me(self, current_user_id: int = Depends(get_current_user)):
        user = self.user_service.get_user(current_user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        return user

    def update_me(self, user: UserUpdate, current_user_id: int = Depends(get_current_user)):
        return self.user_service.update_user(current_user_id, user)

    async def upload_avatar(self, file: UploadFile = File(...), current_user_id: int = Depends(get_current_user)):
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Потрібно завантажити файл зображення")

        os.makedirs("client/uploads/avatars", exist_ok=True)
        extension = os.path.splitext(file.filename or "")[1].lower()
        if extension not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            extension = ".png"
        filename = f"{uuid.uuid4().hex}{extension}"
        relative_path = f"/uploads/avatars/{filename}"
        file_path = os.path.join("client", "uploads", "avatars", filename)

        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        self.user_service.update_user(current_user_id, UserUpdate(avatar_url=relative_path))
        return {"avatar_url": relative_path}

    def search_users(self, query: str, current_user_id: int = Depends(get_current_user)):
        return self.user_service.search_users(query, current_user_id) if query.strip() else []

    def get_friends(self, current_user_id: int = Depends(get_current_user)):
        return self.user_service.get_friends(current_user_id)

    def add_friend(self, friend_id: int, current_user_id: int = Depends(get_current_user)):
        return self.user_service.add_friend(current_user_id, friend_id)

    def accept_friend(self, friend_id: int, current_user_id: int = Depends(get_current_user)):
        return self.user_service.accept_friend(current_user_id, friend_id)

    def reject_friend(self, friend_id: int, current_user_id: int = Depends(get_current_user)):
        return self.user_service.reject_friend(current_user_id, friend_id)

    def remove_friend(self, friend_id: int, current_user_id: int = Depends(get_current_user)):
        return self.user_service.remove_friend(current_user_id, friend_id)

    def get_user(self, user_id: int):
        user = self.user_service.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Користувача не знайдено")
        return user

    def update_user(self, user_id: int, user: UserUpdate):
        return self.user_service.update_user(user_id, user)

    def delete_user(self, user_id: int):
        return self.user_service.delete_user(user_id)
