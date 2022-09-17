from dataclasses import dataclass


@dataclass
class User_rating:
    pk: int
    position: int
    username: str
    reputation: int
    image_link: str
    
    
@dataclass
class Theme_rating:
    theme_slug: str
    position: int
    title: str
    vote_count: int
    questions_count: int
    answer_count: int


@dataclass
class Question_rating:
    position: int
    slug: str
    title: str
    vote_count: int
    answer_counter: int
    
@dataclass
class Answer_rating:
    position: int
    subtitles: str
    vote_count: int
    audio_lenght : float
    words_total: int
    answer_pk: int
    qustion_slug: str
