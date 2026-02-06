class Player:
    # Class variable (shared across all instances)
    game = "Chess"

    def __init__(self, name: str):
        # Instance variable (unique per object)
        self.name = name
        self.score = 0

    def add_points(self, points: int) -> None:
        self.score += points


if __name__ == "__main__":
    p1 = Player("Ernar")
    p2 = Player("Alihan")

    # Example 1: class variable shared
    print("Game p1:", p1.game, "Game p2:", p2.game)

    p1.add_points(10)
    p2.add_points(3)
    print("Scores:", p1.name, p1.score, "|", p2.name, p2.score)

    # Example 3: changing class variable affects all (unless overridden)
    Player.game = "Checkers"
    print("Game after change:", p1.game, p2.game)

    p1.game = "Go"  # creates instance attribute 'game' for p1 only
    print("p1.game:", p1.game, "p2.game:", p2.game, "Player.game:", Player.game)

    p2.nickname = "Pro" # «Создай у объекта p2 новое поле nickname и положи туда "Pro"»
    print("p2.nickname:", p2.nickname)
    del p2.nickname
    print("nickname deleted successfully")