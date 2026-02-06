from app.llm.llm_client import call_robust_llm

def test_text_mode():
    out = call_robust_llm(
        system_prompt="You are a helpful assistant",
        user_prompt="What is 2+2?",
        json_mode=False
    )
    assert "4" in str(out)


def test_json_mode():
    out = call_robust_llm(
        system_prompt="You are a helpful assistant",
        user_prompt="Return JSON with key answer for 2+2",
        json_mode=True
    )
    assert isinstance(out, str)
    assert "answer" in out
