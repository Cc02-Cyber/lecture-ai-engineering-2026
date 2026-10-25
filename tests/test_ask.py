from types import SimpleNamespace

from app import ask as ask_module


def _response(text, input_tokens=12, output_tokens=7):
    return SimpleNamespace(
        usage_metadata=SimpleNamespace(
            prompt_token_count=input_tokens,
            candidates_token_count=output_tokens,
        ),
        text=text,
    )


def test_ask_prints_token_counts_and_returns_response_text(monkeypatch, capsys):
    def send_message(question):
        assert question == "質問"
        return _response("回答")

    chat = SimpleNamespace(send_message=send_message)
    times = iter([10.0, 11.234])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    result = ask_module.ask("質問", chat)

    assert result == "回答"
    assert capsys.readouterr().out == (
        "[tokens] 入力: 12, 出力: 7\n"
        "[time] 応答時間: 1.23秒\n"
    )


def test_ask_reports_unknown_counts_when_usage_is_unavailable(monkeypatch, capsys):
    def send_message(question):
        assert question == "質問"
        return SimpleNamespace(usage_metadata=None, text="回答")

    chat = SimpleNamespace(send_message=send_message)
    times = iter([20.0, 20.5])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(times))

    ask_module.ask("質問", chat)

    assert capsys.readouterr().out == (
        "[tokens] 入力: 不明, 出力: 不明\n"
        "[time] 応答時間: 0.50秒\n"
    )


def test_interactive_mode_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    sent_messages = []

    class FakeChat:
        def send_message(self, message):
            sent_messages.append(message)
            return _response(f"{message}への回答")

    chat = FakeChat()
    client = SimpleNamespace(chats=SimpleNamespace(create=lambda **_: chat))
    monkeypatch.setattr(ask_module.genai, "Client", lambda **_: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    questions = iter(["最初の質問", "続けて質問", "/exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    monkeypatch.setattr("sys.argv", ["app.ask", "--interactive"])
    ask_module.main()

    output = capsys.readouterr().out
    assert sent_messages == ["最初の質問", "続けて質問"]
    assert output.count("[tokens]") == 2
    assert "最初の質問への回答" in output
    assert "続けて質問への回答" in output
