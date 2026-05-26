from abc import ABC, abstractmethod
import dataclasses

@dataclasses.dataclass
class User:
    username: str
    email: str
    phone: str = ""

# --- Абстракция (DIP) ---
class NotificationService(ABC):
    @abstractmethod
    def send_welcome(self, user: User): pass

# --- Реализации (High Cohesion) ---
class EmailNotificationService(NotificationService):
    def send_welcome(self, user: User):
        print(f"[Email] Письмо отправлено на {user.email}")

class SMSNotificationService(NotificationService):
    def send_welcome(self, user: User):
        print(f"[SMS] Сообщение отправлено на {user.phone}")

# --- Бизнес-логика (SRP / Low Coupling) ---
class UserManager:
    def __init__(self, notification_service: NotificationService):
        self.database = {}
        self.notification_service = notification_service # Внедрение зависимости

    def register_user(self, username: str, email: str, phone: str = ""):
        self.database[username] = User(username, email, phone)
        print(f"[БД] Пользователь {username} сохранен.")
        self.notification_service.send_welcome(self.database[username])

# --- Клиентский код ---
if __name__ == "__main__":
    # Сценарий 1: Через Email
    manager_email = UserManager(EmailNotificationService())
    manager_email.register_user("alex", "alex@company.com")

    # Сценарий 2: Переключение на SMS без изменения UserManager
    manager_sms = UserManager(SMSNotificationService())
    manager_sms.register_user("ivan", "ivan@company.com", phone="+79991112233")