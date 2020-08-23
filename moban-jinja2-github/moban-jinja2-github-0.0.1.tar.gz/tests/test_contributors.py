from mock import MagicMock, patch
from nose.tools import eq_


@patch("moban_jinja2_github.contributors.EndPoint")
def test_get_contributors(fake_end_point):
    sample_contributors = [{"url": "author"}, {"url": "contributors"}]
    fake_api = MagicMock(
        get_all_contributors=MagicMock(return_value=sample_contributors)
    )
    fake_end_point.return_value = fake_api

    from moban_jinja2_github.contributors import get_contributors

    actual = get_contributors("user", "repo", "author")
    expected = [{"url": "contributors"}]

    eq_(list(actual), expected)
