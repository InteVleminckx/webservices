class Database:

    def __init__(self):
        self.deleted = set()
        self.liked = set()

        self.deleted_all = False
        self.liked_all = False

    def add_deleted(self, movie_id: int) -> None:
        self.deleted.add(movie_id)
        return

    def movie_is_deleted(self, movie_id: int) -> bool:
        return movie_id in self.deleted

    def delete_all(self):
        self.deleted_all = True
        return

    def like_movie(self, movie_id: int) -> None:
        self.liked.add(movie_id)
        return

    def unlike_movie(self, movie_id: int) -> None:
        self.liked.discard(movie_id)
        return

    def movie_is_liked(self, movie_id: int) -> bool:
        return movie_id in self.liked if not self.liked_all else movie_id not in self.liked

    def like_all(self):
        self.liked_all = not self.liked_all
        return
