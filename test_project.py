from project import find_vid, search_yt, file_changes


def test_find_vid():
    text = "канье вест."
    assert find_vid(text) == 'https://www.youtube.com/watch?v=mbOUwdyse28'


def test_search_yt():
    text = "https://www.youtube.com/watch?v=Jg5wkZ-dJXA&ab_channel=KanyeWestVEVO"
    assert search_yt(text) == 'Why you should listen to My Beautiful Dark Twisted Fantasy (and Runaway)'


def test_file_changes():
    text = 'lol'
    assert file_changes() == text

