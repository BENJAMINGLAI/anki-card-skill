from anki_skill.models import Card


def test_card_creation():
    card = Card(
        question="<b>单源最短路径问题</b> 旨在解决什么问题？",
        answer="找到 <b>源顶点</b> 到 <b>所有其他顶点</b> 的最短路径。<br><br>nidd1742293016393",
        tags=["计算机科学::算法::图论::最短路径"],
    )
    assert card.question == "<b>单源最短路径问题</b> 旨在解决什么问题？"
    assert "nidd1742293016393" in card.answer
    assert card.tags == ["计算机科学::算法::图论::最短路径"]


def test_card_nidd_extraction():
    card = Card(question="Q", answer="A<br><br>nidd1743696000000", tags=[])
    assert card.nidd == "nidd1743696000000"


def test_card_nidd_empty():
    card = Card(question="Q", answer="No nidd here", tags=[])
    assert card.nidd == ""


def test_card_answer_clean():
    card = Card(question="Q", answer="A<br><br>nidd123", tags=[])
    assert card.answer_clean == "A"


def test_card_answer_clean_no_nidd():
    card = Card(question="Q", answer="Just an answer", tags=[])
    assert card.answer_clean == "Just an answer"


def test_card_tags_as_string():
    card = Card(
        question="Q",
        answer="A",
        tags=["操作系统::进程", "计算机科学"],
    )
    assert card.tags_string == "操作系统::进程 计算机科学"


def test_card_answer_plain_text():
    card = Card(
        question="Q",
        answer="<b>加粗</b> 和 <i>斜体</i><br><br>nidd123",
        tags=[],
    )
    assert card.answer_plain == "加粗 和 斜体"


def test_card_is_cloze():
    card = Card(question="{{c1::Mitochondria}} is X.", answer="", tags=[])
    assert card.is_cloze is True


def test_card_is_not_cloze_curly_braces():
    """Curly braces without cloze syntax should not be detected as cloze."""
    card = Card(question="Use {{curly braces}} in templates.", answer="A", tags=[])
    assert card.is_cloze is False


def test_card_multiple_nidd():
    """Only the last nidd should be extracted."""
    card = Card(question="Q", answer="A nidd111<br><br>nidd222", tags=[])
    assert card.nidd == "nidd222"
    assert "nidd111" in card.answer_clean
