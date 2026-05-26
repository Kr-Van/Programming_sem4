import dataclasses

@dataclasses.dataclass
class User:
    username: str
    email: str

class UserManager:
    """Low Cohesion и High Coupling: класс завязан на БД и SMTP одновременно."""
    def __init__(self):
        self.database = {}
        self.smtp_server = "://company.com"

    def register_user(self, username: str, email: str):
        # Обязанность 1: Работа с БД
        self.database[username] = User(username, email)
        print(f"[БД] Пользователь {username} сохранен.")

        # Обязанность 2: Сетевой протокол (Нарушение SRP и DIP)
        print(f"[SMTP] Подключение к {self.smtp_server}...")
        print(f"[SMTP] Email отправлен на {email}.")

if __name__ == "__main__":
    manager = UserManager()
    manager.register_user("alex", "alex@company.com")