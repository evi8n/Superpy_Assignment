def test_remind_reset_date():
    from super import remind_reset_date

    assert remind_reset_date("2022-07-12", "2023-07-31") is None
    assert remind_reset_date("2023-08-07", "2026-07-31") is None
    assert remind_reset_date("2023-08-07", "2023-07-31") is None
    assert remind_reset_date("2023-07-31", "2023-07-31") is None
