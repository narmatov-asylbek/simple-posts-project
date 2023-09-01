# bot
import random
import pathlib

from faker import Faker
import httpx


class Bot:

    def __init__(self, users_number: int, max_posts_per_user: int,
                 max_likes_per_user: int, url: str):
        self.users_number = users_number
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

        self.url = url.rstrip('/')
        self.fake = Faker()

    def _signup_users(self) -> list[tuple[str, str, str, str]]:
        """Creates users, login them, and returns the result"""
        url = self.url + '/api/v1/users/signup/'

        created_users = []
        for _ in range(self.users_number):
            username = self.fake.email()
            password = self.fake.password()
            response = httpx.post(url=url,
                                  json={
                                      'username': username,
                                      'password1': password,
                                      'password2': password
                                  })
            assert response.status_code == 201
            access_token, token_type = self._login(username, password)
            created_users.append(
                (username, password, access_token, token_type))
        return created_users

    def _login(self, username: str, password: str) -> tuple[str, str]:
        url = self.url + '/api/v1/users/login/'
        response = httpx.post(url=url,
                              json={
                                  'username': username,
                                  'password': password
                              }).json()
        return (response['access_token'], response['token_type'])

    def _create_posts(self, users: list[tuple[str, str, str,
                                              str]]) -> list[int]:
        url = self.url + '/api/v1/posts/'

        posts = []
        for _, _, access_token, _ in users:
            for _ in range(self.max_posts_per_user):
                title = self.fake.name()
                content = self.fake.text()
                response = httpx.post(url=url,
                                      headers={
                                          'Authorization':
                                          f'Bearer {access_token}'
                                      },
                                      json={
                                          'title': title,
                                          'text': content
                                      }).json()
                posts.append(response['id'])
        return posts

    def _like_posts(self, users: list[tuple[str, str, str, str]],
                    posts: list[int]) -> None:
        url = self.url + '/api/v1/posts/{post_id}/likes/'

        for _, _, access_token, _ in users:
            for _ in range(self.max_likes_per_user):
                like_url = url.format(post_id=random.choice(posts))
                httpx.post(url=like_url,
                           headers={'Authorization': f'Bearer {access_token}'})

    def run(self) -> None:
        users = self._signup_users()
        posts = self._create_posts(users=users)
        self._like_posts(users=users, posts=posts)


def run_bot(file: str | pathlib.Path = 'bot_config.toml'):
    import tomllib

    file = pathlib.Path(file)
    with file.open('rb') as f:
        data = tomllib.load(f)

    bot = Bot(users_number=data['number_of_users'],
              url=data['url'],
              max_posts_per_user=data['max_posts_per_user'],
              max_likes_per_user=data['max_likes_per_user'])
    bot.run()
    print('Bot finished its job')


if __name__ == '__main__':
    run_bot()
