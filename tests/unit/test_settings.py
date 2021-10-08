from buying_frenzy.settings import Config

def test_config():
    c = Config()
    assert getattr(c, 'DEVELOPMENT') is False
    assert getattr(c, 'DEBUG') is False
    assert getattr(c, 'TESTING') is False
    assert getattr(c, 'SQLALCHEMY_DATABASE_URI') == 'postgresql://lance:lance123@localhost:5432/glinits'
    assert getattr(c, 'SQLALCHEMY_TRACK_MODIFICATIONS') is False
    assert getattr(c, 'SQLALCHEMY_ENGINE_OPTIONS') == dict(
        pool_size=10,
        pool_recycle=120,
        pool_pre_ping=True
    )