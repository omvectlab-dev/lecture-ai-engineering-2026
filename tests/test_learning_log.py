
"""第3回：学習記録の保存と承認制御のテスト。"""

import pytest

from pydantic_ai import DeferredToolRequests, DeferredToolResults
from pydantic_ai.models.test import TestModel

from app import tools
from app.agent import agent


@pytest.mark.parametrize("approved", [False, True])
def test_learning_log_approval(tmp_path, monkeypatch, approved):
    """承認前は保存されず、承認後のみ保存されることを確認する。"""

    # テスト用の一時フォルダに保存先を切り替える
    monkeypatch.setattr(
        tools,
        "__file__",
        str(tmp_path / "app" / "tools.py"),
    )
    log_dir = tmp_path / "learning_log"

    # 保存ツールのみを呼び出すテストモデル
    model = TestModel(call_tools=["save_learning_log"])

    with agent.override(model=model):
        # 承認前の実行
        first = agent.run_sync("学習記録を保存して")

        assert isinstance(first.output, DeferredToolRequests)
        assert len(first.output.approvals) == 1

        call = first.output.approvals[0]
        assert call.tool_name == "save_learning_log"

        # 承認前にはファイルが存在しない
        assert not log_dir.exists()

        # 承認または拒否を渡して再開する
        decisions = DeferredToolResults()
        decisions.approvals[call.tool_call_id] = approved

        agent.run_sync(
            message_history=first.all_messages(),
            deferred_tool_results=decisions,
        )

    # 保存されたMarkdownファイルを確認
    files = list(log_dir.glob("*.md"))

    if approved:
        assert len(files) == 1
        saved_text = files[0].read_text(encoding="utf-8")
        args = call.args_as_dict()
        assert f"# {args['title']}" in saved_text
        assert args["content"] in saved_text
    else:
        assert len(files) == 0
